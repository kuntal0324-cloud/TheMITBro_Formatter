from __future__ import annotations
from dataclasses import dataclass,asdict
from .paper_metrics import compute_metrics

@dataclass(frozen=True)
class ConstraintReport:
    valid:bool
    errors:tuple[str,...]
    warnings:tuple[str,...]
    metrics:dict
    def to_dict(self):return asdict(self)

def validate_selection(selected,blueprint)->ConstraintReport:
    m=compute_metrics(selected);e=[];w=[]
    if m.question_count!=blueprint.total_questions:e.append(f"question_count:{m.question_count}!={blueprint.total_questions}")
    if blueprint.total_marks is not None and m.total_marks!=blueprint.total_marks:e.append(f"total_marks:{m.total_marks}!={blueprint.total_marks}")
    for key,n in blueprint.subject_counts.items():
        if m.subjects.get(key,0)<n:e.append(f"subject:{key}:{m.subjects.get(key,0)}<{n}")
    for key,n in blueprint.topic_counts.items():
        if m.topics.get(key,0)<n:e.append(f"topic:{key}:{m.topics.get(key,0)}<{n}")
    for key,n in blueprint.difficulty_counts.items():
        if m.difficulties.get(key,0)<n:e.append(f"difficulty:{key}:{m.difficulties.get(key,0)}<{n}")
    for key,n in blueprint.type_counts.items():
        if m.question_types.get(key,0)<n:e.append(f"type:{key}:{m.question_types.get(key,0)}<{n}")
    if m.conceptual_count<blueprint.conceptual_min:e.append("conceptual_balance")
    if m.numerical_count<blueprint.numerical_min:e.append("numerical_balance")
    if m.visual_count<blueprint.visual_min:e.append("visual_min")
    if blueprint.visual_max is not None and m.visual_count>blueprint.visual_max:e.append("visual_max")
    if blueprint.max_expected_time_seconds is not None and m.expected_time_seconds>blueprint.max_expected_time_seconds:e.append("time_budget")
    if blueprint.avoid_same_family and m.family_count!=m.question_count:e.append("duplicate_family")
    if blueprint.duration_minutes and m.expected_time_seconds>blueprint.duration_minutes*60:
        w.append("Estimated solving time exceeds declared paper duration.")
    return ConstraintReport(not e,tuple(e),tuple(w),m.to_dict())
