from __future__ import annotations
from dataclasses import dataclass,field,asdict
from datetime import datetime,timezone
from typing import Any

PRODUCTION_SCHEMA_VERSION="2.0"

@dataclass(frozen=True)
class Provenance:
    source_name:str
    source_sha256:str
    imported_at:str
    pipeline_contracts:tuple[str,...]
    parent_version:str|None=None

@dataclass
class ProductionQuestion:
    id:str
    schema_version:str
    revision:int
    lifecycle_status:str
    text:str
    exam:str
    subject:str
    topic:str
    subtopic:str|None
    concept:str|None
    question_type:str
    marks:int|None
    quality_score:float
    family_id:str
    provenance:Provenance
    metadata:dict[str,Any]=field(default_factory=dict)

    def to_dict(self):return asdict(self)

def utc_now()->str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def validate_production_question(q:ProductionQuestion)->list[str]:
    e=[]
    if q.schema_version!=PRODUCTION_SCHEMA_VERSION:e.append("Unsupported production schema version.")
    if not q.id:e.append("Question id is required.")
    if q.revision<1:e.append("Revision must be >= 1.")
    if q.lifecycle_status not in {"DRAFT","REVIEW","APPROVED","REJECTED","ARCHIVED"}:e.append("Invalid lifecycle status.")
    if not q.text.strip():e.append("Question text is empty.")
    if not 0<=q.quality_score<=1:e.append("Quality score must be between 0 and 1.")
    if not q.provenance.source_sha256:e.append("Source SHA-256 is required.")
    return e
