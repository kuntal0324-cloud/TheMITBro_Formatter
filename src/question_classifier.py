from __future__ import annotations

import re
from dataclasses import dataclass

from .question_bank_schema import Classification


@dataclass(frozen=True)
class TopicRule:
    exam: str
    subject: str
    topic: str
    keywords: tuple[str, ...]


# The taxonomy is intentionally explicit and conservative. It can be expanded
# without changing the question-bank record format.
RULES = (
    # GATE EE / Engineering Mathematics
    TopicRule(
        "GATE_EE",
        "Engineering Mathematics",
        "Matrices",
        (
            "matrix",
            "matrices",
            "determinant",
            "det(",
            "det (",
            "eigenvalue",
            "eigenvalues",
            "eigenvector",
            "eigenvectors",
            "rank",
        ),
    ),
    TopicRule(
        "GATE_EE",
        "Engineering Mathematics",
        "Calculus",
        ("derivative", "differentiate", "integration", "integral", "limit", "continuity"),
    ),
    TopicRule(
        "GATE_EE",
        "Engineering Mathematics",
        "Differential Equations",
        ("differential equation", "ode", "pde", "laplace equation"),
    ),
    TopicRule(
        "GATE_EE",
        "Engineering Mathematics",
        "Probability and Statistics",
        ("probability", "random variable", "variance", "mean", "standard deviation", "distribution"),
    ),
    TopicRule(
        "GATE_EE",
        "Engineering Mathematics",
        "Complex Variables",
        ("complex number", "complex variable", "modulus", "argument", "conjugate"),
    ),
    TopicRule(
        "GATE_EE",
        "Engineering Mathematics",
        "Transforms",
        ("fourier", "laplace transform", "z-transform", "z transform"),
    ),
    TopicRule(
        "GATE_EE",
        "Engineering Mathematics",
        "Numerical Methods",
        ("newton-raphson", "newton raphson", "interpolation", "numerical method", "trapezoidal rule"),
    ),
    TopicRule(
        "GATE_EE",
        "Engineering Mathematics",
        "Vector Calculus",
        ("gradient", "divergence", "curl", "vector calculus", "line integral"),
    ),

    # GATE EE
    TopicRule(
        "GATE_EE",
        "Electrical Engineering",
        "Network Theory",
        ("kirchhoff", "thevenin", "norton", "network", "impedance", "admittance", "rc circuit", "rl circuit", "ohm law", "resistor", "voltage source"),
    ),
    TopicRule(
        "GATE_EE",
        "Electrical Engineering",
        "Signals and Systems",
        ("signal", "convolution", "sampling", "system response", "impulse response"),
    ),
    TopicRule(
        "GATE_EE",
        "Electrical Engineering",
        "Electrical Machines",
        ("induction motor", "synchronous motor", "transformer", "dc motor", "dc machine", "alternator"),
    ),
    TopicRule(
        "GATE_EE",
        "Electrical Engineering",
        "Power Systems",
        ("power system", "load flow", "load-flow", "fault", "transmission line", "power factor", "per unit", "slack bus", "pq bus", "pv bus"),
    ),
    TopicRule(
        "GATE_EE",
        "Electrical Engineering",
        "Control Systems",
        ("transfer function", "root locus", "bode", "nyquist", "control system", "state space"),
    ),
    TopicRule(
        "GATE_EE",
        "Electrical Engineering",
        "Power Electronics",
        ("rectifier", "inverter", "chopper", "thyristor", "mosfet", "igbt", "pwm"),
    ),
    TopicRule(
        "GATE_EE",
        "Electrical Engineering",
        "Measurements",
        ("measurement", "instrumentation", "wheatstone", "transducer", "oscilloscope"),
    ),
    TopicRule(
        "GATE_EE",
        "Electrical Engineering",
        "Electronics",
        ("diode", "transistor", "op-amp", "operational amplifier", "amplifier", "bjt"),
    ),


    TopicRule(
        "GATE_EE",
        "Electrical Engineering",
        "Electromagnetic Fields",
        (
            "electric field", "magnetic field", "gauss law", "ampere law",
            "maxwell", "electromagnetic field", "poisson equation",
            "laplace equation", "boundary condition",
        ),
    ),
    TopicRule(
        "GATE_EE",
        "Electrical Engineering",
        "Analog Electronics",
        (
            "operational amplifier", "op-amp", "bjt", "mosfet",
            "amplifier", "biasing", "small signal", "frequency response",
        ),
    ),
    TopicRule(
        "GATE_EE",
        "Electrical Engineering",
        "Digital Electronics",
        (
            "logic gate", "boolean", "flip flop", "flip-flop",
            "counter", "register", "multiplexer", "demultiplexer",
            "karnaugh", "k-map",
        ),
    ),

    # JEE Mathematics
    TopicRule(
        "JEE",
        "Mathematics",
        "Algebra",
        ("quadratic", "polynomial", "sequence", "series", "binomial", "permutation", "combination"),
    ),
    TopicRule(
        "JEE",
        "Mathematics",
        "Calculus",
        ("limit", "continuity", "derivative", "differentiation", "integration", "definite integral"),
    ),
    TopicRule(
        "JEE",
        "Mathematics",
        "Coordinate Geometry",
        ("straight line", "circle", "parabola", "ellipse", "hyperbola", "coordinate geometry"),
    ),
    TopicRule(
        "JEE",
        "Mathematics",
        "Matrices and Determinants",
        ("matrix", "determinant", "matrices"),
    ),
    TopicRule(
        "JEE",
        "Mathematics",
        "Probability and Statistics",
        ("probability", "statistics", "mean", "variance", "standard deviation"),
    ),
    TopicRule(
        "JEE",
        "Mathematics",
        "Trigonometry",
        ("trigonometry", "sin", "cos", "tan", "trigonometric"),
    ),
    TopicRule(
        "JEE",
        "Physics",
        "Mechanics",
        ("velocity", "acceleration", "force", "momentum", "projectile", "newton's law"),
    ),
    TopicRule(
        "JEE",
        "Physics",
        "Electrodynamics",
        ("electric field", "electric potential", "capacitance", "magnetic field", "electromagnetic"),
    ),
    TopicRule(
        "JEE",
        "Physics",
        "Modern Physics",
        ("photoelectric", "nuclear", "radioactive", "de broglie", "bohr", "semiconductor"),
    ),

    TopicRule(
        "JEE",
        "Physics",
        "Oscillations and Waves",
        (
            "simple harmonic", "shm", "oscillation", "wave equation",
            "standing wave", "sound wave", "doppler", "resonance",
        ),
    ),
    TopicRule(
        "JEE",
        "Physics",
        "Optics",
        (
            "ray optics", "wave optics", "lens", "mirror", "interference",
            "diffraction", "polarization", "young double slit",
        ),
    ),
    TopicRule(
        "JEE",
        "Physics",
        "Thermal Physics",
        (
            "thermodynamics", "kinetic theory", "heat", "temperature",
            "entropy", "specific heat", "ideal gas",
        ),
    ),

    TopicRule(
        "JEE",
        "Chemistry",
        "Physical Chemistry",
        ("mole", "thermodynamics", "equilibrium", "electrochemistry", "kinetics"),
    ),
    TopicRule(
        "JEE",
        "Chemistry",
        "Organic Chemistry",
        ("alkane", "alkene", "alkyne", "benzene", "carbonyl", "organic"),
    ),
    TopicRule(
        "JEE",
        "Chemistry",
        "Inorganic Chemistry",
        ("periodic table", "coordination compound", "coordination complex", "inorganic"),
    ),
)


