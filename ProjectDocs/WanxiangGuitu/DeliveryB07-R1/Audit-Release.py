"""Postprocess an ended synthetic run; never read saves or execute game code."""
import argparse
import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--project', type=Path, required=True)
p.add_argument('--run', type=Path, required=True)
p.add_argument('--target', type=Path, required=True)
p.add_argument('--baseline', required=True)
a = p.parse_args()
rows = json.loads((a.run / 'results.json').read_text(encoding='utf-8-sig'))
if not any(r['name'] == 'report.finalized' and r['status'] == 'PASS' for r in rows):
    raise ValueError('Ended run required')

def write(name, obj):
    path = a.target / name
    if path.exists():
        raise ValueError('Fresh evidence output required: ' + name)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha(data):
    return hashlib.sha256(data).hexdigest()

dll = a.run / 'Build/Release/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'
data = dll.read_bytes()
runtime = {s: s.encode() in data for s in ['ForestBossHud', 'ForestBossTelegraph', 'CameraActorFade']}
editor = {s: s.encode() in data for s in ['SetNextSeedForValidation', 'B07ReadabilityVisual', 'B07ActorOcclusion']}
release_ok = all(runtime.values()) and not any(editor.values())
write('release-hud-check.json', dict(status='PASS' if release_ok else 'FAIL',
      scope='Static managed metadata-name check only; not native UI or combat',
      file=dll.relative_to(a.run).as_posix(), sha256=sha(data), runtime=runtime, editor=editor))

expected = {
 'Assets/CombatPrototype/ForestRuins.unity': 'ebc46ce7104b6d6ce90b7f510a59a401d7cdf64ae8babc85a7ebbf881c9d16d4',
 'ProjectSettings/ProjectSettings.asset': '7d06ea8265edaaf0a1a7402cff1e94da015450c58899438ebf4a5d97e37fd451'
}
protected = []
for name, initial in expected.items():
    raw = (a.project / name).read_bytes()
    copy = (a.run / 'Project' / name).read_bytes()
    blob = subprocess.check_output(['git', '-C', str(a.project), 'show', a.baseline + ':' + name])
    protected.append(dict(path=name, initialSha256=initial, currentSha256=sha(raw),
                          isolatedSha256=sha(copy), gitBaselineNormalizedSha256=sha(blob.replace(b'\r\n', b'\n')),
                          unchanged=sha(raw) == initial, isolatedRawEqual=raw == copy,
                          note='User input is not committed. Isolated ProjectSettings may be changed by the existing build isolation policy.'))
write('user-input-proof.json', dict(scope='Hashes only; no user scene/settings payload uploaded', files=protected))

logs = list((a.run / 'Rules').glob('*.log')) + list((a.run / 'Build').glob('*.log'))
for folder in a.run.glob('Normal-*'):
    logs += list(folder.glob('*.log'))
exceptions = []
for path in sorted(logs):
    lines = path.read_text(encoding='utf-8-sig', errors='replace').splitlines()
    for i, line in enumerate(lines):
        if re.match(r'^[\w.]*Exception:', line):
            context = '\n'.join(lines[i:i + 15])
            category = 'Editor.Search internal' if 'UnityEditor.Search.' in context else 'UNCLASSIFIED; inspect full log'
            exceptions.append(dict(log=path.relative_to(a.run).as_posix(), line=i + 1, error=line, category=category))
write('exception-inventory.json', dict(scope='Independent log inventory. No error removed; exit zero does not imply clean logs or known root cause.', items=exceptions))
build_log = a.run / 'Build/build.log'
if not build_log.exists():
    candidates = sorted((a.run / 'Build').glob('*.log'))
    if len(candidates) != 1:
        raise ValueError('Ambiguous build log')
    build_log = candidates[0]
warnings = [dict(line=i + 1, text=line) for i, line in enumerate(build_log.read_text(encoding='utf-8-sig', errors='replace').splitlines()) if re.search(r'\bwarning\b', line, re.I)]
write('build-warning-lines.json', dict(log=build_log.relative_to(a.run).as_posix(), scope='All warning marker lines; this count is not the BuildReport warning total', lines=warnings))
print(json.dumps(dict(releaseMetadata='PASS' if release_ok else 'FAIL', protectedInputsUnchanged=all(r['unchanged'] for r in protected), exceptions=len(exceptions), exceptionCategories=dict(collections.Counter(r['category'] for r in exceptions)), warningLines=len(warnings))))
raise SystemExit(0 if release_ok and all(r['unchanged'] for r in protected) else 1)
