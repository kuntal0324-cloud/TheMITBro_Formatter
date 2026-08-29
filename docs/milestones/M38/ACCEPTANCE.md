# M38 Acceptance — Universal Question Intelligence

M38 is the semantic intelligence layer for the compressed M45 roadmap.

It must:
- classify GATE EE Engineering Mathematics and Electrical Engineering;
- classify JEE Mathematics and Physics;
- map question -> topic -> subtopic -> concept;
- recognize MCQ, MSQ and NAT;
- recover marks when explicitly present;
- estimate difficulty from structural complexity rather than a single keyword;
- estimate reasoning depth, calculation load and solving time;
- expose stable syllabus paths;
- expose concept prerequisites and validate an acyclic prerequisite graph;
- place low-confidence/unrecognized questions into review rather than inventing taxonomy;
- store all intelligence in Question Bank ingestion metadata;
- preserve the complete historical regression suite.

M38 estimates difficulty/time heuristically. These values become calibration inputs
for the later real-corpus qualification milestone rather than being represented as
official exam timing data.
