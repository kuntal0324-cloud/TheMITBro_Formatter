from src.question_intelligence import analyze_question, estimate_difficulty

def test_direct_question_is_not_deep():
    q=analyze_question("Find the determinant of a 2 by 2 matrix.",exam_hint="GATE EE")
    assert q.reasoning_depth in {"Direct","Multi-step"}
    assert q.expected_time_seconds >= 45

def test_advanced_multistep_has_more_load():
    easy=estimate_difficulty("Find the resistance.")
    hard=estimate_difficulty("Using the transfer function, determine stability, then calculate gain margin and phase margin from the Bode plot.")
    assert hard[1] > easy[1]
    assert hard[4] >= easy[4]
