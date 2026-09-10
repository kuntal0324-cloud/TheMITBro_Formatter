from __future__ import annotations
from dataclasses import dataclass,field
import re

@dataclass(frozen=True)
class QualityFinding:
    code:str; severity:str; message:str

@dataclass(frozen=True)
class QuestionQuality:
    status:str; findings:tuple[QualityFinding,...]=()
    @property
    def review_required(self):return self.status!="PASS"

def detect_quality_issues(text:str,question_type:str="UNSPECIFIED")->QuestionQuality:
    low=text.lower(); f=[]
    explicit_task = re.search(
        r"\b(?:find|determine|calculate|which|what|evaluate|prove|show|select|identify|choose|enter|arrange)\b",
        low,
    )
    standard_question_form = re.search(
        r"\b(?:most nearly means|number of [^.?\n]{1,80} is|is paired with|final direction is)\b",
        low,
    )
    if not explicit_task and not standard_question_form:
        f.append(QualityFinding("NO_TASK","REVIEW","No clear task/instruction was detected."))
    if re.search(r"\b(?:insufficient data|cannot be determined|not enough information)\b",low):
        f.append(QualityFinding("EXPLICIT_UNDERDETERMINED","REVIEW","Question explicitly indicates insufficient information."))
    if re.search(r"\bdivide by zero\b|\b1\s*/\s*0\b",low):
        f.append(QualityFinding("IMPOSSIBLE_OPERATION","ERROR","An impossible/undefined operation is stated."))
    if question_type=="MCQ":
        opts=re.findall(r"(?m)^\s*([A-D])[\.\)]\s*(.+)$",text)
        if len(opts)<2:f.append(QualityFinding("MCQ_OPTIONS","ERROR","MCQ does not contain enough options."))
    status="FAIL" if any(x.severity=="ERROR" for x in f) else "REVIEW" if f else "PASS"
    return QuestionQuality(status,tuple(f))
