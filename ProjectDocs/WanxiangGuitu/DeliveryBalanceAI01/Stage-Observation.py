"""Restore only explicitly owned test-clone source; never change source repo/user files."""
import pathlib,sys,subprocess,json,hashlib
repo=pathlib.Path(sys.argv[1]).resolve(); root=pathlib.Path(sys.argv[2]).resolve();mode=sys.argv[3]
project=root/'P/Project'
if mode not in ('before','after','clean'):raise SystemExit('before/after/clean required')
if not str(root).lower().replace('\\','/').startswith('i:/wgcombat/bal01-') or not (root/'owner.json').is_file():raise SystemExit('owned BAL01 root required')
# Caller must prove no Editor owns this project before invoking.
proc=subprocess.check_output(['powershell','-NoProfile','-Command',"@(Get-CimInstance Win32_Process -Filter \"name='Unity.exe'\" | Where-Object {$_.CommandLine -like '*"+str(project)+"*'}).Count"],text=True).strip()
if proc!='0':raise SystemExit('occupied project; no mutation')
names=['CombatEnemy','EnemyProjectile','ForestBossBrain','HeroProgression','EncounterGuard']
records=[]
for name in names:
 rel='Assets/CombatPrototype/'+name+'.cs'
 data=subprocess.check_output(['git','-C',str(repo),'show','77c4c8c3d11ac87b86ce8999cfb8dbd3e3cfdedf:'+rel]) if mode=='before' else (repo/rel).read_bytes()
 (project/rel).write_bytes(data);records.append(dict(path=rel,sha256=hashlib.sha256(data).hexdigest()))
out=root/('Source-'+mode+'.json')
# Each explicit staging operation has a unique receipt, not a rewritten historical record.
i=0
while out.exists():i+=1;out=root/('Source-'+mode+'-'+str(i)+'.json')
out.write_text(json.dumps(dict(mode=mode,files=records),indent=2),encoding='utf-8')
if mode=='clean':
 deferred=root/'DeferredObservation';i=0
 while deferred.exists():i+=1;deferred=root/('DeferredObservation-'+str(i))
 deferred.mkdir(exist_ok=False)
 for rel in ['Assets/CombatPrototype/BAL01Trace.cs','Assets/CombatPrototype/Editor/B06LocalChecks/BAL01Matrix.cs']:
  for suffix in ('','.meta'):
   p=project/(rel+suffix)
   if p.exists():p.rename(deferred/p.name)
print(mode,len(records),'explicit sources staged in owned idle clone')
