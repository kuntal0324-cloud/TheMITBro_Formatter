from src.diagram_taxonomy import (
    MATHEMATICAL_DIAGRAMS,
    ELECTRICAL_ENGINEERING_DIAGRAMS,
    SUPPORTED_DIAGRAMS,
)

def test_foundation_families_present():
    for name in (
        "coordinate_geometry","function_plot","circuit_diagram",
        "phasor_diagram","transformer_equivalent_circuit",
        "motor_diagram","control_system_diagram","waveform"
    ):
        assert name in SUPPORTED_DIAGRAMS
    assert len(MATHEMATICAL_DIAGRAMS) >= 8
    assert len(ELECTRICAL_ENGINEERING_DIAGRAMS) >= 10
