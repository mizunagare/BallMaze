"""Read-only independent B2 golden replay; output restricted to this directory."""
import json,re,struct,hashlib,csv,copy,subprocess
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=Path.cwd()
HEAD='95caf234256613d4a6e4f89a8ab0dc09c397c6b2'
inputs={}
def raw(p):
 p=Path(p); b=p.read_bytes(); inputs[p.as_posix()]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}; return b
def load(p):return json.loads(raw(p).decode('utf-8-sig'))
def text(p):return raw(p).decode('utf-8-sig')
def f(x):return struct.unpack('<f',struct.pack('<f',x))[0]
def bits(x):return struct.unpack('<I',struct.pack('<f',x))[0]
def asset(folder,name):
 p=f'Assets/CombatPrototype/Resources/{folder}/{name}.asset'; t=text(p)
 old=subprocess.run(['git','show',HEAD+':'+p],capture_output=True,check=True).stdout
 inputs[p]['equals_old_HEAD']=raw(p)==old
 return {k:float(v) for k,v in re.findall(r'^  (power|attackFactor|defenseFactor|attackBonus|defenseBonus): ([-.0-9]+)$',t,re.M)}
qs=['White','Green','Purple','Gold','Red']; powers=[asset('QualityData',q)['power'] for q in qs]
names=['sword','spear','staff','bow','armor','trousers','arms','boots','accessory','rig_standard','bag_standard','weapon_twin_blades','weapon_greatsword','weapon_scythe']
defs={t:asset('ItemData',names[t]) for t in [0,1,2,3,6,8,11,12,13]}
containers={n:asset('ContainerData',n) for n in ['rig_standard','bag_standard','rig_heavy','bag_relic']}
payload=json.loads(load('Evidence/Runs04B2/UX04-B2-GOLDEN-FINAL/isolated-save/save.json')['payload'])
camp=payload['profile']['camp']; base=camp['gear']; main0=camp['mainWeapon']
observations=[json.loads(l) for l in text('Evidence/Runs04B2/UX04-B2-GOLDEN-FINAL/b2-observations.jsonl').splitlines() if l]
entry=next(r for r in observations if r['stage']=='entry')
assert len(base)==int(entry['Inventory_count'])==8 and entry['Main']==main0
assert camp['skills'][0]==0
for p in ['Assets/CombatPrototype/ThirdPersonHero.cs','Assets/CombatPrototype/AdventureCombat.cs','Assets/CombatPrototype/HeroProgression.cs','Assets/CombatPrototype/NewWeaponRegistry.cs','ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2/Tools/IntDriverB2.cs']:
 text(p)
for n in ['AdventureLoadout','AdventureItems']:text(OUT/f'old_HEAD_{n}.cs.txt')

def new(t,q):
 a=defs[t]; return dict(id='independent-candidate',type=t,quality=q,board=False,worn=False,overflow=False,dataRevision=1,savedAttack=f(f(powers[q])*f(a['attackFactor'])),savedDefense=f(f(powers[q])*f(a['defenseFactor'])))
def weapon(t):return t<4 or 11<=t<=13
def calc(items,main,rig,bag):
 m=next((i for i in items if i['id']==main and not any(i[k] for k in ['board','worn','overflow']) and weapon(i['type'])),None)
 seen=set(); active=[]
 for i in items:
  if i['id'] in seen:continue
  seen.add(i['id'])
  if not i['overflow'] and not i['worn'] and (i['board'] or i is m):active.append(i)
 # Enumerable.Sum(float) uses double accumulation then casts once; also compute product sequential float32.
 la=f(sum(f(i['savedAttack']) for i in active)); ld=f(sum(f(i['savedDefense']) for i in active if i['board']))
 seq=f(0)
 for i in active:seq=f(seq+f(i['savedAttack']))
 a=f(f(la+f(rig['attackBonus']))+f(bag['attackBonus'])); d=f(f(ld+f(rig['defenseBonus']))+f(bag['defenseBonus']))
 sa=f(f(seq+f(rig['attackBonus']))+f(bag['attackBonus']))
 ap=f(f(f(25)+a)+f(camp['skills'][0]*5)); bp=f(ap*f(1.25 if m and m['type']==1 else 1))
 return a,d,ap,bp,active,la,sa
