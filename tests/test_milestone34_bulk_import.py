from pathlib import Path
from src.question_bulk_import import import_directory

def test_bulk_import(tmp_path: Path):
    source_dir = tmp_path/"input"
    source_dir.mkdir()
    (source_dir/"a.txt").write_text("For matrix A find the determinant.", encoding="utf-8")
    (source_dir/"b.txt").write_text("Find the derivative of x squared.", encoding="utf-8")
    summary = import_directory(source_dir, root=tmp_path/"bank", exam_hint="GATE EE")
    assert summary.processed == 2
    assert summary.failed == 0
    assert summary.auto + summary.review + summary.duplicates == 2
