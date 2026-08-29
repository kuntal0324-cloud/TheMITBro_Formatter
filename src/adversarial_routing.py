from __future__ import annotations
from dataclasses import dataclass
from .question_classifier import classify_question
from .question_intelligence import analyze_question

@dataclass(frozen=True)
class RoutingProbe:
    name:str;text:str;exam_hint:str;forbidden_topic:str|None=None;expected_subject:str|None=None

@dataclass(frozen=True)
class RoutingProbeResult:
    name:str;passed:bool;topic:str;subject:str

def run_probe(p):
    c=classify_question(p.text,exam_hint=p.exam_hint)
    q=analyze_question(p.text,exam_hint=p.exam_hint)
    topic=q.topic if q.topic!="Review Required" else c.topic
    subject=q.subject if q.subject!="Review Required" else c.subject
    ok=True
    if p.forbidden_topic and topic==p.forbidden_topic:ok=False
    if p.expected_subject and subject!=p.expected_subject:ok=False
    return RoutingProbeResult(p.name,ok,topic,subject)

DEFAULT_PROBES=(
 RoutingProbe("det_not_calculus","Evaluate det(A) for A=[[1,2],[3,4]].","GATE EE","Calculus","Engineering Mathematics"),
 RoutingProbe("laplace_equation_em","Electric potential satisfies Laplace equation in a charge-free region. Find the potential.","GATE EE","Differential Equations","Electrical Engineering"),
 RoutingProbe("power_factor_not_probability","An induction motor operates at 0.8 power factor. Determine input current.","GATE EE","Probability and Statistics","Electrical Engineering"),
 RoutingProbe("jee_current_not_gate_network","A wire carries current I in a magnetic field. Find the force.","JEE",None,"Physics"),
)
