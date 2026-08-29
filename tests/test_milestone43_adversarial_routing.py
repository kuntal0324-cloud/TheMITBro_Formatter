from src.adversarial_routing import DEFAULT_PROBES,run_probe
def test_adversarial_routing_probes():
 results=[run_probe(p) for p in DEFAULT_PROBES]
 assert all(r.passed for r in results),[(r.name,r.topic,r.subject) for r in results if not r.passed]
