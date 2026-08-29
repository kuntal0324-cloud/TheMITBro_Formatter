from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class MathSegment:
    text: str
    kind: str
    start: int
    end: int


_PATTERNS = [
    ("display_latex", re.compile(r"\$\$(.+?)\$\$", re.S)),
    ("inline_latex", re.compile(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", re.S)),
    ("latex_env", re.compile(r"\\begin\{(?:b|p|v)?matrix\}.+?\\end\{(?:b|p|v)?matrix\}", re.S)),
    ("matrix_literal", re.compile(r"\[\s*\[[^\n]+?\]\s*\]")),
    ("equation", re.compile(
        r"(?<!\w)(?:[A-Za-z][A-Za-z0-9_{}^]*\s*)?"
        r"(?:=|≤|≥|<|>|\\leq|\\geq)"
        r"\s*[^,.;:\n]+"
    )),
]


def segment_math(text: str) -> list[MathSegment]:
    matches: list[MathSegment] = []
    occupied: list[tuple[int, int]] = []

    def overlaps(a: int, b: int) -> bool:
        return any(not (b <= x or a >= y) for x, y in occupied)

    for kind, pattern in _PATTERNS:
        for m in pattern.finditer(text):
            if overlaps(m.start(), m.end()):
                continue
            matches.append(MathSegment(m.group(0), kind, m.start(), m.end()))
            occupied.append((m.start(), m.end()))

    return sorted(matches, key=lambda s: s.start)
