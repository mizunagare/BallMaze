"""Audit actual trial receipts and publish quantity-based descriptive statistics.
No valuation invented; no save files read. Missing trials never become PASS.
"""
import argparse
import collections
import csv
import datetime
import json
from pathlib import Path
import statistics

p=argparse.ArgumentParser();p.add_argument('--matrix',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
root=a.matrix.resolve(strict=True)
if not a.matrix.is_absolute() or not (root/'owner.json').exists() or a.output.exists():raise ValueError('Owned matrix and fresh output required')
plan=json.loads((Path(__file__).parent/'MATRIX_INPUTS.json').read_text())
rows=[]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
steps=read(root/'results.json') if (root/'results.json').exists() else []
if isinstance(steps,dict):steps=[steps]
for case in plan['cases']:
    folder=root/case['id'];path=folder/'stage2-metrics.json'
    if not path.exists():
        failed=any(x.get('status')=='FAIL' and x.get('name','').startswith(case['id']+'.') for x in steps)
        rows.append(dict(input=case,status='FAIL' if failed else 'NOT_RUN',reason='No completed metric receipt; preserve failed command/dependency; not a valid sortie without Run ID'));continue
    try:d=read(path)
    except (ValueError,OSError) as error:
        rows.append(dict(input=case,status='FAIL',reason='Unreadable metric receipt: '+str(error)));continue
    if d.get('input')!=case:raise ValueError('Receipt/config mismatch '+case['id'])
    d['metricSha256']=__import__('hashlib').sha256(path.read_bytes()).hexdigest()
    process=[]
    for mode in ('Normal','Resume','FinalResume'):
        f=folder/f'process-result-{mode}.json'
        process.append(read(f) if f.exists() else dict(mode=mode,exitCode=None,timedOut=False,missing=True))
    d['processes']=process
    ok=d.get('status')=='PASS' and all(not r.get('missing') and r['exitCode']==0 and not r['timedOut'] for r in process)
    if (folder/'validation-interruption.json').exists():ok=False;d['interruption']=read(folder/'validation-interruption.json')
    d['status']='PASS' if ok else 'FAIL'
    d['materialRetentionByKind']=[None if n==0 else d['kept'][i]/n for i,n in enumerate(d['obtained'])]
    if d.get('assetsStart') is not None and d.get('assetsEnd') is not None:
        d['materialNetAfterCampGrowth']=[n-d['assetsStart'][i] for i,n in enumerate(d['assetsEnd'])]
        seconds=d.get('elapsedSeconds',0)
        d['netPerSimulationSecondByKind']=[n/seconds for n in d['materialNetAfterCampGrowth']] if seconds>0 else None
    if d.get('departureUtc') and d.get('settlementUtc'):
        start=datetime.datetime.fromisoformat(d['departureUtc'].replace('Z','+00:00'));end=datetime.datetime.fromisoformat(d['settlementUtc'].replace('Z','+00:00'))
        delta=(end-start).total_seconds();d['wallSecondsToPendingIncludingRecovery']=delta if delta>=0 else None;d['wallClockStatus']='PASS' if delta>=0 else 'UNRESOLVED'
    d['routeChoiceReason']='Fixed, predeclared strategy/experimental goal; recommendation is observed, not enforced. See score-normal JSON and actual visited POIs/trajectory.'
    rows.append(d)
valid=[r for r in rows if r.get('run')]
complete=[r for r in rows if r['status']=='PASS']
def stats(xs):return dict(n=len(xs),mean=statistics.mean(xs) if xs else None,stdev=statistics.stdev(xs) if len(xs)>1 else None,sampleInsufficient=len(xs)<2)
groups={}
for build in ('Safety','Gather','Boss'):
    sample=[r for r in valid if r['input']['build']==build]
    groups[build]={k:stats([r[k] for r in sample if k in r]) for k in ['elapsedSeconds','damageTaken','potionsUsed','meters']}
matched=[r for r in valid if r['input']['weapon']==3 and r['input']['seed']==1 and r['input']['strategy']=='Gather']
result=dict(status='PASS' if len(complete)==len(plan['cases']) else 'FAIL' if any(r['status']=='FAIL' for r in rows) else 'UNRESOLVED',
 scope='Editor normal enemy AI; quantity-only descriptive experiment, not native/human or balanced release acceptance',
 planned=len(plan['cases']),counts=dict(collections.Counter(r['status'] for r in rows)),validSorties=len(valid),
 extractionSuccessRate=None if not valid else sum(bool(r.get('extracted')) for r in valid)/len(valid),
 materials=['MonsterHide','CrystalShard','BossCore','Wood','Stone','Ore'],
 valuation='No universal value. Per-material retention ratios; material net = final carried+warehouse minus initial carried+warehouse after actual camp growth. This avoids subtracting consumed/lost run loot twice. Potions, gear, badges and pending remain separate.',
 timing='elapsedSeconds is summed active first-Run simulation frame time; UTC to Pending separately includes process recovery overhead. Neither is a GPU benchmark.',
 groupsDescriptiveOnly=groups,matchedBowSeed1Gather=matched,
 balanceConclusion='Evidence insufficient for broad weapon balance: per-condition n=1; descriptive group means mix goals and seeds and are not causal build estimates.',
 nativeUI='NOT_RUN',independentHumanFourWeapons='NOT_RUN',rows=rows)
a.output.mkdir(parents=True)
(a.output/'matrix-summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (a.output/'matrix-results.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['case','weapon','seed','actualSeed','strategy','build','status','run','seconds','meters','damage','potions','keptMaterials','runConsumed','campConsumed','materialNet','keptGear','growthAttack','growthDefense'])
    for r in rows:
        c=r['input'];w.writerow([c['id'],c['weapon'],c['seed'],r.get('actualSeed'),c['strategy'],c['build'],r['status'],r.get('run'),r.get('elapsedSeconds'),r.get('meters'),r.get('damageTaken'),r.get('potionsUsed'),json.dumps(r.get('kept')),json.dumps(r.get('runConsumed')),json.dumps(r.get('campConsumed')),json.dumps(r.get('materialNetAfterCampGrowth')),r.get('keptGear'),r.get('growthAttack'),r.get('growthDefense')])
print(json.dumps(dict(status=result['status'],planned=result['planned'],counts=result['counts'])))
raise SystemExit(0 if result['status']=='PASS' else 1)
