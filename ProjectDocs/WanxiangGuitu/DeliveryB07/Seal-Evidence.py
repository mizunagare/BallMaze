"""Seal an ended isolated run's product source against a fixed Git input.

Evidence postprocessing only: never reads player saves or edits a test project.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--project', type=Path, required=True)
p.add_argument('--run', type=Path, required=True)
p.add_argument('--target', type=Path, required=True)
p.add_argument('--commit', required=True)
p.add_argument('--test-commit', help='Separately recorded normal-driver input; product/rule commit stays fixed')
a = p.parse_args()

def git(*args):
    return subprocess.check_output(['git', '-C', str(a.project), *args])

commit = git('rev-parse', a.commit).decode().strip()
test_commit = git('rev-parse', a.test_commit or a.commit).decode().strip()
paths = [name for name in git('ls-tree', '-r', '--name-only', commit,
                             '--', 'Assets/CombatPrototype').decode().splitlines()
         if name.endswith('.cs')]
rows = []
for name in paths:
    blob = git('show', commit + ':' + name)
    path = a.run / 'Project' / name
    raw = path.read_bytes()
    normalized = raw.replace(b'\r\n', b'\n')
    if normalized != blob.replace(b'\r\n', b'\n'):
        raise ValueError('Frozen product differs from input commit: ' + name)
    rel = Path('Sources') / (name + '.txt')
    out = a.target / rel
    if out.exists():
        raise ValueError('Refusing to overwrite a source snapshot: ' + str(out))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    rows.append(dict(file=rel.as_posix(), path=name, bytes=len(raw),
                     sha256=hashlib.sha256(raw).hexdigest(),
                     normalizedSha256=hashlib.sha256(normalized).hexdigest(),
                     gitNormalizedSha256=hashlib.sha256(blob.replace(b'\r\n', b'\n')).hexdigest()))
if not rows:
    raise ValueError('No product files')
origins = {}
for name in git('ls-tree', '-rz', '--name-only', commit, '--', 'ProjectDocs').decode().split('\0'):
    if name.endswith('.cs.txt') and '/Evidence/' not in name:
        blob = git('show', commit + ':' + name).replace(b'\r\n', b'\n')
        origins.setdefault(hashlib.sha256(blob).hexdigest(), []).append(name)
normal_origins = {}
for name in git('ls-tree', '-rz', '--name-only', test_commit, '--', 'ProjectDocs').decode().split('\0'):
    if name.endswith('.cs.txt') and '/Evidence/' not in name:
        blob = git('show', test_commit + ':' + name).replace(b'\r\n', b'\n')
        normal_origins.setdefault(hashlib.sha256(blob).hexdigest(), []).append(name)
normal = []
for path in sorted(a.run.glob('Normal-*/ExecutedDrivers-*/*.cs')):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()
    matches = normal_origins.get(digest, [])
    if not matches:
        raise ValueError('Executed normal driver does not match declared test commit: ' + str(path))
    normal.append(dict(path=path.relative_to(a.run).as_posix(), sha256=hashlib.sha256(raw).hexdigest(),
                       normalizedSha256=digest, matchingInputPaths=matches))
rules = []
for path in sorted((a.run / 'Project/Assets/CombatPrototype/Editor').rglob('*.cs')):
    name = path.relative_to(a.run / 'Project').as_posix()
    if name in paths:
        continue
    raw = path.read_bytes()
    digest = hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()
    rel = Path('Sources/InjectedTests') / (name + '.txt')
    out = a.target / rel
    if out.exists():
        raise ValueError('Refusing to overwrite injected source: ' + str(out))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    rules.append(dict(file=rel.as_posix(), sha256=hashlib.sha256(raw).hexdigest(),
                      normalizedSha256=digest, matchingInputPaths=origins.get(digest, [])))
(a.target / 'frozen-product-proof.json').write_text(
    json.dumps(dict(commit=commit, normalDriverCommit=test_commit, count=len(rows), equal=True,
                    files=rows, injectedTests=rules, normalDrivers=normal),
               ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(commit=commit, productSources=len(rows), equal=True,
                      injectedTests=len(rules), normalDrivers=len(normal),
                      unmatchedInjectedTests=[r['file'] for r in rules if not r['matchingInputPaths']])))
