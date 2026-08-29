from __future__ import annotations

import re

SI_PREFIXES = {
    "p": "p", "n": "n", "u": r"\mu", "µ": r"\mu", "m": "m",
    "k": "k", "K": "k", "M": "M", "G": "G",
}

UNIT_MAP = {
    "ohm": r"\Omega",
    "Ω": r"\Omega",
    "V": r"\mathrm{V}",
    "A": r"\mathrm{A}",
    "W": r"\mathrm{W}",
    "VA": r"\mathrm{VA}",
    "Hz": r"\mathrm{Hz}",
    "H": r"\mathrm{H}",
    "F": r"\mathrm{F}",
    "C": r"\mathrm{C}",
    "T": r"\mathrm{T}",
}


def normalize_scientific_notation(text: str) -> str:
    s = str(text).replace("µ", "u")

    # Imaginary unit used by Electrical Engineering.
    s = re.sub(r"(?<![A-Za-z])j(?=\s*[-+]?\s*\d|\s*[A-Za-z(])", lambda _: r"\mathrm{j}", s)

    # Degree symbol.
    s = re.sub(r"(-?\d+(?:\.\d+)?)\s*°", lambda m: m.group(1) + r"^{\circ}", s)

    # Omega / ohm.
    s = re.sub(r"\bohms?\b", lambda _: r"\Omega", s, flags=re.I)
    s = s.replace("Ω", r"\Omega")

    # Scientific notation 10^n.
    s = re.sub(r"(\d+(?:\.\d+)?)\s*[x×]\s*10\s*\^\s*([+-]?\d+)",
               lambda m: m.group(1) + r"\times 10^{" + m.group(2) + "}", s)

    return s
