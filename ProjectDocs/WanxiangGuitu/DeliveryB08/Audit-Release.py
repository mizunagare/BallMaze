"""Extend existing post-run release/hash audit; never access player save directories."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--project', type=Path, required=True)
p.add_argument('--run', type=Path, required=True)
p.add_argument('--target', type=Path, required=True)
p.add_argument('--baseline', required=True)
a = p.parse_args()
here = Path(__file__).resolve().parent
subprocess.run([sys.executable, '-B', str(here.parent / 'DeliveryB07-R1/Audit-Release.py'),
                '--project', str(a.project), '--run', str(a.run), '--target', str(a.target),
                '--baseline', a.baseline], check=True)
path = a.run / 'Build/Release/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'
raw = path.read_bytes()
runtime = {name: name.encode() in raw for name in ['Onboarding', 'OnboardingFocus', 'TutorialState', 'hasTutorial', 'CampRuntime']}
editor = {name: name.encode() in raw for name in ['B08Rules', 'B08Visual', 'B08CampPause', 'WGNormalAICheck', 'SetNextSeedForValidation']}
ok = all(runtime.values()) and not any(editor.values())
out = a.target / 'release-onboarding-check.json'
if out.exists():
    raise ValueError('Fresh audit output required')
out.write_text(json.dumps(dict(status='PASS' if ok else 'FAIL',
    scope='Static managed metadata names only; not native UI or final Player adventure',
    file=path.relative_to(a.run).as_posix(), sha256=hashlib.sha256(raw).hexdigest(),
    runtime=runtime, editor=editor), ensure_ascii=False, indent=2) + '\n', encoding='utf8')
inventory = json.loads((a.target / 'exception-inventory.json').read_text(encoding='utf8'))
annotations = []
for item in inventory['items']:
    lines = (a.run / item['log']).read_text(encoding='utf-8-sig', errors='replace').splitlines()
    context = '\n'.join(lines[max(0, item['line'] - 8):item['line'] + 18])
    labels = sorted(set(re.findall(r'B08_(?:VISUAL_)?EXPECTED_[A-Z_]+', context)))
    annotations.append(dict(**item, expectedB08FaultMarkers=labels,
                             annotation='Explicit synthetic fault injection' if labels else item['category']))
(a.target / 'b08-exception-annotations.json').write_text(json.dumps(dict(
    scope='Additional classification; original exception inventory and full logs unchanged', items=annotations),
    ensure_ascii=False, indent=2) + '\n', encoding='utf8')
print(json.dumps(dict(onboardingMetadata='PASS' if ok else 'FAIL', exceptionStarts=len(annotations))))
raise SystemExit(0 if ok else 1)
