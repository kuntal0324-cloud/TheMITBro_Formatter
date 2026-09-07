"""Render source math markup as readable Unicode/plain text.

This is a safety boundary for SVG/PDF paths that do not have a real math
typesetter.  It intentionally favours readable output over displaying raw
LaTeX commands to a learner.  The source expression remains preserved in the
question-bank record for future MathML/TeX rendering.
"""
from __future__ import annotations

import re


COMMANDS = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ",
    "epsilon": "ε", "theta": "θ", "lambda": "λ", "mu": "μ",
    "pi": "π", "rho": "ρ", "sigma": "σ", "tau": "τ", "phi": "φ",
    "omega": "ω", "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ",
    "Lambda": "Λ", "Pi": "Π", "Sigma": "Σ", "Phi": "Φ", "Omega": "Ω",
    "infty": "∞", "pm": "±", "mp": "∓", "times": "×", "cdot": "·",
    "div": "÷", "le": "≤", "leq": "≤", "ge": "≥", "geq": "≥",
    "ne": "≠", "neq": "≠", "approx": "≈", "equiv": "≡", "to": "→",
    "rightarrow": "→", "leftarrow": "←", "Rightarrow": "⇒",
    "sum": "sum ", "prod": "product ", "int": "integral ", "oint": "contour integral ", "partial": "partial ",
    "nabla": "gradient ", "angle": "∠", "degree": "°", "therefore": "therefore",
    "because": "∵", "in": "∈", "notin": "∉", "subset": "⊂",
    "cup": "∪", "cap": "∩", "forall": "∀", "exists": "∃",
    "ldots": "…", "cdots": "⋯", "sin": "sin", "cos": "cos",
    "tan": "tan", "log": "log", "ln": "ln", "exp": "exp",
}

SUPERSCRIPT = str.maketrans("0123456789+-=()n", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ")
SUBSCRIPT = str.maketrans("0123456789+-=()aehi jklmnoprstuvx".replace(" ", ""),
                          "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ")


def _balanced(text: str, start: int) -> tuple[str, int] | None:
    if start >= len(text) or text[start] != "{":
        return None
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
    return None


def _replace_command(text: str, command: str, arity: int, render) -> str:
    needle = "\\" + command
    cursor = 0
    out: list[str] = []
    while True:
        pos = text.find(needle, cursor)
        if pos < 0:
            out.append(text[cursor:])
            break
        out.append(text[cursor:pos])
        at = pos + len(needle)
        while at < len(text) and text[at].isspace():
            at += 1
        args: list[str] = []
        end = at
        for _ in range(arity):
            while end < len(text) and text[end].isspace():
                end += 1
            found = _balanced(text, end)
            if not found:
                break
            arg, end = found
            args.append(arg)
        if len(args) != arity:
            out.append(needle)
            cursor = at
            continue
        out.append(render(*args))
        cursor = end
    return "".join(out)


def _matrices(text: str) -> str:
    pattern = re.compile(
        r"\\begin\{(?:bmatrix|pmatrix|matrix|vmatrix)\}(.*?)"
        r"\\end\{(?:bmatrix|pmatrix|matrix|vmatrix)\}",
        re.S,
    )

    def repl(match: re.Match[str]) -> str:
        body = match.group(1)
        rows = ["  ".join(c.strip() for c in row.split("&")) for row in re.split(r"\\\\", body)]
        return "[" + "; ".join(row for row in rows if row) + "]"

    return pattern.sub(repl, text)


def humanize_math(value: str) -> str:
    """Return learner-facing text with no exposed TeX/Markdown control syntax."""
    text = str(value).replace("\r\n", "\n")
    text = _matrices(text)
    text = re.sub(r"\\(?:left|right|displaystyle|limits|quad|qquad)\b|\\[,;!]", " ", text)
    text = re.sub(r"\\oint_\{?([A-Za-z0-9]+)\}?", r"contour integral over \1 ", text)
    text = re.sub(
        r"\\int_\{([^{}]+)\}\^\{([^{}]+)\}",
        r"integral from \1 to \2 ",
        text,
    )

    # Re-run because fraction arguments can themselves contain fractions.
    for _ in range(8):
        previous = text
        text = _replace_command(text, "frac", 2, lambda a, b: f"({a})/({b})")
        text = _replace_command(text, "dfrac", 2, lambda a, b: f"({a})/({b})")
        text = _replace_command(text, "tfrac", 2, lambda a, b: f"({a})/({b})")
        text = _replace_command(text, "sqrt", 1, lambda a: f"√({a})")
        for name in ("text", "mathrm", "mathbf", "mathit", "operatorname", "overline", "underline"):
            text = _replace_command(text, name, 1, lambda a: a)
        if text == previous:
            break

    text = re.sub(r"\\(?:left|right|displaystyle|limits|quad|qquad)\b|\\[,;!]", " ", text)
    text = re.sub(r"\\([A-Za-z]+)", lambda m: COMMANDS.get(m.group(1), m.group(1)), text)
    text = re.sub(r"\^\{([0-9+\-=()n]+)\}", lambda m: m.group(1).translate(SUPERSCRIPT), text)
    text = re.sub(r"\^([0-9n])", lambda m: m.group(1).translate(SUPERSCRIPT), text)
    text = re.sub(r"_\{([0-9+\-=()aehijklmnoprstuvx]+)\}", lambda m: m.group(1).translate(SUBSCRIPT), text)
    text = re.sub(r"_([0-9aehijklmnoprstuvx])", lambda m: m.group(1).translate(SUBSCRIPT), text)
    text = re.sub(r"_\{?([A-Za-z0-9]+)\}?", r" subscript \1", text)
    text = text.replace("\\(", "").replace("\\)", "").replace("\\[", "").replace("\\]", "")
    text = text.replace("$$", "").replace("$", "")
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    text = text.replace("&", " ")
    text = re.sub(r"[{}]", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return text.strip()


def has_source_math_markup(value: str) -> bool:
    """Detect source control syntax that must never reach learner output."""
    return bool(re.search(r"\$|\\[A-Za-z]+|\\\[|\\\]|\\\(|\\\)|\\begin|\\end", str(value)))
