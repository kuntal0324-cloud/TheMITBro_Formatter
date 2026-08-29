# M39 Acceptance — Answer, Solver & Validation Intelligence

M39 adds independent validation layers to the existing formatter/question-bank stack.

Required:
- symbolic equivalence through the existing SymPy-backed solver utilities;
- numeric comparison with explicit tolerances;
- SI dimensional compatibility for common Mathematics/EE/Physics units;
- MCQ/MSQ/NAT answer-key and option integrity validation;
- independent expected-answer verification when a computed/known value exists;
- deterministic EE/Physics sanity models for explicit equations (including Ohm's law,
  electrical power, Newton's second law and elementary kinematics);
- diagram/text entity consistency;
- supplied solution final-result versus answer-key consistency;
- ambiguity, underdetermination and impossible-operation review flags;
- PASS/FAIL/UNKNOWN/REVIEW behavior that never fabricates a proof;
- M39 validation metadata stored during ingestion;
- complete historical regression remains green.

Scope boundary:
M39 is a validation framework, not a claim that arbitrary GATE/JEE questions can
already be solved perfectly. A rule/model is marked PASS or FAIL only when the
required data can be parsed deterministically. Unsupported cases remain UNKNOWN
or REVIEW. This boundary is intentional and is essential for trustworthy paper
generation later in the roadmap.
