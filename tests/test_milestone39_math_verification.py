from src.math_verification import verify_symbolic,verify_numeric
def test_symbolic_identity():
 assert verify_symbolic("(x+1)^2","x^2+2*x+1").status=="PASS"
def test_symbolic_failure():
 assert verify_symbolic("x+1","x+2").status=="FAIL"
def test_numeric_tolerance():
 assert verify_numeric("3.1415926","3.14159265",rel_tol=1e-6).status=="PASS"
