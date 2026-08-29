from src.question_duplicate_detector import fingerprint, find_duplicate, similarity

def test_normalized_fingerprint():
    assert fingerprint("Find  det(A)") == fingerprint("find det(A)")

def test_exact_duplicate():
    d = find_duplicate("Find det(A).", [{"id": "QB-1", "text": "find det(A)."}])
    assert d.status == "DUPLICATE"
    assert d.matched_id == "QB-1"

def test_similarity_range():
    s = similarity("matrix determinant", "matrix rank")
    assert 0 <= s <= 1
