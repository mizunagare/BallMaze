import json,pathlib,hashlib,subprocess
repo=pathlib.Path(__file__).resolve().parents[4];delivery=pathlib.Path(__file__).resolve().parents[1];root=pathlib.Path('I:/WGCombat/C24B1-1107-A')
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
allowed={'Assets/CombatPrototype/AdventureFlow.Bosses.cs','Assets/CombatPrototype/CombatEnemy.cs','Assets/CombatPrototype/CrystalCavernBossRewards.cs'}
rows=[]
for x in load(delivery/'Evidence/baseline-inputs.json'):
 p=repo/x['path'];actual=sha(p);same=actual==x['sha256'].upper()
 rows.append(dict(path=x['path'],before=x['sha256'],after=actual,status='PASS' if same or x['path'] in allowed else 'FAIL',authorizedChange=not same and x['path'] in allowed))
users=[]
for x in load(delivery/'Evidence/user-files-before.json'):
 current=sha(pathlib.Path(x['path']));users.append(dict(path=x['path'],before=x['after'],after=current,status='PASS' if current==x['after'] else 'FAIL'))
release=load(delivery/'Evidence/release-audit-PureBuild1.json');pure=[]
for name,x in release['files'].items():
 current=sha(root/'PureBuild1/Release'/name);pure.append(dict(path=name,sha256=current,status='PASS' if current==x['sha256'] else 'FAIL'))
output=dict(product=rows,user=users,frozenPure=pure)
(delivery/'Evidence/protection-final.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
print({k:{'count':len(v),'fail':sum(x['status']=='FAIL' for x in v)} for k,v in output.items()})
raise SystemExit(any(x['status']=='FAIL' for v in output.values() for x in v))
