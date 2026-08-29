
from src.question_duplicate_detector import fingerprint
def test_same():
    assert fingerprint("x")==fingerprint("x")
