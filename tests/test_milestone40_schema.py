from src.question_bank_production import promote
from src.question_ingest import ingest
from src.production_schema import validate_production_question
def test_promote_schema(tmp_path):
 p=tmp_path/"q.txt";p.write_text("Find determinant det(A).",encoding="utf-8")
 q=promote(ingest(p,exam_hint="GATE EE"))
 assert q.schema_version=="2.0" and q.revision==1
 assert validate_production_question(q)==[]
 assert q.family_id.startswith("QF-")
