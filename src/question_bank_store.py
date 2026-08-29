from __future__ import annotations

import json
import re
from pathlib import Path

from .question_bank_schema import QuestionRecord
from .question_ingest import copy_original_image


def _safe(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "_", value.strip())
    return value.strip("_") or "Unclassified"


class QuestionBankStore:
    def __init__(self, root: str | Path = "question_bank"):
        self.root = Path(root)
        self.catalog_path = self.root / "catalog.json"
        self.root.mkdir(parents=True, exist_ok=True)

    def _load(self) -> dict:
        if not self.catalog_path.exists():
            return {"schema_version": "1.1", "contract": "M34", "questions": []}
        return json.loads(self.catalog_path.read_text(encoding="utf-8"))

    def _save(self, data: dict) -> None:
        self.catalog_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def add(self, record: QuestionRecord, source_path: Path | None = None) -> Path:
        data = self._load()

        # Idempotency is based on source SHA-256.
        for existing in data["questions"]:
            if existing.get("source_sha256") == record.source_sha256:
                return Path(existing["record_path"])

        c = record.classification
        if c.status == "AUTO":
            folder = (
                self.root / "by_exam" / _safe(c.exam) /
                _safe(c.subject) / _safe(c.topic)
            )
        else:
            folder = self.root / "review"

        folder.mkdir(parents=True, exist_ok=True)
        record_path = folder / f"{record.id}.json"

        if source_path is not None:
            copied = copy_original_image(
                source_path, record, self.root / "assets"
            )
            if copied:
                record.metadata["preserved_source"] = copied

        record_path.write_text(
            json.dumps(record.to_dict(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        entry = record.to_dict()
        entry["record_path"] = str(record_path).replace("\\", "/")
        data["questions"].append(entry)
        self._save(data)
        return record_path
