from src.diagram_fingerprint import spec_fingerprint

def test_stable_spec_fingerprint():
    a = {"diagram_type":"graph","expressions":["x^2"],"output_path":"a.svg"}
    b = {"output_path":"b.svg","expressions":["x^2"],"diagram_type":"graph"}
    assert spec_fingerprint(a) == spec_fingerprint(b)

def test_different_specs_differ():
    assert spec_fingerprint({"x":1}) != spec_fingerprint({"x":2})
