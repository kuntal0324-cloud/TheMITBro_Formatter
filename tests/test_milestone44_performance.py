from src.performance_qualification import qualify_scale
def test_scale_1000_records_is_deterministic():
 records=[]
 for i in range(1000):
  records.append({"id":f"Q{i}","text":f"transformer voltage regulation unique {i}","exam":"GATE_EE",
   "subject":"Electrical Engineering","topic":"Electrical Machines","subtopic":"Transformers",
   "concept":"Transformer","question_type":"NAT"})
 r=qualify_scale(records)
 assert r.records==1000 and r.deterministic
 assert r.index_seconds<5 and r.search_seconds<2 and r.duplicate_probe_seconds<5
