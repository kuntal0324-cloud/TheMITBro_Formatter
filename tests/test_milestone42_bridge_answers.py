from types import SimpleNamespace
from src.mock_paper_bridge import to_paper_spec

def test_m41_bridge_preserves_answers_solutions():
    g=SimpleNamespace(title='M',exam='GATE_EE',blueprint={'duration_minutes':10,'total_marks':1},metrics={},questions=({'id':'Q1','subject':'EE','topic':'T','concept':'C','marks':1,'text':'Question?\nA. 1\nB. 2\n**Answer:** B\n**Solution:** Therefore 2'},))
    p=to_paper_spec(g)
    assert p.questions[0].metadata['answer']=='B'
    assert 'Therefore 2' in p.questions[0].metadata['solution']
