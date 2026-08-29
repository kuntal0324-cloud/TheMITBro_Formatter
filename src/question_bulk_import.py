from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .question_ingest import SUPPORTED
from .question_router import route_source


@dataclass(frozen=True)
class BulkImportSummary:
    processed: int
    auto: int
    review: int
    duplicates: int
    failed: int


def import_directory(
    directory: str | Path,
    *,
    root: str | Path = "question_bank",
    exam_hint: str | None = None,
) -> BulkImportSummary:
    base = Path(directory)
    if not base.is_dir():
        raise NotADirectoryError(base)

    processed = auto = review = duplicates = failed = 0

    for path in sorted(p for p in base.rglob("*") if p.is_file()):
        if path.suffix.lower() not in SUPPORTED:
            continue
        processed += 1
        try:
            result = route_source(path, root=root, exam_hint=exam_hint)
        except Exception:
            failed += 1
            continue

        if result.status == "DUPLICATE":
            duplicates += 1
        elif result.status == "AUTO":
            auto += 1
        else:
            review += 1

    return BulkImportSummary(
        processed=processed,
        auto=auto,
        review=review,
        duplicates=duplicates,
        failed=failed,
    )
