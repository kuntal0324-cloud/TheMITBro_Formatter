#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.gate_ee_set01_release_qualification import OUTPUT, qualify_set01


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare the computed result with committed evidence")
    args = parser.parse_args()
    result = qualify_set01()
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != rendered:
            print("GATE EE SET 01 FORMATTER RELEASE EVIDENCE: STALE")
            return 1
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"GATE EE SET 01 FORMATTER RELEASE EVIDENCE: {result['status']}")
    print(f"Questions: {result['question_count']} | PASS: {result['formatter_pass_count']} | BLOCKED: {result['formatter_blocked_count']}")
    print("Release and sale remain blocked pending exact-artifact release authorization.")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
