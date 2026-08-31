from pathlib import Path
from src.gate_ee_batch_qualification import qualify_batch

JSONL=Path("input/gate_ee_batch_001/BATCH_001_ENGINEERING_MATHEMATICS.jsonl")
HANDOFF=Path("input/gate_ee_batch_001/BATCH_001_FORMATTER_V2_HANDOFF.json")

def test_batch001_final_resolution_is_20_of_20_formatter_pass():
    r=qualify_batch(JSONL,HANDOFF)
    assert r["status"]=="PASS"
    assert r["question_count"]==20
    assert r["formatter_pass_count"]==20
    assert r["formatter_review_count"]==0
    assert r["paper_eligible_count"]==0
    assert r["release_gate"]=="BLOCKED"

def test_resolved_questions_are_revision_two_and_formatter_pass():
    r=qualify_batch(JSONL,HANDOFF)
    x={q["question_id"]:q for q in r["questions"]}
    for qid in ("TMB-GATE-EE-EM-005","TMB-GATE-EE-EM-016"):
        assert x[qid]["source_revision"]==2
        assert x[qid]["formatter_qualification"]=="PASS"
