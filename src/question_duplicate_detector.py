from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Iterable


def normalize_text(text: str) -> str:
    text = text.lower().replace("−", "-")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[“”]", '"', text)
    text = re.sub(r"[‘’]", "'", text)
    return text.strip()


def fingerprint(text: str) -> str:
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()


def similarity(a: str, b: str) -> float:
    return round(
        SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio(),
        4,
    )


@dataclass(frozen=True)
class DuplicateDecision:
    status: str
    similarity: float
    matched_id: str | None = None


def find_duplicate(
    text: str,
    existing: Iterable[dict],
    *,
    flag_threshold: float = 0.95,
    review_threshold: float = 0.80,
) -> DuplicateDecision:
    wanted_fp = fingerprint(text)
    best_score = 0.0
    best_id = None

    for item in existing:
        existing_text = str(item.get("text", ""))
        if not existing_text:
            continue

        if fingerprint(existing_text) == wanted_fp:
            return DuplicateDecision("DUPLICATE", 1.0, item.get("id"))

        score = similarity(text, existing_text)
        if score > best_score:
            best_score = score
            best_id = item.get("id")

    if best_score >= flag_threshold:
        return DuplicateDecision("FLAG", best_score, best_id)
    if best_score >= review_threshold:
        return DuplicateDecision("REVIEW", best_score, best_id)
    return DuplicateDecision("ACCEPT", best_score, best_id)
