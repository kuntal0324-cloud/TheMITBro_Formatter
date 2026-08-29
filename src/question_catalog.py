from __future__ import annotations

import json
from pathlib import Path


def load_catalog(root: str | Path) -> dict:
    path = Path(root) / "catalog.json"
    if not path.exists():
        # Preserve the M33 public contract for an empty catalog.
        return {"questions": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("questions"), list):
        raise ValueError("Invalid question catalog.")
    return data


def search_catalog(
    root: str | Path,
    *,
    exam: str | None = None,
    subject: str | None = None,
    topic: str | None = None,
    text: str | None = None,
) -> list[dict]:
    questions = load_catalog(root)["questions"]
    needle = (text or "").lower().strip()
    out = []

    for item in questions:
        classification = item.get("classification", {})
        if exam and classification.get("exam") != exam:
            continue
        if subject and classification.get("subject") != subject:
            continue
        if topic and classification.get("topic") != topic:
            continue
        if needle and needle not in str(item.get("text", "")).lower():
            continue
        out.append(item)

    return out
