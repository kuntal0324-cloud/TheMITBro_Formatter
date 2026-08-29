from __future__ import annotations
from dataclasses import dataclass,asdict
from copy import deepcopy
from .question_migrations import migrate_catalog

@dataclass(frozen=True)
class MigrationPlan:
    source_version:str
    target_version:str
    before_count:int
    after_count:int
    id_preserved:bool
    reversible_snapshot:dict
    migrated:dict
    def to_dict(self):return asdict(self)

def plan_catalog_migration(data,target="2.0"):
    before=deepcopy(data)
    migrated=migrate_catalog(data,target)
    old_ids=[q.get("id") for q in before.get("questions",[])]
    new_ids=[q.get("id") for q in migrated.get("questions",[])]
    return MigrationPlan(
        str(before.get("schema_version","1.1")),target,len(old_ids),len(new_ids),
        old_ids==new_ids,before,migrated
    )

def validate_migration_plan(plan):
    errors=[]
    if plan.before_count!=plan.after_count:errors.append("question_count_changed")
    if not plan.id_preserved:errors.append("question_ids_changed")
    if plan.migrated.get("schema_version")!=plan.target_version:errors.append("target_version_not_applied")
    return errors
