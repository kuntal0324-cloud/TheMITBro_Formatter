#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.gate_ee_set01_release_qualification import INPUT, content_sha256


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path, help="Question Bank GATE_EE_SET_01_V1.json")
    parser.add_argument("handoff", type=Path, help="Question Bank GATE_EE_SET_01_V1_FORMATTER_HANDOFF.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    handoff = json.loads(args.handoff.read_text(encoding="utf-8"))
    if manifest.get("manifest_content_sha256") != content_sha256(manifest, "manifest_content_sha256"):
        raise SystemExit("Question Bank review manifest self-hash is invalid")
    if handoff.get("handoff_content_sha256") != content_sha256(handoff, "handoff_content_sha256"):
        raise SystemExit("Question Bank Formatter handoff self-hash is invalid")
    manifest_rows = manifest.get("questions", [])
    handoff_rows = handoff.get("paper", {}).get("questions", [])
    if len(manifest_rows) != 65 or len(handoff_rows) != 65:
        raise SystemExit("Question Bank inputs must each contain 65 questions")
    questions = []
    for manifest_row, handoff_row in zip(manifest_rows, handoff_rows):
        if (
            manifest_row.get("position") != handoff_row.get("number")
            or manifest_row.get("question_id") != handoff_row.get("id")
            or manifest_row.get("revision") != handoff_row.get("revision")
        ):
            raise SystemExit(f"Question Bank manifest/handoff mismatch at position {manifest_row.get('position')}")
        questions.append({
            "position": manifest_row["position"],
            "question_id": manifest_row["question_id"],
            "source_revision": manifest_row["revision"],
            "batch_id": manifest_row["batch_id"],
        })
    payload = {
        "input_contract": "GATE_EE_SET01_FORMATTER_RELEASE_INPUT_V1",
        "paper_id": manifest["paper_id"],
        "review_manifest_content_sha256": manifest["manifest_content_sha256"],
        "review_handoff_content_sha256": handoff["handoff_content_sha256"],
        "question_count": len(questions),
        "questions": questions,
        "release_authorized": False,
        "sale_authorized": False,
    }
    payload["input_content_sha256"] = content_sha256(payload, "input_content_sha256")
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not INPUT.is_file() or INPUT.read_text(encoding="utf-8") != rendered:
            print("GATE EE SET 01 FORMATTER RELEASE INPUT: STALE")
            return 1
    else:
        INPUT.parent.mkdir(parents=True, exist_ok=True)
        INPUT.write_text(rendered, encoding="utf-8")
    print("GATE EE SET 01 FORMATTER RELEASE INPUT: PASSED")
    print(f"Questions: {len(questions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
