from __future__ import annotations
from dataclasses import dataclass
import re

# SI base exponent order: M,L,T,I,Theta,N,J
DIMS={
 "m":(0,1,0,0,0,0,0),"meter":(0,1,0,0,0,0,0),"metre":(0,1,0,0,0,0,0),
 "s":(0,0,1,0,0,0,0),"second":(0,0,1,0,0,0,0),
 "kg":(1,0,0,0,0,0,0),"a":(0,0,0,1,0,0,0),"ampere":(0,0,0,1,0,0,0),
 "k":(0,0,0,0,1,0,0),
 "hz":(0,0,-1,0,0,0,0),
 "n":(1,1,-2,0,0,0,0),"newton":(1,1,-2,0,0,0,0),
 "j":(1,2,-2,0,0,0,0),"joule":(1,2,-2,0,0,0,0),
 "w":(1,2,-3,0,0,0,0),"watt":(1,2,-3,0,0,0,0),
 "c":(0,0,1,1,0,0,0),"coulomb":(0,0,1,1,0,0,0),
 "v":(1,2,-3,-1,0,0,0),"volt":(1,2,-3,-1,0,0,0),
 "ohm":(1,2,-3,-2,0,0,0),"ω":(1,2,-3,-2,0,0,0),"Ω":(1,2,-3,-2,0,0,0),
 "f":(-1,-2,4,2,0,0,0),"farad":(-1,-2,4,2,0,0,0),
 "h":(1,2,-2,-2,0,0,0),"henry":(1,2,-2,-2,0,0,0),
 "wb":(1,2,-2,-1,0,0,0),"tesla":(1,0,-2,-1,0,0,0),
 "pa":(1,-1,-2,0,0,0,0),
}

@dataclass(frozen=True)
class DimensionResult:
    status:str
    left:tuple[int,...]|None
    right:tuple[int,...]|None
    message:str

def dimension_of_unit(unit:str):
    u=str(unit).strip().replace("Ω","Ω").lower()
    return DIMS.get(u)

def compare_units(a:str,b:str)->DimensionResult:
    da=dimension_of_unit(a);db=dimension_of_unit(b)
    if da is None or db is None:return DimensionResult("UNKNOWN",da,db,"Unknown unit in dimensional comparison.")
    ok=da==db
    return DimensionResult("PASS" if ok else "FAIL",da,db,
        "Units are dimensionally compatible." if ok else "Units are dimensionally inconsistent.")

def extract_quantity(text:str):
    m=re.search(r"([-+]?\d+(?:\.\d+)?)\s*(Hz|kHz|MHz|V|A|Ω|ohm|W|J|N|F|H|T|m|s|kg)\b",text,re.I)
    return (float(m.group(1)),m.group(2)) if m else None
