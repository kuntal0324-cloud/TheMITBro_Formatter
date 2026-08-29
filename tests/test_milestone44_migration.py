from src.migration_hardening import plan_catalog_migration,validate_migration_plan
def test_migration_preserves_identity_and_count():
 old={"schema_version":"1.1","questions":[{"id":"Q1"},{"id":"Q2"}]}
 p=plan_catalog_migration(old)
 assert validate_migration_plan(p)==[]
 assert p.reversible_snapshot==old
