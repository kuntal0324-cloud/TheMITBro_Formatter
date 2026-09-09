from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import hashlib
import json
import re
import tempfile

from .question_ingest import ingest
from .question_duplicate_detector import find_duplicate
from .question_quality_score import score_question
from .question_formatter import format_document
from .human_math import humanize_math, has_source_math_markup


_EXPLICIT_VISUAL_REFERENCE = re.compile(
    r"\b(?:diagram|figure|shown\s+(?:below|above|in)|as\s+shown|draw|sketch)\b",
    re.I,
)

_ASCII_MATH_PATTERNS = (
    ("ASCII unit name", re.compile(r"\b(?:microfarads?|kilo-ohms?|ohms?)\b", re.I)),
    ("ASCII math function", re.compile(r"\b(?:sqrt|sin|cos|tan|ln|exp)\s*\(", re.I)),
    ("ASCII multiplication", re.compile(r"(?<=\d)\s+x\s+(?=\d)", re.I)),
    ("ASCII fraction", re.compile(r"\b\d+\s*/\s*\d+\b")),
    ("undelimited subscript/power", re.compile(r"[A-Za-z0-9][_^][A-Za-z0-9({-]")),
    ("undelimited electrical value", re.compile(r"\b\d+(?:\.\d+)?\s*(?:V|A|H|F|W|J|kW|kVA|kVAr|mH|mJ|rad/s)\b")),
)


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


def _source_math_contract(q: dict) -> dict:
    values = [str(q.get("stem", "")), str(q.get("solution", ""))]
    values.extend(str(option) for option in q.get("options", []))
    segments = 0
    violations: list[str] = []
    for value in values:
        parts = re.split(r"(?<!\\)\$", value)
        if len(parts) % 2 == 0:
            violations.append("unbalanced inline-math delimiter")
            continue
        segments += (len(parts) - 1) // 2
        outside_math = " ".join(parts[::2])
        for label, pattern in _ASCII_MATH_PATTERNS:
            if pattern.search(outside_math):
                violations.append(label)
    violations = sorted(set(violations))
    return {
        "status": "PASS" if not violations else "FAIL",
        "inline_math_segments": segments,
        "violations": violations,
    }


def qualify_batch(jsonl_path: str | Path, handoff_path: str | Path) -> dict:
    jsonl_path = Path(jsonl_path)
    handoff_path = Path(handoff_path)
    handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    batch_id = handoff.get("batch_id", "UNSPECIFIED_BATCH")

    errors = []
    if handoff.get("formatter_required_version") != "2.0.0":
        errors.append("Formatter version contract mismatch.")
    if _sha256(jsonl_path) != handoff.get("source_sha256"):
        errors.append("Question Bank handoff checksum mismatch.")
    if errors:
        return {
            "batch_id": batch_id,
            "status": "BLOCKED",
            "errors": errors,
            "question_count": 0,
            "formatter_pass_count": 0,
            "formatter_review_count": 0,
            "invalid_count": 0,
            "paper_eligible_count": 0,
            "independent_human_review_required": True,
            "release_gate": "BLOCKED",
            "questions": [],
        }

    questions = [json.loads(x) for x in jsonl_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    results = []
    prior = []

    with tempfile.TemporaryDirectory(prefix=f"tmb-{str(batch_id).lower()}-") as tmp:
        tmp = Path(tmp)
        for q in questions:
            md = _question_markdown(q)
            path = tmp / f"{q['id']}.md"
            path.write_text(md, encoding="utf-8")

            record = ingest(path, exam_hint="GATE_EE")

            # Canonical Question Bank records carry an explicit diagram field.
            # Component words such as "resistor" are useful visual-intelligence
            # cues, but they do not make a fully text-defined problem depend on
            # a missing figure.  Respect diagram=null unless the stem itself
            # explicitly requests or references a visual.
            diagram_declared = q.get("diagram") is not None
            visual_referenced = bool(_EXPLICIT_VISUAL_REFERENCE.search(q["stem"]))
            if not diagram_declared and not visual_referenced:
                record.metadata["requires_visual_review"] = False

            quality = score_question(record)
            dup = find_duplicate(md, prior)
            formatted = humanize_math(format_document(md))
            source_math = _source_math_contract(q)

            intelligence = record.metadata.get("question_intelligence", {})
            validation = record.metadata.get("validation_intelligence", {})

            # This qualification deliberately reports what Formatter v2.0 can
            # establish. It never invents independent human review.
            syllabus_match = (
                record.classification.exam == "GATE_EE"
                and record.classification.subject == q["subject"]
                and record.classification.topic == q["topic"]
            )
            render_pass = bool(formatted.strip()) and not has_source_math_markup(formatted)
            invalid = (
                record.metadata.get("validation_status") == "FAIL"
                or dup.status == "REJECT"
                or not render_pass
                or source_math["status"] != "PASS"
            )
            formatter_pass = (
                not invalid
                and syllabus_match
                and record.classification.status == "AUTO"
                and record.metadata.get("validation_status") == "PASS"
                and quality.grade == "A"
                and not quality.blockers
                and dup.status == "ACCEPT"
                and render_pass
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
                    "status": "PASS" if render_pass else "FAIL",
                    "bytes": len(formatted.encode("utf-8")),
                    "source_markup_exposed": has_source_math_markup(formatted),
                },
                "source_math_contract": source_math,
                "diagram_contract": {
                    "declared": diagram_declared,
                    "explicitly_referenced": visual_referenced,
                    "review_required": record.metadata.get("requires_visual_review", False),
                },
                "syllabus_match": syllabus_match,
                "formatter_qualification": (
                    "PASS" if formatter_pass else "INVALID" if invalid else "REVIEW"
                ),
                "independent_human_review": "PENDING",
                "paper_eligible": False,
            })
            prior.append({"id":q["id"], "text":md})

    passed = sum(r["formatter_qualification"] == "PASS" for r in results)
    review = sum(r["formatter_qualification"] == "REVIEW" for r in results)
    invalid = sum(r["formatter_qualification"] == "INVALID" for r in results)
    return {
        "qualification_contract": "GATE_EE_2027_FORMATTER_STRICT_R1",
        "batch_id": batch_id,
        "corpus": handoff.get("corpus"),
        "domain": handoff.get("domain"),
        "formatter_version": "2.0.0",
        "source_sha256": _sha256(jsonl_path),
        "question_count": len(results),
        "formatter_pass_count": passed,
        "formatter_review_count": review,
        "invalid_count": invalid,
        "paper_eligible_count": 0,
        "independent_human_review_required": True,
        "release_gate": "BLOCKED",
        "status": (
            "BLOCKED" if len(results) != handoff.get("question_count") or invalid
            else "REVIEW_REQUIRED" if review
            else "PASS"
        ),
        "questions": results,
    }


def write_qualification(jsonl_path: str | Path, handoff_path: str | Path, output_path: str | Path) -> dict:
    result = qualify_batch(jsonl_path, handoff_path)
    Path(output_path).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result
