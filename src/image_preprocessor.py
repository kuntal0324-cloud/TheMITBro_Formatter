from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SUPPORTED_IMAGES = {".jpg", ".jpeg", ".png"}


@dataclass(frozen=True)
class PreprocessResult:
    source: Path
    output: Path
    width: int
    height: int
    operations: tuple[str, ...]


def preprocess(
    path: str | Path,
    *,
    output_path: str | Path | None = None,
    grayscale: bool = True,
    autocontrast: bool = True,
    sharpen: bool = True,
) -> PreprocessResult:
    """
    Apply conservative OCR-oriented preprocessing using Pillow only.

    The function deliberately avoids destructive transformations.  It keeps the
    original image intact and writes a processed copy when output_path is given.
    """
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(source)
    if source.suffix.lower() not in SUPPORTED_IMAGES:
        raise ValueError(f"Unsupported image type: {source.suffix}")

    try:
        from PIL import Image, ImageEnhance, ImageOps
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Image preprocessing requires Pillow.") from exc

    with Image.open(source) as img:
        img = ImageOps.exif_transpose(img)
        operations: list[str] = ["exif_transpose"]

        if grayscale:
            img = img.convert("L")
            operations.append("grayscale")

        if autocontrast:
            img = ImageOps.autocontrast(img)
            operations.append("autocontrast")

        if sharpen:
            img = ImageEnhance.Sharpness(img).enhance(1.35)
            operations.append("sharpen")

        width, height = img.size
        target = Path(output_path) if output_path is not None else source
        if output_path is not None:
            target.parent.mkdir(parents=True, exist_ok=True)
            save_img = img
            if target.suffix.lower() in {".jpg", ".jpeg"} and save_img.mode not in {"L", "RGB"}:
                save_img = save_img.convert("RGB")
            save_img.save(target)

    return PreprocessResult(
        source=source,
        output=target,
        width=width,
        height=height,
        operations=tuple(operations),
    )
