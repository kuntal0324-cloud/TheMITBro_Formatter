from src.question_ingest import ingest

def test_m38_metadata(tmp_path):
    p=tmp_path/"q.txt"
    p.write_text("""**Type:** NAT
**Marks:** 2
For a series RLC circuit, determine the resonant frequency and impedance.""",encoding="utf-8")
    r=ingest(p,exam_hint="GATE EE")
    m=r.metadata
    assert m["question_intelligence_contract"]=="M38"
    assert m["question_type"]=="NAT"
    assert m["marks"]==2
    assert m["concept"]=="Phasor impedance and resonance"
    assert m["syllabus_path"][0]=="GATE_EE"
    assert m["expected_time_seconds"]>0
