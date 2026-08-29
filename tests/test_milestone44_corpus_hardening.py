from src.corpus_loader import load_builtin_corpus
from src.corpus_qualification import qualify_corpus
def test_m43_remaining_failures_hardened():
 r=qualify_corpus(load_builtin_corpus())
 assert r.pass_rate>=.95
 assert r.failed<=3
