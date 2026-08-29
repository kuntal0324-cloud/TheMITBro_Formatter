# M41 Acceptance — Intelligent Mock-Paper Generator

M41 selects questions from the M40 production Question Bank using an explicit,
machine-readable blueprint.

Required:
- exact question-count and optional marks budget;
- minimum subject/topic coverage;
- difficulty distribution;
- MCQ/MSQ/NAT distribution;
- conceptual and numerical balance;
- visual-question minimum/maximum;
- expected-solving-time ceiling;
- production quality and lifecycle filters;
- question-family and strong near-duplicate avoidance;
- deterministic output for identical bank + blueprint + seed;
- constraint report and metrics for every successful paper;
- bridge into the existing QuestionPaper `PaperSpec` rendering architecture;
- complete historical regression.

Boundary:
M41 does not hard-code a claim that one blueprint is the current official GATE/JEE
pattern. Exam structures are represented as data/configuration and can be certified
against the target exam specification during M43. When a bank cannot satisfy the
blueprint, generation fails explicitly rather than silently relaxing constraints.