def _normalize(text: str) -> str:
    text = text.lower().replace("−", "-")

    # Normalize common mathematical notation so the classifier
    # understands equivalent representations.
    text = re.sub(r"\bdet\s*\(", "det(", text)
    text = re.sub(r"\beig\s*\(", "eig(", text)
    text = re.sub(r"\brank\s*\(", "rank(", text)

    # Normalize whitespace without destroying mathematical notation.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def _keyword_hits(text: str, keywords: tuple[str, ...]) -> list[str]:
    """
    Match ordinary topic keywords and mathematical notation.

    Mathematical notation is only accepted when the current topic
    explicitly declares that notation as one of its keywords.
    """
    hits: list[str] = []

    normalized_keywords = {
        keyword.lower().strip()
        for keyword in keywords
    }

    # ------------------------------------------------------------
    # Ordinary words / phrases
    # ------------------------------------------------------------

    notation_aliases = {
        "det(",
        "rank(",
        "eig(",
    }

    for keyword in normalized_keywords:
        if keyword in notation_aliases:
            continue

        pattern = rf"(?<!\w){re.escape(keyword)}(?!\w)"

        if re.search(pattern, text):
            hits.append(keyword)

    # ------------------------------------------------------------
    # Mathematical notation
    # ------------------------------------------------------------

    notation_patterns = {
        "det(": r"(?<!\w)det\s*\(",
        "rank(": r"(?<!\w)rank\s*\(",
        "eig(": r"(?<!\w)eig\s*\(",
    }

    for label, pattern in notation_patterns.items():
        if label in normalized_keywords and re.search(pattern, text):
            hits.append(label)

    # ------------------------------------------------------------
    # Eigenvalue / eigenvector terminology
    # ------------------------------------------------------------

    if "eigenvalue" in normalized_keywords:
        if re.search(r"(?<!\w)eigenvalues?\b", text):
            hits.append("eigenvalue")

    if "eigenvector" in normalized_keywords:
        if re.search(r"(?<!\w)eigenvectors?\b", text):
            hits.append("eigenvector")

    return sorted(set(hits))


