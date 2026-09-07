from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class DiagramTextCheck:
    status:str; message:str; missing:tuple[str,...]=()

def validate_diagram_text(text:str,visual_structure:dict|None)->DiagramTextCheck:
    # Text-only questions with no visual cues have no diagram contract to
    # validate.  Treat that state as satisfied; actual image uncertainty is
    # tracked separately by ``requires_visual_review`` during ingestion.
    if not visual_structure:
        if re.search(r"\b(?:diagram|figure|shown\s+(?:below|above|in)|as\s+shown)\b",text,re.I):
            return DiagramTextCheck("UNKNOWN","Question references a visual that was not recovered.")
        return DiagramTextCheck("PASS","No diagram is required.")
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
