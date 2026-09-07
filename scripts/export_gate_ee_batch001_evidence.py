"""Generate checksum-bound strict Formatter evidence for GATE EE Batch 001."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.gate_ee_batch_qualification import write_qualification


INPUT = ROOT / "input/gate_ee_batch_001/BATCH_001_ENGINEERING_MATHEMATICS.jsonl"
HANDOFF = ROOT / "input/gate_ee_batch_001/BATCH_001_FORMATTER_V2_HANDOFF.json"
REPORT = ROOT / "output/gate_ee_batch_001/FORMATTER_V2_STRICT_REQUALIFICATION.json"
EXPORT = ROOT / "output/gate_ee_batch_001/QUESTION_BANK_FINAL_EVIDENCE_EXPORT.json"
SUMMARY = ROOT / "GATE_EE_BATCH001_QUALIFICATION_SUMMARY.json"


def main() -> int:
    result = write_qualification(INPUT, HANDOFF, REPORT)
    payload = {
        "export_contract": "GATE_EE_2027_FORMATTER_STRICT_EVIDENCE_R2",
        "formatter_version": result["formatter_version"],
        "batch_id": "BATCH_001",
        "source_sha256": result["source_sha256"],
        "question_count": result["question_count"],
        "formatter_pass_count": result["formatter_pass_count"],
        "formatter_review_count": result["formatter_review_count"],
        "invalid_count": result["invalid_count"],
        "status": result["status"],
        "paper_eligible_count": result["paper_eligible_count"],
        "independent_human_review_required": result["independent_human_review_required"],
        "release_gate": result["release_gate"],
        "qualification_report": REPORT.name,
        "qualification_report_sha256": hashlib.sha256(REPORT.read_bytes()).hexdigest(),
    }
    EXPORT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    summary = {
        "status": result["status"],
        "qualification_contract": result["qualification_contract"],
        "question_count": result["question_count"],
        "formatter_pass_count": result["formatter_pass_count"],
        "formatter_review_count": result["formatter_review_count"],
        "invalid_count": result["invalid_count"],
        "render_pass_count": sum(q["render"]["status"] == "PASS" for q in result["questions"]),
        "source_markup_exposed_count": sum(q["render"]["source_markup_exposed"] for q in result["questions"]),
        "validation_pass_count": sum(q["validation"]["status"] == "PASS" for q in result["questions"]),
        "quality_grade_a_count": sum(q["quality"]["grade"] == "A" for q in result["questions"]),
        "syllabus_match_count": sum(q["syllabus_match"] for q in result["questions"]),
        "paper_eligible_count": result["paper_eligible_count"],
        "independent_human_review_required": result["independent_human_review_required"],
        "release_gate": result["release_gate"],
        "source_sha256": result["source_sha256"],
        "qualification_report": str(REPORT.relative_to(ROOT)),
        "qualification_report_sha256": payload["qualification_report_sha256"],
        "note": "Formatter qualification passed; named independent human review is still required before paper eligibility.",
    }
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print(f"Strict status: {result['status']}")
    print(f"PASS: {result['formatter_pass_count']}")
    print(f"REVIEW: {result['formatter_review_count']}")
    print(f"INVALID: {result['invalid_count']}")
    print("Paper-eligible: 0 (named human review pending)")
    return 0 if (
        result["status"] == "PASS"
        and result["formatter_pass_count"] == result["question_count"]
        and result["formatter_review_count"] == 0
        and result["invalid_count"] == 0
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
