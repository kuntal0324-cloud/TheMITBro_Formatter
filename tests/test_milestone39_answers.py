from src.answer_validation import validate_answer_key,validate_option_set,verify_answer_against_expected
def sample():
 return """Which is correct?
A. 2
B. 4
C. 6
D. 8
**Answer:** B"""
def test_mcq_key():
 assert validate_answer_key(sample(),"MCQ").status=="PASS"
def test_duplicate_options():
 assert validate_option_set({"A":"2","B":"2"},"MCQ").status=="FAIL"
def test_independent_expected():
 assert verify_answer_against_expected(sample(),"4").status=="PASS"
