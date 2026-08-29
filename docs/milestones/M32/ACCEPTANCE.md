# M32 — Question Bank Ingestion & Automatic Routing

## Goal

Turn TheMITbro Formatter v1.0.0 into a question-bank ingestion layer that can
accept text or JPG/JPEG sources and automatically route each question to its
exam, subject, and topic.

## Safety of classification

Automatic routing is conservative. Questions with no reliable classification
or competing classifications are sent to `question_bank/review/` rather than
being silently misclassified.

## Requirements

- text ingestion
- JPG/JPEG OCR ingestion
- source SHA-256 identity
- idempotent duplicate prevention
- explicit exam/subject/topic taxonomy
- confidence score
- review queue
- original image preservation
- machine-readable catalog
- deterministic routing rules
