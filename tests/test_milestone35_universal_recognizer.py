from src.universal_math_recognizer import recognize_question_math

def test_calculus_recognition():
    r = recognize_question_math("Evaluate ∫ x² dx")
    assert "calculus" in r.features
    assert r.math_confidence == 1.0

def test_vector_calculus_recognition():
    r = recognize_question_math("Find ∇ × A")
    assert "vector_calculus" in r.features
