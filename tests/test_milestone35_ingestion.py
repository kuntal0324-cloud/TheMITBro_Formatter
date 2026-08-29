from pathlib import Path
from src.question_ingest import ingest

def test_ingestion_carries_math_metadata(tmp_path: Path):
    source = tmp_path / "q.txt"
    source.write_text("For A=[[1,2],[3,4]], find det(A).", encoding="utf-8")
    record = ingest(source, exam_hint="GATE EE")
    assert record.classification.topic == "Matrices"
    assert record.metadata["ingestion_contract"] == "M35"
    assert "matrix" in record.metadata["math_features"]
    assert "normalized_math_text" in record.metadata
