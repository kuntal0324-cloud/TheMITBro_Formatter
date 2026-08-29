from src.deterministic_build import stable_question_id,build_fingerprint
def test_stable_ids_and_fingerprint():
 h="abcdef"*11
 assert stable_question_id(h)==stable_question_id(h)
 a=build_fingerprint({"b":2,"a":1},[1,2])
 b=build_fingerprint({"a":1,"b":2},[1,2])
 assert a==b
