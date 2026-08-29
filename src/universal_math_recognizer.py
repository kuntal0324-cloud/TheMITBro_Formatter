from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .math_ocr_normalizer import MathRecognition, recognize_math
from .math_segmenter import MathSegment, segment_math
from .scientific_notation_normalizer import normalize_scientific_notation


@dataclass(frozen=True)
class UniversalRecognitionResult:
    text: str
    normalized_text: str
    math_confidence: float
    features: tuple[str, ...]
    warnings: tuple[str, ...]
    segments: tuple[MathSegment, ...]


def recognize_question_math(
    text: str,
    *,
    ocr_confidence: float = 1.0,
) -> UniversalRecognitionResult:
    scientific = normalize_scientific_notation(text)
    recognition: MathRecognition = recognize_math(
        scientific,
        ocr_confidence=ocr_confidence,
    )

    return UniversalRecognitionResult(
        text=text,
        normalized_text=recognition.normalized,
        math_confidence=recognition.confidence,
        features=recognition.features,
        warnings=recognition.warnings,
        segments=tuple(segment_math(recognition.normalized)),
    )
