# M32 — Question Bank Ingestion

M32 adds the first production question-bank layer on top of Formatter v1.0.0.

### Supported inputs

- Markdown/text files
- JPG/JPEG question images

### Automatic routing

Questions are classified by deterministic keyword rules into an explicit
exam/subject/topic taxonomy. Low-confidence or ambiguous questions are routed
to review instead of guessed.

### Duplicate handling

The source SHA-256 is used for idempotent ingestion.

### JPG preservation

Original image sources are copied into `question_bank/assets/` so OCR output
does not destroy the original evidence.

### Next

M33 should expand the taxonomy, add batch import, richer structured extraction
(options/answers/diagrams), and corpus-level routing validation.
