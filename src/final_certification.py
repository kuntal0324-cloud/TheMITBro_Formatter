from __future__ import annotations
from dataclasses import dataclass,asdict
from pathlib import Path
import json
from .contract_registry import final_contract_registry
from .final_baseline import audit_repository,FROZEN_VERSION
from .corpus_loader import load_builtin_corpus
from .corpus_qualification import qualify_corpus

@dataclass(frozen=True)
class FinalCertification:
    product:str
    version:str
    milestone:int
    contracts_frozen:int
    corpus_total:int
    corpus_passed:int
    corpus_pass_rate:float
    repository_audit:dict
    ready_for_real_content:bool
    architecture_frozen:bool=True
    contract:str="M45"
    def to_dict(self):return asdict(self)

def certify_v2(root=".")->FinalCertification:
    audit=audit_repository(root)
    corpus=qualify_corpus(load_builtin_corpus(root))
    contracts=final_contract_registry()
    ready=(
        not audit.errors
        and len(contracts)==44
        and corpus.pass_rate==1.0
        and audit.m44_certified
    )
    return FinalCertification(
        "TheMITbro Formatter",FROZEN_VERSION,45,len(contracts),
        corpus.total,corpus.passed,corpus.pass_rate,audit.to_dict(),ready
    )

def write_final_certification(path,root="."):
    c=certify_v2(root)
    Path(path).write_text(json.dumps(c.to_dict(),indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return c
