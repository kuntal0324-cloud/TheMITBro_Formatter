from pathlib import Path
def test_historical_contract_markers_preserved():
 text=Path("src/question_ingest.py").read_text(encoding="utf-8")
 for marker in ['"ingestion_contract": "M35"','"diagram_contract": "M36"',
                '"visual_intelligence_contract": "M37"',
                '"question_intelligence_contract": "M38"',
                '"validation_intelligence_contract": "M39"']:
  assert marker in text
