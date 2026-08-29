# M35 Acceptance — Universal Mathematical Recognition

M35 establishes a conservative recognition layer for GATE EE and IIT-JEE
question-bank production.

Acceptance requirements:
- Unicode mathematical symbols normalize to stable LaTeX-compatible text.
- Superscripts and subscripts are preserved structurally.
- Matrices/determinants, calculus, differential equations, probability,
  statistics, complex variables, transforms, and vector calculus are detected.
- Electrical Engineering notation such as j, ohm/Omega, degrees and scientific
  notation is preserved.
- Math segmentation identifies LaTeX, matrix literals and equation-like spans.
- Question ingestion stores normalized math metadata without discarding the
  original source text.
- Low-confidence OCR/math remains routed to Review.
- GATE EE taxonomy includes Electromagnetic Fields, Analog Electronics and
  Digital Electronics.
- JEE Physics taxonomy expands to Optics, Oscillations/Waves and Thermal Physics.
- Full historical regression remains green.

Scope boundary:
M35 recognizes and normalizes mathematical/scientific notation. It does not
claim pixel-level equation reconstruction or semantic diagram understanding.
Those remain the focus of later milestones.
