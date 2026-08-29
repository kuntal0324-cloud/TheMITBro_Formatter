from src.diagram_intelligence import analyze_diagram_text, generate_detected_diagram

def test_circuit_detection():
    d = analyze_diagram_text("Draw a circuit with a voltage source, resistor and capacitor.")
    assert d.family == "engineering"
    assert d.diagram_type == "circuit_diagram"
    assert d.confidence >= 0.8

def test_phasor_detection():
    d = analyze_diagram_text("Draw the phasor diagram for V=220∠30 and I=10∠-20.")
    assert d.diagram_type == "phasor_diagram"

def test_transformer_detection():
    d = analyze_diagram_text("Draw the transformer equivalent circuit with R1, X1 and R2'.")
    assert d.diagram_type == "transformer_equivalent_circuit"

def test_control_system_detection():
    d = analyze_diagram_text("Draw the feedback control system block diagram with transfer function G(s).")
    assert d.diagram_type == "control_system_diagram"

def test_waveform_detection():
    d = analyze_diagram_text("Sketch the PWM waveform with 50 percent duty cycle.")
    assert d.diagram_type == "waveform"
