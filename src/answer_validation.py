from __future__ import annotations
from dataclasses import dataclass,field
import re
from .answer_parser import parse_answer_bundle
from .math_verification import verify_value

@dataclass(frozen=True)
class AnswerValidation:
    status:str
    message:str
    details:dict=field(default_factory=dict)

def validate_option_set(options:dict[str,str],question_type:str="MCQ")->AnswerValidation:
    if question_type in {"MCQ","MSQ"} and len(options)<2:
        return AnswerValidation("FAIL","Choice question has fewer than two options.",{"count":len(options)})
    vals=[re.sub(r"\s+"," ",v.strip().lower()) for v in options.values()]
    if len(vals)!=len(set(vals)):
        return AnswerValidation("FAIL","Duplicate answer options detected.")
    return AnswerValidation("PASS","Option set is structurally valid.",{"count":len(options)})

def validate_answer_key(text:str,question_type:str="UNSPECIFIED")->AnswerValidation:
    b=parse_answer_bundle(text)
    if b.answer is None:return AnswerValidation("UNKNOWN","No answer key supplied.")
    ans=b.answer.strip().upper()
    if question_type=="MCQ":
        key=re.sub(r"[^A-D]","",ans)
        if len(key)!=1:return AnswerValidation("FAIL","MCQ answer key must identify one option.",{"answer":b.answer})
        if b.options and key not in b.options:return AnswerValidation("FAIL","MCQ answer key is not present in options.",{"answer":key})
    if question_type=="MSQ":
        keys=tuple(dict.fromkeys(re.findall(r"[A-D]",ans)))
        if not keys:return AnswerValidation("FAIL","MSQ answer key contains no option letters.")
        if b.options and any(k not in b.options for k in keys):
            return AnswerValidation("FAIL","MSQ answer references a missing option.",{"answer":keys})
    return AnswerValidation("PASS","Answer key is structurally consistent.",{"answer":b.answer})

def verify_answer_against_expected(text:str,expected)->AnswerValidation:
    b=parse_answer_bundle(text)
    if b.answer is None:return AnswerValidation("UNKNOWN","No answer key supplied.")
    key=re.sub(r"[^A-D]","",b.answer.upper())
    actual=b.options.get(key,b.answer) if len(key)==1 else b.answer
    r=verify_value(actual,expected)
    return AnswerValidation(r.status,r.message,{"actual":actual,"expected":str(expected),**r.details})
