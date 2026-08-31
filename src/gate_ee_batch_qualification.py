from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import hashlib
import json
import tempfile

from .question_ingest import ingest
from .question_duplicate_detector import find_duplicate
from .question_quality_score import score_question
from .question_formatter import format_document


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _question_markdown(q: dict) -> str:
    lines = [
        f"### {q['id']}",
        "",
        f"**Exam:** {q['exam']}",
        f"**Subject:** {q['subject']}",
        f"**Topic:** {q['topic']}",
        f"**Subtopic:** {q['subtopic']}",
        f"**Concept:** {q['concept']}",
        f"**Difficulty:** {q['difficulty']}",
        f"**Type:** {q['type']}",
        f"**Marks:** {q['marks']}",
        "",
        q["stem"],
        "",
    ]
    for label, option in zip(("A","B","C","D"), q.get("options", [])):
        lines.append(f"{label}. {option}")
    if q.get("options"):
        lines.append("")
    answer = q["answer"]
    if isinstance(answer, list):
        answer = ",".join(answer)
    lines += [
        f"**Answer:** {answer}",
        "",
        "**Solution:**",
        q["solution"],
        "",
    ]
    return "\n".join(lines)


def qualify_batch(jsonl_path: str | Path, handoff_path: str | Path) -> dict:
    jsonl_path = Path(jsonl_path)
    handoff_path = Path(handoff_path)
    handoff = json.loads(handoff_path.read_text(encoding="utf-8"))

    errors = []
    if handoff.get("formatter_required_version") != "2.0.0":
        errors.append("Formatter version contract mismatch.")
    if _sha256(jsonl_path) != handoff.get("source_sha256"):
        errors.append("Question Bank handoff checksum mismatch.")
    if errors:
        return {"status":"BLOCKED","errors":errors,"questions":[]}

    questions = [json.loads(x) for x in jsonl_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    results = []
    prior = []

    with tempfile.TemporaryDirectory(prefix="tmb-batch001-") as tmp:
        tmp = Path(tmp)
        for q in questions:
            md = _question_markdown(q)
            path = tmp / f"{q['id']}.md"
            path.write_text(md, encoding="utf-8")

            record = ingest(path, exam_hint="GATE_EE")
            quality = score_question(record)
            dup = find_duplicate(md, prior)
            formatted = format_document(md)

            intelligence = record.metadata.get("question_intelligence", {})
            validation = record.metadata.get("validation_intelligence", {})

            # This qualification deliberately reports what Formatter v2.0 can
            # establish. It never invents independent human review.
            formatter_pass = (
                record.classification.exam == "GATE_EE"
                and record.classification.subject == "Engineering Mathematics"
                and record.classification.status in {"AUTO","REVIEW"}
                and dup.status == "ACCEPT"
                and bool(formatted.strip())
            )

            results.append({
                "question_id": q["id"],
                "source_revision": q["revision"],
                "classification": {
                    "exam": record.classification.exam,
                    "subject": record.classification.subject,
                    "topic": record.classification.topic,
                    "status": record.classification.status,
                    "confidence": record.classification.confidence,
                },
                "question_intelligence": intelligence,
                "validation": {
                    "status": record.metadata.get("validation_status"),
                    "answer_status": record.metadata.get("answer_validation_status"),
                    "solution_status": record.metadata.get("solution_validation_status"),
                    "review_required": record.metadata.get("requires_validation_review"),
                    "findings": record.metadata.get("quality_findings", []),
                    "raw": validation,
                },
                "quality": quality.to_dict(),
                "duplicate": asdict(dup),
                "render": {
                    "status": "PASS" if formatted.strip() else "FAIL",
                    "bytes": len(formatted.encode("utf-8")),
                },
                "formatter_qualification": "PASS" if formatter_pass else "REVIEW",
                "independent_human_review": "PENDING",
                "paper_eligible": False,
            })
            prior.append({"id":q["id"], "text":md})

    passed = sum(r["formatter_qualification"] == "PASS" for r in results)
    review = len(results) - passed
    return {
        "qualification_contract": "GATE_EE_BATCH001_FORMATTER_V2_Q1",
        "formatter_version": "2.0.0",
        "source_sha256": _sha256(jsonl_path),
        "question_count": len(results),
        "formatter_pass_count": passed,
        "formatter_review_count": review,
        "paper_eligible_count": 0,
        "independent_human_review_required": True,
        "release_gate": "BLOCKED",
        "status": "PASS" if len(results) == handoff.get("question_count") else "BLOCKED",
        "questions": results,
    }


def write_qualification(jsonl_path: str | Path, handoff_path: str | Path, output_path: str | Path) -> dict:
    result = qualify_batch(jsonl_path, handoff_path)
    Path(output_path).write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result
