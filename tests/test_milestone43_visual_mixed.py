from src.corpus_loader import load_builtin_corpus
from src.corpus_qualification import qualify_case
def test_mixed_diagram_cases_detect_visuals():
 cases=[c for c in load_builtin_corpus() if "diagram" in c.tags]
 results=[qualify_case(c) for c in cases]
 assert len(results)>=8
 assert sum(r.visual_ok for r in results)/len(results)>=.75
