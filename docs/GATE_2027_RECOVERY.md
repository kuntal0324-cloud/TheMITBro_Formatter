# GATE 2027 recovery contract

## What changed

- Removed Numerical Methods from the GATE EE taxonomy. It is present in XE, not EE.
- Routed Laplace, Fourier and Z transforms to EE Signals and Systems; Fourier series remains Engineering Mathematics / Calculus.
- Added General Aptitude routing seeds and official EE section naming.
- Split mixed text/image OCR sources into independently routed question records.
- Preserved OCR line breaks and extracted stem, options, answer and solution into structured metadata.
- Added segment-level idempotency so one upload can safely create many question records.
- Added a learner-facing math boundary that converts source TeX-like markup into readable Unicode/plain text for non-typesetting renderers.
- Prevented automated promotion to `APPROVED`; a named human decision is required.
- Made Batch 001 qualification strict: classification, syllabus match, content validation, quality, duplicate and render gates must all pass.

## Current Batch 001 result

The revised 20-question source renders without exposed source markup, but it is **not qualified**:

- Formatter pass: 0
- Formatter review: 20
- Content validation review: 20
- Syllabus route match: 20
- Paper eligible: 0

This result is intentionally conservative. All syllabus routes now match; the 20 content-validation reviews must be resolved before human final QA.

## Input APIs

- Use `ingest_many(path, exam_hint="GATE EE")` to extract every question from a text/JPG/PNG source.
- Use `route_source_many(...)` to classify and persist every extracted question.
- `ingest(...)` refuses a multi-question source instead of silently discarding later questions.

Source math is retained internally for future MathML or real typesetting. Learner-facing SVG/HTML/PDF paths must pass `has_source_math_markup(...) == False`.
