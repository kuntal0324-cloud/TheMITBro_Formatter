from __future__ import annotations
import re
from pathlib import Path
from .diagram_intelligence import analyze_diagram_text,analyze_image_geometry
from .visual_structure import VisualEntity,VisualRelation,VisualStructure

def _components(t):
    pats=[("resistor",r"\b(?:resistor|R\d+)\b"),("capacitor",r"\b(?:capacitor|C\d+)\b"),
          ("inductor",r"\b(?:inductor|L\d+)\b"),("voltage_source",r"\b(?:voltage source|Vs)\b"),
          ("current_source",r"\b(?:current source|Is)\b"),("diode",r"\b(?:diode|D\d+)\b"),
          ("switch",r"\b(?:switch|S\d+)\b"),("op_amp",r"\b(?:op[- ]?amp|operational amplifier)\b"),
          ("transformer",r"\btransformer\b"),("motor",r"\b(?:motor|machine)\b")]
    out=[];seen=set()
    for kind,p in pats:
        for m in re.finditer(p,t,re.I):
            k=(kind,m.group(0).lower())
            if k in seen:continue
            seen.add(k);out.append(VisualEntity(f"E{len(out)+1}",kind,m.group(0)))
    return out

def _circuit(t):
    es=_components(t); low=t.lower()
    topology="series" if "series" in low else "parallel" if "parallel" in low else None
    rs=[]
    if topology:
        rs=[VisualRelation(a.id,b.id,topology) for a,b in zip(es,es[1:])]
    warns=() if topology else ("Components recovered; connectivity was not explicitly stated.",)
    return VisualStructure("engineering","circuit_diagram",tuple(es),tuple(rs),
        {"topology":topology},.94 if len(es)>=2 else .72,warns).ensure_valid()

def _phasor(t):
    es=[]
    for n,m,a in re.findall(r"\b([A-Za-z]\w*)\s*=\s*(-?\d+(?:\.\d+)?)\s*∠\s*(-?\d+(?:\.\d+)?)",t):
        es.append(VisualEntity(f"P{len(es)+1}","phasor",n,m,properties={"magnitude":float(m),"angle_deg":float(a)}))
    return VisualStructure("engineering","phasor_diagram",tuple(es),confidence=.97 if es else .6,
        warnings=() if es else ("No explicit phasor values recovered.",)).ensure_valid()

def _control(t,typ):
    es=[]
    for n,x in re.findall(r"\b([GHF])\s*\(\s*s\s*\)\s*=\s*([^,.;\n]+)",t,re.I):
        es.append(VisualEntity(f"B{len(es)+1}","transfer_block",n.upper()+"(s)",x.strip()))
    rs=[VisualRelation(a.id,b.id,"signal_flow",directed=True) for a,b in zip(es,es[1:])]
    fb=bool(re.search(r"\bfeedback\b",t,re.I))
    if fb and len(es)>1:rs.append(VisualRelation(es[-1].id,es[0].id,"feedback",directed=True))
    return VisualStructure("engineering",typ,tuple(es),tuple(rs),{"feedback":fb},.92 if es else .65).ensure_valid()

def _wave(t):
    low=t.lower();kind="pwm" if "pwm" in low else "square" if "square" in low else "sine" if "sine" in low else "waveform"
    props={"waveform":kind}
    d=re.search(r"(\d+(?:\.\d+)?)\s*(?:%|percent)?\s*duty",t,re.I)
    f=re.search(r"(\d+(?:\.\d+)?)\s*(Hz|kHz|MHz)",t,re.I)
    if d:props["duty_cycle_percent"]=float(d.group(1))
    if f:props["frequency"]={"value":float(f.group(1)),"unit":f.group(2)}
    return VisualStructure("engineering","waveform",properties=props,confidence=.94).ensure_valid()

def _coord(t):
    es=[]
    for i,(n,x,y) in enumerate(re.findall(r"(?:\b([A-Z])\s*)?\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)",t)):
        es.append(VisualEntity(f"P{i+1}","point",n or chr(65+i),position=(float(x),float(y))))
    return VisualStructure("mathematical","coordinate_geometry",tuple(es),properties={"coordinate_system":"cartesian"},confidence=.97).ensure_valid()

def _function(t,typ):
    xs=[m.group(1).strip() for m in re.finditer(r"(?:y|f\s*\(\s*x\s*\))\s*=\s*([^.;\n]+)",t,re.I)]
    es=tuple(VisualEntity(f"F{i+1}","function",f"f{i+1}",x) for i,x in enumerate(xs))
    return VisualStructure("mathematical",typ,es,properties={"expressions":xs},confidence=.96 if xs else .72).ensure_valid()

def _geometry(t):
    m=re.search(r"\btriangle\s+([A-Z]{3})\b",t,re.I); names=list(m.group(1).upper()) if m else []
    es=tuple(VisualEntity(f"V{i+1}","vertex",n) for i,n in enumerate(names));rs=[]
    if len(es)==3:
        rs=[VisualRelation(es[a].id,es[b].id,"side") for a,b in ((0,1),(1,2),(2,0))]
    return VisualStructure("mathematical","geometric_figure",es,tuple(rs),{"shape":"triangle" if m else "geometry"},.94 if m else .7).ensure_valid()

def _physics(t,typ):
    low=t.lower();es=[];props={}
    if typ=="free_body_diagram":
        for x in ("weight","normal force","friction","tension","spring force"):
            if x in low:es.append(VisualEntity(f"F{len(es)+1}","force",x.title()))
    elif typ=="ray_diagram":
        for x in ("lens","mirror","object","image","focus","principal axis"):
            if x in low:es.append(VisualEntity(f"O{len(es)+1}","optical_entity",x.title()))
    elif typ=="field_line_diagram":props["field"]="electric" if "electric" in low else "magnetic" if "magnetic" in low else "field"
    else:props["domain"]="kinematics" if typ=="motion_graph" else "waves"
    return VisualStructure("physics",typ,tuple(es),properties=props,confidence=.9).ensure_valid()

def understand_visual(text:str,*,image_path:str|Path|None=None):
    # Resolve generic circuit text before legacy high-confidence R1/X1 transformer cues.
    if re.search(r"\bcircuit\b",text,re.I) and not re.search(r"\btransformer\b",text,re.I):
        return _circuit(text)
    d=analyze_diagram_text(text)
    if not d.present:
        if image_path:
            x=analyze_image_geometry(image_path)
            if x.present:return VisualStructure("visual","diagram_candidate",properties={"requires_semantic_review":True},
                confidence=x.confidence,warnings=("Pixel structure needs semantic review.",)).ensure_valid()
        return None
    typ=d.diagram_type
    if typ=="circuit_diagram":return _circuit(text)
    if typ=="phasor_diagram":return _phasor(text)
    if typ in {"control_system_diagram","block_diagram","signal_diagram"}:return _control(text,typ)
    if typ=="waveform":return _wave(text)
    if typ=="coordinate_geometry":return _coord(text)
    if typ in {"graph","function_plot"}:return _function(text,typ)
    if typ=="geometric_figure":return _geometry(text)
    if typ in {"free_body_diagram","ray_diagram","field_line_diagram","motion_graph","wave_diagram"}:return _physics(text,typ)
    return VisualStructure(d.family or "other",typ,properties={"detected":True},confidence=d.confidence,
        warnings=("Family recognized; exact structure requires explicit source data.",)).ensure_valid()
