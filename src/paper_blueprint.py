from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Mapping

_ALLOWED_TYPES={"MCQ","MSQ","NAT","UNSPECIFIED"}
_ALLOWED_DIFFICULTIES={"Easy","Medium","Hard"}

@dataclass(frozen=True)
class PaperBlueprint:
    exam:str
    title:str
    total_questions:int
    total_marks:int|None=None
    duration_minutes:int|None=None
    subject_counts:Mapping[str,int]=field(default_factory=dict)
    topic_counts:Mapping[str,int]=field(default_factory=dict)
    difficulty_counts:Mapping[str,int]=field(default_factory=dict)
    type_counts:Mapping[str,int]=field(default_factory=dict)
    conceptual_min:int=0
    numerical_min:int=0
    visual_min:int=0
    visual_max:int|None=None
    max_expected_time_seconds:int|None=None
    min_quality_score:float=0.0
    approved_only:bool=False
    avoid_same_family:bool=True
    deterministic_seed:str="TheMITbro-M41"

    def validate(self)->"PaperBlueprint":
        if not self.exam.strip():raise ValueError("Blueprint exam is required.")
        if not self.title.strip():raise ValueError("Blueprint title is required.")
        if self.total_questions<=0:raise ValueError("total_questions must be positive.")
        if self.total_marks is not None and self.total_marks<=0:raise ValueError("total_marks must be positive.")
        if self.duration_minutes is not None and self.duration_minutes<=0:raise ValueError("duration_minutes must be positive.")
        if not 0<=self.min_quality_score<=1:raise ValueError("min_quality_score must be in [0,1].")
        for name,mapping in (
            ("subject_counts",self.subject_counts),("topic_counts",self.topic_counts),
            ("difficulty_counts",self.difficulty_counts),("type_counts",self.type_counts)
        ):
            if any(int(v)<0 for v in mapping.values()):raise ValueError(f"{name} cannot contain negative counts.")
        if any(k not in _ALLOWED_DIFFICULTIES for k in self.difficulty_counts):
            raise ValueError("Unknown difficulty in blueprint.")
        if any(k not in _ALLOWED_TYPES for k in self.type_counts):
            raise ValueError("Unknown question type in blueprint.")
        for value in (self.conceptual_min,self.numerical_min,self.visual_min):
            if value<0:raise ValueError("Minimum balance counts cannot be negative.")
        if self.visual_max is not None and self.visual_max<self.visual_min:
            raise ValueError("visual_max cannot be smaller than visual_min.")
        if sum(self.subject_counts.values())>self.total_questions:
            raise ValueError("Subject count requirements exceed total_questions.")
        if sum(self.difficulty_counts.values())>self.total_questions:
            raise ValueError("Difficulty count requirements exceed total_questions.")
        if sum(self.type_counts.values())>self.total_questions:
            raise ValueError("Question-type requirements exceed total_questions.")
        return self

    def to_dict(self):return asdict(self)
