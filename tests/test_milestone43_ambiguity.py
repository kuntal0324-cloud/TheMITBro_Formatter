from src.question_quality_validator import detect_quality_issues
def test_ambiguous_and_impossible_are_not_silently_accepted():
 assert detect_quality_issues("The data are insufficient; cannot be determined.","UNSPECIFIED").status=="REVIEW"
 assert detect_quality_issues("Calculate 1/0 by divide by zero.","NAT").status=="FAIL"
