from pathlib import Path
import json

from src.gate_ee_batch_qualification import qualify_batch
from src.question_classifier import classify_question
from src.question_quality_validator import detect_quality_issues


JSONL = Path("input/gate_ee_batch_003/BATCH_003_GENERAL_APTITUDE.jsonl")
HANDOFF = Path("input/gate_ee_batch_003/BATCH_003_FORMATTER_V2_HANDOFF.json")
EVIDENCE = Path("output/gate_ee_batch_003/FORMATTER_V2_QUALIFICATION.json")


def test_batch003_strict_formatter_qualification_passes_all_records():
    result = qualify_batch(JSONL, HANDOFF)
    assert result["batch_id"] == "BATCH_003"
    assert result["domain"] == "General Aptitude"
    assert result["status"] == "PASS"
    assert result["question_count"] == 20
    assert result["formatter_pass_count"] == 20
    assert result["formatter_review_count"] == 0
    assert result["invalid_count"] == 0
    assert all(row["formatter_qualification"] == "PASS" for row in result["questions"])


def test_batch003_covers_the_four_official_general_aptitude_routes():
    result = qualify_batch(JSONL, HANDOFF)
    routes = {row["classification"]["topic"] for row in result["questions"]}
    assert routes == {
        "Verbal Aptitude",
        "Quantitative Aptitude",
        "Analytical Aptitude",
        "Spatial Aptitude",
    }
    assert all(row["classification"]["subject"] == "General Aptitude" for row in result["questions"])
    assert all(row["classification"]["status"] == "AUTO" for row in result["questions"])


def test_standard_gate_prompt_forms_are_detected_as_tasks():
    prompts = (
        "Enter the net percentage increase.",
        "The word qualified most nearly means",
        "The number of valid sequences is",
        "Under the rule, 11 is paired with",
        "Its final direction is",
    )
    for prompt in prompts:
        assert detect_quality_issues(prompt).status == "PASS"


def test_spatial_aptitude_has_an_independent_formatter_route():
    result = classify_question(
        "In a spatial aptitude paper folding task, determine the result after mirroring.",
        exam_hint="GATE_EE",
    )
    assert (result.subject, result.topic, result.status) == (
        "General Aptitude", "Spatial Aptitude", "AUTO"
    )


def test_batch003_committed_evidence_is_reproducible():
    reproduced = json.loads(json.dumps(qualify_batch(JSONL, HANDOFF)))
    assert json.loads(EVIDENCE.read_text(encoding="utf-8")) == reproduced


def test_batch003_remains_blocked_pending_named_human_review():
    result = qualify_batch(JSONL, HANDOFF)
    assert result["paper_eligible_count"] == 0
    assert result["independent_human_review_required"] is True
    assert result["release_gate"] == "BLOCKED"
