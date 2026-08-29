from src.contract_registry import final_contract_registry
def test_m1_to_m44_registry_complete_and_frozen():
 rows=final_contract_registry()
 assert len(rows)==44
 assert [r.milestone for r in rows]==list(range(1,45))
 assert all(r.status=="FROZEN" for r in rows)
