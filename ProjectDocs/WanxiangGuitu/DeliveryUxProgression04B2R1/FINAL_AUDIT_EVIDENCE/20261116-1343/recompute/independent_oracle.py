#!/usr/bin/env python3
"""New independent read-only oracle; no import/exec of historical verifier or game.
Run from workspace root with python -B. Writes exclusively beside this script.
Computations use primitive binary32 operations, asset scalars, and original raw JSON.
"""
from pathlib import Path
import json,csv,struct,re,hashlib,copy,collections
ROOT=Path.cwd().resolve(); OUT=Path(__file__).resolve().parent
assert OUT == ROOT/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/recompute'
SESSION=ROOT/'Evidence/Runs04B2R1/SESSION-20261116-1115/A03'
NINE='GearItem Inventory EquipmentGrid Main Reserve Worn Overflow AttackPower Container'.split()
WEAPON={0,1,2,3,11,12,13}; ROLES='None Main Reserve Board Overflow Worn ContainerRig ContainerBag'.split()
rows=[]; risks=[]; snapshots=[]; strength=[]; files=[]; ctx={}
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def obj(x): return json.loads(x) if isinstance(x,str) and x[:1] in ('{','[') else x
def f(x): return struct.unpack('f',struct.pack('f',float(x)))[0]
def bit(x): return struct.pack('<f',f(x)).hex()
def plus(x,y): return f(f(x)+f(y))
def times(x,y): return f(f(x)*f(y))
def accum(values):
 s=0.
 for v in values: s=plus(s,v)
 return s
def same(a,b):
 if isinstance(a,float):
  try: return bit(a)==bit(b)
  except (ValueError,TypeError,OverflowError): return False
 return a==b
def check(name,a,b,status=None,detail=''):
 rows.append(dict(ctx,check=name,status=status or ('PASS' if same(a,b) else 'FAIL'),expected=a,actual=b,detail=detail))
def tree(name,a,b):
 if isinstance(a,dict):
  check(name+'.keys',True,isinstance(b,dict) and set(a)<=set(b))
  for k,v in a.items(): tree(name+'.'+k,v,b.get(k) if isinstance(b,dict) else None)
 else: check(name,a,b)
def note(name,detail,expected=None,actual=None): check(name,expected,actual,'INFO',detail)
def units(s):
 b=s.encode('utf-16-le','surrogatepass')
 return struct.unpack('<'+'H'*(len(b)//2),b)
def fnv(s):
 h=0xcbf29ce484222325
 for n in units(s): h=((h^n)*0x100000001b3)&((1<<64)-1)
 return format(h,'016x')
def asset(p):
 d={}
 for line in p.read_text(encoding='utf-8-sig').splitlines():
  m=re.fullmatch(r'  (\w+):\s*(.*?)\s*',line)
  if not m: continue
  k,v=m.groups()
  try: d[k]=json.loads(v)
  except ValueError: d[k]=v
 return d
assets={}
for folder,key in [('ItemData','definitionId'),('QualityData','quality'),('ContainerData','definitionId')]:
 assets[folder]={}
 for p in sorted((ROOT/'Assets/CombatPrototype/Resources'/folder).glob('*.asset')):
  d=asset(p); assets[folder][d[key]]=d
  files.append(dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),kind='asset'))

def stats(i):
 if i['dataRevision']>0: return f(i['savedAttack']),f(i['savedDefense'])
 t=int(i['type']); q=(8,19,43,78,132)[int(i['quality'])]; tier=int(i['legacyTier'])
 if t in WEAPON: return f(tier*15 if tier>0 else q),0.
 atk=times(q,.35) if t==6 else times(q,.5) if t==8 else 0.
 defense=f(tier*5) if tier>0 else times(q,.4 if t==4 else .3 if t==5 else .2) if t not in (9,10) else 0.
 return atk,defense

def model(r):
 main_index=next((n for n,i in enumerate(r['items']) if i and r['main'] and i['id']==r['main'] and i['type'] in WEAPON and not(i['board'] or i['worn'] or i['overflow'])),None)
 seen=set(); active=[]
 for n,i in enumerate(r['items']):
  if i is None or (i['id'] or '') in seen: continue
  seen.add(i['id'] or '')
  if not(i['worn'] or i['overflow']) and (i['board'] or n==main_index): active.append((n,i))
 a=accum(stats(i)[0] for _,i in active); d=accum(stats(i)[1] for _,i in active if i['board'])
 # container bonuses are added to attack exactly once, not both in Active and again here.
 for slot in ('rig','bag'):
  a=plus(a,(r[slot] or {}).get('attackBonus',0)); d=plus(d,(r[slot] or {}).get('defenseBonus',0))
 rank=f(int(r['rank'])*5); attack=plus(plus(r['baseDamage'],a),rank)
 wt=r['items'][main_index]['type'] if main_index is not None else 0
 return dict(baseDamage=f(r['baseDamage']),progressionBonus=rank,loadoutAttack=a,loadoutDefense=d,attackPower=attack,basicPower=times(attack,1.25 if wt==1 else 1),mainContribution=accum(stats(i)[0] for n,i in active if n==main_index),reserveContribution=accum(stats(i)[0] for _,i in active if r['reserve'] and i['id']==r['reserve']),accessoryContribution=accum(stats(i)[0] for _,i in active if i['type']==8),armsContribution=accum(stats(i)[0] for _,i in active if i['type']==6),boardContribution=accum(stats(i)[0] for _,i in active if i['board']),containerBonus=plus((r['rig'] or {}).get('attackBonus',0),(r['bag'] or {}).get('attackBonus',0)),weaponType=wt,activeCount=len(active))

