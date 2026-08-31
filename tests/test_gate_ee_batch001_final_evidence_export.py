from pathlib import Path
import json, hashlib

def test_batch001_final_evidence_export_matches_report():
    report_path=Path("output/gate_ee_batch_001/FORMATTER_V2_QUALIFICATION.json")
    report=json.loads(report_path.read_text())
    export=json.loads(Path("output/gate_ee_batch_001/QUESTION_BANK_FINAL_EVIDENCE_EXPORT.json").read_text())
    assert export["source_sha256"]==report["source_sha256"]
    assert export["qualification_report_sha256"]==hashlib.sha256(report_path.read_bytes()).hexdigest()
    assert export["formatter_pass_count"]==20
    assert export["formatter_review_count"]==0
    assert export["paper_eligible_count"]==0
    assert export["independent_human_review_required"] is True
