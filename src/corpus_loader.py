from __future__ import annotations
import json
from pathlib import Path
from .corpus_qualification_schema import CorpusCase

def load_jsonl(path)->tuple[CorpusCase,...]:
    p=Path(path)
    out=[]
    for n,line in enumerate(p.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip():continue
        data=json.loads(line)
        data["tags"]=tuple(data.get("tags",()))
        out.append(CorpusCase(**data))
    ids=[x.case_id for x in out]
    if len(ids)!=len(set(ids)):raise ValueError("Duplicate corpus case_id.")
    return tuple(out)

def load_builtin_corpus(root=None):
    base=Path(root) if root else Path(__file__).resolve().parents[1]
    return load_jsonl(base/"qualification_corpus"/"m43_gate_jee_hostile.jsonl")
