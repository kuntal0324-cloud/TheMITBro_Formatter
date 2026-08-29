from __future__ import annotations
from dataclasses import dataclass,asdict
import os

@dataclass(frozen=True)
class ProductionRuntime:
    max_source_bytes:int=8*1024*1024
    max_bulk_files:int=5000
    max_question_chars:int=200000
    deterministic_ids:bool=True
    atomic_writes:bool=True
    verify_after_write:bool=True
    backup_before_replace:bool=True
    reject_symlinks:bool=True
    contract:str="M44"

    def to_dict(self):return asdict(self)

DEFAULT_RUNTIME=ProductionRuntime()

def runtime_from_env()->ProductionRuntime:
    def num(name,default):
        raw=os.getenv(name)
        return int(raw) if raw else default
    return ProductionRuntime(
        max_source_bytes=num("THEMITBRO_MAX_SOURCE_BYTES",DEFAULT_RUNTIME.max_source_bytes),
        max_bulk_files=num("THEMITBRO_MAX_BULK_FILES",DEFAULT_RUNTIME.max_bulk_files),
        max_question_chars=num("THEMITBRO_MAX_QUESTION_CHARS",DEFAULT_RUNTIME.max_question_chars),
    )
