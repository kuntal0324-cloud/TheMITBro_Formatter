from __future__ import annotations
from dataclasses import dataclass,asdict
from .paper_blueprint import PaperBlueprint
from .paper_candidates import candidate_from_dict,stable_rank
from .paper_constraints import validate_selection
from .semantic_duplicate_detector import cosine_similarity

@dataclass(frozen=True)
class GeneratedMockPaper:
    title:str
    exam:str
    question_ids:tuple[str,...]
    questions:tuple[dict,...]
    blueprint:dict
    metrics:dict
    validation:dict
    deterministic:bool=True
    generator_contract:str="M41"
    def to_dict(self):return asdict(self)

def _eligible(items,blueprint):
    out=[]
    for item in items:
        c=candidate_from_dict(item)
        if not c.id or not c.text:continue
        if c.exam!=blueprint.exam:continue
        if c.quality_score<blueprint.min_quality_score:continue
        if blueprint.approved_only and c.lifecycle_status!="APPROVED":continue
        out.append(c)
    out.sort(key=lambda x:(stable_rank(blueprint.deterministic_seed,x.id),x.id))
    return out

def _count(selected,attr,value):
    return sum(getattr(x,attr)==value for x in selected)

def _need_priority(c,selected,b):
    score=0
    if c.subject in b.subject_counts:
        score+=40*max(0,b.subject_counts[c.subject]-_count(selected,"subject",c.subject))
    if c.topic in b.topic_counts:
        score+=35*max(0,b.topic_counts[c.topic]-_count(selected,"topic",c.topic))
    if c.difficulty in b.difficulty_counts:
        score+=30*max(0,b.difficulty_counts[c.difficulty]-_count(selected,"difficulty",c.difficulty))
    if c.question_type in b.type_counts:
        score+=30*max(0,b.type_counts[c.question_type]-_count(selected,"question_type",c.question_type))
    if c.conceptual and sum(x.conceptual for x in selected)<b.conceptual_min:score+=22
    if c.numerical and sum(x.numerical for x in selected)<b.numerical_min:score+=22
    if c.visual and sum(x.visual for x in selected)<b.visual_min:score+=20
    score+=int(c.quality_score*10)
    return score

def _can_add(c,selected,b):
    if b.avoid_same_family and c.family_id in {x.family_id for x in selected}:return False
    if b.visual_max is not None and c.visual and sum(x.visual for x in selected)>=b.visual_max:return False
    if b.max_expected_time_seconds is not None and sum(x.expected_time_seconds for x in selected)+c.expected_time_seconds>b.max_expected_time_seconds:return False
    # avoid strong text-near-duplicates even when family IDs differ
    if any(cosine_similarity(c.text,x.text)>=.94 for x in selected):return False
    if b.total_marks is not None and sum(x.marks for x in selected)+c.marks>b.total_marks:return False
    return True

def generate_mock_paper(items,blueprint:PaperBlueprint)->GeneratedMockPaper:
    b=blueprint.validate();pool=_eligible(items,b)
    selected=[]
    remaining=list(pool)
    while len(selected)<b.total_questions:
        valid=[x for x in remaining if _can_add(x,selected,b)]
        if not valid:break
        # strongest unmet constraint first; stable hash remains deterministic tie-breaker
        valid.sort(key=lambda x:(-_need_priority(x,selected,b),stable_rank(b.deterministic_seed,x.id),x.id))
        chosen=valid[0];selected.append(chosen);remaining.remove(chosen)

    # Exact mark reconciliation: deterministic single-question swaps.
    if b.total_marks is not None and len(selected)==b.total_questions:
        target=b.total_marks
        current=sum(x.marks for x in selected)
        if current!=target:
            for i,old in enumerate(list(selected)):
                for new in remaining:
                    trial=selected[:i]+[new]+selected[i+1:]
                    if sum(x.marks for x in trial)==target and _can_add(new,selected[:i]+selected[i+1:],b):
                        selected=trial;current=target;break
                if current==target:break

    report=validate_selection(selected,b)
    if not report.valid:
        raise ValueError("Blueprint cannot be satisfied by the supplied bank: "+"; ".join(report.errors))

    return GeneratedMockPaper(
        b.title,b.exam,tuple(x.id for x in selected),tuple(x.raw for x in selected),
        b.to_dict(),report.metrics,report.to_dict()
    )
