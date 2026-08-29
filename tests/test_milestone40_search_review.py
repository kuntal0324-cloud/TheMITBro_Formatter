from src.production_search import ProductionIndex
from src.review_queue import build_review_item
from src.question_quality_score import QualityScore
class C: status="REVIEW"
class R: id="Q1";classification=C()
def test_search_filters():
 i=ProductionIndex();i.add({"id":"Q1","text":"transformer voltage regulation","exam":"GATE_EE","subject":"Electrical Engineering","topic":"Electrical Machines","subtopic":"Transformers","concept":"Transformer equivalent circuit","question_type":"NAT"})
 assert [x["id"] for x in i.search("transformer",exam="GATE_EE")]==["Q1"]
def test_review_queue():
 q=QualityScore(.5,"D",{},("validation_review",))
 assert build_review_item(R(),q).priority==80
