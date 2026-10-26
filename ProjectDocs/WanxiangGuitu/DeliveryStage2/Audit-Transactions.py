"""Read-only conservation audit of completed synthetic experiment projections.

No saves or game APIs are read; raw transaction receipts stay unchanged.
"""
import argparse
import collections
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--run', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
root = a.run.resolve(strict=True)
if not a.run.is_absolute() or not (root / 'owner.json').is_file() or a.output.exists():
    raise ValueError('Owned run and fresh output required')

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

summary = read(root / 'Stage2Summary/matrix-summary.json')
rows = []
totals = collections.Counter()
for metric in summary['rows']:
    folder = root / 'Stage2Matrix' / metric['input']['id']
    tx = [json.loads(line) for line in (folder / 'stage2-transactions.jsonl').read_text(encoding='utf-8-sig').splitlines() if line.strip()]
    departure = next(x for x in tx if x['label'] == 'depart')
    settlement = read(folder / 'b4-first-settlement.json')
    expected_end = [start + found - used_run - used_camp for start, found, used_run, used_camp in zip(metric['assetsStart'], metric['obtained'], metric['runConsumed'], metric['campConsumed'])]
    expected_return = [start + found - used for start, found, used in zip(departure['materials'], metric['obtained'], metric['runConsumed'])]
    actual_return = [x + y for x, y in zip(settlement['returnedMaterials'], settlement['keptMaterials'])]
    picked = {}
    manufactured = {}
    for before, after in zip(tx, tx[1:]):
        ids = {x['id'] for x in before['items']}
        additions = {x['id']: x for x in after['items'] if x['id'] not in ids}
        if before['label'].startswith('before-pickup:') and after['label'] == before['label'].replace('before-pickup:', 'after-pickup:', 1) + ':True':
            picked.update(additions)
        if before['label'] == 'before-cost:gathered-pre-boss-weapon' and after['label'] == 'after-cost:gathered-pre-boss-weapon:True':
            manufactured.update(additions)
    strategy = metric['input']['strategy']
    totals[strategy + 'PickedGear'] += len(picked)
    totals[strategy + 'RunCraftedGear'] += len(manufactured)
    ok = expected_end == metric['assetsEnd'] and expected_return == actual_return and not set(picked).intersection(manufactured)
    rows.append(dict(case=metric['input']['id'], status='PASS' if ok else 'FAIL',
        materialEquationExpected=expected_end, actualEndAssets=metric['assetsEnd'],
        beforeSettlementExpected=expected_return, settlementReturnedPlusKept=actual_return,
        actualPickedGear=list(picked.values()), actualRunManufacturedGear=list(manufactured.values()),
        keptGearCount=metric['keptGear'], growthItemId=metric['growthItem']))
ok = len(rows) == summary['planned'] and all(x['status'] == 'PASS' for x in rows)
out = dict(status='PASS' if ok else 'FAIL',
    scope='Read-only quantity conservation; picked gear separated from run-crafted gear. No save mutation or invented valuation.',
    rows=rows, totals=dict(totals))
a.output.parent.mkdir(parents=True, exist_ok=True)
a.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(status=out['status'], cases=len(rows), totals=dict(totals))))
raise SystemExit(0 if ok else 1)
