from src.paper_blueprint import PaperBlueprint
from src.mock_paper_generator import generate_mock_paper
from src.mock_paper_bridge import to_paper_spec
def test_bridge_to_existing_renderer_ir():
 bank=[{"id":"Q1","text":"Which is correct?\nA. One\nB. Two\nC. Three\nD. Four","exam":"GATE_EE","subject":"Electrical Engineering","topic":"Networks",
 "subtopic":"x","concept":"c","question_type":"MCQ","marks":1,"quality_score":.9,"family_id":"F1","lifecycle_status":"APPROVED",
 "metadata":{"difficulty":"Easy","calculation_load":"Low","reasoning_depth":"Direct","expected_time_seconds":60}}]
 g=generate_mock_paper(bank,PaperBlueprint("GATE_EE","Mock",1,total_marks=1,duration_minutes=10))
 p=to_paper_spec(g)
 assert p.exam=="GATE_EE" and len(p.questions)==1 and len(p.questions[0].options)==4
