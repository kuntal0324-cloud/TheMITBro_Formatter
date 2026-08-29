from __future__ import annotations

import hashlib
import shutil
import uuid
from pathlib import Path

from .question_bank_schema import QuestionRecord
from .question_classifier import classify_question
from .question_ocr import extract_text as extract_ocr_text
from .universal_math_recognizer import recognize_question_math
from .visual_question_analyzer import analyze_visual_question
from .universal_visual_intelligence import understand_visual
from .question_intelligence import analyze_question
from .validation_intelligence import validate_question_content


SUPPORTED = {".txt", ".md", ".jpg", ".jpeg", ".png"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_text(path: Path) -> tuple[str, str, float]:
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED:
        raise ValueError(f"Unsupported question source: {path.suffix}")

    result = extract_ocr_text(path)
    return result.text, result.source_type, result.confidence


def ingest(path: str | Path, *, exam_hint: str | None = None) -> QuestionRecord:
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(source)

    text, source_type, confidence = extract_text(source)
    text = text.strip()
    if not text:
        raise ValueError("Question source contains no readable text.")

    recognition = recognize_question_math(
        text,
        ocr_confidence=confidence,
    )

    # Classification deliberately uses the original extracted text.  The M32/M34
    # classifier taxonomy is trained on human-readable terminology and notation
    # such as det(A).  The normalized math form is stored separately for
    # rendering/search and must not distort routing.
    classification = classify_question(
        text,
        exam_hint=exam_hint,
    )

    # OCR/math uncertainty can never silently become an AUTO classification.
    if (
        source_type == "image"
        and (
            confidence < 0.85
            or recognition.math_confidence < 0.80
        )
    ):
        classification.status = "REVIEW"
        classification.topic = "Review Required"

    visual = analyze_visual_question(
        text,
        image_path=source if source_type == "image" else None,
    )
    visual_structure = understand_visual(
        text, image_path=source if source_type == "image" else None
    )
    intelligence = analyze_question(text, exam_hint=exam_hint)
    validation = validate_question_content(
        text,
        question_type=intelligence.question_type,
        visual_structure=visual_structure.to_dict() if visual_structure else None,
    )

    return QuestionRecord(
        id="QB-" + uuid.uuid4().hex[:12].upper(),
        schema_version="1.1",
        source_type=source_type,
        source_sha256=sha256_file(source),
        source_name=source.name,
        text=text,
        classification=classification,
        metadata={
            "ocr_confidence": confidence,
            "math_confidence": recognition.math_confidence,
            "math_features": list(recognition.features),
            "math_warnings": list(recognition.warnings),
            "normalized_math_text": recognition.normalized_text,
            "diagram_present": visual.diagram_present,
            "diagram_type": visual.diagram_type,
            "diagram_family": visual.diagram_family,
            "diagram_confidence": visual.confidence,
            "diagram_signals": list(visual.text_analysis.signals),
            "visual_structure": visual_structure.to_dict() if visual_structure else None,
            "visual_structure_confidence": visual_structure.confidence if visual_structure else 0.0,
            "visual_structure_warnings": list(visual_structure.warnings) if visual_structure else [],
            "requires_visual_review": bool(visual_structure and (visual_structure.confidence < 0.75 or visual_structure.warnings)),
            "ingestion_contract": "M35",
            "diagram_contract": "M36",
            "visual_intelligence_contract": "M37",
            "question_intelligence": intelligence.to_dict(),
            "question_type": intelligence.question_type,
            "marks": intelligence.marks,
            "difficulty": intelligence.difficulty,
            "difficulty_score": intelligence.difficulty_score,
            "reasoning_depth": intelligence.reasoning_depth,
            "calculation_load": intelligence.calculation_load,
            "expected_time_seconds": intelligence.expected_time_seconds,
            "subtopic": intelligence.subtopic,
            "concept": intelligence.concept,
            "syllabus_path": list(intelligence.syllabus_path),
            "prerequisites": list(intelligence.prerequisites),
            "question_intelligence_contract": "M38",
            "validation_intelligence": validation.to_dict(),
            "validation_status": validation.status,
            "answer_validation_status": validation.answer_status,
            "solution_validation_status": validation.solution_status,
            "diagram_text_validation_status": validation.diagram_text_status,
            "domain_validation_checks": list(validation.domain_checks),
            "quality_findings": list(validation.findings),
            "requires_validation_review": validation.review_required,
            "validation_intelligence_contract": "M39",
        },
    )


def copy_original_image(
    source: Path,
    record: QuestionRecord,
    assets_dir: Path,
) -> str | None:
    if record.source_type != "image":
        return None

    assets_dir.mkdir(parents=True, exist_ok=True)
    target = assets_dir / f"{record.id}{source.suffix.lower()}"
    shutil.copy2(source, target)
    return str(target)
