from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import math
import re
from typing import Iterable

from .diagram_detector import detect_diagram_type
from .engineering_diagram_generator import ENGINEERING_TYPES, EngineeringDiagramGenerator
from .mathematical_diagram_generator import MATHEMATICAL_TYPES, MathematicalDiagramGenerator


@dataclass(frozen=True)
class DiagramAnalysis:
    present: bool
    family: str | None
    diagram_type: str | None
    confidence: float
    signals: tuple[str, ...] = field(default_factory=tuple)
    reason: str = ""
    source: str = "text"


MATHEMATICAL_HINTS = {
    "coordinate_geometry": (
        r"\bcoordinate plane\b", r"\bcoordinate geometry\b",
        r"\bpoint\s+[A-Z]\b", r"\bx[- ]axis\b", r"\by[- ]axis\b",
        r"\bparabola\b", r"\bellipse\b", r"\bhyperbola\b",
    ),
    "function_plot": (
        r"\bplot\b", r"\bgraph of\b", r"\bf\s*\(\s*x\s*\)",
        r"\by\s*=", r"\bcurve\b",
    ),
    "geometric_figure": (
        r"\btriangle\b", r"\bcircle\b", r"\bquadrilateral\b",
        r"\bpolygon\b", r"\btangent\b", r"\bchord\b",
    ),
    "probability_diagram": (
        r"\bprobability tree\b", r"\btree diagram\b",
        r"\bconditional probability\b",
    ),
    "venn_diagram": (
        r"\bvenn\b", r"\bset diagram\b", r"\bintersection of sets\b",
    ),
    "number_line": (
        r"\bnumber line\b", r"\binterval\b",
    ),
    "statistical_plot": (
        r"\bhistogram\b", r"\bbox plot\b", r"\bscatter plot\b",
        r"\bbar graph\b", r"\bfrequency polygon\b",
    ),
    "vector_diagram": (
        r"\bvector diagram\b", r"\bresultant vector\b", r"\bvector addition\b",
    ),
}

ENGINEERING_HINTS = {
    "circuit_diagram": (
        r"\bcircuit\b", r"\bresistor\b", r"\bcapacitor\b", r"\binductor\b",
        r"\bvoltage source\b", r"\bcurrent source\b", r"\bRLC\b",
        r"\bwheatstone bridge\b", r"\bbridge diagram\b",
    ),
    "phasor_diagram": (
        r"\bphasor\b", r"∠", r"\bphase angle\b", r"\bpower factor\b",
    ),
    "block_diagram": (
        r"\bblock diagram\b", r"\bforward path\b",
    ),
    "control_system_diagram": (
        r"\bcontrol system\b", r"\bfeedback\b", r"\btransfer function\b",
        r"\bsumming point\b",
    ),
    "signal_diagram": (
        r"\bsignal flow\b", r"\bsignal diagram\b",
    ),
    "waveform": (
        r"\bwaveform\b", r"\bsine wave\b", r"\bsquare wave\b",
        r"\btriangular wave\b", r"\bpulse\b", r"\bduty cycle\b",
    ),
    "transformer_equivalent_circuit": (
        r"\btransformer\b.*\bequivalent circuit\b",
        r"\bR1\b", r"\bX1\b", r"\bR2'?(\b|[^A-Za-z0-9])",
    ),
    "motor_diagram": (
        r"\binduction motor\b", r"\bsynchronous motor\b",
        r"\bstator\b", r"\brotor\b", r"\bslip\b",
    ),
    "logic_circuit": (
        r"\blogic circuit\b", r"\bAND gate\b", r"\bOR gate\b",
        r"\bNOT gate\b", r"\bNAND\b", r"\bNOR\b", r"\bXOR\b",
    ),
    "network_diagram": (
        r"\bnetwork diagram\b", r"\bnodes?\b.*\bbranches?\b",
    ),
}



PHYSICS_HINTS = {
 "free_body_diagram":(r"\bfree[- ]body diagram\b",r"\bFBD\b",r"\bnormal force\b.*\bfriction\b"),
 "ray_diagram":(r"\bray diagram\b",r"\bprincipal axis\b.*\b(?:lens|mirror)\b",r"\bconvex lens\b"),
 "field_line_diagram":(r"\bfield lines?\b",r"\belectric field diagram\b",r"\bmagnetic field diagram\b"),
 "motion_graph":(r"\bposition[- ]time graph\b",r"\bvelocity[- ]time graph\b",r"\bacceleration[- ]time graph\b"),
 "wave_diagram":(r"\bwave diagram\b",r"\bwave profile\b",r"\bwavelength\b.*\bamplitude\b"),
}

