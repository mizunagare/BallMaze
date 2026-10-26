"""Supplement the existing release audit with Stage2 coverage and full log inventory.

Postprocessing only, no game or save access. Exceptions are retained, not suppressed.
"""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import re

p = argparse.ArgumentParser()
p.add_argument('--run', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
root = a.run.resolve(strict=True)
if not a.run.is_absolute() or not (root / 'owner.json').is_file() or a.output.exists():
    raise ValueError('Owned run and fresh output required')
def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
rows = read(root / 'results.json')
if not any(x['name'] == 'report.finalized' and x['status'] == 'PASS' for x in rows):
    raise ValueError('Finalized All required')
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
rules = list(csv.DictReader((root / 'Rules/stage2-100-seeds.csv').read_text(encoding='utf-8-sig').splitlines()))
physical = list(csv.reader((root / 'Rules/stage2-physical.csv').read_text(encoding='utf-8-sig').splitlines()))
paths = [json.loads(line) for line in (root / 'Rules/stage2-physical-paths.jsonl').read_text().splitlines() if line.strip()]
matrix = read(root / 'Stage2Summary/matrix-summary.json')
processes = read(root / 'Stage2Matrix/results.json')
controlled = read(root / 'ControlledPlayer/results.json')
negative_names = {'probe.nonzero', 'probe.timeout'}
unexpected = [x for x in rows if x['status'] == 'FAIL' and x['name'] not in negative_names]
items = []; markers = []; logs = []
for f in sorted(root.rglob('*.log')):
    rel = f.relative_to(root)
    if any(part in {'Project', 'Library', 'Worker', 'DeferredTestSources'} for part in rel.parts): continue
    lines = f.read_text(encoding='utf-8-sig', errors='replace').splitlines()
    logs.append(dict(path=rel.as_posix(), sha256=digest(f), bytes=f.stat().st_size))
    for i, line in enumerate(lines):
        context = '\n'.join(lines[max(0, i - 5): i + 18])
        if re.match(r'^[\w.]*Exception:', line):
            category = 'Editor.Search internal' if 'UnityEditor.Search.' in context else 'Synthetic log-gate probe' if rel.parts[0] == 'Stage2LogGateProbes' else 'Inspect original context; not inferred clean from exit0'
            items.append(dict(log=rel.as_posix(), line=i + 1, error=line, category=category, context=context))
        if any(s in line for s in ('Got a UNKNOWN', 'JobTempAlloc', 'debugger-agent: Unable', 'abort_threads: Failed')):
            markers.append(dict(log=rel.as_posix(), line=i + 1, text=line))
build = root / 'Build/WanxiangBuild.ValidateBuild.log'
text = build.read_text(encoding='utf-8-sig', errors='replace')
artifacts = []
for name in ('WanxiangGuitu.exe', 'UnityPlayer.dll', 'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'):
    f = root / 'Build/Release' / name
    artifacts.append(dict(path=f.relative_to(root).as_posix(), bytes=f.stat().st_size, sha256=digest(f)))
out = dict(scope='Fresh finalized All; controlled/domain/native/human scopes remain distinct. Full log marker inventory is diagnostic, not an engine root-cause assertion.',
    coordinatorCounts=dict(collections.Counter(x['status'] for x in rows)), unexpectedFailures=unexpected,
    rulesRequested=len(rules), uniqueRuleSeeds=len({x['requested'] for x in rules}), ruleBossVersions=sorted({x['boss'] for x in rules}),
    physicalRequests=len(physical), uniqueActualPhysicalSeeds=len({x[1] for x in physical}), navigationProofs=len(paths),
    matrixCounts=matrix['counts'], matrixProcessCounts=dict(collections.Counter(x['status'] for x in processes)),
    controlledPlayerCounts=dict(collections.Counter(x['status'] for x in controlled)),
    build=dict(errors=int(re.search(r'^errors=(\d+)', text, re.M)[1]), warnings=int(re.search(r'^warnings=(\d+)', text, re.M)[1]), artifacts=artifacts),
    logCount=len(logs), logManifest=logs, exceptionCounts=dict(collections.Counter(x['category'] for x in items)), exceptions=items,
    otherDiagnosticMarkers=markers, nativeFourWeapons='NOT_RUN', humanFourWeapons='NOT_RUN',
    status='PASS' if not unexpected and len(rules) == 100 and len({x[1] for x in physical}) >= 20 and matrix['status'] == 'PASS' else 'FAIL',
    statusMeaning='Automated coverage and expected failure propagation only; Stage2 independent player acceptance remains OPEN')
a.output.parent.mkdir(parents=True, exist_ok=True)
a.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: out[k] for k in ('status', 'coordinatorCounts', 'uniqueRuleSeeds', 'uniqueActualPhysicalSeeds', 'navigationProofs', 'matrixProcessCounts', 'controlledPlayerCounts', 'exceptionCounts', 'logCount')}))
raise SystemExit(0 if out['status'] == 'PASS' else 1)
