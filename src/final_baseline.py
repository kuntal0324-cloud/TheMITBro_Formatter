from __future__ import annotations
from dataclasses import dataclass,asdict
from pathlib import Path
import hashlib,json

FROZEN_VERSION="2.0.0"

@dataclass(frozen=True)
class BaselineAudit:
    version:str
    source_files:int
    test_files:int
    workflow_files:int
    milestone_docs:int
    required_docs_present:bool
    m44_certified:bool
    corpus_pass_rate:float
    baseline_sha256:str
    errors:tuple[str,...]
    contract:str="M45"
    def to_dict(self):return asdict(self)

def _sha(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def _fingerprint(root:Path,paths:list[Path])->str:
    h=hashlib.sha256()
    for p in sorted(paths,key=lambda x:str(x.relative_to(root))):
        rel=str(p.relative_to(root)).replace("\\","/")
        h.update(rel.encode());h.update(b"\0");h.update(_sha(p).encode());h.update(b"\n")
    return h.hexdigest()

def audit_repository(root=".")->BaselineAudit:
    base=Path(root)
    errors=[]
    src=list((base/"src").glob("*.py"))
    tests=list((base/"tests").glob("test_*.py"))
    workflows=list((base/".github/workflows").glob("*.yml"))
    milestone_docs=list((base/"docs/milestones").glob("M*/ACCEPTANCE.md"))
    required=[
        base/"README.md",base/"VERSION",base/"requirements.txt",
        base/"docs/ROADMAP.md",base/"docs/ARCHITECTURE.md",
        base/"docs/FORMAT_SPECIFICATION.md",base/"docs/RELEASE_PROCESS.md",
        base/"m44-production-certification.json",
    ]
    required_ok=all(p.is_file() for p in required)
    if not required_ok:errors.append("required_release_document_missing")
    cert={}
    try:cert=json.loads((base/"m44-production-certification.json").read_text(encoding="utf-8"))
    except Exception:errors.append("m44_certification_unreadable")
    m44_ok=bool(cert.get("ready_for_final_certification")) and cert.get("corpus_pass_rate",0)>=.95
    if not m44_ok:errors.append("m44_not_certified")
    # Hash the implementation/release surface, excluding generated M45 manifests
    # to avoid circular self-hashing.
    hash_paths=src+tests+workflows+[p for p in required if p.exists()]
    digest=_fingerprint(base,hash_paths)
    return BaselineAudit(
        FROZEN_VERSION,len(src),len(tests),len(workflows),len(milestone_docs),
        required_ok,m44_ok,float(cert.get("corpus_pass_rate",0.0)),digest,tuple(errors)
    )
