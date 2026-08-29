from src.universal_visual_intelligence import understand_visual
def test_coordinates():
 v=understand_visual("On coordinate plane plot A(1,2), B(-3,4).")
 assert [e.position for e in v.entities]==[(1.0,2.0),(-3.0,4.0)]
def test_function():
 v=understand_visual("Plot graph of y=x^2+2*x+1.")
 assert "x^2+2*x+1" in v.properties["expressions"]
def test_geometry():
 v=understand_visual("In triangle ABC, draw the geometric figure.")
 assert len(v.entities)==3 and len(v.relations)==3
def test_fbd():
 v=understand_visual("Draw a free-body diagram showing weight, normal force and friction.")
 assert v.family=="physics" and len(v.entities)>=3
def test_ray():
 v=understand_visual("Draw the ray diagram for an object before a convex lens on the principal axis.")
 assert v.family=="physics" and v.diagram_type=="ray_diagram"
def test_field():
 v=understand_visual("Sketch electric field lines around the charges.")
 assert v.diagram_type=="field_line_diagram"
