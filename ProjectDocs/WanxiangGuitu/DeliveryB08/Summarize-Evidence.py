"""Derive B08 results only from this ended All; no save envelopes are read."""
import argparse
import collections
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--run', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
here = Path(__file__).resolve().parent
subprocess.run([sys.executable, '-B', str(here.parent / 'DeliveryB07/Summarize-Evidence.py'),
                '--run', str(a.run), '--output', str(a.output)], check=True)
def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
result = read(a.output)
root = a.run / 'Normal-Tutorial'
points = [root / ('b08-checkpoint-' + str(i) + '.json') for i in [1, 2, 3]]
if all(path.is_file() for path in points):
    first, second, third = map(read, points)
    settlement = read(root / 'b08-settlement.json')
    result['tutorial'] = dict(
        scope='Normal NPC AI and Editor domain bot; not native UI',
        checkpoints=[dict(stage=v['stage'], profile=v['profile'], run=v['run'], region=v['region'],
                          tutorial=json.loads(v['tutorial']), ledger=v['ledger'], gear=v['gear'],
                          warehouse=v['warehouse'], seed=json.loads(v['layout'])['seed'],
                          layoutSha256=hashlib.sha256(v['layout'].encode()).hexdigest(),
                          streams=v['streams']) for v in [first, second, third]],
        firstRun=first['run'], secondRun=second['run'], differentRuns=first['run'] != second['run'],
        secondAndThirdEqual=all(second[k] == third[k] for k in second if k != 'stage'),
        keptMaterials=dict(zip(['hide', 'crystal', 'core', 'wood', 'stone', 'ore'], settlement['keptMaterials'])),
        journal=(root / 'normal-results.txt').read_text(encoding='utf-8-sig').splitlines(),
        source='Real resource kills, actual pickup, actual free-exit channel, commit/acknowledge, withdrawal and manufacture. No tutorial rewards.')
else:
    result['tutorial'] = dict(status='NOT_RUN', reason='Incomplete tutorial checkpoints; inspect actual process failures')
visual = a.run / 'Rules/b08-visual.txt'
if visual.is_file():
    result['onboardingVisual'] = dict(journal=visual.read_text(encoding='utf-8-sig').splitlines(),
                                      scope='Controlled rendered fixtures, not native UI or human usability')
result['b08Methods'] = {r['name']: r['status'] for r in read(a.run / 'results.json') if r['name'].startswith(('B08', 'normal-ai.Tutorial'))}
a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
print(json.dumps(dict(b08=result['b08Methods'], normalProcesses=len(result['normalProcesses']), playerProcesses=len(result['playerProcesses']))))
