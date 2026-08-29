from src.corpus_loader import load_builtin_corpus
from src.corpus_qualification import qualify_corpus
def test_builtin_hostile_corpus_size_and_domains():
 cases=load_builtin_corpus()
 assert len(cases)>=70
 assert {"Engineering Mathematics","Electrical Engineering","Mathematics","Physics"} <= {c.subject for c in cases}
def test_corpus_pass_rate_is_qualification_gated():
 report=qualify_corpus(load_builtin_corpus())
 assert report.total>=70
 assert report.pass_rate>=0.75
