from __future__ import annotations
from pathlib import Path
import hashlib,json
from .contract_registry import registry_dict
from .final_baseline import audit_repository,FROZEN_VERSION

def build_final_manifest(root="."):
    base=Path(root)
    audit=audit_repository(base)
    return {
        "product":"TheMITbro Formatter",
        "release":"v2.0.0",
        "milestone":"M45",
        "architecture_status":"FROZEN",
        "content_production_status":"READY",
        "baseline_sha256":audit.baseline_sha256,
        "contracts":registry_dict(),
        "historical_contract_markers":["M35","M36","M37","M38","M39","M40","M41","M42","M43","M44"],
        "next_operational_phase":"Real GATE EE / IIT-JEE content production",
    }

def write_final_manifest(path,root="."):
    p=Path(path)
    p.write_text(json.dumps(build_final_manifest(root),indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return p
