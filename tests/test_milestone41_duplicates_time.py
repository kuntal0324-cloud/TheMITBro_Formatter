import pytest
from src.paper_blueprint import PaperBlueprint
from src.mock_paper_generator import generate_mock_paper
def q(i,fam,t=60):
 return {"id":f"Q{i}","text":f"Unique task {i} matrix calculation","exam":"GATE_EE","subject":"Engineering Mathematics","topic":"Linear Algebra",
 "subtopic":"Matrices","concept":"Matrix","question_type":"NAT","marks":1,"quality_score":.9,"family_id":fam,
 "lifecycle_status":"APPROVED","metadata":{"difficulty":"Medium","calculation_load":"High","reasoning_depth":"Direct","expected_time_seconds":t}}
def test_family_duplicate_avoidance():
 bank=[q(1,"F1"),q(2,"F1"),q(3,"F2")]
 p=generate_mock_paper(bank,PaperBlueprint("GATE_EE","M",2))
 assert p.metrics["family_count"]==2
def test_time_budget_impossible():
 with pytest.raises(ValueError):
  generate_mock_paper([q(1,"F1",100),q(2,"F2",100)],PaperBlueprint("GATE_EE","M",2,max_expected_time_seconds=150))
