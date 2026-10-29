"""Recompute finite paired observations; never turn censored windows into victories."""
import pathlib,json,csv,statistics,collections,sys
root=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);out.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
folders={'before':sys.argv[3] if len(sys.argv)>3 else 'MatrixBeforeFrozen','after':sys.argv[4] if len(sys.argv)>4 else 'MatrixAfterFrozen'};phases={k:read(root/v/'matrix.json') for k,v in folders.items()}
fields=['seed','rep','type','policy','initialHP','initialDefense','initialPower','initialLevel','initialRanks','initialStreams','initialPositions','enemyCount']
before={r['sample']:r for r in phases['before']['rows']};after={r['sample']:r for r in phases['after']['rows']};bad=[]
if set(before)!=set(after):bad.append(['sample-set'])
for key in before.keys()&after.keys():
 for f in fields:
  if before[key][f]!=after[key][f]:bad.append([key,f,before[key][f],after[key][f]])
if [x['layout'] for x in phases['before']['runs']]!=[x['layout'] for x in phases['after']['runs']]:bad.append(['layout'])
for phase,d in phases.items():
 if len(d['runs'])!=9 or len({r['run'] for r in d['runs']})!=9 or len(d['rows'])!=108:bad.append([phase,'9 independent Runs /108 sample count'])
 if not all(x['xpMatchesWhenSurviving'] for x in d['rows']):bad.append([phase,'XP source reconciliation'])
flat=[];events=[]
for phase,d in phases.items():
 for r in d['rows']:
  ev=[readline for line in (root/folders[phase]/'Samples'/r['sample']/'events.jsonl').read_text(encoding='utf-8-sig').splitlines() if (readline:=json.loads(line))]
  xp=[e for e in ev if e['kind']=='xp'];upgrade=[dict(timeFromSample=e['time']-r['startedTime'],entity=e['entity'],levelBefore=e['levelBefore'],levelAfter=e['levelAfter'],remainder=e['remainder']) for e in xp if e['levelAfter']>e['levelBefore']]
  row=dict(phase=phase,**r,levelUps=r['finalLevel']-r['initialLevel'],unhitActionsWithinWindow=r['releases']-r['hitActions'],unreleasedTelegraphsAtCutoff=r['windups']-r['releases'],upgrades=json.dumps(upgrade),xpSources=json.dumps([dict(entity=e['entity'],xp=e['xp'],timeFromSample=e['time']-r['startedTime']) for e in xp]))
  flat.append(row);events.extend(dict(phase=phase,sample=r['sample'],**e,timeFromSample=e['time']-r['startedTime']) for e in ev)
with (out/'BALANCE_MATRIX.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
groups=[]
for phase in phases:
 for kind in ['Melee','Ranged','Elite','Warden','Tide','Mixed']:
  a=[x for x in flat if x['phase']==phase and x['type']==kind];ttk=[x['ttk'] for x in a if x['ttk']>=0];releases=sum(x['releases'] for x in a)
  groups.append(dict(phase=phase,type=kind,n=len(a),meanDamage=statistics.mean(x['damage'] for x in a),minDamage=min(x['damage'] for x in a),maxDamage=max(x['damage'] for x in a),damageSD=statistics.stdev(x['damage'] for x in a),completedTTKCount=len(ttk),meanCompletedTTK=statistics.mean(ttk) if ttk else None,censored=sum(x['outcome']=='WINDOW_END_CENSORED' for x in a),deaths=sum(x['outcome']=='PLAYER_DEAD' for x in a),windups=sum(x['windups'] for x in a),releases=releases,hitActions=sum(x['hitActions'] for x in a),hitRate=sum(x['hitActions'] for x in a)/releases if releases else None,heals=sum(x['heals'] for x in a),dodges=sum(x['dodges'] for x in a),dodgeBlockedContacts=sum(x['dodgeBlocks'] for x in a),levelUps=sum(x['levelUps'] for x in a),xp=sum(x['experience'] for x in a)))
with (out/'matrix-group-summary.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=list(groups[0]));w.writeheader();w.writerows(groups)
with (out/'combat-events.jsonl').open('w',encoding='utf-8') as f:
 for e in events:f.write(json.dumps(e,ensure_ascii=False)+'\n')
checks=dict(status='FAIL' if bad else 'PASS',matchingRecordedInputFields=fields,positionPrecision='Unity Vector3.ToString records rounded displayed positions; not a claim of bit-identical full physics snapshots',mismatches=bad,scope='Same frozen conditional controller, not identical raw button frame playback. 6-second active windows; TTK=-1 is censored. Explicit per-sample legacy global RNG; Flow disabled only in controlled fixture. Run-owned RNG tested separately.',groups=groups)
(out/'paired-check.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(checks['status'],len(flat),'observations',len(events),'events')
if bad:raise SystemExit(1)
