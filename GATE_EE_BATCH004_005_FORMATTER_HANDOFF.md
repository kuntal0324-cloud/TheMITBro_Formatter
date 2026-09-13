# GATE EE Batches 004–005 Formatter Handoff

Date: 2026-09-13

## Qualified inputs

- Batch 004 Signals and Systems: 15 questions, source SHA-256 `0d0eb24d9f82f1f511f8dcb879dd78d5684fa73c444a8319d6bc01bdd7961b66`.
- Batch 005 Electromagnetic Fields: 12 questions, source SHA-256 `f30c6d8b1a522d75effdc46b147c87a723e57ecc0a43ef74624daa9da25fb89e`.
- Combined result: 27 Formatter PASS / 0 REVIEW / 0 invalid, with six checksum-bound SVGs.

The deterministic evidence files are:

- `output/gate_ee_batch_004/FORMATTER_V2_QUALIFICATION.json` — SHA-256 `25f128b7778a9504e0ddd76380b91be92fea82511952f400ede72f827b201834`.
- `output/gate_ee_batch_005/FORMATTER_V2_QUALIFICATION.json` — SHA-256 `d1ed63b24f739b5df1b81ca035b3b52b5ecee81c56c6b72036143e12ec96dd8b`.

## Reproduction

```bash
python -m pip install -r requirements.txt
python -m pytest -q tests/test_gate_ee_batch004_qualification.py tests/test_gate_ee_batch005_qualification.py
python -m src.run_gate_ee_batch_qualification \
  --jsonl input/gate_ee_batch_004/BATCH_004_SIGNALS_AND_SYSTEMS.jsonl \
  --handoff input/gate_ee_batch_004/BATCH_004_FORMATTER_V2_HANDOFF.json \
  --output output/gate_ee_batch_004/FORMATTER_V2_QUALIFICATION.json
python -m src.run_gate_ee_batch_qualification \
  --jsonl input/gate_ee_batch_005/BATCH_005_ELECTROMAGNETIC_FIELDS.jsonl \
  --handoff input/gate_ee_batch_005/BATCH_005_FORMATTER_V2_HANDOFF.json \
  --output output/gate_ee_batch_005/FORMATTER_V2_QUALIFICATION.json
git diff --exit-code -- output/gate_ee_batch_004/FORMATTER_V2_QUALIFICATION.json
git diff --exit-code -- output/gate_ee_batch_005/FORMATTER_V2_QUALIFICATION.json
python -m pytest -q
git diff --check
```

Expected full regression: 844 passed. The two existing `src.main` runpy warnings are non-failing historical warnings.

## Gate boundary

Formatter PASS is not human approval. Neither batch becomes paper-eligible or sellable until its completed, checksum-bound human-QA PDF is imported, validated and separately promoted in the Question Bank repository.
