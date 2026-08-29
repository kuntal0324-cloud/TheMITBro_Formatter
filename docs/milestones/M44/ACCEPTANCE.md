# M44 Acceptance — Production Hardening & End-to-End Platform

M44 is the production-hardening milestone. It validates that the project operates
as one system rather than as isolated milestone modules.

Acceptance requires:

- hardening the remaining M43 corpus failures and maintaining >=95% qualification;
- deterministic source-derived Question Bank IDs for the production pipeline;
- deterministic paper-selection/build fingerprints;
- configured source-size and bulk-count limits;
- symlink/path-traversal defenses in hardened I/O utilities;
- atomic, integrity-checked persistence;
- Question Bank record integrity auditing;
- release ZIP CRC, duplicate-entry and path-safety auditing;
- recovery-point creation and verified restore;
- migration planning with pre-migration snapshots and identity/count preservation;
- 1,000-record search/duplicate scale qualification;
- full input -> ingest/OCR/math/visual -> classification -> validation ->
  production bank -> mock-paper selection -> professional publication -> ZIP workflow;
- complete historical regression;
- dedicated CI certification report.

## Contract preservation

Historical M35-M43 contracts and the four M30 release-documentation files remain
part of the supported repository contract. M44 adds new hardening behavior rather
than deleting earlier interfaces.

## Scope boundary

M44 is a production engineering hardening layer, not a claim of infallible OCR,
visual semantics, or solving. Unsupported cases continue to use REVIEW/UNKNOWN.
Performance thresholds in CI are smoke/qualification thresholds, not a universal
hardware SLA.
