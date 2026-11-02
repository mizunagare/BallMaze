import json,hashlib,subprocess
from pathlib import Path
r=Path('I:/WGCombat/CP04BR-1102-A');result={}
for name in ['protected','history']:
 rows=json.loads((r/(name+'-before.json')).read_text(encoding='utf-8-sig'));bad=[]
 for x in rows:
  p=Path(x['root'])/x['path'] if 'root' in x else Path(x['path'])
  h=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
  if h!=x['sha256'].lower():bad.append({'path':str(p),'before':x['sha256'],'after':h})
 result[name]={'count':len(rows),'mismatches':bad}
p=Path('H:/unity/WanxiangGuitu-CP04/Assets/CombatPrototype/CombatAim.cs');result['aimSHA256']=hashlib.sha256(p.read_bytes()).hexdigest();result['frozenExact']=p.read_bytes()==(r/'aim-frozen.cs.txt').read_bytes()
(r/'protection-after.json').write_text(json.dumps(result,indent=2));print(result)

