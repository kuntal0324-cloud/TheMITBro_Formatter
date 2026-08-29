from __future__ import annotations
from collections import Counter
from dataclasses import dataclass,asdict

@dataclass(frozen=True)
class PaperMetrics:
    question_count:int
    total_marks:int
    expected_time_seconds:int
    subjects:dict[str,int]
    topics:dict[str,int]
    difficulties:dict[str,int]
    question_types:dict[str,int]
    conceptual_count:int
    numerical_count:int
    visual_count:int
    family_count:int
    def to_dict(self):return asdict(self)

def compute_metrics(candidates)->PaperMetrics:
    xs=list(candidates)
    return PaperMetrics(
        len(xs),sum(x.marks for x in xs),sum(x.expected_time_seconds for x in xs),
        dict(Counter(x.subject for x in xs)),dict(Counter(x.topic for x in xs)),
        dict(Counter(x.difficulty for x in xs)),dict(Counter(x.question_type for x in xs)),
        sum(x.conceptual for x in xs),sum(x.numerical for x in xs),sum(x.visual for x in xs),
        len({x.family_id for x in xs}),
    )
