from src.domain_validation import run_domain_checks
from src.question_classifier import classify_question
from src.question_intelligence import analyze_question
from src.gate_ee_batch_qualification import qualify_batch
from src.question_quality_validator import detect_quality_issues
import hashlib
import json


def test_descriptive_network_text_does_not_run_partial_identity_models():
    checks = run_domain_checks(
        "A resistor network has a Thevenin voltage and maximum power transfer."
    )
    assert checks == ()


def test_explicit_ohm_identity_is_still_verified():
    checks = run_domain_checks("For a resistor, V=10, I=2 and R=5.")
    assert len(checks) == 1
    assert checks[0].model == "Ohm law"
    assert checks[0].status == "PASS"


def test_electric_circuits_classifier_covers_passive_and_transient_content():
    passive = classify_question(
        "A series capacitor and inductor network has stored energy.",
        exam_hint="GATE_EE",
    )
    transient = classify_question(
        "For an RC network, determine the capacitor time constant and initial value.",
        exam_hint="GATE_EE",
    )
    for result in (passive, transient):
        assert result.subject == "Electrical Engineering"
        assert result.topic == "Electric Circuits"
        assert result.status == "AUTO"


def test_electric_circuits_taxonomy_covers_two_port_and_three_phase_content():
    two_port = analyze_question(
        "For a two-port network with z-parameter data, find its input impedance.",
        exam_hint="GATE_EE",
    )
    three_phase = analyze_question(
        "A balanced three-phase star-connected load has a specified line voltage.",
        exam_hint="GATE_EE",
    )
    for result in (two_port, three_phase):
        assert result.subject == "Electrical Engineering"
        assert result.topic == "Electric Circuits"
        assert result.review_required is False


def test_text_defined_resistor_problem_does_not_invent_missing_diagram_gate(tmp_path):
    source = tmp_path / "batch.jsonl"
    question = {
        "id": "TMB-GATE-EE-NT-999", "exam": "GATE_EE",
        "subject": "Electrical Engineering", "topic": "Electric Circuits",
        "subtopic": "Circuit Laws and Analysis", "concept": "KCL and KVL",
        "difficulty": "Easy", "type": "MCQ", "marks": 1,
        "estimated_time_seconds": 60,
        "stem": "Using KCL, determine the current in a text-defined resistor network.",
        "options": ["1 A", "2 A", "3 A", "4 A"], "answer": "A",
        "solution": "The stated KCL equation gives the required current.\nFinal answer: A",
        "diagram": None, "family_id": "TEST-NT-999", "revision": 1,
        "status": "DRAFT", "provenance": {"originality": "ORIGINAL_THEMITBRO"},
        "review": {},
    }
    source.write_text(json.dumps(question) + "\n", encoding="utf-8")
    handoff = tmp_path / "handoff.json"
    handoff.write_text(json.dumps({
        "formatter_required_version": "2.0.0",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "question_count": 1,
    }), encoding="utf-8")
    result = qualify_batch(source, handoff)
    contract = result["questions"][0]["diagram_contract"]
    assert contract == {
        "declared": False,
        "explicitly_referenced": False,
        "review_required": False,
    }


def test_select_is_a_valid_multiple_select_instruction():
    result = detect_quality_issues(
        "Select every correct statement; one or more options may be correct.",
        "MSQ",
    )
    assert result.status == "PASS"