def preview(r,c,role,replace_container=False):
 before=model(r); after=before; feasible=True; reason=''
 if c is not None and role:
  r=copy.deepcopy(r); c=copy.deepcopy(c); r['items']=[i for i in r['items'] if i['id']!=c['id']]
  if role==1:
   if c['type'] not in WEAPON: feasible=False; reason='候选不是武器，不能设为主武器'
   else:
    c.update(board=False,worn=False,overflow=False)
    if c['id']==r['reserve']: r['reserve']=r['main']
    r['main']=c['id']
  elif role==2:
   if c['type'] not in WEAPON or c['id']==r['main']: feasible=False; reason='候选不能设为备用武器'
   else: c.update(board=False,worn=False,overflow=False); r['reserve']=c['id']
  elif role==3:
   if c['type'] in (9,10) or c['id'] in (r['main'],r['reserve']): feasible=False; reason='容器或携带中的武器不能放入装备盘'
   else: c.update(board=True,worn=False,overflow=False)
  elif role==4: c.update(board=False,worn=False,overflow=True,x=-1,y=-1)
  elif role in (5,6,7):
   if c['type'] not in (9,10): feasible=False; reason='候选不是容器，不能穿戴'
   else:
    c.update(board=False,worn=True,overflow=False,x=-1,y=-1)
    if replace_container:
     for i in r['items']:
      if i['type']==c['type']: i['worn']=False
  if feasible:
   r['items'].append(c)
   for slot,t,default in [('rig',9,'rig_standard'),('bag',10,'bag_standard')]:
    worn=next((i for i in r['items'] if i['worn'] and i['type']==t),None)
    r[slot]=assets['ContainerData'][worn['definitionId'] if worn else default]
   after=model(r)
 return dict(before=before,after=after,deltaAttackPower=plus(after['attackPower'],-before['attackPower']),deltaBasicPower=plus(after['basicPower'],-before['basicPower']),deltaLoadoutAttack=plus(after['loadoutAttack'],-before['loadoutAttack']),itemAttack=stats(c)[0] if c else 0.,itemDefense=stats(c)[1] if c else 0.,role=role,feasible=feasible,reason=reason)

def display(i): return str(assets['QualityData'][i['quality']]['displayName'])+'·'+str(assets['ItemData'][i['definitionId']]['displayName'])
def sort_ids(o,r):
 spec=obj(o.get('spec',o.get('key',o.get('FilterKey',o.get('CurrentKey')))))
 if isinstance(spec,dict):
  names=[('category',['All','Weapon','Accessory','Arms','Armor','Container','Other']),('status',['All','Main','Reserve','Worn','Board','Unused','Overflow','Warehouse']),('sort',['None','AttackDesc','AttackAsc','QualityDesc','QualityAsc','TypeAsc','NameAsc'])]
  d=dict(spec)
  for k,ns in names:
   if isinstance(d.get(k),str): d[k]=ns.index(d[k])
  cat,mask,st,sort,fav,text=d.get('category',0),d.get('qualityMask',0),d.get('status',0),d.get('sort',0),d.get('favoritesOnly',False),d.get('text','')
 else:
  parts=spec.split('|',5); cat,mask,st,sort,fav=map(int,parts[:5]); text=parts[5]
 selected=[]; favorites=obj(o.get('favoriteIds',r.get('favoriteIds',[])))
 if fav and not favorites: raise ValueError('missing favoriteIds')
 for i in r['items']:
  t=i['type']; ic=5 if t in (9,10) else 1 if t in WEAPON else 2 if t==8 else 3 if t==6 else 4 if t in (4,5,7) else 6
  ist=3 if i['worn'] else 6 if i['overflow'] else 4 if i['board'] else 1 if i['id']==r['main'] else 2 if i['id']==r['reserve'] else 5
  if (cat and ic!=cat) or (mask and not(mask&(1<<i['quality']))) or (st and st!=ist) or (fav and i['id'] not in favorites) or (text and text.lower() not in display(i).lower()): continue
  selected.append(i)
 if sort:
  def key(i):
   v={1:lambda:-stats(i)[0],2:lambda:stats(i)[0],3:lambda:-i['quality'],4:lambda:i['quality'],5:lambda:i['type'],6:lambda:units(display(i))}[sort]()
   return v,units(i['id'])
  selected.sort(key=key)
 return [i['id'] for i in selected]

