from src.solution_validation import validate_solution
from src.diagram_text_validator import validate_diagram_text
from src.question_quality_validator import detect_quality_issues
def test_solution_final_matches_answer():
 t="""A. 2
B. 4
C. 6
D. 8
**Answer:** B
**Solution:** Compute 2+2. Therefore 4"""
 assert validate_solution(t).status=="PASS"

def test_standard_final_answer_marker_validates_mcq_key():
 t="""A. 2
B. 4
C. 6
D. 8
**Answer:** B
**Solution:** Compute 2+2.
Final answer: B"""
 assert validate_solution(t).status=="PASS"

def test_standard_final_answer_marker_validates_msq_keys():
 t="""A. True
B. True
C. False
D. True
**Answer:** A, B, D
**Solution:** Check each statement independently.
Final answer: A, B, D"""
 assert validate_solution(t).status=="PASS"

def test_last_final_answer_marker_controls_validation():
 t="""A. 2
B. 4
C. 6
D. 8
**Answer:** B
**Solution:** An intermediate attempt gives 6. Therefore 6.
Final answer: B"""
 assert validate_solution(t).status=="PASS"

def test_wrong_standard_final_answer_key_fails():
 t="""A. 2
B. 4
C. 6
D. 8
**Answer:** B
**Solution:** Compute 2+2.
Final answer: C"""
 assert validate_solution(t).status=="FAIL"
def test_impossible_operation():
 q=detect_quality_issues("Calculate 1/0 by divide by zero.","NAT")
 assert q.status=="FAIL"
def test_no_task_review():
 assert detect_quality_issues("A resistor of 5 ohm is connected.","UNSPECIFIED").status=="REVIEW"

def test_text_only_question_has_no_diagram_review_blocker():
 assert validate_diagram_text("Calculate 2+2.",None).status=="PASS"

def test_missing_referenced_diagram_still_requires_review():
 assert validate_diagram_text("Calculate the value shown in the figure below.",None).status=="UNKNOWN"
