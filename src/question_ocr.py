from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

from .image_preprocessor import SUPPORTED_IMAGES, preprocess


SUPPORTED_TEXT = {".txt", ".md"}
SUPPORTED_INPUTS = SUPPORTED_TEXT | SUPPORTED_IMAGES


@dataclass(frozen=True)
class OCRResult:
    text: str
    confidence: float
    source_type: str
    engine: str
    preprocessed: bool = False


def _ocr_image(path: Path) -> OCRResult:
    try:
        import pytesseract
        from PIL import Image
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "Image OCR requires Pillow and pytesseract."
        ) from exc

    with TemporaryDirectory(prefix="themitbro_m34_") as tmp:
        processed = Path(tmp) / f"processed{path.suffix.lower()}"
        preprocess(path, output_path=processed)

        try:
            data = pytesseract.image_to_data(
                Image.open(processed),
                output_type=pytesseract.Output.DICT,
            )
        except Exception as exc:
            raise RuntimeError(f"OCR failed for {path.name}: {exc}") from exc

        words: list[str] = []
        confidences: list[float] = []

        for token, raw_conf in zip(data.get("text", []), data.get("conf", [])):
            token = str(token).strip()
            if not token:
                continue
            words.append(token)
            try:
                conf = float(raw_conf)
            except (TypeError, ValueError):
                continue
            if conf >= 0:
                confidences.append(conf)

        text = " ".join(words).strip()
        confidence = (
            sum(confidences) / len(confidences) / 100.0
            if confidences
            else 0.0
        )

        return OCRResult(
            text=text,
            confidence=round(max(0.0, min(1.0, confidence)), 3),
            source_type="image",
            engine="tesseract",
            preprocessed=True,
        )


def extract_text(path: str | Path) -> OCRResult:
    """
    Extract text from text/markdown files or OCR an image.

    Text files are lossless and therefore receive confidence 1.0.
    Image OCR is preprocessed before Tesseract runs.
    """
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(source)

    suffix = source.suffix.lower()
    if suffix not in SUPPORTED_INPUTS:
        raise ValueError(f"Unsupported input: {source.suffix}")

    if suffix in SUPPORTED_TEXT:
        return OCRResult(
            text=source.read_text(encoding="utf-8"),
            confidence=1.0,
            source_type="text",
            engine="native",
            preprocessed=False,
        )

    return _ocr_image(source)
