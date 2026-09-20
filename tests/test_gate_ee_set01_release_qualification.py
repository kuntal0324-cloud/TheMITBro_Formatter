import json

from src.gate_ee_set01_release_qualification import INPUT, OUTPUT, qualify_set01


def test_set01_release_selection_has_exact_all_pass_formatter_evidence():
    result = qualify_set01()
    assert result["status"] == "PASS"
    assert result["question_count"] == result["formatter_pass_count"] == 65
    assert result["formatter_blocked_count"] == 0
    assert [row["position"] for row in result["questions"]] == list(range(1, 66))
    assert len({row["question_id"] for row in result["questions"]}) == 65
    assert all(row["formatter_release_qualification"] == "PASS" for row in result["questions"])


def test_set01_release_evidence_is_reproducible_and_non_authorizing():
    assert json.loads(OUTPUT.read_text(encoding="utf-8")) == qualify_set01()
    result = qualify_set01()
    assert result["release_gate"] == "BLOCKED_PENDING_EXACT_ARTIFACT_RELEASE_AUTHORIZATION"
    assert result["release_authorized"] is False
    assert result["sale_authorized"] is False
    assert INPUT.is_file()

