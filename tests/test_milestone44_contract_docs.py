from pathlib import Path
def test_historical_docs_permanently_preserved():
 required=["docs/ROADMAP.md","docs/ARCHITECTURE.md","docs/FORMAT_SPECIFICATION.md","docs/RELEASE_PROCESS.md"]
 assert all(Path(x).is_file() for x in required)
