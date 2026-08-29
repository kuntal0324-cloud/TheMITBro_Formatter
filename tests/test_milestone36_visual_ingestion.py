from pathlib import Path
from src.question_ingest import ingest

def test_ingestion_stores_diagram_metadata(tmp_path: Path):
    q = tmp_path / "q.txt"
    q.write_text(
        "A resistor and capacitor are connected to a voltage source. "
        "Draw the circuit diagram and determine the impedance.",
        encoding="utf-8",
    )
    record = ingest(q, exam_hint="GATE EE")
    assert record.metadata["ingestion_contract"] == "M35"
    assert record.metadata["diagram_contract"] == "M36"
    assert record.metadata["diagram_present"] is True
    assert record.metadata["diagram_type"] == "circuit_diagram"
    assert record.metadata["diagram_family"] == "engineering"
