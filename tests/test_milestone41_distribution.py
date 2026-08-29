from src.paper_blueprint import PaperBlueprint
from src.mock_paper_generator import generate_mock_paper
def mk(i,subject,topic):
 return {"id":f"Q{i}","text":f"Unique question {i} {topic}","exam":"JEE","subject":subject,"topic":topic,"subtopic":"x","concept":"c",
 "question_type":"MCQ","marks":1,"quality_score":.9,"family_id":f"F{i}","lifecycle_status":"APPROVED",
 "metadata":{"difficulty":"Medium","calculation_load":"Low","reasoning_depth":"Direct","expected_time_seconds":60}}
def test_subject_topic_coverage():
 bank=[mk(1,"Mathematics","Calculus"),mk(2,"Mathematics","Algebra"),mk(3,"Physics","Mechanics"),mk(4,"Physics","Optics")]
 b=PaperBlueprint("JEE","JEE Mock",4,subject_counts={"Mathematics":2,"Physics":2},topic_counts={"Calculus":1,"Optics":1})
 p=generate_mock_paper(bank,b)
 assert p.metrics["subjects"]["Mathematics"]==2
 assert p.metrics["subjects"]["Physics"]==2
