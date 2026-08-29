from __future__ import annotations
from dataclasses import dataclass,asdict
from pathlib import Path
import json
from .corpus_loader import load_builtin_corpus
from .corpus_qualification import qualify_corpus

@dataclass(frozen=True)
class ProductionCertification:
    corpus_total:int
    corpus_passed:int
    corpus_pass_rate:float
    historical_contracts:tuple[str,...]
    ready_for_final_certification:bool
    contract:str="M44"
    def to_dict(self):return asdict(self)

def certify_m44():
    r=qualify_corpus(load_builtin_corpus())
    contracts=("M35","M36","M37","M38","M39","M40","M41","M42","M43","M44")
    return ProductionCertification(r.total,r.passed,r.pass_rate,contracts,r.pass_rate>=.95)

def write_certification(path):
    c=certify_m44()
    Path(path).write_text(json.dumps(c.to_dict(),indent=2)+"\n",encoding="utf-8")
    return c
