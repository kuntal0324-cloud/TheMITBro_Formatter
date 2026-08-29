from src.solution_validation import validate_solution
from src.question_quality_validator import detect_quality_issues
def test_solution_final_matches_answer():
 t="""A. 2
B. 4
C. 6
D. 8
**Answer:** B
**Solution:** Compute 2+2. Therefore 4"""
 assert validate_solution(t).status=="PASS"
def test_impossible_operation():
 q=detect_quality_issues("Calculate 1/0 by divide by zero.","NAT")
 assert q.status=="FAIL"
def test_no_task_review():
 assert detect_quality_issues("A resistor of 5 ohm is connected.","UNSPECIFIED").status=="REVIEW"
