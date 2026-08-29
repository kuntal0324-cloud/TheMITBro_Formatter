from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .diagram_intelligence import (
    DiagramAnalysis,
    analyze_diagram_text,
    analyze_image_geometry,
)


@dataclass(frozen=True)
class VisualQuestionAnalysis:
    diagram_present: bool
    diagram_type: str | None
    diagram_family: str | None
    confidence: float
    text_analysis: DiagramAnalysis
    image_analysis: DiagramAnalysis | None = None


def analyze_visual_question(
    text: str,
    *,
    image_path: str | Path | None = None,
) -> VisualQuestionAnalysis:
    text_result = analyze_diagram_text(text)
    image_result = None

    if image_path is not None:
        image_result = analyze_image_geometry(image_path)

    if text_result.present:
        return VisualQuestionAnalysis(
            True,
            text_result.diagram_type,
            text_result.family,
            text_result.confidence,
            text_result,
            image_result,
        )

    if image_result is not None and image_result.present:
        return VisualQuestionAnalysis(
            True,
            image_result.diagram_type,
            image_result.family,
            image_result.confidence,
            text_result,
            image_result,
        )

    return VisualQuestionAnalysis(
        False,
        None,
        None,
        0.0,
        text_result,
        image_result,
    )
