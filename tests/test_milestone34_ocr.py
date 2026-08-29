from pathlib import Path
from src.question_ocr import extract_text

def test_text_ingestion_is_lossless(tmp_path: Path):
    source = tmp_path / "q.txt"
    source.write_text("Find det(A).", encoding="utf-8")
    result = extract_text(source)
    assert result.text == "Find det(A)."
    assert result.confidence == 1.0
    assert result.source_type == "text"

def test_png_is_supported_even_when_ocr_backend_is_mocked(tmp_path, monkeypatch):
    import src.question_ocr as qocr
    source = tmp_path / "q.png"
    source.write_bytes(b"png")
    sentinel = qocr.OCRResult("matrix", 0.93, "image", "mock", True)
    monkeypatch.setattr(qocr, "_ocr_image", lambda p: sentinel)
    assert qocr.extract_text(source) == sentinel
