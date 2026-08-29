from src.final_baseline import audit_repository
def test_final_baseline_audit_clean():
 a=audit_repository(".")
 assert a.version=="2.0.0"
 assert a.required_docs_present
 assert a.m44_certified
 assert a.corpus_pass_rate==1.0
 assert not a.errors
 assert len(a.baseline_sha256)==64
