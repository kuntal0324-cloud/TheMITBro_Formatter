from __future__ import annotations
from dataclasses import dataclass,asdict

@dataclass(frozen=True)
class QualityScore:
    score:float
    grade:str
    components:dict
    blockers:tuple[str,...]
    def to_dict(self):return asdict(self)

def score_question(record)->QualityScore:
    m=record.metadata
    components={}
    components["classification"]=max(0,min(1,float(getattr(record.classification,"confidence",0))))
    components["ocr"]=max(0,min(1,float(m.get("ocr_confidence",1))))
    components["math"]=max(0,min(1,float(m.get("math_confidence",1))))
    components["taxonomy"]=max(0,min(1,float((m.get("question_intelligence") or {}).get("taxonomy_confidence",0))))
    val=str(m.get("validation_status","REVIEW"))
    components["validation"]={"PASS":1.0,"REVIEW":.55,"UNKNOWN":.45,"FAIL":0}.get(val,.45)
    blockers=[]
    if record.classification.status!="AUTO":blockers.append("classification_review")
    if m.get("requires_visual_review"):blockers.append("visual_review")
    if m.get("requires_validation_review"):blockers.append("validation_review")
    if val=="FAIL":blockers.append("validation_failure")
    weights={"classification":.20,"ocr":.10,"math":.15,"taxonomy":.20,"validation":.35}
    score=sum(components[k]*weights[k] for k in weights)
    score=max(0,score-.08*len(set(blockers)))
    score=round(max(0,min(1,score)),3)
    grade="A" if score>=.90 and not blockers else "B" if score>=.75 else "C" if score>=.60 else "D"
    return QualityScore(score,grade,components,tuple(sorted(set(blockers))))
