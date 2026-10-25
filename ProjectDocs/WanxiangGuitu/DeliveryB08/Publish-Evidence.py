"""Extend the existing allowlisted publisher with synthetic B08 diagnostics.

No save envelopes, plans, binaries or ground-loot pages are published.
Earlier directed runs may have mutable projects; only explicitly frozen sources
are copied and labelled. This tool never launches Unity or changes test inputs.
"""
import argparse
import hashlib
import importlib.util
import json
import struct
import subprocess
import sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--run', type=Path, required=True)
p.add_argument('--target', type=Path, required=True)
a = p.parse_args()
here = Path(__file__).resolve().parent
subprocess.run([sys.executable, '-B', str(here.parent / 'DeliveryB07-R1/Publish-Evidence.py'),
                '--run', str(a.run), '--target', str(a.target)], check=True)
spec = importlib.util.spec_from_file_location('publisher', here.parent / 'DeliveryUI01/Automation/publish-evidence.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
paths = []
for folder in [a.run, a.run / 'Rules'] + sorted(a.run.glob('Normal-*')):
    for item in sorted(folder.glob('b08-*')):
        if item.is_file() and item.suffix in {'.json', '.txt', '.csv', '.jsonl'} and item.name != 'b08-settlement.json':
            paths.append(item.relative_to(a.run).as_posix())
for name in ['tool-safety-failure.json', 'normal-local-handoff.json']:
    if (a.run / name).is_file():
        paths.append(name)
for folder in sorted(a.run.glob('B08-*')):
    if folder.is_dir():
        for pattern in ['process-*.json', 'timeline-*.json', 'analysis-*.json', 'b08-analysis-*.json',
                        'close-*.json', 'player-*.log', 'player-*.command.json', 'player-*.exit.json',
                        'player-*.desktop-process.json', 'storage-audit.jsonl']:
            paths += [item.relative_to(a.run).as_posix() for item in sorted(folder.glob(pattern)) if item.is_file()]
if paths:
    m.publish(a.run, a.target / 'B08Diagnostics', sorted(set(paths)))
logs = [item.relative_to(a.run).as_posix() for item in sorted((a.run / 'Rules').glob('B08*.log'))]
if logs:
    m.publish(a.run, a.target / 'B08Logs', logs, archive=True)
images = []
for folder in [a.run, a.run / 'Rules']:
    for item in sorted(folder.glob('b08-*.png')):
        raw = item.read_bytes()
        if raw[:8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError('Invalid PNG: ' + str(item))
        rel = Path('B08Screens') / item.name
        output = a.target / rel
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.exists():
            raise ValueError('Ambiguous screenshot name')
        output.write_bytes(raw)
        width, height = struct.unpack('>II', raw[16:24])
        images.append(dict(file=rel.as_posix(), width=width, height=height,
                           sha256=hashlib.sha256(raw).hexdigest(),
                           scope='Controlled actual Unity renderer; NPC disabled; NOT native UI or human usability'))
(a.target / 'b08-screens.json').write_text(json.dumps(images, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
for folder in sorted(a.run.glob('Normal-*')):
    path = folder / 'b08-settlement.json'
    if not path.is_file():
        continue
    obj = json.loads(path.read_text(encoding='utf-8-sig'))
    result = {key: obj.get(key) for key in ['settlementId', 'runId', 'outcome', 'status', 'acknowledged',
                                         'returnedMaterials', 'keptMaterials', 'lostMaterials']}
    for key in ['returnedGear', 'keptGear', 'lostGear']:
        result[key] = [dict(id=i['id'], type=i['type'], quality=i['quality']) for i in obj.get(key, [])]
    result.update(originalSha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  scope='Synthetic pending display before actual commit; plans deliberately omitted')
    dest = a.target / 'SettlementSummaries' / (folder.name + '.json')
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
# These folders are explicit historical source snapshots, not the mutable Project.
sources = []
for name in ['PreviousSources', 'NormalInputSources']:
    for item in sorted((a.run / name).rglob('*')):
        if not item.is_file() or not (item.name.endswith('.cs') or item.name.endswith('.cs.txt')):
            continue
        raw = item.read_bytes()
        rel = Path('B08Sources') / name / item.relative_to(a.run / name)
        rel = rel.with_name(rel.name + '.txt')
        output = a.target / rel
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(raw)
        sources.append(dict(file=rel.as_posix(), sha256=hashlib.sha256(raw).hexdigest(),
                            bytes=len(raw), scope='Historical frozen source; not current mutable Project'))
(a.target / 'b08-sources.json').write_text(json.dumps(sources, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
