from src.question_ingest import ingest
def test_question_bank_visual_structure(tmp_path):
 p=tmp_path/"q.txt";p.write_text("Draw a series circuit with resistor R1 and capacitor C1.",encoding="utf-8")
 r=ingest(p,exam_hint="GATE EE")
 assert r.metadata["visual_intelligence_contract"]=="M37"
 assert r.metadata["visual_structure"]["diagram_type"]=="circuit_diagram"
 assert r.metadata["visual_structure"]["properties"]["topology"]=="series"
 assert r.metadata["requires_visual_review"] is False
