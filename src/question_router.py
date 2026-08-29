from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .question_bank_store import QuestionBankStore
from .question_duplicate_detector import DuplicateDecision, find_duplicate
from .question_ingest import ingest


@dataclass(frozen=True)
class RouteResult:
    status: str
    path: Path | None
    question_id: str | None
    duplicate: DuplicateDecision | None = None


def route_source(
    source: str | Path,
    *,
    root: str | Path = "question_bank",
    exam_hint: str | None = None,
) -> RouteResult:
    source = Path(source)
    record = ingest(source, exam_hint=exam_hint)
    store = QuestionBankStore(Path(root))
    catalog = store._load()

    decision = find_duplicate(record.text, catalog.get("questions", []))

    if decision.status == "DUPLICATE":
        return RouteResult(
            status="DUPLICATE",
            path=None,
            question_id=decision.matched_id,
            duplicate=decision,
        )

    if decision.status in {"FLAG", "REVIEW"}:
        record.classification.status = "REVIEW"
        record.classification.topic = "Review Required"
        record.metadata["duplicate_status"] = decision.status
        record.metadata["duplicate_similarity"] = decision.similarity
        record.metadata["duplicate_match"] = decision.matched_id

    path = store.add(record, source)
    return RouteResult(
        status=record.classification.status,
        path=path,
        question_id=record.id,
        duplicate=decision,
    )
