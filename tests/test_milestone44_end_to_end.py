from pathlib import Path
from src.paper_blueprint import PaperBlueprint
from src.end_to_end_platform import build_end_to_end
def test_complete_input_to_release_pipeline(tmp_path):
 src=tmp_path/"input";src.mkdir()
 questions=[
 """**Type:** MCQ
**Marks:** 1
A resistor circuit uses Ohm law. Which relation is correct?
A. V=IR
B. V=I/R
C. V=R/I
D. V=I+R
**Answer:** A""",
 """**Type:** NAT
**Marks:** 1
A transformer has turns ratio 10. Determine secondary voltage for 100 V primary. Numerical Answer Type: enter a number.""",
 """**Type:** MCQ
**Marks:** 1
For a control system transfer function G(s)=1/(s+1), which statement is correct?
A. Stable first order
B. Unstable
C. No pole
D. Infinite gain
**Answer:** A""",
 ]
 for i,q in enumerate(questions,1):(src/f"q{i}.txt").write_text(q,encoding="utf-8")
 b=PaperBlueprint("GATE_EE","M44 E2E",3,total_marks=3,deterministic_seed="m44")
 r=build_end_to_end(src,tmp_path/"out",b,exam_hint="GATE EE")
 assert r.imported==3 and r.failed==0
 assert Path(r.release_zip).is_file()
 assert r.bank_integrity["valid"] and r.release_integrity["valid"]
 assert (tmp_path/"out"/"end-to-end-manifest.json").is_file()
