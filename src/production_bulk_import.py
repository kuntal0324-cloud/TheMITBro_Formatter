from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from .question_ingest import ingest,SUPPORTED
from .question_bank_production import promote,persist_production_question
from .semantic_duplicate_detector import find_semantic_duplicate
from .review_queue import build_review_item
from .question_quality_score import score_question
from .question_integrity import atomic_write_json

@dataclass(frozen=True)
class ProductionImportSummary:
    processed:int; imported:int; review:int; duplicates:int; failed:int

def import_production_directory(directory,*,root="question_bank_production",exam_hint=None):
    src=Path(directory);dest=Path(root)
    if not src.is_dir():raise NotADirectoryError(src)
    existing=[];queue=[];processed=imported=review=duplicates=failed=0
    for p in sorted(x for x in src.rglob("*") if x.is_file() and x.suffix.lower() in SUPPORTED):
        processed+=1
        try:
            record=ingest(p,exam_hint=exam_hint)
            d=find_semantic_duplicate(record.text,existing)
            if d.status=="DUPLICATE":
                duplicates+=1;continue
            prod=promote(record)
            if d.status=="REVIEW":prod.lifecycle_status="REVIEW"
            persist_production_question(prod,dest)
            item=build_review_item(record,score_question(record))
            if item:queue.append(item.to_dict())
            existing.append(prod.to_dict());imported+=1
            if prod.lifecycle_status=="REVIEW":review+=1
        except Exception:
            failed+=1
    atomic_write_json(dest/"review_queue.json",{"contract":"M40","items":queue})
    return ProductionImportSummary(processed,imported,review,duplicates,failed)
