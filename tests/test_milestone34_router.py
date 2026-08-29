from pathlib import Path
from src.question_router import route_source

def test_route_matrix_question(tmp_path: Path):
    source = tmp_path / "q.txt"
    source.write_text("For matrix A, find the determinant.", encoding="utf-8")
    result = route_source(source, root=tmp_path/"bank", exam_hint="GATE EE")
    assert result.path is not None
    assert "Engineering_Mathematics" in str(result.path)
    assert "Matrices" in str(result.path)

def test_duplicate_is_not_stored_twice(tmp_path: Path):
    source = tmp_path / "q.txt"
    source.write_text("For matrix A, find the determinant.", encoding="utf-8")
    bank = tmp_path/"bank"
    first = route_source(source, root=bank, exam_hint="GATE EE")
    second = route_source(source, root=bank, exam_hint="GATE EE")
    assert first.path is not None
    assert second.status == "DUPLICATE"
