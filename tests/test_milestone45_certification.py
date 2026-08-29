from src.final_certification import certify_v2
def test_v2_final_certification_ready():
 c=certify_v2(".")
 assert c.version=="2.0.0"
 assert c.contracts_frozen==44
 assert c.corpus_passed==c.corpus_total==72
 assert c.corpus_pass_rate==1.0
 assert c.ready_for_real_content
 assert c.architecture_frozen
