from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "input/gate_ee_set01/GATE_EE_SET_01_RELEASE_INPUT.json"
OUTPUT = ROOT / "output/gate_ee_set01/FORMATTER_RELEASE_CANDIDATE_EVIDENCE.json"

BATCH_REPORTS = {
    "BATCH_001": ROOT / "output/gate_ee_batch_001/FORMATTER_V2_STRICT_REQUALIFICATION.json",
    "BATCH_002": ROOT / "output/gate_ee_batch_002/FORMATTER_V2_QUALIFICATION.json",
    "BATCH_003": ROOT / "output/gate_ee_batch_003/FORMATTER_V2_QUALIFICATION.json",
    "BATCH_004": ROOT / "output/gate_ee_batch_004/FORMATTER_V2_QUALIFICATION.json",
    "BATCH_005": ROOT / "output/gate_ee_batch_005/FORMATTER_V2_QUALIFICATION.json",
}


def canonical_bytes(payload: Any) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")


def content_sha256(payload: dict[str, Any], field: str) -> str:
    unsigned = dict(payload)
    unsigned.pop(field, None)
    return hashlib.sha256(canonical_bytes(unsigned)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _row_passes(row: dict[str, Any]) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if row.get("formatter_qualification") != "PASS":
        failures.append("formatter qualification is not PASS")
    validation = row.get("validation", {})
    if validation.get("status") != "PASS" or validation.get("review_required") is not False:
        failures.append("validation is not a review-free PASS")
    quality = row.get("quality", {})
    if quality.get("grade") != "A" or quality.get("blockers"):
        failures.append("quality grade is not blocker-free A")
    if row.get("duplicate", {}).get("status") != "ACCEPT":
        failures.append("duplicate gate is not ACCEPT")
    render = row.get("render", {})
    if render.get("status") != "PASS" or render.get("source_markup_exposed") is not False:
        failures.append("render gate is not clean PASS")
    if row.get("source_math_contract", {}).get("status") != "PASS":
        failures.append("source-math contract is not PASS")
    diagram = row.get("diagram_contract", {})
    if diagram.get("declared") and diagram.get("status") != "PASS":
        failures.append("declared diagram contract is not PASS")
    if row.get("syllabus_match") is not True:
        failures.append("syllabus match is not true")
    return not failures, failures


def qualify_set01(input_path: str | Path = INPUT) -> dict[str, Any]:
    input_path = Path(input_path)
    payload = load_json(input_path)
    errors: list[str] = []
    if payload.get("input_contract") != "GATE_EE_SET01_FORMATTER_RELEASE_INPUT_V1":
        errors.append("input contract mismatch")
    if payload.get("paper_id") != "GATE_2027_EE_SET_01":
        errors.append("paper ID mismatch")
    if payload.get("input_content_sha256") != content_sha256(payload, "input_content_sha256"):
        errors.append("input self-hash mismatch")
    if payload.get("release_authorized") is not False or payload.get("sale_authorized") is not False:
        errors.append("Formatter input must not authorize release or sale")

    questions = payload.get("questions", [])
    if len(questions) != 65:
        errors.append(f"input must contain 65 selected questions, found {len(questions)}")
    if [row.get("position") for row in questions] != list(range(1, 66)):
        errors.append("question positions must be exactly 1 through 65")
    ids = [row.get("question_id") for row in questions]
    if len(ids) != len(set(ids)):
        errors.append("selected question IDs are not unique")

    reports: dict[str, dict[str, Any]] = {}
    report_rows: dict[tuple[str, str], dict[str, Any]] = {}
    sources: dict[str, dict[str, Any]] = {}
    for batch_id, path in BATCH_REPORTS.items():
        report = load_json(path)
        reports[batch_id] = report
        sources[batch_id] = {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(path),
            "status": report.get("status"),
        }
        for row in report.get("questions", []):
            report_rows[(batch_id, row.get("question_id"))] = row

    results: list[dict[str, Any]] = []
    for selected in questions:
        batch_id = selected.get("batch_id")
        question_id = selected.get("question_id")
        report_row = report_rows.get((batch_id, question_id))
        failures: list[str] = []
        if report_row is None:
            failures.append("question is absent from the declared batch report")
        else:
            if report_row.get("source_revision") != selected.get("source_revision"):
                failures.append("source revision differs from the release input")
            passed, row_failures = _row_passes(report_row)
            if not passed:
                failures.extend(row_failures)
        results.append({
            "position": selected.get("position"),
            "question_id": question_id,
            "source_revision": selected.get("source_revision"),
            "batch_id": batch_id,
            "formatter_release_qualification": "PASS" if not failures else "BLOCKED",
            "failures": failures,
        })

    passed_count = sum(row["formatter_release_qualification"] == "PASS" for row in results)
    blocked_count = len(results) - passed_count
    status = "PASS" if not errors and passed_count == 65 and blocked_count == 0 else "BLOCKED"
    output: dict[str, Any] = {
        "evidence_contract": "GATE_EE_SET01_FORMATTER_RELEASE_CANDIDATE_EVIDENCE_V1",
        "paper_id": payload.get("paper_id"),
        "review_manifest_content_sha256": payload.get("review_manifest_content_sha256"),
        "review_handoff_content_sha256": payload.get("review_handoff_content_sha256"),
        "input": {
            "path": input_path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(input_path),
            "content_sha256": payload.get("input_content_sha256"),
        },
        "batch_reports": sources,
        "question_count": len(results),
        "formatter_pass_count": passed_count,
        "formatter_blocked_count": blocked_count,
        "status": status,
        "errors": errors,
        "questions": results,
        "release_gate": "BLOCKED_PENDING_EXACT_ARTIFACT_RELEASE_AUTHORIZATION",
        "release_authorized": False,
        "sale_authorized": False,
    }
    output["evidence_content_sha256"] = content_sha256(output, "evidence_content_sha256")
    return output

