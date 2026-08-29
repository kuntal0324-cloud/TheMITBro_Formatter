# M43 Acceptance — Real GATE/JEE Corpus Qualification

M43 changes the validation philosophy from isolated feature tests to hostile,
cross-pipeline qualification.

The bundled corpus contains original, exam-style questions covering:
- GATE EE Engineering Mathematics;
- GATE EE Electrical Engineering;
- JEE Mathematics;
- JEE Physics;
- MCQ/MSQ/NAT forms;
- equations, circuits, phasors, graphs, ray diagrams and free-body diagrams;
- OCR-like corruption and layout disturbance;
- adversarial terminology that can confuse overlapping taxonomies;
- ambiguous and impossible statements that must be reviewed rather than accepted.

Qualification layers:
1. classification/routing;
2. M38 topic/type intelligence;
3. M35 math-recognition survivability;
4. M36/M37 visual detection;
5. M39 ambiguity/impossibility gating;
6. M41 deterministic mock-paper generation;
7. M42 remains covered by the historical publishing regression.

Important boundary:
The corpus is original and representative; it is not copied from copyrighted
GATE/JEE papers. "Real corpus qualification" here means realistic exam-form,
hostile system qualification. Image tests generate photographed-page-like fixtures
locally. They validate preprocessing deterministically without claiming that CI
has a production-grade OCR benchmark camera dataset.

The default qualification gate is 75% corpus pass rate. M44 may raise this threshold
after remaining hard cases are corrected and performance is stabilized.
