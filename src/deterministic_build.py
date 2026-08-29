from __future__ import annotations
import hashlib,json
from pathlib import Path

def stable_question_id(source_sha256:str)->str:
    return "QB-"+str(source_sha256).upper()[:12]

def canonical_json_bytes(data)->bytes:
    return json.dumps(data,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode("utf-8")

def build_fingerprint(*objects)->str:
    h=hashlib.sha256()
    for obj in objects:
        h.update(canonical_json_bytes(obj));h.update(b"\0")
    return h.hexdigest()

def file_sha256(path)->str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
