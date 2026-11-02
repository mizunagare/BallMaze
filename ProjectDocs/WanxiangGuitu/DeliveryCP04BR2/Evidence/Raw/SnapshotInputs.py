import json,hashlib
from pathlib import Path
r=Path('I:/WGCombat/CP04BR2-1102-A');out=[]
for project,role in [('Fixed','isolated Mono probe build'),('Control','isolated pure build')]:
 folder=r/project/'Project/Library/Bee'
 for p in folder.glob('Player*-inputdata.json'):
  j=json.loads(p.read_text(encoding='utf-8-sig'));found=[]
  def walk(v,path=''):
   if isinstance(v,dict):
    for k,x in v.items():
     if k=='Services':found.append({'path':path+'/'+k,'data':x})
     else:walk(x,path+'/'+k)
   elif isinstance(v,list):
    for i,x in enumerate(v):walk(x,path+'/'+str(i))
  walk(j)
  if found:out.append({'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'role':role,'services':found})
(r/'bee-services-snapshots.json').write_text(json.dumps(out,indent=2))
source=Path('H:/unity/WanxiangGuitu-CP04');contracts=[]
for name in ['CombatAim.cs','AdventureCombat.cs','PlayerHudPresenter.cs']:
 p=source/'Assets/CombatPrototype'/name;lines=p.read_text(encoding='utf-8-sig').splitlines();contracts.append({'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'relevantLines':[{'line':i+1,'text':s.strip()} for i,s in enumerate(lines) if any(x in s for x in ['CombatAim.Solve','AimPreview','void LateUpdate','void Fire(','void Release(','LastReleaseFrame==','bool Ready =>'])]})
(r/'frequency-source-audit.json').write_text(json.dumps(contracts,indent=2));print(out)
