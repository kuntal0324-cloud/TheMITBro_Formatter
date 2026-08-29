import pytest
from src.paper_blueprint import PaperBlueprint
from src.mock_paper_generator import generate_mock_paper
def test_quality_and_approval_filter():
 bank=[{"id":"Q1","text":"x unique","exam":"GATE_EE","subject":"EE","topic":"T","subtopic":"S","concept":"C","question_type":"MCQ","marks":1,
 "quality_score":.5,"family_id":"F1","lifecycle_status":"REVIEW","metadata":{"difficulty":"Easy","calculation_load":"Low","reasoning_depth":"Direct","expected_time_seconds":50}}]
 with pytest.raises(ValueError):
  generate_mock_paper(bank,PaperBlueprint("GATE_EE","M",1,min_quality_score=.8,approved_only=True))
