from src.question_classifier import classify_question

def test_jee_optics():
    c = classify_question(
        "A thin convex lens forms a real image. Find the focal length.",
        exam_hint="JEE",
    )
    assert c.subject == "Physics"
    assert c.topic == "Optics"

def test_gate_em_fields():
    c = classify_question(
        "Use Gauss law to determine the electric field.",
        exam_hint="GATE EE",
    )
    assert c.subject == "Electrical Engineering"
    assert c.topic == "Electromagnetic Fields"
