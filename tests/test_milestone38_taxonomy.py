from src.question_intelligence import analyze_question
from src.syllabus_index import syllabus_tree

def test_gate_transformer_taxonomy():
    q=analyze_question("A transformer equivalent circuit is used to calculate voltage regulation.",exam_hint="GATE EE")
    assert q.exam=="GATE_EE"
    assert q.subject=="Electrical Engineering"
    assert q.topic=="Electrical Machines"
    assert q.subtopic=="Transformers"
    assert q.concept=="Transformer equivalent circuit"

def test_jee_math_conic():
    q=analyze_question("Find the tangent to the parabola y^2=4ax.",exam_hint="JEE")
    assert q.subject=="Mathematics"
    assert q.topic=="Coordinate Geometry"
    assert q.subtopic=="Conic sections"

def test_jee_physics_optics():
    q=analyze_question("A convex lens forms an image. Use the lens relation to determine image distance.",exam_hint="JEE")
    assert q.subject=="Physics"
    assert q.topic=="Ray Optics"

def test_syllabus_tree_has_foundations():
    gate=syllabus_tree("GATE_EE")
    jee=syllabus_tree("JEE")
    assert "Electrical Engineering" in gate
    assert "Engineering Mathematics" in gate
    assert "Mathematics" in jee and "Physics" in jee
