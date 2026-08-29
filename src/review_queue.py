from __future__ import annotations
from dataclasses import dataclass,asdict
from datetime import datetime,timezone

@dataclass(frozen=True)
class ReviewItem:
    question_id:str
    priority:int
    reasons:tuple[str,...]
    created_at:str
    status:str="OPEN"
    def to_dict(self):return asdict(self)

def build_review_item(record,quality):
    reasons=list(quality.blockers)
    if record.classification.status!="AUTO":reasons.append("classification_review")
    priority=100 if "validation_failure" in reasons else 80 if reasons else 0
    if priority==0:return None
    return ReviewItem(record.id,priority,tuple(sorted(set(reasons))),
        datetime.now(timezone.utc).replace(microsecond=0).isoformat())
