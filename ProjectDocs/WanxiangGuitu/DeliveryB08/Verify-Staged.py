"""Verify staged evidence bytes/LFS OIDs and exclude protected user files.

No Git mutations, save access, game launches or cleanup. Receipt excludes itself.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--project', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--evidence-root',default='ProjectDocs/WanxiangGuitu/DeliveryB08/Evidence')
a = p.parse_args()
repo = a.project.resolve(strict=True)
root = (repo / a.evidence_root).resolve()
if not root.is_relative_to(repo) or root.name != 'Evidence':
    raise ValueError('Contained repository Evidence root required')
if not a.output.resolve().is_relative_to(root) or a.output.exists():
    raise ValueError('Fresh receipt inside specified evidence required')
prefix = root.relative_to(repo).as_posix() + '/'
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
files = [n for n in git('ls-files', '-z', '--', prefix).decode().split('\0') if n and (repo / n).resolve() != a.output.resolve()]
disk = {n.relative_to(repo).as_posix() for n in root.rglob('*') if n.is_file() and n.resolve() != a.output.resolve()}
missing = sorted(disk - set(files))
bad = []
lfs = 0
proc = subprocess.Popen(['git', '-C', str(repo), 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
try:
    for name in files:
        proc.stdin.write((':' + name + '\n').encode())
        proc.stdin.flush()
        header = proc.stdout.readline().decode().strip().split()
        if len(header) != 3:
            raise ValueError('Staged blob unavailable: ' + name)
        blob = proc.stdout.read(int(header[2]))
        proc.stdout.read(1)
        raw = (repo / name).read_bytes()
        if blob.startswith(b'version https://git-lfs.github.com/spec/v1'):
            oid = re.search(rb'oid sha256:([a-f0-9]{64})', blob)
            lfs += 1
            equal = oid and oid.group(1).decode() == hashlib.sha256(raw).hexdigest()
        else:
            equal = blob == raw
        if not equal:
            bad.append(dict(path=name, reason='Staged bytes differ from published working payload'))
finally:
    proc.stdin.close()
    proc.wait()
protected = git('diff', '--cached', '--name-only', '--', 'Assets/CombatPrototype/ForestRuins.unity', 'ProjectSettings/ProjectSettings.asset').decode().splitlines()
ok = bool(files) and not bad and not missing and not protected
result = dict(status='PASS' if ok else 'FAIL',
              scope='Git staged evidence bytes/LFS payload OIDs, excluding this new receipt itself; not gameplay acceptance',
              files=len(files), lfsPayloads=lfs, missing=missing, mismatches=bad, stagedProtectedFiles=protected)
a.output.parent.mkdir(parents=True, exist_ok=True)
a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
print(json.dumps(result))
raise SystemExit(0 if ok else 1)
