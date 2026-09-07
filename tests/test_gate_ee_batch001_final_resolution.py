from pathlib import Path
from src.gate_ee_batch_qualification import qualify_batch

JSONL=Path("input/gate_ee_batch_001/BATCH_001_ENGINEERING_MATHEMATICS.jsonl")
HANDOFF=Path("input/gate_ee_batch_001/BATCH_001_FORMATTER_V2_HANDOFF.json")

def test_batch001_strict_qualification_resolves_every_review_without_release():
    r=qualify_batch(JSONL,HANDOFF)
    assert r["status"]=="PASS"
    assert r["question_count"]==20
    assert r["formatter_pass_count"]==20
    assert r["formatter_review_count"]==0
    assert r["invalid_count"]==0
    assert r["paper_eligible_count"]==0
    assert r["release_gate"]=="BLOCKED"

def test_phase4_revisions_pass_formatter_but_remain_human_pending():
    r=qualify_batch(JSONL,HANDOFF)
    x={q["question_id"]:q for q in r["questions"]}
    for qid, result in x.items():
        assert result["source_revision"] >= 2
        assert result["formatter_qualification"]=="PASS"
        assert result["independent_human_review"]=="PENDING"
        assert result["paper_eligible"] is False
