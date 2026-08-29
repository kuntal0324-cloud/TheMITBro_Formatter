from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class ParsedAnswer:
    answer: str | None
    options: dict[str,str]
    solution: str | None

def parse_options(text:str)->dict[str,str]:
    out={}
    # Markdown/plain GATE/JEE choices.
    for m in re.finditer(r"(?m)^\s*([A-D])[\.\)]\s*(.+?)\s*$",text):
        out[m.group(1).upper()]=m.group(2).strip()
    return out

def parse_answer(text:str)->str|None:
    patterns=(
        r"\*\*(?:Correct )?Answer:\*\*\s*([^\n]+)",
        r"(?mi)^\s*(?:correct\s+)?answer\s*[:=-]\s*([^\n]+)",
        r"(?mi)^\s*answer\s+key\s*[:=-]\s*([^\n]+)",
    )
    for p in patterns:
        m=re.search(p,text,re.I|re.M)
        if m:return m.group(1).strip()
    return None

def parse_solution(text:str)->str|None:
    m=re.search(r"(?is)\*\*Solution:\*\*\s*(.+?)(?=\n\s*(?:---|###|\*\*Answer:|\*\*Correct Answer:)|\Z)",text)
    if m:return m.group(1).strip()
    m=re.search(r"(?is)(?:^|\n)\s*Solution\s*:\s*(.+?)(?=\n\s*(?:---|###|Answer\s*:)|\Z)",text)
    return m.group(1).strip() if m else None

def parse_answer_bundle(text:str)->ParsedAnswer:
    return ParsedAnswer(parse_answer(text),parse_options(text),parse_solution(text))
