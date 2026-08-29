from src.question_ingest import ingest
def test_m39_metadata(tmp_path):
 p=tmp_path/"q.txt"
 p.write_text("""**Type:** MCQ
**Marks:** 1
For a resistor V=10, I=2, R=5. Which value is the resistance?
A. 2
B. 5
C. 10
D. 20
**Answer:** B
**Solution:** From V=IR, R=10/2. Therefore 5
""",encoding="utf-8")
 r=ingest(p,exam_hint="GATE EE")
 m=r.metadata
 assert m["validation_intelligence_contract"]=="M39"
 assert m["answer_validation_status"]=="PASS"
 assert any(x["model"]=="Ohm law" and x["status"]=="PASS" for x in m["domain_validation_checks"])
 assert m["solution_validation_status"]=="PASS"
