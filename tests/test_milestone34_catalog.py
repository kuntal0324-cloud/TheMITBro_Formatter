import json
from pathlib import Path
from src.question_catalog import load_catalog, search_catalog

def test_empty_catalog_contract(tmp_path: Path):
    # M34 intentionally preserves the M33 empty-catalog contract.
    assert load_catalog(tmp_path) == {"questions": []}

def test_search_catalog(tmp_path: Path):
    payload = {
        "schema_version": "1.1",
        "contract": "M34",
        "questions": [{
            "id": "QB-1",
            "text": "matrix determinant",
            "classification": {
                "exam": "GATE_EE",
                "subject": "Engineering Mathematics",
                "topic": "Matrices"
            }
        }]
    }
    (tmp_path/"catalog.json").write_text(json.dumps(payload), encoding="utf-8")
    hits = search_catalog(tmp_path, topic="Matrices")
    assert [x["id"] for x in hits] == ["QB-1"]
