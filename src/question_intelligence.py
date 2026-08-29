from __future__ import annotations

from dataclasses import dataclass, asdict, field
import math
import re

from .question_taxonomy import NODES, ConceptNode


@dataclass(frozen=True)
class QuestionIntelligence:
    exam: str
    subject: str
    topic: str
    subtopic: str
    concept: str
    taxonomy_confidence: float
    question_type: str
    marks: int | None
    difficulty: str
    difficulty_score: float
    reasoning_depth: str
    calculation_load: str
    expected_time_seconds: int
    syllabus_path: tuple[str, ...]
    prerequisites: tuple[str, ...]
    signals: tuple[str, ...] = ()
    review_required: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


def _norm_exam(exam_hint: str | None) -> str | None:
    if not exam_hint:
        return None
    x = re.sub(r"[^A-Za-z0-9]+", "", exam_hint).upper()
    if "GATE" in x and "EE" in x:
        return "GATE_EE"
    if "JEE" in x:
        return "JEE"
    return None


def _keyword_hit(text_low: str, keyword: str) -> bool:
    k = keyword.lower()
    if re.fullmatch(r"[a-z0-9 ]+", k):
        return bool(re.search(r"(?<![a-z0-9])" + re.escape(k) + r"(?![a-z0-9])", text_low))
    return k in text_low


def _taxonomy(text: str, exam_hint: str | None) -> tuple[ConceptNode | None, float, tuple[str, ...]]:
    low = text.lower()
    exam = _norm_exam(exam_hint)
    candidates = []
    for node in NODES:
        if exam and node.exam != exam:
            continue
        hits = tuple(k for k in node.keywords if _keyword_hit(low, k))
        if hits:
            # Specific/multiword terms carry more evidence.
            weighted = sum(1.25 if (" " in h or "-" in h or "(" in h) else 1.0 for h in hits)
            score = min(0.99, 0.55 + 0.11 * weighted)
            candidates.append((score, len(hits), max(map(len, hits)), node, hits))
    if not candidates:
        return None, 0.0, ()
    candidates.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
    score, _, _, node, hits = candidates[0]
    return node, round(score, 3), hits


def detect_question_type(text: str) -> str:
    low = text.lower()

    if re.search(r"\b(msq|multiple select|one or more options|more than one option|multiple correct)\b", low):
        return "MSQ"
    if re.search(r"\b(nat|numerical answer type|enter (?:a )?number|numerical value|answer is an integer|answer is a number)\b", low):
        return "NAT"

    # Four or more explicit answer choices -> MCQ unless wording says multiple.
    option_lines = re.findall(r"(?m)^\s*(?:[A-D][.)]|[1-4][.)])\s+", text)
    if len(option_lines) >= 2 or re.search(r"\bwhich of the following\b", low):
        return "MCQ"

    # GATE-style explicit question type metadata.
    m = re.search(r"\*\*Type:\*\*\s*(MCQ|MSQ|NAT)", text, re.I)
    if m:
        return m.group(1).upper()

    return "UNSPECIFIED"


def extract_marks(text: str) -> int | None:
    patterns = (
        r"\*\*Marks:\*\*\s*(\d+)",
        r"\bmarks?\s*[:=-]\s*(\d+)",
        r"\[(\d+)\s*marks?\]",
    )
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            return int(m.group(1))
    return None


def _complexity_features(text: str) -> dict[str, int | bool]:
    low = text.lower()
    equations = len(re.findall(r"=", text))
    operators = len(re.findall(r"[+\-*/^]|\\(?:int|sum|prod|frac|sqrt|partial|nabla)", text))
    numbers = len(re.findall(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?", text))
    steps = len(re.findall(r"\b(?:then|hence|therefore|first|next|substitute|solve|calculate|determine|derive|prove)\b", low))
    advanced = sum(bool(re.search(p, low)) for p in (
        r"eigen", r"differential equation", r"fourier", r"laplace",
        r"root locus", r"nyquist", r"load flow", r"symmetrical components",
        r"maxwell", r"convolution", r"three dimensional", r"rotational",
    ))
    conceptual = bool(re.search(r"\b(?:conceptually|qualitative|which statement|correct statement|reason|explain)\b", low))
    diagram = bool(re.search(r"\b(?:diagram|graph|plot|circuit|phasor|waveform|ray|free-body|free body)\b", low))
    return {
        "equations": equations, "operators": operators, "numbers": numbers,
        "steps": steps, "advanced": advanced, "conceptual": conceptual, "diagram": diagram,
    }


def estimate_difficulty(text: str) -> tuple[str, float, str, str, int]:
    f = _complexity_features(text)
    words = len(re.findall(r"\b\w+\b", text))

    score = 0.15
    score += min(0.18, f["equations"] * 0.035)
    score += min(0.18, f["operators"] * 0.018)
    score += min(0.12, f["numbers"] * 0.012)
    score += min(0.14, f["steps"] * 0.035)
    score += min(0.20, f["advanced"] * 0.08)
    score += min(0.08, words / 700)
    if f["diagram"]:
        score += 0.05
    score = round(min(1.0, score), 3)

    difficulty = "Easy" if score < 0.34 else "Medium" if score < 0.66 else "Hard"

    depth_score = f["steps"] + f["advanced"] + (1 if f["conceptual"] else 0)
    reasoning = "Direct" if depth_score <= 1 else "Multi-step" if depth_score <= 3 else "Deep"

    calc_score = f["operators"] + f["numbers"] + 2 * f["equations"]
    calculation = "Low" if calc_score < 8 else "Moderate" if calc_score < 20 else "High"

    base = 70
    base += 40 * (reasoning == "Multi-step") + 95 * (reasoning == "Deep")
    base += 35 * (calculation == "Moderate") + 80 * (calculation == "High")
    base += 30 if f["diagram"] else 0
    base += min(120, int(words * 0.7))
    expected = int(max(45, min(480, base)))

    return difficulty, score, reasoning, calculation, expected


def analyze_question(text: str, *, exam_hint: str | None = None) -> QuestionIntelligence:
    node, confidence, signals = _taxonomy(text, exam_hint)
    qtype = detect_question_type(text)
    marks = extract_marks(text)
    difficulty, score, reasoning, calc, expected = estimate_difficulty(text)

    if node is None:
        exam = _norm_exam(exam_hint) or "UNKNOWN"
        return QuestionIntelligence(
            exam=exam, subject="Review Required", topic="Review Required",
            subtopic="Review Required", concept="Review Required",
            taxonomy_confidence=0.0, question_type=qtype, marks=marks,
            difficulty=difficulty, difficulty_score=score,
            reasoning_depth=reasoning, calculation_load=calc,
            expected_time_seconds=expected,
            syllabus_path=(exam, "Review Required"),
            prerequisites=(), signals=(),
            review_required=True,
        )

    return QuestionIntelligence(
        exam=node.exam, subject=node.subject, topic=node.topic,
        subtopic=node.subtopic, concept=node.concept,
        taxonomy_confidence=confidence, question_type=qtype, marks=marks,
        difficulty=difficulty, difficulty_score=score,
        reasoning_depth=reasoning, calculation_load=calc,
        expected_time_seconds=expected,
        syllabus_path=(node.exam, node.subject, node.topic, node.subtopic, node.concept),
        prerequisites=node.prerequisites, signals=signals,
        review_required=confidence < 0.66,
    )
