from src.math_ocr_normalizer import recognize_math

def test_unicode_math_normalization():
    r = recognize_math("∫ x² dx ≤ ∞")
    assert r.confidence == 1.0
    assert r"\leq" in r.normalized
    assert r"\infty" in r.normalized
    assert "^{2}" in r.normalized

def test_matrix_and_determinant_features():
    r = recognize_math("For A=[[1,2],[3,4]], find det(A)")
    assert "matrix" in r.features
    assert "determinant" in r.features
    assert r"\mathrm{det}" in r.normalized
