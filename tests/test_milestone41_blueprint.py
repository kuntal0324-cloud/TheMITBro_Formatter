import pytest
from src.paper_blueprint import PaperBlueprint
def test_blueprint_validates():
 b=PaperBlueprint("GATE_EE","Mock",4,total_marks=6,type_counts={"MCQ":2,"NAT":2})
 assert b.validate() is b
def test_impossible_internal_counts_rejected():
 with pytest.raises(ValueError):
  PaperBlueprint("JEE","X",2,difficulty_counts={"Easy":3}).validate()
