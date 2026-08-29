# TheMITbro Question Bank — M32

The question bank is a structured ingestion and routing layer on top of
TheMITbro Formatter v1.0.0.

## Input

Accepted source types:

- `.txt`
- `.md`
- `.jpg`
- `.jpeg`

A question may be imported with:

```bash
python scripts/m32_import_question.py path/to/question.txt
```

or:

```bash
python scripts/m32_import_question.py path/to/question.jpg --exam "GATE EE"
```

## Automatic routing

The importer:

1. reads text directly or OCRs an image;
2. normalizes whitespace without rewriting mathematical meaning;
3. detects exam/subject/topic using a deterministic taxonomy;
4. computes a confidence score;
5. writes high-confidence questions into the correct `by_exam/<exam>/<subject>/<topic>/` folder;
6. sends low-confidence questions to `question_bank/review/` instead of guessing;
7. records the original source SHA-256 and ingestion metadata in `catalog.json`.

The original image is preserved under `question_bank/assets/` when an image
source is imported.

## Important design rule

Automatic classification must be conservative. A low-confidence question is
**not** silently assigned to a random topic. It enters the review queue.

## Storage

```text
question_bank/
├── catalog.json
├── README.md
├── assets/
├── review/
└── by_exam/
    ├── GATE_EE/
    ├── JEE/
    └── GENERAL/
```
