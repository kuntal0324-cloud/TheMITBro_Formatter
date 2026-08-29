from __future__ import annotations
from dataclasses import dataclass,asdict
import time
from .semantic_duplicate_detector import find_semantic_duplicate
from .production_search import ProductionIndex

@dataclass(frozen=True)
class PerformanceReport:
    records:int
    index_seconds:float
    search_seconds:float
    duplicate_probe_seconds:float
    deterministic:bool
    contract:str="M44"
    def to_dict(self):return asdict(self)

def qualify_scale(records,query="transformer"):
    xs=list(records)
    t=time.perf_counter();idx=ProductionIndex()
    for x in xs:idx.add(x)
    index_s=time.perf_counter()-t
    t=time.perf_counter();a=idx.search(query);search_s=time.perf_counter()-t
    t=time.perf_counter()
    probe=find_semantic_duplicate(xs[0]["text"],xs[1:]) if len(xs)>1 else None
    dup_s=time.perf_counter()-t
    # deterministic index/search result on repeat
    b=idx.search(query)
    return PerformanceReport(len(xs),round(index_s,6),round(search_s,6),round(dup_s,6),a==b)
