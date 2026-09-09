from pathlib import Path
import json

from src.gate_ee_batch_qualification import qualify_batch


JSONL = Path("input/gate_ee_batch_002/BATCH_002_ELECTRIC_CIRCUITS.jsonl")
HANDOFF = Path("input/gate_ee_batch_002/BATCH_002_FORMATTER_V2_HANDOFF.json")
EVIDENCE = Path("output/gate_ee_batch_002/FORMATTER_V2_QUALIFICATION.json")


def test_batch002_strict_formatter_qualification_passes_all_records():
    result = qualify_batch(JSONL, HANDOFF)
    assert result["batch_id"] == "BATCH_002"
    assert result["domain"] == "Electric Circuits"
    assert result["status"] == "PASS"
    assert result["question_count"] == 20
    assert result["formatter_pass_count"] == 20
    assert result["formatter_review_count"] == 0
    assert result["invalid_count"] == 0
    assert all(row["formatter_qualification"] == "PASS" for row in result["questions"])


def test_batch002_remains_blocked_from_paper_eligibility():
    result = qualify_batch(JSONL, HANDOFF)
    assert result["paper_eligible_count"] == 0
    assert result["independent_human_review_required"] is True
    assert result["release_gate"] == "BLOCKED"
    assert all(row["paper_eligible"] is False for row in result["questions"])


def test_batch002_records_are_auto_routed_and_render_cleanly():
    result = qualify_batch(JSONL, HANDOFF)
    for row in result["questions"]:
        assert row["classification"]["subject"] == "Electrical Engineering"
        assert row["classification"]["topic"] == "Electric Circuits"
        assert row["classification"]["status"] == "AUTO"
        assert row["validation"]["status"] == "PASS"
        assert row["quality"]["grade"] == "A"
        assert not row["quality"]["blockers"]
        assert row["render"]["status"] == "PASS"
        assert row["render"]["source_markup_exposed"] is False


def test_batch002_committed_evidence_is_reproducible():
    reproduced = json.loads(json.dumps(qualify_batch(JSONL, HANDOFF)))
    assert json.loads(EVIDENCE.read_text(encoding="utf-8")) == reproduced
