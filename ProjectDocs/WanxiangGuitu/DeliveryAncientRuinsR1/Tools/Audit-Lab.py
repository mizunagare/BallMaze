from pathlib import Path
import hashlib
import json
import subprocess
import sys

worktree, lab, output = map(Path, sys.argv[1:])
paths = subprocess.check_output(
    ["git", "-C", str(worktree), "ls-files", "-z", "--", "Assets", "Packages", "ProjectSettings"]
).decode().split("\0")
paths = sorted(set(paths) - {""})
def sha(raw):
    return hashlib.sha256(raw).hexdigest()

differences = []
for relative in paths:
    source = (worktree / relative).read_bytes()
    path = lab / relative
    actual = path.read_bytes() if path.is_file() else None
    if source == actual:
        continue
    def normalized(raw):
        return b"\n".join(line.rstrip(b" \t") for line in raw.replace(b"\r\n", b"\n").split(b"\n"))
    differences.append(dict(path=relative, repositorySHA256=sha(source),
        testSHA256=sha(actual) if actual is not None else None,
        whitespaceOnly=actual is not None and normalized(source) == normalized(actual)))
if output.exists():
    raise FileExistsError(output)
output.write_text(json.dumps(dict(trackedInputs=len(paths), differences=differences), indent=2), encoding="utf-8")
print(len(paths), "tracked product paths;", len(differences), "raw differences")
