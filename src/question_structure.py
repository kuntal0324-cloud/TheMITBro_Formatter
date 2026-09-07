"""Best-effort structure extraction; source text always remains the authority."""
from __future__ import annotations

import re


OPTION = re.compile(r"(?m)^\s*(?:\(?([A-D])\)?[.)]|\(([A-D])\))\s+(.+?)\s*$")
ANSWER = re.compile(r"(?im)^\s*(?:\*\*)?answer(?:\s+key)?(?:\*\*)?\s*[:=-]\s*(.+?)\s*$")
SOLUTION = re.compile(r"(?im)^\s*(?:\*\*)?(?:detailed\s+)?solution(?:\*\*)?\s*[:=-]?\s*$")


def parse_question_structure(text: str) -> dict:
    options = []
    for match in OPTION.finditer(text):
        options.append({"label": match.group(1) or match.group(2), "text": match.group(3).strip()})
    answer_match = ANSWER.search(text)
    solution_match = SOLUTION.search(text)
    cut_candidates = [m.start() for m in (OPTION.search(text), answer_match, solution_match) if m]
    stem_end = min(cut_candidates) if cut_candidates else len(text)
    stem_lines = []
    for line in text[:stem_end].splitlines():
        if re.match(r"^\s*(?:#{1,4}\s+)?(?:TMB-|Q(?:uestion)?\s*\d+|\d+[.)])", line, re.I):
            continue
        if re.match(r"^\s*\*\*(?:Exam|Subject|Topic|Subtopic|Concept|Difficulty|Type|Marks):\*\*", line, re.I):
            continue
        if line.strip():
            stem_lines.append(line.strip())
    solution = ""
    if solution_match:
        solution = text[solution_match.end():].strip()
    return {
        "stem": "\n".join(stem_lines).strip(),
        "options": options,
        "answer": answer_match.group(1).strip() if answer_match else None,
        "solution": solution or None,
        "parse_status": "STRUCTURED" if stem_lines and (options or answer_match) else "PARTIAL",
    }
