from src.concept_graph import build_concept_graph, prerequisites_for, validate_acyclic

def test_graph_is_acyclic():
    assert validate_acyclic() is True

def test_prerequisite():
    assert "Matrix operations" in prerequisites_for("Determinants and rank")

def test_graph_nonempty():
    assert len(build_concept_graph()) > 20
