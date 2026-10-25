"""Check published evidence bytes and allowlists, independently of gameplay results."""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--root', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
root = a.root.resolve(strict=True)
if root.name != 'Evidence' or root.parent.name not in {'DeliveryB07', 'DeliveryB07-R1'}:
    raise ValueError('Explicit B07 or B07-R1 evidence root required')
if not a.output.resolve().is_relative_to(root) or a.output.exists():
    raise ValueError('Fresh output inside evidence root required')
errors = []
checked = 0
archives = 0
files = sorted(path for path in root.rglob('*') if path.is_file())
secret = re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{25,}|Authorization:\s*Bearer\s+(?!\[REDACTED\])[^\s"<>]{12,})', re.I)
for path in files:
    rel = path.relative_to(root).as_posix()
    if path.name in {'save.json', 'save.backup.json'} or path.suffix.lower() in {'.exe', '.dll', '.pdb', '.dmp', '.dat'}:
        errors.append(dict(path=rel, reason='Forbidden save/binary/dump'))
    if any(part.lower() in {'library', 'temp', 'dumps', 'release', 'ground-loot'} for part in path.relative_to(root).parts):
        errors.append(dict(path=rel, reason='Forbidden artifact directory'))
    data = path.read_bytes()
    if path.suffix != '.png' and secret.search(data):
        errors.append(dict(path=rel, reason='Potential credential; values deliberately omitted'))
    if path.suffix == '.zip':
        with zipfile.ZipFile(path) as z:
            if z.testzip() is not None:
                errors.append(dict(path=rel, reason='Archive CRC failure'))
            for name in z.namelist():
                if Path(name).suffix.lower() not in {'.log', '.txt', '.json', '.jsonl', '.csv', '.md', '.stdout', '.stderr'} or Path(name).name in {'save.json', 'save.backup.json'}:
                    errors.append(dict(path=rel, reason='Forbidden archive member', member=name))
                if secret.search(z.read(name)):
                    errors.append(dict(path=rel, reason='Potential credential in archive; values omitted', member=name))
        archives += 1
    if path.suffix != '.json':
        continue
    obj = json.loads(data.decode('utf-8-sig'))
    records = []
    zipped = False
    if path.name in {'manifest.json', 'log-manifest.json'} and isinstance(obj, dict) and 'files' in obj:
        zipped = path.name == 'log-manifest.json'
        records = [(r['path'], r['publishedSha256']) for r in obj['files']]
    elif path.name in {'source-snapshots.json', 'b07-executed-driver-sources.json', 'b07-screens.json', 'b4-screens.json', 'r1-screens.json', 'readability-screens.json', 'screens.json'} and isinstance(obj, list):
        records = [(r['file'], r['sha256']) for r in obj]
    elif path.name == 'source-snapshots.json' and isinstance(obj, dict) and 'files' in obj and all(isinstance(r,dict) and 'file' in r and 'sha256' in r for r in obj['files']):
        records = [(r['file'], r['sha256']) for r in obj['files']]
    elif path.name == 'frozen-product-proof.json':
        records = [(r['file'], r['sha256']) for r in obj['files'] + obj.get('injectedTests', [])]
    if zipped:
        with zipfile.ZipFile(path.parent / 'logs-redacted.zip') as z:
            for name, expected in records:
                actual = hashlib.sha256(z.read(name.replace('\\', '/'))).hexdigest()
                if actual != expected:
                    errors.append(dict(path=rel, reason='Published archive hash mismatch', member=name))
                checked += 1
    else:
        for name, expected in records:
            target = (path.parent / name).resolve()
            if not target.is_relative_to(root) or not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != expected:
                errors.append(dict(path=rel, reason='Published file hash mismatch', member=name))
            checked += 1
result = dict(status='PASS' if not errors else 'FAIL', files=len(files), archives=archives,
              checkedHashes=checked, errors=errors,
              scope='Published-byte integrity/allowlist check, not gameplay or native UI acceptance')
a.output.parent.mkdir(parents=True, exist_ok=True)
a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(status=result['status'], files=len(files), checkedHashes=checked, errors=len(errors))))
raise SystemExit(0 if not errors else 1)
