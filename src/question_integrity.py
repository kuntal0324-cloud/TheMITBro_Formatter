from __future__ import annotations
import hashlib,json
from pathlib import Path

def payload_hash(data:dict)->str:
    clean=dict(data);clean.pop("integrity_sha256",None)
    raw=json.dumps(clean,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode()
    return hashlib.sha256(raw).hexdigest()

def seal(data:dict)->dict:
    out=dict(data);out["integrity_sha256"]=payload_hash(out);return out

def verify(data:dict)->bool:
    expected=data.get("integrity_sha256")
    return bool(expected) and expected==payload_hash(data)

def atomic_write_json(path,data):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix(p.suffix+".tmp")
    tmp.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    # read-back protects against serialization/write corruption before replace
    check=json.loads(tmp.read_text(encoding="utf-8"))
    # JSON round-tripping converts tuples to lists; compare canonical serialized
    # representations rather than Python container types.
    expected=json.loads(json.dumps(data,ensure_ascii=False))
    if check!=expected:
        tmp.unlink(missing_ok=True);raise IOError("Integrity read-back failed.")
    tmp.replace(p)
