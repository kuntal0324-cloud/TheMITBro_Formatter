from src.scientific_notation_normalizer import normalize_scientific_notation

def test_electrical_notation():
    s = normalize_scientific_notation("Z = 10 + j5 ohm")
    assert r"\mathrm{j}" in s
    assert r"\Omega" in s

def test_phasor_degree_notation():
    s = normalize_scientific_notation("V = 230∠30°")
    assert r"30^{\circ}" in s
