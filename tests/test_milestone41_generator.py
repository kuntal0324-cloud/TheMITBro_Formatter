from src.paper_blueprint import PaperBlueprint
from src.mock_paper_generator import generate_mock_paper
def item(i,topic,difficulty,qtype,marks,calc="Low",visual=False):
 return {"id":f"Q{i}","text":f"Question {i} about {topic} unique{i}","exam":"GATE_EE","subject":"Electrical Engineering",
 "topic":topic,"subtopic":"S","concept":topic,"question_type":qtype,"marks":marks,"quality_score":.95,
 "family_id":f"F{i}","lifecycle_status":"APPROVED","metadata":{"difficulty":difficulty,"calculation_load":calc,
 "reasoning_depth":"Direct","expected_time_seconds":90,"diagram_present":visual}}
def bank():
 return [item(1,"Machines","Easy","MCQ",1),item(2,"Machines","Medium","NAT",2,"High"),
 item(3,"Networks","Medium","MCQ",1,"Low",True),item(4,"Control","Hard","NAT",2,"High"),
 item(5,"Power","Easy","MCQ",1),item(6,"Signals","Hard","MSQ",2,"Moderate",True)]
def test_balanced_generation():
 b=PaperBlueprint("GATE_EE","Mock",4,total_marks=6,difficulty_counts={"Easy":1,"Medium":1,"Hard":1},
 type_counts={"MCQ":1,"NAT":1},conceptual_min=1,numerical_min=1,visual_min=1,max_expected_time_seconds=500)
 p=generate_mock_paper(bank(),b)
 assert len(p.question_ids)==4 and p.metrics["total_marks"]==6
 assert p.metrics["visual_count"]>=1 and p.validation["valid"]
def test_deterministic():
 b=PaperBlueprint("GATE_EE","Mock",3,deterministic_seed="abc")
 assert generate_mock_paper(bank(),b).question_ids==generate_mock_paper(bank(),b).question_ids
