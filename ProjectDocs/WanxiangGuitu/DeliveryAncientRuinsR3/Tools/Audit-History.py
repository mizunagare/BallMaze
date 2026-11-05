import hashlib
import json
from pathlib import Path
import sys

prior, root = map(Path, sys.argv[1:])
rows = json.loads((prior / "Evidence/manifest.json").read_text(encoding="utf-8-sig"))
original = Path("I:/WGCombat/C1R2-1105-A")
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
errors = []
for row in rows:
    for file, key in ((original / row["sourceRelative"], "sourceSHA256"),
                      (prior / "Evidence" / row["path"], "publishedSHA256")):
        if sha(file) != row[key]:
            errors.append(str(file))
protected = json.loads(Path("I:/WGCombat/C1-1105-A/protected-before.json").read_text(encoding="utf-8-sig"))
changed = [row["path"] for row in protected if sha(Path(row["path"])) != row["sha256"]]
out = root / "Audit"
out.mkdir(exist_ok=True)
(out / "protection.json").write_text(json.dumps(dict(
    r2OriginalAndPublishedPairs=len(rows), r2Mismatches=errors,
    previousProtectedFiles=len(protected), protectedChanges=changed), indent=2), encoding="utf-8")
print(len(rows), "R2 evidence pairs;", len(protected), "protected original files")
if errors or changed:
    raise SystemExit("Protected file mismatch")
