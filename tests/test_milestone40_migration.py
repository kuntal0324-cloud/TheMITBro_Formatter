from src.question_migrations import migrate_catalog
def test_migration_preserves_questions():
 old={"schema_version":"1.1","questions":[{"id":"Q1"}]}
 new=migrate_catalog(old)
 assert new["schema_version"]=="2.0" and new["questions"]==old["questions"]
 assert new["production_contract"]=="M40"
