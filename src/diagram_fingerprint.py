from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


def normalize_diagram_spec(spec: dict) -> dict:
    """
    Stable JSON normalization for duplicate/search metadata.
    Presentation-only fields are retained except volatile output paths.
    """
    def clean(value):
        if isinstance(value, dict):
            return {
                str(k): clean(v)
                for k, v in sorted(value.items(), key=lambda item: str(item[0]))
                if k not in {"output_path", "generated_at"}
            }
        if isinstance(value, list):
            return [clean(v) for v in value]
        if isinstance(value, float):
            return round(value, 8)
        return value
    return clean(spec)


def spec_fingerprint(spec: dict) -> str:
    payload = json.dumps(
        normalize_diagram_spec(spec),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def image_fingerprint(path: str | Path) -> str:
    source = Path(path)
    h = hashlib.sha256()
    with source.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
