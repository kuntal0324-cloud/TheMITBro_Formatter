from src.corpus_loader import load_builtin_corpus
from src.corpus_adversary import deterministic_noise,hostile_variants
from src.corpus_qualification import qualify_case
def test_noise_deterministic():
 c=load_builtin_corpus()[0]
 assert deterministic_noise(c.text,c.case_id,.2)==deterministic_noise(c.text,c.case_id,.2)
def test_hostile_variant_pipeline_survives():
 cases=load_builtin_corpus()[:12]
 surviving=0
 for c in cases:
  for kind,text in hostile_variants(c):
   if qualify_case(c,text).classification_ok:surviving+=1
 assert surviving>=24
