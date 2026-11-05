import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

source, root = map(Path, sys.argv[1:])
base = "dff9e0971bf101ea70ec854f559ae5ca22f824c7"
def git(*args):
    return subprocess.check_output(["git", "-C", str(source), *args])
if git("diff", "--name-only", base, "--", "Assets", "Packages", "ProjectSettings"):
    raise ValueError("reference checkout product does not match frozen base")
names = sorted(set(git("ls-files", "-z", "--", "Assets", "Packages", "ProjectSettings").decode().split("\0")) - {""})
if not names:
    raise ValueError("empty product inventory")
items = []
for name in names:
    path = source / name
    if not path.is_file() or path.is_symlink():
        raise ValueError(name)
    raw = path.read_bytes()
    if raw.startswith(b"version https://git-lfs.github.com/spec/v1"):
        raise ValueError(f"unmaterialized LFS input {name}")
    digest = hashlib.sha256(raw).hexdigest()
    for label in ("ProjectA", "ProjectB"):
        destination = root / label / name
        if destination.exists():
            raise FileExistsError(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)
        if hashlib.sha256(destination.read_bytes()).hexdigest() != digest:
            raise ValueError(destination)
    items.append(dict(path=name, sha256=digest, bytes=len(raw)))
(root / "frozen-inputs.json").write_text(json.dumps(dict(base=base, tracked=items), indent=2), encoding="utf-8")
print(f"{len(items)} locked input files copied and hashed independently twice")
