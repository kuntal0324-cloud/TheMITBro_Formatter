from __future__ import annotations
from pathlib import Path
from .production_schema import ProductionQuestion,Provenance,PRODUCTION_SCHEMA_VERSION,utc_now,validate_production_question
from .question_family import family_id
from .question_quality_score import score_question
from .question_integrity import seal,atomic_write_json
from .question_versioning import make_revision

def promote(record)->ProductionQuestion:
    q=score_question(record);m=record.metadata;c=record.classification
    lifecycle="APPROVED" if q.grade=="A" and not q.blockers else "REVIEW"
    contracts=tuple(x for x in ("M35","M36","M37","M38","M39") if x in {
        m.get("ingestion_contract"),m.get("diagram_contract"),m.get("visual_intelligence_contract"),
        m.get("question_intelligence_contract"),m.get("validation_intelligence_contract")})
    return ProductionQuestion(
        id=record.id,schema_version=PRODUCTION_SCHEMA_VERSION,revision=1,lifecycle_status=lifecycle,
        text=record.text,exam=c.exam,subject=c.subject,topic=c.topic,subtopic=m.get("subtopic"),concept=m.get("concept"),
        question_type=m.get("question_type","UNSPECIFIED"),marks=m.get("marks"),quality_score=q.score,
        family_id=family_id(record),
        provenance=Provenance(record.source_name,record.source_sha256,utc_now(),contracts),
        metadata={"quality":q.to_dict(),"legacy_schema_version":record.schema_version,
                  "validation_status":m.get("validation_status"),"difficulty":m.get("difficulty"),
                  "difficulty_score":m.get("difficulty_score"),
                  "reasoning_depth":m.get("reasoning_depth"),
                  "calculation_load":m.get("calculation_load"),
                  "expected_time_seconds":m.get("expected_time_seconds"),
                  "diagram_present":m.get("diagram_present",False),
                  "diagram_type":m.get("diagram_type"),
                  "syllabus_path":m.get("syllabus_path",[])}
    )

def persist_production_question(question:ProductionQuestion,root):
    errors=validate_production_question(question)
    if errors:raise ValueError("; ".join(errors))
    base=Path(root);data=seal(question.to_dict())
    path=base/"records"/f"{question.id}.json"
    atomic_write_json(path,data)
    rev=make_revision(question.id,data,question.revision)
    atomic_write_json(base/"versions"/question.id/f"{question.revision:04d}.json",{"revision":rev.to_dict(),"record":data})
    return path