def _collect_matches(text: str, rules: dict[str, tuple[str, ...]]) -> list[tuple[str, tuple[str, ...]]]:
    out: list[tuple[str, tuple[str, ...]]] = []
    for typ, patterns in rules.items():
        hits = tuple(p for p in patterns if re.search(p, text, re.I | re.S))
        if hits:
            out.append((typ, hits))
    return out


def analyze_diagram_text(text: str) -> DiagramAnalysis:
    """
    Conservative semantic diagram analysis for question text/OCR.

    It combines the legacy detector with richer M36 mathematical and
    Electrical Engineering cue sets.  It does not infer topology that is not
    present in the source.
    """
    raw = str(text)
    legacy = detect_diagram_type(raw)

    math_hits = _collect_matches(raw, MATHEMATICAL_HINTS)
    eng_hits = _collect_matches(raw, ENGINEERING_HINTS)
    physics_hits = _collect_matches(raw, PHYSICS_HINTS)

    candidates: list[tuple[float, str, str, tuple[str, ...], str]] = []

    for typ, hits in math_hits:
        score = min(0.98, 0.72 + 0.07 * len(hits))
        candidates.append((score, "mathematical", typ, hits, "M36 mathematical cues"))

    for typ, hits in eng_hits:
        score = min(0.98, 0.74 + 0.07 * len(hits))
        candidates.append((score, "engineering", typ, hits, "M36 engineering cues"))

    for typ, hits in physics_hits:
        score = min(0.98, 0.76 + 0.07 * len(hits))
        candidates.append((score, "physics", typ, hits, "M37 physics cues"))

    if legacy is not None:
        family = (
            "engineering" if legacy.diagram_type in ENGINEERING_TYPES
            else "mathematical" if legacy.diagram_type in MATHEMATICAL_TYPES
            else "other"
        )
        candidates.append(
            (
                legacy.confidence,
                family,
                legacy.diagram_type,
                tuple(legacy.matched_terms),
                "legacy detector",
            )
        )

    if not candidates:
        return DiagramAnalysis(False, None, None, 0.0, (), "No diagram cues detected.", "text")

    candidates.sort(key=lambda x: (x[0], len(x[3])), reverse=True)
    score, family, typ, hits, reason = candidates[0]
    return DiagramAnalysis(
        True,
        family,
        typ,
        round(score, 3),
        tuple(sorted(set(hits))),
        reason,
        "text",
    )


def analyze_image_geometry(path: str | Path) -> DiagramAnalysis:
    """
    Lightweight image-geometry screening.

    This intentionally answers only whether an image plausibly contains
    diagram-like line structure. It does not claim semantic circuit/graph
    recognition from pixels.
    """
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(source)

    try:
        from PIL import Image, ImageFilter, ImageOps
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Image diagram screening requires Pillow.") from exc

    with Image.open(source) as img:
        img = ImageOps.exif_transpose(img).convert("L")
        # Downscale for stable CI performance.
        img.thumbnail((900, 900))
        edges = img.filter(ImageFilter.FIND_EDGES)
        hist = edges.histogram()
        total = sum(hist) or 1
        strong = sum(hist[80:])
        edge_ratio = strong / total

    # Conservative gate: text-only scans are allowed to remain false.
    present = edge_ratio >= 0.035
    confidence = min(0.90, max(0.0, (edge_ratio - 0.02) * 6.0)) if present else 0.0

    return DiagramAnalysis(
        present=present,
        family="visual" if present else None,
        diagram_type="diagram_candidate" if present else None,
        confidence=round(confidence, 3),
        signals=(f"edge_ratio={edge_ratio:.4f}",),
        reason="Image line-structure screening.",
        source="image",
    )


def generate_detected_diagram(
    question: str,
    *,
    data=None,
    output_path: str | Path | None = None,
    width: int = 1000,
    height: int = 650,
):
    analysis = analyze_diagram_text(question)
    if not analysis.present or not analysis.diagram_type:
        raise ValueError("No supported diagram request detected.")

    if analysis.family == "engineering":
        return EngineeringDiagramGenerator().generate(
            question, data=data, output_path=output_path, width=width, height=height
        )

    if analysis.family == "mathematical":
        return MathematicalDiagramGenerator().generate(
            question, data=data, output_path=output_path, width=width, height=height
        )

    raise ValueError(f"Unsupported diagram family: {analysis.family}")
