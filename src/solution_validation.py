from __future__ import annotations
from dataclasses import dataclass,field
import re
from .answer_parser import parse_answer_bundle
from .math_verification import verify_value

@dataclass(frozen=True)
class SolutionValidation:
    status:str; message:str; details:dict=field(default_factory=dict)

def validate_solution(text:str)->SolutionValidation:
    b=parse_answer_bundle(text)
    if not b.solution:return SolutionValidation("UNKNOWN","No solution supplied.")
    if not b.answer:return SolutionValidation("UNKNOWN","Solution exists but no answer key is available.")
    # Strong deterministic check only when solution has explicit final-answer marker.
    m=re.search(r"(?mi)(?:therefore|hence|final answer|answer)\s*[:=]?\s*([^\n.]+)",b.solution)
    if not m:return SolutionValidation("UNKNOWN","Solution has no explicit final-result statement.")
    final=m.group(1).strip()
    key=re.sub(r"[^A-D]","",b.answer.upper())
    target=b.options.get(key,b.answer) if len(key)==1 else b.answer
    r=verify_value(final,target)
    return SolutionValidation(r.status,
        "Solution final result agrees with the answer." if r.status=="PASS" else
        "Solution final result disagrees with the answer." if r.status=="FAIL" else r.message,
        {"solution_final":final,"answer_value":target})
