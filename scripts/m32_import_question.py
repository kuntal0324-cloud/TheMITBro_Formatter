#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.question_ingest import ingest
from src.question_bank_store import QuestionBankStore


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import one text or JPG/JPEG question into TheMITbro Question Bank."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("--exam", help="Optional exam hint, e.g. 'GATE EE' or 'JEE'.")
    args = parser.parse_args()

    record = ingest(args.input, exam_hint=args.exam)
    path = QuestionBankStore().add(record, args.input)

    print(f"Question ID: {record.id}")
    print(f"Source type: {record.source_type}")
    print(f"Exam: {record.classification.exam}")
    print(f"Subject: {record.classification.subject}")
    print(f"Topic: {record.classification.topic}")
    print(f"Confidence: {record.classification.confidence:.3f}")
    print(f"Status: {record.classification.status}")
    print(f"Stored: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
