# M36 Acceptance — Mathematical & Electrical Engineering Diagram Intelligence

M36 unifies the previously separate mathematical and engineering diagram
subsystems into a Question Bank visual-intelligence layer.

Acceptance:
- Mathematical diagram detection: coordinate geometry, graph/function plot,
  geometry, probability tree, Venn, number line, statistical plot, vectors.
- Electrical Engineering detection: circuits, phasors, control/block/signal
  diagrams, waveforms, transformer equivalent circuits, motor diagrams,
  logic circuits and network diagrams.
- Existing mathematical/engineering generators remain the rendering backend.
- Diagram metadata is attached to Question Bank records.
- Stable diagram-spec fingerprints support future duplicate detection/search.
- Image uploads receive conservative line-structure screening.
- Full historical regression remains green.

Safety/accuracy boundary:
M36 does not claim computer-vision-level semantic reconstruction of arbitrary
diagram pixels. OCR/text semantics and structured diagram data remain the
authoritative sources. Unknown topology is not fabricated.
