from __future__ import annotations
from copy import deepcopy

def migrate_catalog(data:dict,target="2.0")->dict:
    out=deepcopy(data)
    current=str(out.get("schema_version","1.1"))
    if current==target:return out
    if target!="2.0":raise ValueError("Unsupported migration target.")
    if not isinstance(out.get("questions",[]),list):raise ValueError("Invalid catalog questions.")
    out["schema_version"]="2.0"
    out["production_contract"]="M40"
    out.setdefault("migrations",[]).append({"from":current,"to":"2.0","milestone":"M40"})
    return out
