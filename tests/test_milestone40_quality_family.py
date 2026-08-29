from src.question_ingest import ingest
from src.question_quality_score import score_question
from src.question_family import family_id
def test_quality_and_family(tmp_path):
 p=tmp_path/"q.txt";p.write_text("""**Type:** MCQ
Find determinant det(A).
A. 1
B. 2
C. 3
D. 4
**Answer:** A""",encoding="utf-8")
 r=ingest(p,exam_hint="GATE EE");q=score_question(r)
 assert 0<=q.score<=1 and q.grade in {"A","B","C","D"}
 assert family_id(r).startswith("QF-")
