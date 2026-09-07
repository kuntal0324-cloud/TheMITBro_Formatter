from pathlib import Path

from src.human_math import humanize_math, has_source_math_markup
from src.question_classifier import classify_question
from src.question_ingest import ingest_many
from src.question_router import route_source_many
from src.question_bank_production import promote


def test_learner_output_hides_source_math_markup():
    source = r"$z=\frac{-b\pm\sqrt{b^2-4ac}}{2a}$ and $\theta_1$"
    rendered = humanize_math(source)
    assert rendered == "z=(-b±√(b²-4ac))/(2a) and θ₁"
    assert not has_source_math_markup(rendered)


def test_gate_ee_syllabus_guards():
    numerical = classify_question("Use the Newton-Raphson numerical method to find a root.", exam_hint="GATE EE")
    assert numerical.status == "REVIEW"
    assert numerical.topic == "Review Required"
    assert "out_of_syllabus:numerical_methods" in numerical.signals

    transform = classify_question("Find the Laplace transform of the signal x(t).", exam_hint="GATE EE")
    assert (transform.subject, transform.topic, transform.status) == (
        "Electrical Engineering", "Signals and Systems", "AUTO"
    )

    series = classify_question("Find the Fourier series coefficient of f(x).", exam_hint="GATE EE")
    assert (series.subject, series.topic, series.status) == (
        "Engineering Mathematics", "Calculus", "AUTO"
    )

    complex_item = classify_question("Use the residue theorem to evaluate the contour integral.", exam_hint="GATE EE")
    assert (complex_item.subject, complex_item.topic, complex_item.status) == (
        "Engineering Mathematics", "Complex Variables", "AUTO"
    )

    pde = classify_question("Solve the partial differential equation for the heat mode.", exam_hint="GATE EE")
    assert (pde.subject, pde.topic, pde.status) == (
        "Engineering Mathematics", "Differential Equations", "AUTO"
    )


def test_mixed_text_is_split_structured_and_routed(tmp_path: Path):
    source = tmp_path / "mixed.txt"
    source.write_text(
        """Question 1. Find the determinant of matrix A.
A. 1
B. 2
C. 3
D. 4
Answer: B
Solution:
Use cofactor expansion.

Question 2. For a signal x(t), determine its Laplace transform.
Answer: 1/s
Solution:
Integrate from zero to infinity.
""",
        encoding="utf-8",
    )
    records = ingest_many(source, exam_hint="GATE EE")
    assert len(records) == 2
    assert records[0].metadata["structured_question"]["options"][0]["label"] == "A"
    assert records[1].classification.topic == "Signals and Systems"
    results = route_source_many(source, root=tmp_path / "bank", exam_hint="GATE EE")
    assert len(results) == 2
    assert all(result.path and result.path.exists() for result in results)


def test_automation_never_self_approves(tmp_path: Path):
    source = tmp_path / "q.txt"
    source.write_text("Find the determinant of matrix A.", encoding="utf-8")
    question = promote(ingest_many(source, exam_hint="GATE EE")[0])
    assert question.lifecycle_status == "REVIEW"
    assert question.metadata["automation_recommendation"] in {"READY_FOR_HUMAN_REVIEW", "REVISE"}
