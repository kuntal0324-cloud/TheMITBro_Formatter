from src.question_intelligence import detect_question_type, extract_marks

def test_mcq():
    t="Which of the following is correct?\nA. One\nB. Two\nC. Three\nD. Four"
    assert detect_question_type(t)=="MCQ"

def test_msq():
    assert detect_question_type("One or more options may be correct. Select all valid choices.")=="MSQ"

def test_nat():
    assert detect_question_type("Numerical Answer Type: enter a number.")=="NAT"

def test_marks():
    assert extract_marks("**Marks:** 2") == 2
