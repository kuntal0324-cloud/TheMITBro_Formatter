from src.diagram_intelligence import analyze_diagram_text, generate_detected_diagram

def test_coordinate_geometry_detection():
    d = analyze_diagram_text("On the coordinate plane plot points A(1,2) and B(3,4).")
    assert d.present
    assert d.family == "mathematical"
    assert d.diagram_type == "coordinate_geometry"

def test_function_plot_detection_and_generation():
    d = analyze_diagram_text("Plot the function f(x)=x^2 on the graph.")
    assert d.diagram_type in {"function_plot", "graph"}
    result = generate_detected_diagram("Plot the function f(x)=x^2.")
    assert result["svg"].startswith("<svg")
