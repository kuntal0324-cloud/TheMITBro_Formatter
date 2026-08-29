from dataclasses import dataclass,field,asdict
from typing import Any
@dataclass(frozen=True)
class VisualEntity:
    id:str; kind:str; label:str=""; value:str|None=None
    position:tuple[float,float]|None=None
    properties:dict[str,Any]=field(default_factory=dict)
@dataclass(frozen=True)
class VisualRelation:
    source:str; target:str; kind:str; label:str=""; directed:bool=False
@dataclass(frozen=True)
class VisualStructure:
    family:str; diagram_type:str
    entities:tuple[VisualEntity,...]=()
    relations:tuple[VisualRelation,...]=()
    properties:dict[str,Any]=field(default_factory=dict)
    confidence:float=0.0; warnings:tuple[str,...]=()
    def ensure_valid(self):
        ids=[x.id for x in self.entities]
        if len(ids)!=len(set(ids)): raise ValueError("Duplicate visual entity ID.")
        known=set(ids)
        if any(r.source not in known or r.target not in known for r in self.relations):
            raise ValueError("Visual relation references unknown entity.")
        if not 0<=self.confidence<=1: raise ValueError("Invalid confidence.")
        return self
    def to_dict(self): return asdict(self)
