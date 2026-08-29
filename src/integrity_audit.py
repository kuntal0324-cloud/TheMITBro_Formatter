from __future__ import annotations
from dataclasses import dataclass,asdict
from pathlib import Path
from zipfile import ZipFile
import json,hashlib
from .question_integrity import verify as verify_record

@dataclass(frozen=True)
class IntegrityAudit:
    valid:bool
    checked:int
    errors:tuple[str,...]
    sha256:str|None=None
    def to_dict(self):return asdict(self)

def audit_production_bank(root):
    base=Path(root);errors=[];count=0
    for p in sorted((base/"records").glob("*.json")) if (base/"records").exists() else []:
        count+=1
        try:data=json.loads(p.read_text(encoding="utf-8"))
        except Exception:errors.append(f"invalid_json:{p.name}");continue
        if not verify_record(data):errors.append(f"record_hash:{p.name}")
        if data.get("id") and p.stem!=data["id"]:errors.append(f"id_path_mismatch:{p.name}")
    return IntegrityAudit(not errors,count,tuple(errors))

def audit_zip(path):
    p=Path(path);errors=[]
    with ZipFile(p) as z:
        bad=z.testzip()
        if bad:errors.append(f"zip_crc:{bad}")
        names=z.namelist()
        if len(names)!=len(set(names)):errors.append("duplicate_zip_entry")
        for n in names:
            parts=Path(n).parts
            if n.startswith("/") or ".." in parts:errors.append(f"unsafe_zip_path:{n}")
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    return IntegrityAudit(not errors,len(names),tuple(errors),h)
