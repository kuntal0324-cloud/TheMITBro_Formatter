from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class DiagramTextCheck:
    status:str; message:str; missing:tuple[str,...]=()

def validate_diagram_text(text:str,visual_structure:dict|None)->DiagramTextCheck:
    if not visual_structure:return DiagramTextCheck("UNKNOWN","No visual structure available.")
    typ=visual_structure.get("diagram_type")
    entities=visual_structure.get("entities") or []
    kinds={str(e.get("kind","")).lower() for e in entities}
    labels={str(e.get("label","")).lower() for e in entities}
    low=text.lower();required=[]
    mapping={
        "resistor":"resistor","capacitor":"capacitor","inductor":"inductor",
        "voltage source":"voltage_source","current source":"current_source",
        "lens":"optical_entity","mirror":"optical_entity",
    }
    for word,kind in mapping.items():
        if word in low: required.append((word,kind))
    missing=tuple(word for word,kind in required if kind not in kinds and word not in labels)
    if missing:return DiagramTextCheck("FAIL","Diagram structure is missing explicitly requested entities.",missing)
    return DiagramTextCheck("PASS","Diagram structure is consistent with explicit textual entities.")
