import pytest
from src.visual_structure import VisualEntity,VisualRelation,VisualStructure
from src.universal_visual_intelligence import understand_visual
def test_series_circuit():
 v=understand_visual("Draw a series circuit with voltage source, resistor R1, inductor L1 and capacitor C1.")
 assert v.diagram_type=="circuit_diagram" and len(v.entities)>=4 and len(v.relations)>=3
def test_no_fabricated_connectivity():
 v=understand_visual("The circuit contains resistor R1 and capacitor C1.")
 assert len(v.entities)>=2 and v.relations==() and v.warnings
def test_ir_rejects_dangling():
 with pytest.raises(ValueError):VisualStructure("engineering","circuit_diagram",(VisualEntity("A","R"),),(VisualRelation("A","B","wire"),),confidence=.9).ensure_valid()
