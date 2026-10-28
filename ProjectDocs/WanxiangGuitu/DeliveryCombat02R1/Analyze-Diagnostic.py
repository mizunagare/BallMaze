import argparse,json,hashlib,csv
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();root=Path(a.root);out=root/'Analysis';out.mkdir(exist_ok=False)
rows=[];trials=[]
def check(ok,name,detail=''):rows.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
for fixed in [False,True]:
 for n in range(1,4):
  base=(root/'Fixed' if fixed else (root/'Observed' if (root/'Observed').is_dir() else root))/'Stores'/f'{n:02}'
  data=[json.loads(x) for x in (base/'snapshots.jsonl').read_text(encoding='utf-8-sig').splitlines()]
  take=lambda name:next(x for x in data if x['phase']==name)
  before=take('before-original-load');after=take('after-original-load');single=take('before-single:Warden')
  first=next(x for x in data if x['phase']=='save-hook:after-publish' and (x.get('run') or {}).get('runId'))
  runid=first['run']['runId'];seed=first['run']['seed'];p0=first['disks'][0]['path'];p1=before['disks'][0]['path']
  sessions=single['sessions'];bosses=[x for x in single['sessionEnemies'] if x['kind'] in ['Warden','Tide']]
  record={'phase':'Fixed' if fixed else 'Observed','trial':n,'pid':single['pid'],'initialRunId':runid,'initialSeed':seed,'region':first['run']['region'],'regionInstanceId':first['run']['regionInstanceId'],'generationVersion':first['run']['generationVersion'],'targetWave':first['run']['targetWave'],'firstFixtureFrame':first['frame'],'beforeLoadFrame':before['frame'],'beforeLoadRevision':before['revision'],'firstSavePath':p0,'beforeLoadSavePath':p1,'beforeLoadAtCamp':before['atCamp'],'afterLoadAtCamp':after['atCamp'],'afterLoadRunId':(after.get('run') or {}).get('runId'),'singleBosses':[(x['id'],x['enemy'],x['brain'],x['brainInitialized']) for x in bosses],'sceneHandle':single['session']['sceneHandle'],'maxDepth':max(x['depth'] for x in data),'snapshotCount':len(data)}
  trials.append(record)
  check(len(sessions)==1,f'{record["phase"]}.{n} one actual session')
  check(all(x['randomBefore']==x['randomAfter'] and x['streamsBefore']==x['streamsAfter'] for x in data),f'{record["phase"]}.{n} observer does not advance RNG')
  generations=[x for x in data if x['phase'].startswith('generated-boss:')];check(len(generations)==40,f'{record["phase"]}.{n} forty requests captured')
  with (out/f'{record["phase"]}-{n}-generation.csv').open('w',newline='',encoding='utf-8') as f:
   writer=csv.DictWriter(f,fieldnames=['request','accepted','revision','bossVersion','attempt','fallback','failures']);writer.writeheader()
   for x in generations:
    layout=next(y['layout'] for y in x['forests'] if y['active']);writer.writerow({'request':int(x['phase'].split(':')[1]),'accepted':layout['seed'],'revision':layout['revision'],'bossVersion':layout['bossVersion'],'attempt':layout['generationAttempt'],'fallback':layout['fallback'],'failures':json.dumps(layout['generationFailures'],ensure_ascii=False)})
  if not fixed:
   reset=next(x for x in data if x['phase']=='save-hook:after-publish' and 'InitializeDefaultStorage' in x.get('saveCaller',''))
   check(first['frame']==1 and reset['frame']==2 and p0!=p1 and before['atCamp'] and after['atCamp'] and not bosses,f'Observed.{n} deferred Start resets fixture and wrong path is loaded')
   error=json.loads((base/'first-harness-exception.json').read_text());check('Sequence contains no matching element' in error['message'],f'Observed.{n} original Single failure reproduced')
  else:
   ready=take('product-start-observed');gate=take('product-start-complete-before-fixture')
   check(gate['frame']>ready['frame'] and p0==p1 and not before['atCamp'] and not after['atCamp'] and after['run']['runId']==runid,f'Fixed.{n} original Run and storage retained after readiness gate')
   check(len(bosses)==2 and all(x['brainInitialized'] for x in bosses),f'Fixed.{n} both actual Boss references initialized')
   active={x['enemy'] for x in single['actualEnemies'] if x['active']};check(all(x['enemy'] in active for x in single['sessionEnemies']),f'Fixed.{n} session array matches actual scene references')
   check(not (base/'first-harness-exception.json').exists() and 'RUN_PROFILE_GROUND_STREAM_LEDGER_READY_FOR_NEW_PROCESS' in (base/'b07-rules.txt').read_text(),f'Fixed.{n} all original rule assertions completed')
  check(not (base/'observer-errors.txt').exists(),f'{record["phase"]}.{n} observer completed without error')
(out/'checks.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');(out/'trials.json').write_text(json.dumps(trials,ensure_ascii=False,indent=2),encoding='utf-8');print({s:sum(x['status']==s for x in rows) for s in ['PASS','FAIL']})
raise SystemExit(any(x['status']=='FAIL' for x in rows))
