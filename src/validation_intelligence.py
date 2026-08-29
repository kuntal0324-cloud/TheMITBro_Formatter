from __future__ import annotations
from dataclasses import dataclass,asdict
from .answer_parser import parse_answer_bundle
from .answer_validation import validate_option_set,validate_answer_key
from .domain_validation import run_domain_checks
from .diagram_text_validator import validate_diagram_text
from .question_quality_validator import detect_quality_issues
from .solution_validation import validate_solution

@dataclass(frozen=True)
class ValidationIntelligence:
    status:str
    answer_status:str
    option_status:str
    solution_status:str
    diagram_text_status:str
    domain_checks:tuple[dict,...]
    quality_status:str
    findings:tuple[dict,...]
    review_required:bool
    def to_dict(self):return asdict(self)

def validate_question_content(text:str,*,question_type:str="UNSPECIFIED",visual_structure:dict|None=None)->ValidationIntelligence:
    b=parse_answer_bundle(text)
    options=validate_option_set(b.options,question_type)
    answer=validate_answer_key(text,question_type)
    solution=validate_solution(text)
    diagram=validate_diagram_text(text,visual_structure)
    domains=run_domain_checks(text)
    quality=detect_quality_issues(text,question_type)

    hard_fail=any(x=="FAIL" for x in (options.status,answer.status,solution.status,diagram.status,quality.status)) or any(x.status=="FAIL" for x in domains)
    unknown=any(x in {"UNKNOWN","REVIEW"} for x in (answer.status,solution.status,diagram.status,quality.status)) or any(x.status=="UNKNOWN" for x in domains)
    status="FAIL" if hard_fail else "REVIEW" if unknown else "PASS"
    findings=tuple({"code":x.code,"severity":x.severity,"message":x.message} for x in quality.findings)
    return ValidationIntelligence(
        status,answer.status,options.status,solution.status,diagram.status,
        tuple({"status":x.status,"model":x.model,"expected":x.expected,"supplied":x.supplied,"message":x.message} for x in domains),
        quality.status,findings,status!="PASS"
    )
