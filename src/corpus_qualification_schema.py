from __future__ import annotations
from dataclasses import dataclass,field,asdict

@dataclass(frozen=True)
class CorpusCase:
    case_id:str
    exam:str
    subject:str
    expected_topic:str
    text:str
    expected_type:str="UNSPECIFIED"
    expected_review:bool=False
    tags:tuple[str,...]=()
    notes:str=""

@dataclass(frozen=True)
class CaseResult:
    case_id:str
    passed:bool
    classification_ok:bool
    type_ok:bool
    review_ok:bool
    math_ok:bool
    visual_ok:bool
    expected_topic:str
    actual_topic:str
    diagnostics:tuple[str,...]=()

@dataclass(frozen=True)
class QualificationReport:
    total:int
    passed:int
    failed:int
    pass_rate:float
    by_subject:dict[str,dict]
    by_tag:dict[str,dict]
    results:tuple[CaseResult,...]
    contract:str="M43"

    def to_dict(self):return asdict(self)
