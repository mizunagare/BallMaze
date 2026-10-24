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
a = p.parse_args()

def git(*args):
    return subprocess.check_output(['git', '-C', str(a.project), *args])

commit = git('rev-parse', a.commit).decode().strip()
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
(a.target / 'frozen-product-proof.json').write_text(
    json.dumps(dict(commit=commit, count=len(rows), equal=True, files=rows),
               ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(commit=commit, productSources=len(rows), equal=True)))
