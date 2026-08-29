from src.question_intelligence import analyze_question

def test_unknown_question_routes_to_review():
    q=analyze_question("Determine the answer from the information given.",exam_hint="JEE")
    assert q.review_required is True
    assert q.topic=="Review Required"