def idlist(v):
 if isinstance(v,list): return v
 if v.startswith('['): return json.loads(v)
 return v.split('|' if '|' in v else ',') if v else []

run_metrics=[]
for manifest in sorted(SESSION.glob('*/run-manifest.json')):
 m=load(manifest); directory=manifest.parent; ctx=dict(mode=m['mode'],runId=m['runId'],seq=None)
 for key,val in [('exitCode',0),('completeFlag','PASS'),('timedOut',False),('forcedTermination',False),('verdict','PLAYER_RUN_COMPLETED')]: check('manifest.'+key,val,m.get(key))
 for rel,expected in m['files'].items():
  p=(directory/rel).resolve(); check('file.safe.'+rel,True,p.is_relative_to(directory.resolve()))
  if not p.is_relative_to(directory.resolve()): continue
  data=p.read_bytes(); digest=hashlib.sha256(data).hexdigest()
  check('file.bytes.'+rel,expected['bytes'],len(data)); check('file.sha256.'+rel,expected['sha256'].lower(),digest)
  files.append(dict(path=p.relative_to(ROOT).as_posix(),bytes=len(data),sha256=digest,kind='manifest'))
 check('manifest.coverage',sorted(m['files']),sorted(p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file() and p!=manifest))
 observations=[json.loads(line) for line in (directory/'r1-observations.jsonl').read_text(encoding='utf-8-sig').splitlines() if line.strip()]
 metrics=dict(mode=m['mode'],observations=len(observations),raw=0,MainEvaluations=0,nonMainEvaluations=0,sort=0,preview9=0)
 for o in observations:
  ctx=dict(mode=m['mode'],runId=m['runId'],seq=o['seq'],stage=o['stage']); r=obj(o.get('raw'))
  if r is None:
   note('raw.boot-not-initialized','No initialized hero at boot; not PASS'); continue
  metrics['raw']+=1; s=model(r)
  snapshots.append(dict(ctx,**s))
  for k in ('attackPower','basicPower'): check('D24.live.'+k,s[k],r[k])
  check('Strength.bonus',s['progressionBonus'],r['bonus'])
  for published,key in [('AttackPower','attackPower'),('GearAttack','loadoutAttack'),('GearDefense','loadoutDefense'),('AttackBonus','progressionBonus')]:
   if published in o: check('D24.published.'+published,s[key],o[published])
  for slot in ('rig','bag'):
   if r[slot]:
    source=assets['ContainerData'][r[slot]['definitionId']]
    for k in ('attackBonus','defenseBonus'): check(slot+'.asset.'+k,f(source[k]),r[slot][k])
  for group in ('items','warehouse'):
   for n,i in enumerate(r[group]):
    a,d=stats(i)
    for k,v in [('derivedAttack',a),('derivedDefense',d)]:
     if k in i: check(group+'.'+str(n)+'.'+k,v,i[k])
    if i['dataRevision']>0 and i['legacyTier']<=0 and i['origin']!=3 and not (i['originRunId'] or '').lower().startswith('legacy'):
     definition=assets['ItemData'][i['definitionId']]; q=assets['QualityData'][i['quality']]
     for k,factor in [('savedAttack','attackFactor'),('savedDefense','defenseFactor')]: check(group+'.'+str(n)+'.asset.'+k,0. if i['type'] in (9,10) else times(q['power'],definition[factor]),i[k])
  if o['stage']=='strength': strength.append(dict(ctx,rank=r['rank'],main=r['main'],attackPower=s['attackPower'],basicPower=s['basicPower'],progressionBonus=s['progressionBonus'],loadoutAttack=s['loadoutAttack'],note=o.get('note')))
  if o['stage']=='sort':
   metrics['sort']+=1; expected=sort_ids(o,r)
   if 'publishedIds' in o: check('sort.publishedIds',expected,idlist(o['publishedIds']))
   else: note('sort.no-structured-publishedIds','Do not promote note text to published evidence',expected,{'FilterKey':o.get('FilterKey'),'SortKey':o.get('SortKey')})
   if 'renderedIds' in o: check('sort.renderedIds',expected,idlist(o['renderedIds']))
  if o['stage']=='preview9':
   metrics['preview9']+=1
   before=obj(o['beforeJson']); after=obj(o['afterJson']); cb=obj(o['canonicalBeforeJson']); ca=obj(o['canonicalAfterJson'])
   for name,value in [('before',before),('after',after),('canonicalBefore',cb),('canonicalAfter',ca),('rawCanonical',r['canonical'])]: check('C06.keys.'+name,sorted(NINE),sorted(value))
   for k in NINE:
    check('C06.hash.unchanged.'+k,before[k],after[k]); check('C06.plaintext.unchanged.'+k,cb[k],ca[k]); check('FNV.before.'+k,fnv(cb[k]),before[k]); check('FNV.after.'+k,fnv(ca[k]),after[k]); check('C06.rawCanonical.'+k,ca[k],r['canonical'][k])
  if 'evaluationJson' in o:
   ev=obj(o['evaluationJson']); c=obj(o.get('candidateJson')); role=ev['role']; role=ROLES.index(role) if isinstance(role,str) else role
   prediction=preview(r,c,role); check('preview.candidateId',c['id'] if c else None,o.get('candidateId'))
   if role==1: metrics['MainEvaluations']+=1; tree('Main',prediction,ev)
   else:
    metrics['nonMainEvaluations']+=1; tree('nonMain.before',prediction['before'],ev['before'])
    for k in ('role','itemAttack','itemDefense','feasible','reason'): check('nonMain.'+k,prediction[k],ev[k])
    ideal=preview(r,c,role,True); differences={k:dict(expected=ideal['after'][k],actual=ev['after'].get(k)) for k in ideal['after'] if not same(ideal['after'][k],ev['after'].get(k))}
    risks.append(dict(ctx,role=role,candidate=c,asImplemented=prediction,intendedReplacement=ideal,recorded=ev,intendedAfterDifferences=differences))
    note('preview.non-Main-after-not-targeted','C06 read-only only; independent numerical diagnostics retained, not promoted to PASS.',ideal,ev)
 run_metrics.append(metrics)
