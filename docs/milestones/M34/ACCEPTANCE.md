# M34 Acceptance — OCR Pipeline Integration

M34 connects the M33 OCR foundation to a real ingestion pipeline.

Acceptance:
- Pillow preprocessing with EXIF correction, grayscale, autocontrast and sharpening.
- TXT/MD lossless ingestion.
- JPG/JPEG/PNG OCR path using Tesseract.
- OCR-confidence gating: images below 0.85 go to review.
- Automatic exam/subject/topic routing through the M32 classifier.
- Exact and near-duplicate detection.
- Catalog validation and filtering.
- Recursive bulk import.
- Full historical regression remains green.

Scope boundary:
M34 does not claim universal mathematical OCR or semantic diagram recognition.
Those remain M35/M36 responsibilities.
