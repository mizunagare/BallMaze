"""Independently reassert remaining structural/receipt checks from original inputs.
No historical expected/actual/status is used to derive a check result.
Historical mapping is performed only after all independent evidence is calculated.
"""
from pathlib import Path
import json,csv,collections,re
R=Path.cwd(); O=Path(__file__).parent; S=R/'Evidence/Runs04B2R1/SESSION-20261116-1115/A03'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
rows=[]; ctx={}
def check(k,e,a): rows.append(dict(ctx,check=k,expected=e,actual=a,status='PASS' if e==a else 'FAIL'))
def present(k,v): check(k,True,v)
ITEM_FIELDS='origin originRunId id affixes type quality x y board legacyTier definitionId dataRevision rotation widthOverride heightOverride overflow worn savedAttack savedDefense'.split()
RAW_FIELDS='items warehouse rig bag baseDamage rank bonus attackPower basicPower main reserve canonical'.split()
CONTAINER_FIELDS='definitionId displayName description type quality width height blockedCells moveBonus attackBonus defenseBonus harvestBonus woodCost hideCost oreCost'.split()
SNAPSHOT_FIELDS='baseDamage progressionBonus loadoutAttack loadoutDefense attackPower basicPower mainContribution reserveContribution accessoryContribution armsContribution boardContribution containerBonus weaponType activeCount'.split()
assets={}
for folder,key in [('ItemData','definitionId'),('QualityData','quality'),('ContainerData','definitionId')]:
 paths=list((R/'Assets/CombatPrototype/Resources'/folder).glob('*.asset')); present('asset-source-'+folder,bool(paths)); assets[folder]={}
 for p in paths:
  scalars={}
  for line in p.read_text(encoding='utf-8-sig').splitlines():
   if not line.startswith('  ') or line.startswith('    ') or ':' not in line: continue
   k,v=line.strip().split(':',1); v=v.strip()
   try: scalars[k]=json.loads(v)
   except ValueError: scalars[k]=v
  assets[folder][scalars[key]]=scalars
present('session.exists',S.is_dir()); manifests=sorted(S.glob('*/run-manifest.json')); present('session.manifests.nonempty',bool(manifests)); seen=set()
for p in manifests:
 m=read(p); d=p.parent; ctx=dict(runId=m.get('runId'),mode=m.get('mode'))
 present('manifest.runId',isinstance(m.get('runId'),str) and bool(m['runId'])); present('manifest.pid',isinstance(m.get('pid'),int) and m['pid']>0)
 present('manifest.files.nonempty',isinstance(m.get('files'),dict) and bool(m['files']))
 for rel in m.get('files',{}):
  target=(d/rel).resolve()
  if target.is_relative_to(d.resolve()): present('file.exists:'+rel,target.is_file())
 result=d/'result.json'; present('result.exists',result.is_file())
 if result.is_file():
  r=read(result); check('result.manifest-copy',m.get('resultJson'),r)
  for k in ('runId','mode'):
   if k in r: check('result.'+k,m.get(k),r[k])
  verdict=r.get('result',r.get('overall',r.get('status',r.get('pass',r.get('success')))))
  present('result.success',verdict is True or verdict=='PASS')
  if 'failed' in r: check('result.failed',0,r['failed'])
  if isinstance(r.get('checks'),int):
   check('result.check-count',len(r.get('detail',[])),r['checks']); check('result.passed-count',sum(x.get('result')=='PASS' for x in r.get('detail',[])),r.get('passed'))
  details=r.get('detail',r.get('checks',[])); details=details if isinstance(details,list) else []
  for n,c in enumerate(details):
   ok=not c.upper().startswith('FAIL') if isinstance(c,str) else c.get('result',c.get('status',c.get('pass'))) in ('PASS',True)
   present('result.check.'+str(n),ok)
 command=d/'Player.command.json'
 if command.is_file():
  c=read(command)
  for k in ('runId','mode','buildId'): check('command.'+k,m.get(k),c.get(k))
  if 'pid' in c: check('command.pid',m.get('pid'),c['pid'])
 ip=d/'r1-input-events.jsonl'
 if not ip.is_file():
  candidates=list(d.glob('*input*.jsonl'))
  if len(candidates)==1: ip=candidates[0]
 present('input.raw-file.exists',ip.is_file())
 events=[json.loads(x) for x in ip.read_text(encoding='utf-8-sig').splitlines() if x.strip()] if ip.is_file() else []
 kinds={e.get('kind') for e in events}; mode=m['mode'].lower()
 required=set() if any(x in mode for x in ('guid','golden','strength','restart')) else {'native-mouse-down','native-mouse-up','native-window'} if 'imgui' in mode else {'mouse-down','mouse-up','ugui-raycast'}
 for kind in sorted(required): present('input.kind.'+kind,kind in kinds)
 for e in events:
  if e.get('kind')=='native-window':
   vals={}
   for fragment in e.get('detail','').split():
    if '=' in fragment:
     key,val=fragment.split('=',1)
     if key in ('ownPid','windowPid','foregroundPid') and val.isdigit(): vals[key]=int(val)
   for k in ('ownPid','windowPid','foregroundPid'): check('input.'+k,m.get('pid'),vals.get(k))
 op=d/'r1-observations.jsonl'; present('observations.exists',op.is_file())
 obs=[json.loads(x) for x in op.read_text(encoding='utf-8-sig').splitlines() if x.strip()] if op.is_file() else []
 present('observations.nonempty',bool(obs)); raw_count=0
 for o in obs:
  ctx=dict(runId=m.get('runId'),mode=m.get('mode'),seq=o.get('seq'),stage=o.get('stage'))
  check('observation.runId',m.get('runId'),o.get('runId'))
  if 'raw' in o: raw_count+=1
  raw=o.get('raw'); raw=json.loads(raw) if isinstance(raw,str) else raw
  if raw is None and o.get('stage')=='boot': continue
  present('raw.exists',isinstance(raw,dict))
  if not isinstance(raw,dict): continue
  present('raw.fields',set(RAW_FIELDS)<=set(raw)); present('live.fields',{'attackPower','basicPower'}<=set(raw))
  for slot in ('rig','bag'):
   c=raw[slot]
   if c is not None:
    present(slot+'.fields',set(CONTAINER_FIELDS)<=set(c)); present(slot+'.asset-source',c.get('definitionId') in assets['ContainerData'])
  for group in ('items','warehouse'):
   for n,i in enumerate(raw[group]):
    name=group+'['+str(n)+':'+str(i.get('id'))+']'
    present(name+'.fields',set(ITEM_FIELDS)<=set(i))
    if i['dataRevision']>0 and i['legacyTier']<=0 and i['origin']!=3 and not str(i['originRunId'] or '').lower().startswith('legacy'):
     present(name+'.asset-source',i['definitionId'] in assets['ItemData'] and i['quality'] in assets['QualityData'])
 present('run.raw-input.present',raw_count>0)
 ctx={'runId':m.get('runId')}; present('session.runId.unique',m.get('runId') not in seen); seen.add(m.get('runId'))
