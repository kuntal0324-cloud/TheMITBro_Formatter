from pathlib import Path
from src.gate_ee_batch_qualification import qualify_batch
J=Path("input/gate_ee_batch_001/BATCH_001_ENGINEERING_MATHEMATICS.jsonl"); H=Path("input/gate_ee_batch_001/BATCH_001_FORMATTER_V2_HANDOFF.json")
def test_count_checksum():
 r=qualify_batch(J,H); assert r["status"]=="PASS" and r["question_count"]==20
def test_human_gate_preserved():
 r=qualify_batch(J,H); assert r["paper_eligible_count"]==0 and r["release_gate"]=="BLOCKED" and all(x["independent_human_review"]=="PENDING" for x in r["questions"])
def test_unique_no_duplicate():
 r=qualify_batch(J,H); ids=[x["question_id"] for x in r["questions"]]; assert len(set(ids))==20 and all(x["duplicate"]["status"]=="ACCEPT" for x in r["questions"])
def test_render_smoke():
 r=qualify_batch(J,H); assert all(x["render"]["status"]=="PASS" for x in r["questions"])
