# M42 Acceptance - Professional Publishing Engine

M42 turns an M41-selected `PaperSpec` into a versioned, release-ready publication.

Acceptance requires professional Markdown, self-contained print HTML, deterministic
paper PDF, answer/solution publications, equation/matrix/table preservation,
structured diagram publication, pagination, sections/instructions, paper identity
and semantic version/revision metadata, identity-aware headers/footers, SHA-256
release manifest, machine-readable paper spec, and a single release ZIP.

M42 builds on the existing M17-M21 rendering stack rather than replacing it.
The SVG composition layer remains the source of truth for paper-page layout.

Boundary: detailed solutions are published only when supplied by the validated
question record. M42 does not fabricate missing solutions. M43 will qualify the
complete pipeline using realistic/adversarial GATE/JEE corpora and visual output.
