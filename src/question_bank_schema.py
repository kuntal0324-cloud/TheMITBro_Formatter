from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Classification:
    exam: str
    subject: str
    topic: str
    confidence: float
    signals: list[str] = field(default_factory=list)
    status: str = "AUTO"


@dataclass
class QuestionRecord:
    id: str
    schema_version: str
    source_type: str
    source_sha256: str
    source_name: str
    text: str
    classification: Classification
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