# Historical checks are counted as evidence, never used as numerical oracle.
hist=ROOT/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/EVIDENCE/recompute-A03'
historical=load(hist/'details.json')['checks']
with (hist/'checks.csv').open(encoding='utf-8-sig',newline='') as stream: historical_csv=list(csv.DictReader(stream))
hcounts=dict(collections.Counter(x['status'] for x in historical)); ccounts=dict(collections.Counter(x['status'] for x in historical_csv))
ctx={'mode':'historical-classification'}
check('historical.counts.expected',{'PASS':23191,'INFO':20},hcounts); check('historical.csv.counts',hcounts,ccounts); check('historical.csv.length',len(historical),len(historical_csv))
check('historical.row.identity',[(x.get('runId',''),x['check'],x['status']) for x in historical],[(x.get('runId',''),x['check'],x['status']) for x in historical_csv])
info_rows=[x for x in historical if x['status']=='INFO']; info_counts=dict(collections.Counter(x['check'] for x in info_rows))
check('historical.INFO.classification',{'raw.boot-not-initialized':9,'sort.no-structured-publishedIds':4,'preview.non-Main-after-not-targeted':7},info_counts)
history=dict(count=len(historical),counts=hcounts,csvCounts=ccounts,byMode={mode:dict(collections.Counter(x['status'] for x in historical if x.get('mode')==mode)) for mode in sorted({x.get('mode','asset/session') for x in historical})},infoCounts=info_counts,infoRows=info_rows)
counts=dict(collections.Counter(x['status'] for x in rows)); summary=dict(oracle='new-independent-raw-asset-binary32',runs=run_metrics,counts=counts,historicalCounts=hcounts,historicalInfoCounts=info_counts,files=len(files),assets=sum(x['kind']=='asset' for x in files),strength=strength,numericalRiskCases=[{'mode':r['mode'],'seq':r['seq'],'role':r['role'],'differences':r['intendedAfterDifferences']} for r in risks if r['intendedAfterDifferences']],limitations=['Canonical Inventory lacks complete raw fields: supplied UTF16 plaintext hash verified, not independently reconstructed.','Current source assets hashed; does not alone establish Player build provenance.','Non-Main after numerical semantics excluded from C06; replacement diagnostic separate from acceptance failures.'])
for name,data in [('oracle_summary.json',summary),('oracle_details.json',rows),('oracle_failures.json',[x for x in rows if x['status']=='FAIL']),('oracle_nonmain_risks.json',risks),('oracle_files_sha256.json',files),('oracle_snapshots.json',snapshots),('historical_classification.json',history)]:
 p=OUT/name
 if p.exists(): raise RuntimeError('refuse overwrite '+str(p))
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+chr(10),encoding='utf-8')
with (OUT/'oracle_checks.csv').open('x',encoding='utf-8-sig',newline='') as stream:
 writer=csv.DictWriter(stream,fieldnames=['mode','runId','seq','stage','check','status','expected','actual','detail']); writer.writeheader()
 for row in rows: writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list,tuple)) else v for k,v in row.items()})
print(json.dumps(summary,ensure_ascii=False,indent=2))
