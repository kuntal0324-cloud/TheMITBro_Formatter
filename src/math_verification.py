from __future__ import annotations
from dataclasses import dataclass,field
import math,re
from .solver import verify_equality

@dataclass(frozen=True)
class CheckResult:
    status:str
    message:str
    confidence:float=0.0
    details:dict=field(default_factory=dict)

def _numeric(s):
    try:return float(str(s).strip())
    except Exception:return None

def verify_symbolic(actual,expected)->CheckResult:
    r=verify_equality(str(actual),str(expected))
    return CheckResult(r.status,r.message,1.0 if r.status in {"PASS","FAIL"} else 0.0,dict(r.details))

def verify_numeric(actual,expected,*,abs_tol=1e-9,rel_tol=1e-6)->CheckResult:
    a=_numeric(actual);b=_numeric(expected)
    if a is None or b is None:return CheckResult("UNKNOWN","A numeric value could not be parsed.")
    ok=math.isclose(a,b,abs_tol=abs_tol,rel_tol=rel_tol)
    return CheckResult("PASS" if ok else "FAIL","Numeric values agree." if ok else "Numeric values disagree.",1.0,
                       {"actual":a,"expected":b,"abs_error":abs(a-b)})

def verify_value(actual,expected)->CheckResult:
    if _numeric(actual) is not None and _numeric(expected) is not None:
        return verify_numeric(actual,expected)
    return verify_symbolic(actual,expected)
