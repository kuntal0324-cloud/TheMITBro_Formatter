from src.math_segmenter import segment_math

def test_segments_latex_and_matrix():
    text = r"Given $x^2+1=0$ and A=[[1,2],[3,4]], determine the roots."
    segments = segment_math(text)
    kinds = {s.kind for s in segments}
    assert "inline_latex" in kinds
    assert "matrix_literal" in kinds
