# GATE EE Batch 001 — Formatter v2.0 Qualification Bridge

Consumes the Question Bank Batch 001 handoff under `input/gate_ee_batch_001/`, verifies SHA-256, and records Formatter v2.0 classification, M38 intelligence, M39 validation signals, quality score, duplicate decision and render smoke result for each of 20 questions.

This stage never claims independent human review. `paper_eligible` remains false and the release gate remains BLOCKED until the Question Bank receives actual independent review.

Run: `python -m src.run_gate_ee_batch_qualification`.
