from __future__ import annotations
from dataclasses import dataclass,field
import math,re

@dataclass(frozen=True)
class DomainCheck:
    status:str; model:str; expected:float|None; supplied:float|None
    message:str; details:dict=field(default_factory=dict)

def _num(text,label):
    m=re.search(rf"\b{label}\s*=\s*([-+]?\d+(?:\.\d+)?)",text,re.I)
    return float(m.group(1)) if m else None

def validate_ohms_law(text:str)->DomainCheck:
    v=_num(text,"V");i=_num(text,"I");r=_num(text,"R")
    if None in (v,i,r):return DomainCheck("UNKNOWN","Ohm law",None,None,"V, I and R were not all explicit.")
    expected=i*r;ok=math.isclose(v,expected,rel_tol=1e-6,abs_tol=1e-9)
    return DomainCheck("PASS" if ok else "FAIL","Ohm law",expected,v,"V = I R is satisfied." if ok else "V = I R is violated.")

def validate_electric_power(text:str)->DomainCheck:
    p=_num(text,"P");v=_num(text,"V");i=_num(text,"I")
    if None in (p,v,i):return DomainCheck("UNKNOWN","Electrical power",None,None,"P, V and I were not all explicit.")
    expected=v*i;ok=math.isclose(p,expected,rel_tol=1e-6,abs_tol=1e-9)
    return DomainCheck("PASS" if ok else "FAIL","Electrical power",expected,p,"P = V I is satisfied." if ok else "P = V I is violated.")

def validate_newton_second_law(text:str)->DomainCheck:
    f=_num(text,"F");m=_num(text,"m");a=_num(text,"a")
    if None in (f,m,a):return DomainCheck("UNKNOWN","Newton second law",None,None,"F, m and a were not all explicit.")
    expected=m*a;ok=math.isclose(f,expected,rel_tol=1e-6,abs_tol=1e-9)
    return DomainCheck("PASS" if ok else "FAIL","Newton second law",expected,f,"F = m a is satisfied." if ok else "F = m a is violated.")

def validate_kinematics_v_uat(text:str)->DomainCheck:
    v=_num(text,"v");u=_num(text,"u");a=_num(text,"a");t=_num(text,"t")
    if None in (v,u,a,t):return DomainCheck("UNKNOWN","Kinematics v=u+at",None,None,"v, u, a and t were not all explicit.")
    expected=u+a*t;ok=math.isclose(v,expected,rel_tol=1e-6,abs_tol=1e-9)
    return DomainCheck("PASS" if ok else "FAIL","Kinematics v=u+at",expected,v,"v = u + at is satisfied." if ok else "v = u + at is violated.")

def run_domain_checks(text:str):
    low=text.lower(); out=[]
    if re.search(r"\bohm|resistor|resistance\b",low):out.append(validate_ohms_law(text))
    if re.search(r"\bpower\b",low) and "v" in low and "i" in low:out.append(validate_electric_power(text))
    if re.search(r"\bnewton|force\b",low):out.append(validate_newton_second_law(text))
    if re.search(r"\bkinematic|velocity|acceleration\b",low):out.append(validate_kinematics_v_uat(text))
    return tuple(out)
