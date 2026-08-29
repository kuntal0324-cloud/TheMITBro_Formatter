from __future__ import annotations
from pathlib import Path
import json

class SecurityViolation(ValueError):pass

def safe_child(root,path)->Path:
    base=Path(root).resolve()
    p=Path(path)
    candidate=(base/p).resolve() if not p.is_absolute() else p.resolve()
    try:
        candidate.relative_to(base)
    except ValueError as exc:
        raise SecurityViolation(f"Path escapes root: {path}") from exc
    return candidate

def reject_symlink(path)->None:
    p=Path(path)
    if p.is_symlink():
        raise SecurityViolation(f"Symbolic links are not accepted: {p}")

def bounded_read_text(path,*,max_bytes:int)->str:
    p=Path(path)
    reject_symlink(p)
    size=p.stat().st_size
    if size>max_bytes:raise SecurityViolation(f"Source exceeds size limit: {size}>{max_bytes}")
    return p.read_text(encoding="utf-8")

def load_json_object(path,*,max_bytes:int=8*1024*1024)->dict:
    raw=bounded_read_text(path,max_bytes=max_bytes)
    try:data=json.loads(raw)
    except json.JSONDecodeError as exc:raise ValueError(f"Invalid JSON: {path}") from exc
    if not isinstance(data,dict):raise ValueError("Expected a JSON object.")
    return data
