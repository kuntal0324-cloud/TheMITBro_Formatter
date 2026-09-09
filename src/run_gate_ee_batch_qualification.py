from __future__ import annotations
import argparse
from pathlib import Path
from .gate_ee_batch_qualification import write_qualification

def main() -> int:
    p = argparse.ArgumentParser(description="Qualify a checksum-bound GATE EE source batch through frozen Formatter v2.0.")
    p.add_argument("--jsonl", type=Path, default=Path("input/gate_ee_batch_001/BATCH_001_ENGINEERING_MATHEMATICS.jsonl"))
    p.add_argument("--handoff", type=Path, default=Path("input/gate_ee_batch_001/BATCH_001_FORMATTER_V2_HANDOFF.json"))
    p.add_argument("--output", type=Path, default=Path("output/gate_ee_batch_001/FORMATTER_V2_QUALIFICATION.json"))
    args = p.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    r = write_qualification(args.jsonl, args.handoff, args.output)
    print(f"GATE EE {r['batch_id']} — FORMATTER v2.0 QUALIFICATION")
    print(f"Status: {r['status']}")
    print(f"Questions: {r['question_count']}")
    print(f"Formatter PASS: {r['formatter_pass_count']}")
    print(f"Formatter REVIEW: {r['formatter_review_count']}")
    print(f"Paper-eligible: {r['paper_eligible_count']}")
    print(f"Independent human review required: {r['independent_human_review_required']}")
    print(f"Release gate: {r['release_gate']}")
    return 0 if r["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
