"""Read-only R1 publication/input audit. Never edits a save or a test receipt."""
from pathlib import Path
import json,sys,hashlib,subprocess,csv
root=Path(sys.argv[1]);repo=Path(sys.argv[2]);base=repo/'ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01R1'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def norm(b):return b.replace(b'\r\n',b'\n')
rel='Assets/CombatPrototype/ForestBossBrain.cs';current=(repo/rel).read_bytes()
old=subprocess.check_output(['git','-C',str(repo),'show','b040b550a5725511a34867de4a2cb27dc56a2b95:'+rel])
expected=old.replace(b'void OnDisable(){CancelIntent();if(enemy!=null)enemy.ClearReleasedThreat();}',b'void OnDisable(){CancelIntent();}')
inputs={r['path'].replace('\\','/'):r for r in read(root/'PureBuildFinal/build-inputs.json')}
okay=norm(current)==norm(expected) and sha(current)==inputs[rel]['sha256'].lower()
product=[dict(path=rel,finalCanonicalLF=sha(norm(current)),finalRawSHA256=sha(current),baselineCanonicalLF=sha(norm(old)),pureBuildSHA256=inputs[rel]['sha256'],status='PASS' if okay else 'FAIL')]
user=[]
for r in read(root/'user-before.json'):
 after=sha(Path(r['Path']).read_bytes());user.append(dict(path=r['Path'],before=r['Hash'],after=after,status='PASS' if after==r['Hash'].lower() else 'FAIL'))
history=subprocess.check_output(['git','-C',str(repo),'diff','--name-only','b040b550a5725511a34867de4a2cb27dc56a2b95','--','ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01']).decode().strip()
rows=[];results=[]
for phase,seeds in [('BeforeClear',[418,419]),('AfterClear',[418,419,420])]:
 for seed in seeds:
  store=root/f'{phase}{seed}Store';j=read(store/'r1.json');checks=j['checks']
  results.append(dict(phase=phase,seed=seed,passCount=sum(c['status']=='PASS' for c in checks),failCount=sum(c['status']=='FAIL' for c in checks),scope=j['scope']))
  for c in checks:rows.append(dict(phase=phase,seed=seed,**c))
paired=[]
for seed in [418,419]:
 a=root/f'BeforeClear{seed}';b=root/f'AfterClear{seed}'
 same=(a/'EncaiR1.cs.txt').read_bytes()==(b/'EncaiR1.cs.txt').read_bytes()
 lanesA=(root/f'BeforeClear{seed}Store/initial-lanes.jsonl').read_bytes()
 lanesB=(root/f'AfterClear{seed}Store/initial-lanes.jsonl').read_bytes()
 # Same requested seed, deterministic bounded candidate selection and final poses.
 lanesEqual=lanesA==lanesB
 configsEqual=read(root/f'BeforeClear{seed}Store/r1-config.json')==read(root/f'AfterClear{seed}Store/r1-config.json')
 paired.append(dict(seed=seed,driverSHA256=sha((a/'EncaiR1.cs.txt').read_bytes()),sameDriver=same,sameConfig=configsEqual,sameInitialLanes=lanesEqual,status='PASS' if same and configsEqual and lanesEqual else 'FAIL'))
with (base/'RESULTS.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['phase','seed','sample','name','status','detail']);w.writeheader();w.writerows(rows)
allOkay=okay and not history and all(r['status']=='PASS' for r in user+paired) and all(r['failCount']==0 and r['passCount']==80 for r in results if r['phase']=='AfterClear')
binding=dict(status='PASS' if allOkay else 'FAIL',baseline='b040b550a5725511a34867de4a2cb27dc56a2b95',productSources=product,userFiles=user,oldDeliveryDiff=history,paired=paired,results=results,scope='Only one lifecycle call removed; old delivery untouched; final pure build bytes and final fixed-fixture pairs checked. Historical FAIL retained separately, not reclassified.')
(root/'input-binding.json').write_text(json.dumps(binding,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(status=binding['status'],results=results,paired=paired,userFiles=len(user)),ensure_ascii=False))
if not allOkay:raise SystemExit(1)
