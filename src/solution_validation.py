from __future__ import annotations
from dataclasses import dataclass,field
import re
from .answer_parser import parse_answer_bundle
from .math_verification import verify_value

@dataclass(frozen=True)
class SolutionValidation:
    status:str; message:str; details:dict=field(default_factory=dict)


def _extract_final_result(solution: str) -> str | None:
    """Return the last explicit final-result statement in a solution.

    ``Final answer:`` is the production contract.  The therefore/hence form is
    retained for backwards compatibility with the frozen Formatter corpus.
    Selecting the last marker prevents an intermediate conclusion from being
    mistaken for the final answer.
    """
    markers = list(re.finditer(
        r"(?mi)^\s*(?:final\s+answer|answer)\s*[:=]\s*([^\n]+?)\s*$",
        solution,
    ))
    if markers:
        return markers[-1].group(1).strip().rstrip(".")

    conclusions = list(re.finditer(
        r"(?mi)(?:therefore|hence)\s*[:=]?\s*([^\n.]+)",
        solution,
    ))
    return conclusions[-1].group(1).strip() if conclusions else None


def _option_keys(value: str) -> tuple[str, ...]:
    """Extract distinct standalone option labels without matching words."""
    return tuple(dict.fromkeys(re.findall(r"(?<![A-Z])[A-D](?![A-Z])", value.upper())))

def validate_solution(text:str)->SolutionValidation:
    b=parse_answer_bundle(text)
    if not b.solution:return SolutionValidation("UNKNOWN","No solution supplied.")
    if not b.answer:return SolutionValidation("UNKNOWN","Solution exists but no answer key is available.")
    final=_extract_final_result(b.solution)
    if final is None:
        return SolutionValidation("UNKNOWN","Solution has no explicit final-result statement.")

    answer_keys=_option_keys(b.answer)
    final_keys=_option_keys(final)
    if b.options and answer_keys and final_keys:
        ok=final_keys==answer_keys
        return SolutionValidation(
            "PASS" if ok else "FAIL",
            "Solution final option key agrees with the answer." if ok else
            "Solution final option key disagrees with the answer.",
            {"solution_final":final,"answer_value":b.answer},
        )

    key="".join(answer_keys)
    target=b.options.get(key,b.answer) if len(key)==1 else b.answer
    r=verify_value(final,target)
    return SolutionValidation(r.status,
        "Solution final result agrees with the answer." if r.status=="PASS" else
        "Solution final result disagrees with the answer." if r.status=="FAIL" else r.message,
        {"solution_final":final,"answer_value":target})
