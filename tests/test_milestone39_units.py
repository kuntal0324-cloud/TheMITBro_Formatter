from src.unit_dimensions import compare_units,dimension_of_unit
def test_voltage_dimension():
 assert compare_units("V","V").status=="PASS"
def test_incompatible_dimensions():
 assert compare_units("V","A").status=="FAIL"
def test_ohm_known():
 assert dimension_of_unit("ohm") is not None
