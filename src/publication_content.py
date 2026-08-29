from __future__ import annotations
from dataclasses import dataclass, asdict
from .answer_parser import parse_answer_bundle

@dataclass(frozen=True)
class AnswerEntry:
    number: int
    question_id: str
    answer: str
    solution: str | None

    def to_dict(self):
        return asdict(self)


def answer_entries(paper):
    out = []
    for i, q in enumerate(paper.questions, 1):
        meta = q.metadata or {}
        answer = meta.get("answer")
        solution = meta.get("solution")
        if answer is None or solution is None:
            bundle = parse_answer_bundle(meta.get("source_text", "") or q.text)
            if answer is None:
                answer = bundle.answer
            if solution is None:
                solution = bundle.solution
        out.append(AnswerEntry(q.number or i, q.id, str(answer or "Not supplied"), solution))
    return tuple(out)
