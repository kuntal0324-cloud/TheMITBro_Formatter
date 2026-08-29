from src.diagram_text_validator import validate_diagram_text
def test_consistent_circuit():
 v={"diagram_type":"circuit_diagram","entities":[{"kind":"resistor","label":"R1"},{"kind":"capacitor","label":"C1"}]}
 assert validate_diagram_text("Draw a resistor and capacitor circuit.",v).status=="PASS"
def test_missing_component():
 v={"diagram_type":"circuit_diagram","entities":[{"kind":"resistor","label":"R1"}]}
 assert validate_diagram_text("Draw a resistor and capacitor circuit.",v).status=="FAIL"
