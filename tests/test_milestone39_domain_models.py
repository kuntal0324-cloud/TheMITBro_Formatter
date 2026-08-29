from src.domain_validation import validate_ohms_law,validate_newton_second_law
def test_ohm_pass():
 assert validate_ohms_law("For a resistor V=10, I=2, R=5.").status=="PASS"
def test_ohm_fail():
 assert validate_ohms_law("For a resistor V=12, I=2, R=5.").status=="FAIL"
def test_newton():
 assert validate_newton_second_law("Using Newton law, F=6, m=2, a=3.").status=="PASS"