rows=[]
for obs in [r for r in observations if 'goldenName' in r]:
 name=obs['goldenName']; items=copy.deepcopy(base); main=main0; rig=containers['rig_standard']; bag=containers['bag_standard']; cand=None
 if name.startswith('main-'):cand=new(0,qs.index(name[5:])); main=cand['id']
 elif name.startswith('weapon-'):
  t={'Sword':0,'Spear':1,'Staff':2,'Bow':3,'TwinBlades':11,'Greatsword':12,'Scythe':13}[name[7:]];cand=new(t,2); main=cand['id']
 elif name.startswith('board-'):cand=new(8 if name.endswith('Accessory') else 6,4);cand['board']=True
 elif name=='reserve-red':cand=new(0,4)
 elif name.startswith('state-'):
  cand=new(0,3); state=name[6:];cand['board']=state=='Board';cand['overflow']=state=='Overflow';cand['worn']=state=='Worn'
 elif name=='container-bonus':rig=containers['rig_heavy'];bag=containers['bag_relic']
 else:assert name=='baseline'
 if cand:items.append(cand)
 a,d,ap,bp,active,active_sum,seq=calc(items,main,rig,bag)
 # AP/BP in original B2 are only 0.### text, not persisted IEEE bit fields. Do NOT claim bit-exact AP proof.
 note=obs['note']; oa=float(re.search(r'attackPower=([0-9.]+)',note)[1]);ob=float(re.search(r'basicPower=([0-9.]+)',note)[1])
 row=dict(name=name,observation_seq=obs['seq'],active_ids=[i['id'] for i in active],candidate=cand,active_sum=active_sum,rig_attack=rig['attackBonus'],bag_attack=bag['attackBonus'],attack=a,attack_bits=bits(a),legacy_bits=int(obs['legacyBits']),unified_bits=int(obs['unifiedBits']),defense=d,defense_bits=bits(d),legacy_defense_bits=int(obs['legacyDefenseBits']),unified_defense_bits=int(obs['unifiedDefenseBits']),AP=ap,AP_bits=bits(ap),BP=bp,BP_bits=bits(bp),AP_observed_text=oa,BP_observed_text=ob)
 row['attack_bits_match']=row['attack_bits']==row['legacy_bits']==row['unified_bits']==bits(seq)
 row['defense_bits_match']=row['defense_bits']==row['legacy_defense_bits']==row['unified_defense_bits']
 row['AP_BP_text_match']=abs(ap-oa)<0.0005 and abs(bp-ob)<0.0005
 rows.append(row)
assert len(rows)==21
manifest_rows=[]
for mode in ['GOLDEN','UGUI','IMGUI','FAVSEED','RESTART','READBACK']:
 p=Path(f'Evidence/Runs04B2/UX04-B2-{mode}-FINAL/run-manifest.json');m=load(p); checks=[]
 for rel,expected in m['files'].items():
  file=p.parent/rel; b=raw(file); checks.append(dict(path=file.as_posix(),size_ok=len(b)==expected['bytes'],hash_ok=hashlib.sha256(b).hexdigest()==expected['sha256']))
 complete=text(p.parent/'b2-complete.txt').strip(); obs=[json.loads(l) for l in text(p.parent/'b2-observations.jsonl').splitlines() if l]
 errors=[r for r in obs if r.get('stage')=='error'];done=[r for r in obs if r.get('stage')=='done']
 ok=m['exitCode']==0 and m['verdict']=='PLAYER_RUN_COMPLETED' and not m['timedOut'] and not m['forcedTermination'] and complete=='PASS' and not errors and len(done)==1 and all(c['size_ok'] and c['hash_ok'] for c in checks)
 manifest_rows.append(dict(runId=m['runId'],mode=m['mode'],exitCode=m['exitCode'],verdict=m['verdict'],pid=m['pid'],buildId=m['buildId'],dllSHA256=m['dllSHA256'],driverDllSHA256=m['driverDllSHA256'],files_checked=len(checks),checks=checks,observations=len(obs),errors=len(errors),complete=complete,pass_checks=ok))
result=dict(scope='original B2 only; no A03 recompute',old_HEAD=HEAD,counts=dict(golden_rows=len(rows),attack_bit_pass=sum(r['attack_bits_match'] for r in rows),defense_bit_pass=sum(r['defense_bits_match'] for r in rows),AP_BP_text_pass=sum(r['AP_BP_text_match'] for r in rows),manifest_pass=sum(r['pass_checks'] for r in manifest_rows),manifest_files=sum(r['files_checked'] for r in manifest_rows)),limitations=['Candidate GUIDs/affixes were not persisted per synthetic row. Rebuilt from original driver type/quality/state inputs and unchanged HEAD assets; IDs replaced with unique placeholder; affixes do not enter Attack/Defense expressions.','AP and BP output are decimal text 0.###, not original IEEE bit fields; computed bits supplied but only text equivalence can be checked.','Historical oracle first failed run and corrected script/output not found; old FINAL_AUDIT line 114 is narrative only.','No Player launch or build performed.'],baseline=dict(main=main0,gear=base,skills=camp['skills']),rows=rows,manifests=manifest_rows,inputs=inputs)
(OUT/'GOLDEN_REVIEW.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
fields=['name','observation_seq','active_sum','rig_attack','bag_attack','attack','attack_bits','legacy_bits','unified_bits','attack_bits_match','defense','defense_bits','legacy_defense_bits','unified_defense_bits','defense_bits_match','AP','AP_bits','BP','BP_bits','AP_observed_text','BP_observed_text','AP_BP_text_match']
with (OUT/'GOLDEN_REVIEW.csv').open('w',newline='',encoding='utf-8-sig') as fp:
 w=csv.DictWriter(fp,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
print(json.dumps(result['counts']))
print('manifest status:',[(r['runId'],r['pass_checks'],r['files_checked']) for r in manifest_rows])
print('asset HEAD equality:',all(v.get('equals_old_HEAD',True) for v in inputs.values()))
