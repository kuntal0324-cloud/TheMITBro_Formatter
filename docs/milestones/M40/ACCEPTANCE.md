# M40 Acceptance — Question Bank Production Engine

M40 converts the ingestion/intelligence pipeline into a durable production Question Bank.

Acceptance requires:
- canonical schema v2.0 while retaining historical record compatibility;
- production bulk import with duplicate suppression;
- lexical + semantic near-duplicate screening;
- stable question-family IDs that tolerate numeric variants;
- quality scoring using classification, OCR, mathematics, taxonomy and M39 validation;
- provenance and immutable revision metadata;
- in-memory inverted search index with structured filters;
- prioritized review queues;
- explicit catalog migration to production schema;
- SHA-256 payload sealing and atomic JSON writes with read-back;
- dedicated M40 CI plus the complete historical regression.

Accuracy boundary:
M40's semantic duplicate detector is deterministic token/lexical intelligence, not a
claim of neural embedding equivalence. Borderline cases are REVIEW rather than
silently deleted. Production approval is conservative: unresolved blockers remain
in REVIEW.
