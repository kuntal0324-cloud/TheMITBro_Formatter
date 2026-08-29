from __future__ import annotations
from dataclasses import dataclass, asdict
import hashlib
import json
import re

@dataclass(frozen=True)
class PublicationIdentity:
    paper_id: str
    version: str
    revision: int
    content_sha256: str
    release_label: str

    def to_dict(self):
        return asdict(self)


def _slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", str(value)).strip("-").upper()
    return value or "PAPER"


def content_hash(paper) -> str:
    data = paper.to_dict() if hasattr(paper, "to_dict") else dict(paper)
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def build_identity(paper, *, version: str = "1.0.0", revision: int = 1) -> PublicationIdentity:
    digest = content_hash(paper)
    exam = getattr(paper, "exam", None) if hasattr(paper, "exam") else paper.get("exam")
    paper_id = f"TMB-{_slug(exam or 'EXAM')}-{digest[:12].upper()}"
    return PublicationIdentity(paper_id, version, int(revision), digest, f"{paper_id}-v{version}-r{revision}")
