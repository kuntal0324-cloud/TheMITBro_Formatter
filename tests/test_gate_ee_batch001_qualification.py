from pathlib import Path
import json
from src.gate_ee_batch_qualification import qualify_batch

JSONL = Path("input/gate_ee_batch_001/BATCH_001_ENGINEERING_MATHEMATICS.jsonl")
HANDOFF = Path("input/gate_ee_batch_001/BATCH_001_FORMATTER_V2_HANDOFF.json")

def test_batch001_handoff_checksum_and_count():
    r = qualify_batch(JSONL, HANDOFF)
    assert r["status"] == "PASS"
    assert r["question_count"] == 20

def test_batch001_never_claims_human_review():
    r = qualify_batch(JSONL, HANDOFF)
    assert r["independent_human_review_required"] is True
    assert r["paper_eligible_count"] == 0
    assert r["release_gate"] == "BLOCKED"
    assert all(q["independent_human_review"] == "PENDING" for q in r["questions"])
    assert all(q["paper_eligible"] is False for q in r["questions"])

def test_batch001_unique_formatter_results():
    r = qualify_batch(JSONL, HANDOFF)
    ids = [q["question_id"] for q in r["questions"]]
    assert len(ids) == 20
    assert len(set(ids)) == 20
    assert all(q["duplicate"]["status"] == "ACCEPT" for q in r["questions"])

def test_batch001_render_smoke():
    r = qualify_batch(JSONL, HANDOFF)
    assert all(q["render"]["status"] == "PASS" for q in r["questions"])
    assert all(q["render"]["bytes"] > 0 for q in r["questions"])
