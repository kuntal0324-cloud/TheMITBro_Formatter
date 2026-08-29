from __future__ import annotations
from dataclasses import dataclass,asdict
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json,shutil,uuid

@dataclass(frozen=True)
class RecoveryPoint:
    transaction_id:str
    created_at:str
    files:tuple[dict,...]
    status:str="PREPARED"
    def to_dict(self):return asdict(self)

def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
    return h.hexdigest()

def create_recovery_point(paths,backup_root):
    tid=uuid.uuid4().hex
    base=Path(backup_root)/tid;base.mkdir(parents=True,exist_ok=False)
    entries=[]
    for src in map(Path,paths):
        if not src.exists():continue
        target=base/src.name
        shutil.copy2(src,target)
        entries.append({"source":str(src),"backup":str(target),"sha256":sha256_file(target)})
    rp=RecoveryPoint(tid,datetime.now(timezone.utc).replace(microsecond=0).isoformat(),tuple(entries))
    (base/"recovery.json").write_text(json.dumps(rp.to_dict(),indent=2)+"\n",encoding="utf-8")
    return rp

def restore_recovery_point(point):
    for item in point.files:
        backup=Path(item["backup"])
        if not backup.exists() or sha256_file(backup)!=item["sha256"]:
            raise IOError("Recovery backup integrity failure.")
        target=Path(item["source"]);target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(backup,target)
    return True