# Map only to old rows NOT mapped by numerical oracle; no old values drive assertions.
historical=read(R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/EVIDENCE/recompute-A03/details.json')['checks']
prior=read(O/'historical_oracle_mapping.json')['mapping']; byold={x['historicalRowIndex']:x for x in prior}
index=collections.defaultdict(list)
for n,x in enumerate(rows): index[(x.get('runId'),x.get('mode'),x.get('seq'),x['check'])].append((n,x))
mapping=[]; remaining=[]
for n,x in enumerate(historical):
 if byold[n]['classification']!='NOT_REASSERTED_BY_NEW_ORACLE': continue
 evidence=index.get((x.get('runId'),x.get('mode'),x.get('seq'),x['check']),[])
 record=dict(historicalRowIndex=n,mode=x.get('mode'),runId=x.get('runId'),seq=x.get('seq'),check=x['check'],classification='INDEPENDENTLY_REASSERTED' if evidence and all(z['status']=='PASS' for _,z in evidence) else 'REMAINING_NOT_MAPPED',evidence=[dict(oracleRowIndex=i,status=z['status']) for i,z in evidence])
 mapping.append(record)
 if record['classification']=='REMAINING_NOT_MAPPED': remaining.append(record)
summary=dict(assertionCounts={k:sum(x['status']==k for x in rows) for k in ('PASS','FAIL','INFO')},mappingCounts=dict(collections.Counter(x['classification'] for x in mapping)),remainingUniqueChecks=dict(collections.Counter(x['check'] for x in remaining)),scope='Supplement independent structural and receipt assertions only. No historical expected/actual values used; original PASS flag is not proof. Inventory canonical reconstruction limitation unaffected.')
for name,data in [('supplemental_structure_details.json',rows),('supplemental_structure_summary.json',summary),('supplemental_structure_mapping.json',mapping),('supplemental_remaining.json',remaining)]:
 dest=O/name
 if dest.exists(): raise RuntimeError('refuse overwrite '+str(dest))
 dest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+chr(10),encoding='utf-8')
with (O/'supplemental_structure_checks.csv').open('x',encoding='utf-8-sig',newline='') as s:
 w=csv.DictWriter(s,fieldnames=['runId','mode','seq','stage','check','expected','actual','status']); w.writeheader()
 for r in rows: w.writerow(r)
print(json.dumps(summary,ensure_ascii=False,indent=2))
