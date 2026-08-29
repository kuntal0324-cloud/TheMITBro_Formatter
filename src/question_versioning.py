from __future__ import annotations
from dataclasses import dataclass,asdict
from datetime import datetime,timezone
import hashlib,json

def canonical_hash(data:dict)->str:
    clean=dict(data);clean.pop("integrity_sha256",None)
    return hashlib.sha256(json.dumps(clean,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode()).hexdigest()

@dataclass(frozen=True)
class Revision:
    question_id:str
    revision:int
    timestamp:str
    content_sha256:str
    reason:str
    parent_sha256:str|None=None
    def to_dict(self):return asdict(self)

def make_revision(question_id,data,revision=1,reason="import",parent_sha256=None):
    return Revision(question_id,revision,datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                    canonical_hash(data),reason,parent_sha256)
