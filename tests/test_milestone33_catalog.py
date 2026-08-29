
from src.question_catalog import load_catalog
def test_empty(tmp_path):
    assert load_catalog(tmp_path)=={"questions":[]}
