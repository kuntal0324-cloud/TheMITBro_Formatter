from __future__ import annotations
from dataclasses import dataclass
import hashlib

@dataclass(frozen=True)
class PaperCandidate:
    id:str
    text:str
    exam:str
    subject:str
    topic:str
    subtopic:str|None
    concept:str|None
    question_type:str
    marks:int
    difficulty:str
    calculation_load:str
    reasoning_depth:str
    expected_time_seconds:int
    visual:bool
    quality_score:float
    family_id:str
    lifecycle_status:str
    raw:dict

    @property
    def numerical(self)->bool:
        return self.calculation_load in {"Moderate","High"} or self.question_type=="NAT"

    @property
    def conceptual(self)->bool:
        return self.calculation_load=="Low" and self.reasoning_depth in {"Direct","Multi-step","Deep"}

def candidate_from_dict(item:dict)->PaperCandidate:
    meta=item.get("metadata") or {}
    marks=item.get("marks")
    return PaperCandidate(
        id=str(item.get("id","")),
        text=str(item.get("text","")),
        exam=str(item.get("exam","")),
        subject=str(item.get("subject","")),
        topic=str(item.get("topic","")),
        subtopic=item.get("subtopic"),
        concept=item.get("concept"),
        question_type=str(item.get("question_type","UNSPECIFIED")),
        marks=int(marks if marks is not None else 1),
        difficulty=str(meta.get("difficulty","Medium")),
        calculation_load=str(meta.get("calculation_load","Low")),
        reasoning_depth=str(meta.get("reasoning_depth","Direct")),
        expected_time_seconds=int(meta.get("expected_time_seconds",90) or 90),
        visual=bool(meta.get("diagram_present") or meta.get("visual_required") or meta.get("diagram_type")),
        quality_score=float(item.get("quality_score",0.0)),
        family_id=str(item.get("family_id") or item.get("id","")),
        lifecycle_status=str(item.get("lifecycle_status","REVIEW")),
        raw=item,
    )

def stable_rank(seed:str,candidate_id:str)->int:
    return int(hashlib.sha256(f"{seed}|{candidate_id}".encode()).hexdigest(),16)
