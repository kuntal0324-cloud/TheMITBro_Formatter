from __future__ import annotations
from dataclasses import dataclass,asdict
from pathlib import Path
import json,shutil
from .production_runtime import DEFAULT_RUNTIME
from .question_ingest import ingest,SUPPORTED
from .question_bank_production import promote,persist_production_question
from .deterministic_build import stable_question_id,build_fingerprint
from .semantic_duplicate_detector import find_semantic_duplicate
from .paper_blueprint import PaperBlueprint
from .mock_paper_generator import generate_mock_paper
from .mock_paper_bridge import to_paper_spec
from .professional_publisher import publish_release
from .integrity_audit import audit_production_bank,audit_zip
from .question_integrity import atomic_write_json

@dataclass(frozen=True)
class EndToEndResult:
    imported:int
    duplicates:int
    failed:int
    bank_root:str
    paper_id:str
    release_zip:str
    bank_integrity:dict
    release_integrity:dict
    build_fingerprint:str
    contract:str="M44"
    def to_dict(self):return asdict(self)

def build_end_to_end(source_dir,output_dir,blueprint:PaperBlueprint,*,exam_hint=None,runtime=DEFAULT_RUNTIME):
    src=Path(source_dir);out=Path(output_dir)
    if not src.is_dir():raise NotADirectoryError(src)
    files=sorted(p for p in src.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED)
    if len(files)>runtime.max_bulk_files:raise ValueError("Bulk source count exceeds configured production limit.")
    bank=out/"question_bank";release_root=out/"releases"
    bank.mkdir(parents=True,exist_ok=True);release_root.mkdir(parents=True,exist_ok=True)

    production=[];duplicates=failed=0
    for path in files:
        if runtime.reject_symlinks and path.is_symlink():
            failed+=1;continue
        if path.stat().st_size>runtime.max_source_bytes:
            failed+=1;continue
        try:
            rec=ingest(path,exam_hint=exam_hint)
            if len(rec.text)>runtime.max_question_chars:raise ValueError("Question text exceeds configured limit.")
            rec.id=stable_question_id(rec.source_sha256)
            dup=find_semantic_duplicate(rec.text,production)
            if dup.status=="DUPLICATE":
                duplicates+=1;continue
            prod=promote(rec)
            persist_production_question(prod,bank)
            production.append(prod.to_dict())
        except Exception:
            failed+=1

    paper=generate_mock_paper(production,blueprint)
    spec=to_paper_spec(paper)
    release=publish_release(spec,release_root,version="2.0.0",revision=1)

    bank_audit=audit_production_bank(bank)
    zip_audit=audit_zip(release.package_path)
    if not bank_audit.valid:raise IOError("Production bank integrity audit failed.")
    if not zip_audit.valid:raise IOError("Release ZIP integrity audit failed.")

    fingerprint=build_fingerprint(
        blueprint.to_dict(),
        [{"id":q["id"],"source_sha256":q["provenance"]["source_sha256"]} for q in production],
        {"paper_id":release.paper_id,"version":release.version},
    )
    summary=EndToEndResult(len(production),duplicates,failed,str(bank),release.paper_id,
                           release.package_path,bank_audit.to_dict(),zip_audit.to_dict(),fingerprint)
    atomic_write_json(out/"end-to-end-manifest.json",summary.to_dict())
    return summary
