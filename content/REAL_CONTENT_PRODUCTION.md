# Real Content Production — Operating Procedure

The Formatter v2.0 architecture remains frozen. Real content should enter through controlled source batches and leave only through reviewed production releases.

## Three-repository contract
1. **TheMITbro Question Bank** owns original authoring, review state, question IDs and release manifests.
2. **TheMITbro Formatter v2.0** validates/normalizes content, builds the production bank, selects blueprint-compliant papers and publishes deterministic releases.
3. **TheMITbro website** sells only immutable release PDFs referenced by an approved Question Bank release manifest.

## Release gate
A paid paper must have: human technical review; independently checked answer/solution; no unresolved REVIEW/UNKNOWN blockers; approved diagram; blueprint qualification; deterministic build fingerprint; PDF checksum; product ID/price mapping; final purchase/download test.

## Recommended first production target
Build one complete GATE EE paper using the official exam-year pattern, because it exercises Engineering Mathematics, EE subjects, MCQ/MSQ/NAT, 1/2-mark selection, diagrams, solutions and the full publisher. Do not make the paper public until every selected question is APPROVED and the generated release passes human QA.
