"""Derive review summaries from an ended synthetic run; no save files are read."""
import argparse
import collections
import csv
import json
import re
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--run', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

owner = read(a.run / 'owner.json')
if owner.get('kind') != 'WanxiangGuitu isolated unattended run':
    raise ValueError('Owned synthetic run required')
rows = read(a.run / 'results.json')
if not any(r['name'] == 'report.finalized' for r in rows):
    raise ValueError('Run has not finalized')
materials = ['MonsterHide', 'CrystalShard', 'BossCore', 'Wood', 'Stone', 'Ore']
report = dict(counts=dict(collections.Counter(r['status'] for r in rows)),
              expectedProbeFailures=[r['name'] for r in rows if r['status'] == 'FAIL' and r['scope'] == 'harness-negative'],
              unexpectedFailures=[r['name'] for r in rows if r['status'] == 'FAIL' and r['scope'] != 'harness-negative'],
              normalProcesses=[dict(name=r['name'], status=r['status'], exitCode=r['exitCode'], timedOut=r['timedOut']) for r in rows if r['scope'] == 'normal-ai'],
              adventures={}, playerProcesses=[])
for strategy in ['Land', 'Lake']:
    root = a.run / ('Normal-' + strategy)
    checkpoints = [root / ('b4-checkpoint-' + str(stage) + '.json') for stage in [1, 2]]
    if not all(path.exists() for path in checkpoints):
        report['adventures'][strategy] = dict(status=next((r['status'] for r in rows if r['name'] == 'normal-ai.' + strategy + '.Normal'), 'NOT_RUN'), reason='Complete checkpoint dependency absent; per-process results retain the actual failure/skip')
        continue
    first, second = map(read, checkpoints)
    settlement = read(root / 'b4-first-settlement.json')
    lines = (root / 'normal-results.txt').read_text(encoding='utf-8-sig').splitlines()
    combat = list(csv.reader((root / 'boss-combat.csv').read_text(encoding='utf-8-sig').splitlines()))
    layout = json.loads(first['layout'])
    report['adventures'][strategy] = dict(
        scope='Editor domain bot and normal NPC AI, not final Player combat or native UI',
        run=first['run'], successorRun=second['run'], region=first['region'],
        seed=first['seed'], terrainVersion=layout['terrain']['version'], bossVersion=layout['bossVersion'],
        huntsBeforeExtraction=json.loads(first['hunts']), huntsAfterNextDeparture=json.loads(second['hunts']),
        ferryReceipt=first['receipt'], ledgerBeforeExtraction=first['ledger'],
        keptMaterials=dict(zip(materials, settlement['keptMaterials'])),
        returnedMaterials=dict(zip(materials, settlement['returnedMaterials'])),
        keptGear=[dict(id=i['id'], type=i['type'], quality=i['quality']) for i in settlement['keptGear']],
        returnedGearIds=[i['id'] for i in settlement['returnedGear']],
        actualAttackKinds=sorted({row[3] for row in combat}),
        observedBossStates=sorted({row[2] for row in combat}),
        maxObservedReleases=max(int(row[6]) for row in combat),
        journal=lines,
        fixture='Starter white bow/sword; carried stone2 ore2 and five actually crafted potions. Synthetic camp reserves stone1 ore2. Gathered wood used to craft a bow before combat; combat uses the existing selected white bow. Growth comes from actual level choices; no health/stat override.')
for folder in sorted(a.run.glob('*')):
    if not folder.is_dir():
        continue
    for path in sorted(folder.glob('process-[12].json')):
        info = read(path)
        report['playerProcesses'].append(dict(cell=folder.name, passId=path.stem, **info))
report['limitations'] = dict(shutdownRootCause='UNRESOLVED', nativeU16='NOT_RUN', humanUsability='NOT_RUN',
                             playerScope='Final non-development launch, background WM_CLOSE, exit audit and new-process restore. Not physical titlebar or native-input acceptance.')
a.output.parent.mkdir(parents=True, exist_ok=True)
if a.output.exists():
    raise ValueError('Fresh summary output required')
a.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(counts=report['counts'], unexpectedFailures=report['unexpectedFailures'],
                      normalProcesses=len(report['normalProcesses']), playerProcesses=len(report['playerProcesses']))))
