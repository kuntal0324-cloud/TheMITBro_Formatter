from pathlib import Path
import json

from src.gate_ee_batch_qualification import qualify_batch


JSONL = Path("input/gate_ee_batch_005/BATCH_005_ELECTROMAGNETIC_FIELDS.jsonl")
HANDOFF = Path("input/gate_ee_batch_005/BATCH_005_FORMATTER_V2_HANDOFF.json")
EVIDENCE = Path("output/gate_ee_batch_005/FORMATTER_V2_QUALIFICATION.json")


def _result():
    return qualify_batch(JSONL, HANDOFF)


def test_batch005_strict_qualification_passes_all_emft_records():
    result = _result()
    assert result["status"] == "PASS"
    assert result["domain"] == "Electromagnetic Fields"
    assert result["question_count"] == 12
    assert result["formatter_pass_count"] == 12
    assert result["formatter_review_count"] == result["invalid_count"] == 0
    assert all(row["classification"]["topic"] == "Electromagnetic Fields" for row in result["questions"])


def test_batch005_checksum_bound_diagrams_are_complete():
    diagrams = [row["diagram_contract"] for row in _result()["questions"] if row["diagram_contract"]["declared"]]
    assert len(diagrams) == 3
    assert all(row["status"] == "PASS" and row["asset_sha256"] for row in diagrams)
    assert all(row["alt_text"] and row["caption"] for row in diagrams)


def test_batch005_evidence_is_reproducible_and_not_promoted():
    result = _result()
    reproduced = json.loads(json.dumps(result))
    assert json.loads(EVIDENCE.read_text(encoding="utf-8")) == reproduced
    assert result["paper_eligible_count"] == 0
    assert result["independent_human_review_required"] is True
    assert result["release_gate"] == "BLOCKED"
