from src.question_versioning import canonical_hash,make_revision
def test_version_hash_stable():
 a={"b":2,"a":1};b={"a":1,"b":2};assert canonical_hash(a)==canonical_hash(b)
def test_revision():
 r=make_revision("Q1",{"x":1},2,"edit","old");assert r.revision==2 and r.parent_sha256=="old"
