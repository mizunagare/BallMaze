from pathlib import Path
import json
r=Path('I:/WGCombat/CP04BR2-1102-A')
for project,target in [('Fixed','MonoBuild'),('Control','ConnectControlBuild')]:
 for p in (r/project/'Project/Library/Bee').glob('Player*-inputdata.json'):
  j=json.loads(p.read_text(encoding='utf-8-sig'));hits=[]
  def walk(x,path=''):
   if isinstance(x,dict):
    for k,v in x.items():walk(v,path+'/'+k)
   elif isinstance(x,list):
    for i,v in enumerate(x):walk(v,path+'/'+str(i))
   elif isinstance(x,str) and target.lower() in x.lower():hits.append((path,x[:250]))
  walk(j)
  if hits:print(project,p.name,hits[:8])
