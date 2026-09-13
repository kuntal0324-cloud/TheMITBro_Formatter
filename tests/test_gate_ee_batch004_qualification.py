from pathlib import Path
import json

from src.gate_ee_batch_qualification import qualify_batch


JSONL = Path("input/gate_ee_batch_004/BATCH_004_SIGNALS_AND_SYSTEMS.jsonl")
HANDOFF = Path("input/gate_ee_batch_004/BATCH_004_FORMATTER_V2_HANDOFF.json")
EVIDENCE = Path("output/gate_ee_batch_004/FORMATTER_V2_QUALIFICATION.json")


def _result():
    return qualify_batch(JSONL, HANDOFF)


def test_batch004_strict_qualification_passes_all_signals_records():
    result = _result()
    assert result["status"] == "PASS"
    assert result["domain"] == "Signals and Systems"
    assert result["question_count"] == 15
    assert result["formatter_pass_count"] == 15
    assert result["formatter_review_count"] == result["invalid_count"] == 0
    assert all(row["classification"]["topic"] == "Signals and Systems" for row in result["questions"])


def test_batch004_checksum_bound_diagrams_are_complete():
    diagrams = [row["diagram_contract"] for row in _result()["questions"] if row["diagram_contract"]["declared"]]
    assert len(diagrams) == 3
    assert all(row["status"] == "PASS" and row["asset_sha256"] for row in diagrams)
    assert all(row["alt_text"] and row["caption"] for row in diagrams)


def test_batch004_evidence_is_reproducible_and_not_promoted():
    result = _result()
    reproduced = json.loads(json.dumps(result))
    assert json.loads(EVIDENCE.read_text(encoding="utf-8")) == reproduced
    assert result["paper_eligible_count"] == 0
    assert result["independent_human_review_required"] is True
    assert result["release_gate"] == "BLOCKED"
