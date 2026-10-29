"""Summarize controlled samples without treating matrix coverage as human accuracy."""
import csv,json,statistics,pathlib,sys
root=pathlib.Path(sys.argv[1]); result={}
for phase in ('Before','BeforePaired','BeforeVerified','After','FixedBefore','FixedAfter'):
 p=root/phase/'matrix.csv'
 if not p.exists():continue
 rows=list(csv.DictReader(p.open(encoding='utf-8-sig'))); groups={}
 for row in rows:groups.setdefault((row['weapon'],row['action']),[]).append(row)
 result[phase]={ '/'.join(k):{'n':len(v),'hits':sum(r['hit']=='1' for r in v),'coverageHitRate':sum(r['hit']=='1' for r in v)/len(v),'coverageMissRate':sum(r['hit']=='0' for r in v)/len(v),'damageValues':sorted({float(r['applied']) for r in v}),'medianHitLatency':statistics.median([float(r['hitLatency']) for r in v if float(r['hitLatency'])>=0]) if any(float(r['hitLatency'])>=0 for r in v) else None} for k,v in groups.items()}
strict=(root/'FixedBefore'/'measurement.json').exists() and (root/'FixedAfter'/'measurement.json').exists()
before=root/('FixedBefore' if strict else 'BeforeVerified' if (root/'BeforeVerified'/'matrix.csv').exists() else 'BeforePaired')/'matrix.csv';after=root/('FixedAfter' if strict else 'After')/'matrix.csv'
if before.exists() and after.exists():
 def index(p):
  result={};occurrences={}
  for r in csv.DictReader(p.open(encoding='utf-8-sig')):
   key=tuple(r[k] for k in ('weapon','action','body','distance','angle','height','duplicate','wall'));n=occurrences.get(key,0);occurrences[key]=n+1;result[key+(str(n),)]=r
  return result
 a,b=index(before),index(after);result['comparison']={'baseline':before.parent.name,'afterPhase':after.parent.name,'sameCaseKeys':a.keys()==b.keys(),'before':len(a),'after':len(b),'damageOrHitChanges':[{'key':k,'before':a[k],'after':b[k]} for k in a.keys()&b.keys() if (a[k]['hit'],float(a[k]['applied']))!=(b[k]['hit'],float(b[k]['applied']))]}
if strict:
 x,y=[json.loads((root/p/'identity.json').read_text(encoding='utf-8-sig')) for p in ('FixedBefore','FixedAfter')]
 result['fixedInput']={'seeds':[x['seed'],y['seed']],'layoutSeeds':[x['checkpoint']['forest']['seed'],y['checkpoint']['forest']['seed']],'layoutRevisions':[x['checkpoint']['forest']['revision'],y['checkpoint']['forest']['revision']],'streamVersion':[x['randomStreams']['version'],y['randomStreams']['version']],'sameInitialStreams':x['randomStreams']==y['randomStreams'],'weaponConfigurationEqual':json.loads((root/'FixedBefore'/'weapons.json').read_text(encoding='utf-8-sig'))['weapons']==json.loads((root/'FixedAfter'/'weapons.json').read_text(encoding='utf-8-sig'))['weapons']}
for phase in ('BeforePaired','BeforeVerified','After'):
 p=root/phase/'duels.csv'
 if not p.exists():continue
 groups={}
 for r in csv.DictReader(p.open(encoding='utf-8-sig')):groups.setdefault((r['weapon'],r['body']),[]).append(r)
 result[phase+'Duels']={'/'.join(k):{'n':len(v),'terminal':[r['terminal'] for r in v],'meanSeconds':statistics.mean(float(r['seconds']) for r in v),'meanReceivedDamage':statistics.mean(float(r['receivedDamage']) for r in v),'meanKillWindowDPS':statistics.mean(float(r['killWindowDPS']) for r in v),'minSeconds':min(float(r['seconds']) for r in v),'maxSeconds':max(float(r['seconds']) for r in v)} for k,v in groups.items()}
(root/'comparison.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
if 'comparison' in result and (not result['comparison']['sameCaseKeys'] or result['comparison']['damageOrHitChanges']):raise SystemExit(1)
if strict and (result['fixedInput']['seeds']!=[418,418] or not result['fixedInput']['sameInitialStreams'] or not result['fixedInput']['weaponConfigurationEqual']):raise SystemExit(1)
