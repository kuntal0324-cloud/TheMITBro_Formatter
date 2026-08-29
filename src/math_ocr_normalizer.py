from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable

from .math_normalizer import normalize_expression, validate_expression


MATH_SYMBOLS = set(
    "∫∑∏√∞∂∇≤≥≠≈±×÷πθλμσφωΔδαβγερτ"
)

COMMON_OCR_REPLACEMENTS = {
    "−": "-",
    "–": "-",
    "—": "-",
    "×": r"\times ",
    "÷": r"\div ",
    "≤": r"\leq ",
    "≥": r"\geq ",
    "≠": r"\neq ",
    "∞": r"\infty ",
    "π": r"\pi ",
    "θ": r"\theta ",
    "λ": r"\lambda ",
    "μ": r"\mu ",
    "σ": r"\sigma ",
    "ω": r"\omega ",
    "Δ": r"\Delta ",
    "∂": r"\partial ",
    "∇": r"\nabla ",
}

SUPERSCRIPTS = {
    "⁰":"0","¹":"1","²":"2","³":"3","⁴":"4",
    "⁵":"5","⁶":"6","⁷":"7","⁸":"8","⁹":"9",
    "⁺":"+","⁻":"-",
}

SUBSCRIPTS = {
    "₀":"0","₁":"1","₂":"2","₃":"3","₄":"4",
    "₅":"5","₆":"6","₇":"7","₈":"8","₉":"9",
}


@dataclass(frozen=True)
class MathRecognition:
    source: str
    normalized: str
    confidence: float
    features: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)


def _replace_script_runs(text: str, mapping: dict[str, str], marker: str) -> str:
    chars = "".join(re.escape(k) for k in mapping)
    pattern = re.compile(f"([{chars}]+)")
    def repl(match: re.Match[str]) -> str:
        value = "".join(mapping[ch] for ch in match.group(1))
        return marker + "{" + value + "}"
    return pattern.sub(repl, text)


def _normalize_common_ocr(text: str) -> str:
    s = text
    for old, new in COMMON_OCR_REPLACEMENTS.items():
        s = s.replace(old, new)

    s = _replace_script_runs(s, SUPERSCRIPTS, "^")
    s = _replace_script_runs(s, SUBSCRIPTS, "_")

    # Conservative OCR confusions inside mathematical contexts.
    s = re.sub(r"(?<=\d)[Oo](?=\d)", "0", s)
    s = re.sub(r"(?<=\d)[Il](?=\d)", "1", s)

    # Normalize determinant/rank/trace notation.
    s = re.sub(r"\bdet\s*\(", r"\\mathrm{det}(", s, flags=re.I)
    s = re.sub(r"\brank\s*\(", r"\\mathrm{rank}(", s, flags=re.I)
    s = re.sub(r"\btr\s*\(", r"\\mathrm{tr}(", s, flags=re.I)

    # Common textual operators.
    s = re.sub(r"\bsqrt\s*\(([^()]+)\)", r"\\sqrt{\1}", s, flags=re.I)
    s = re.sub(r"\blim\s*_\s*([A-Za-z])\s*[-=]*>\s*([^\s,;]+)",
               r"\\lim_{\1\\to \2}", s, flags=re.I)

    # "a/b" stays text unless clearly fraction-like.
    s = re.sub(r"(?<![\w)])\(([^()]+)\)\s*/\s*\(([^()]+)\)",
               r"\\frac{\1}{\2}", s)

    return re.sub(r"[ \t]+", " ", s).strip()


def detect_math_features(text: str) -> tuple[str, ...]:
    low = text.lower()
    features: list[str] = []

    checks = (
        ("matrix", bool(re.search(r"\[\s*\[|\\begin\{(?:b|p|v)?matrix\}", text))),
        ("determinant", bool(re.search(r"\bdet(?:erminant)?\b|\\mathrm\{det\}", low))),
        ("calculus", bool(re.search(r"∫|\\int|derivative|differentiat|integral|limit", low))),
        ("differential_equation", bool(re.search(r"\bode\b|\bpde\b|differential equation|dy\s*/\s*dx", low))),
        ("vector_calculus", bool(re.search(r"∇|\\nabla|gradient|divergence|curl", low))),
        ("probability_statistics", bool(re.search(r"probability|random variable|variance|standard deviation|expectation", low))),
        ("complex", bool(re.search(r"complex|conjugate|arg(?:ument)?|modulus|\bj\b", low))),
        ("transform", bool(re.search(r"fourier|laplace|z[- ]?transform", low))),
        ("summation", "∑" in text or r"\sum" in text),
        ("integral", "∫" in text or r"\int" in text),
        ("root", "√" in text or r"\sqrt" in text),
        ("subscript", bool(re.search(r"_[{A-Za-z0-9]", text))),
        ("superscript", bool(re.search(r"\^[{A-Za-z0-9]", text))),
    )

    for name, present in checks:
        if present:
            features.append(name)
    return tuple(features)


def recognize_math(text: str, *, ocr_confidence: float = 1.0) -> MathRecognition:
    source = str(text)
    normalized = _normalize_common_ocr(source)
    normalized = normalize_expression(normalized)
    validation = validate_expression(normalized)

    features = detect_math_features(source + " " + normalized)

    structural_penalty = min(0.35, 0.08 * len(validation.warnings))
    confidence = max(0.0, min(1.0, float(ocr_confidence) - structural_penalty))

    return MathRecognition(
        source=source,
        normalized=normalized,
        confidence=round(confidence, 3),
        features=features,
        warnings=tuple(validation.warnings),
    )
