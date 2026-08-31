# GATE EE Batch 001 — Formatter v2.0 Qualification Bridge

This production bridge consumes the immutable Question Bank handoff for Batch 001 without modifying the frozen M1–M45 processing contracts.

## Input
- `input/gate_ee_batch_001/BATCH_001_ENGINEERING_MATHEMATICS.jsonl`
- `input/gate_ee_batch_001/BATCH_001_FORMATTER_V2_HANDOFF.json`

The handoff SHA-256 must match before qualification starts.

## Qualification
For each of the 20 questions the bridge records:
- Formatter classification
- M38 question intelligence
- M39 validation signals
- production quality score
- within-batch duplicate decision
- formatting/render smoke result
- Formatter qualification decision

## Safety/quality boundary
Formatter qualification is **not independent human review**. This bridge therefore always keeps `paper_eligible=false` and the release gate BLOCKED. A later Question Bank review/promote stage must combine this report with actual independent technical/answer/solution review before promotion.

## Run
`python -m src.run_gate_ee_batch_qualification`
