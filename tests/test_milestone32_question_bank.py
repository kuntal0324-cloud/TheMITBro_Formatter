from pathlib import Path
import json

from src.question_classifier import classify_question
from src.question_ingest import ingest
from src.question_bank_store import QuestionBankStore


def test_gate_matrix_question_routes_to_matrices():
    c = classify_question(
        r"For A = [[1,2],[3,4]], find the determinant and eigenvalues.",
        exam_hint="GATE EE",
    )
    assert c.exam == "GATE_EE"
    assert c.subject == "Engineering Mathematics"
    assert c.topic == "Matrices"
    assert c.status == "AUTO"
    assert c.confidence >= 0.70


def test_jee_physics_routes_to_electrodynamics():
    c = classify_question(
        "Find the electric field and electric potential due to a point charge.",
        exam_hint="JEE",
    )
    assert c.exam == "JEE"
    assert c.subject == "Physics"
    assert c.topic == "Electrodynamics"


def test_ambiguous_question_goes_to_review():
    c = classify_question(
        "Find the mean and variance of a random variable using a matrix representation.",
    )
    assert c.status == "REVIEW"
    assert c.topic == "Review Required"


def test_text_ingestion_and_routing(tmp_path: Path):
    source = tmp_path / "q.txt"
    source.write_text(
        "For A = [[1,2],[3,4]], find det(A).",
        encoding="utf-8",
    )
    record = ingest(source, exam_hint="GATE EE")
    out = QuestionBankStore(tmp_path / "question_bank").add(record, source)

    assert out.exists()
    assert "Engineering_Mathematics" in str(out)
    assert "Matrices" in str(out)

    catalog = json.loads(
        (tmp_path / "question_bank/catalog.json").read_text(encoding="utf-8")
    )
    assert len(catalog["questions"]) == 1


def test_duplicate_source_is_idempotent(tmp_path: Path):
    source = tmp_path / "q.md"
    source.write_text("Solve the differential equation y' + y = 0.", encoding="utf-8")

    bank = QuestionBankStore(tmp_path / "question_bank")
    first = bank.add(ingest(source, exam_hint="GATE EE"), source)
    second = bank.add(ingest(source, exam_hint="GATE EE"), source)

    assert first == second


def test_unsupported_input_is_rejected(tmp_path: Path):
    source = tmp_path / "q.pdf"
    source.write_text("not supported", encoding="utf-8")
    try:
        ingest(source)
    except ValueError as exc:
        assert "Unsupported" in str(exc)
    else:
        raise AssertionError("Expected unsupported input failure")