def classify_question(
    text: str,
    *,
    exam_hint: str | None = None,
) -> Classification:
    t = _normalize(text)
    candidates = []

    for rule in RULES:
        if exam_hint:
            eh = exam_hint.lower().replace(" ", "_")

            if eh in {"gate", "gate_ee", "gate-ee"} and rule.exam != "GATE_EE":
                continue
            if eh == "jee" and rule.exam != "JEE":
                continue

        hits = _keyword_hits(t, rule.keywords)
        if hits:
            score = min(0.99, 0.58 + 0.12 * len(set(hits)))
            candidates.append((score, len(hits), rule, hits))

    # ------------------------------------------------------------
    # No classification
    # ------------------------------------------------------------

    if not candidates:
        return Classification(
            "GENERAL",
            "Unclassified",
            "Review Required",
            0.0,
            [],
            "REVIEW",
        )

    # ------------------------------------------------------------
    # Rank candidates
    # ------------------------------------------------------------

    candidates.sort(
        key=lambda x: (x[0], x[1]),
        reverse=True,
    )

    best_score, _, best_rule, best_hits = candidates[0]

    # ------------------------------------------------------------
    # M32 ambiguity protection
    # ------------------------------------------------------------

    meaningful = [
        item
        for item in candidates
        if item[0] >= 0.70
    ]

    meaningful_destinations = {
        (
            item[2].exam,
            item[2].subject,
            item[2].topic,
        )
        for item in meaningful
    }

    if len(meaningful_destinations) > 1:
        all_signals = sorted(
            {
                signal
                for item in meaningful
                for signal in item[3]
            }
        )

        return Classification(
            best_rule.exam,
            best_rule.subject,
            "Review Required",
            round(max(0.0, best_score - 0.15), 3),
            all_signals,
            "REVIEW",
        )

    # ------------------------------------------------------------
    # Close-score protection
    # ------------------------------------------------------------

    if len(candidates) > 1:
        second = candidates[1]

        different_destination = (
            best_rule.exam,
            best_rule.subject,
            best_rule.topic,
        ) != (
            second[2].exam,
            second[2].subject,
            second[2].topic,
        )

        if different_destination and abs(best_score - second[0]) < 0.08:
            return Classification(
                best_rule.exam,
                best_rule.subject,
                "Review Required",
                round(max(0.0, best_score - 0.15), 3),
                sorted(set(best_hits)),
                "REVIEW",
            )

    # ------------------------------------------------------------
    # Final classification
    # ------------------------------------------------------------

    return Classification(
        best_rule.exam,
        best_rule.subject,
        best_rule.topic,
        round(best_score, 3),
        sorted(set(best_hits)),
        "AUTO" if best_score >= 0.70 else "REVIEW",
    )
    
