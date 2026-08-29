from src.paper_blueprint import PaperBlueprint
from src.mock_paper_qualification import qualify_mock_paper
def item(i,exam,subject,topic,qtype,diff,marks=1,visual=False):
 return {"id":f"{exam}-{i}","text":f"Unique {topic} question {i} with value {i+10}","exam":exam,"subject":subject,
 "topic":topic,"subtopic":"S","concept":topic,"question_type":qtype,"marks":marks,"quality_score":.95,
 "family_id":f"F-{exam}-{i}","lifecycle_status":"APPROVED",
 "metadata":{"difficulty":diff,"calculation_load":"High" if qtype=="NAT" else "Low",
 "reasoning_depth":"Multi-step","expected_time_seconds":90,"diagram_present":visual}}
def test_gate_mock_qualification():
 bank=[]
 for i in range(18):
  bank.append(item(i,"GATE_EE","Electrical Engineering",["Network Theory","Electrical Machines","Power Systems"][i%3],
                   ["MCQ","MSQ","NAT"][i%3],["Easy","Medium","Hard"][i%3],1+(i%2),i%5==0))
 b=PaperBlueprint("GATE_EE","Qualified GATE EE",9,type_counts={"MCQ":2,"MSQ":2,"NAT":2},
  difficulty_counts={"Easy":2,"Medium":2,"Hard":2},visual_min=1,numerical_min=2,conceptual_min=2)
 r=qualify_mock_paper(bank,b)
 assert r.generated and r.deterministic and r.question_count==9
def test_jee_mock_qualification():
 bank=[]
 for i in range(20):
  subject="Mathematics" if i%2==0 else "Physics"
  bank.append(item(i,"JEE",subject,"Calculus" if subject=="Mathematics" else "Mechanics",
                   "MCQ" if i%3 else "NAT",["Easy","Medium","Hard"][i%3],1,i%7==0))
 b=PaperBlueprint("JEE","Qualified JEE",10,subject_counts={"Mathematics":4,"Physics":4},visual_min=1)
 r=qualify_mock_paper(bank,b)
 assert r.generated and r.deterministic
