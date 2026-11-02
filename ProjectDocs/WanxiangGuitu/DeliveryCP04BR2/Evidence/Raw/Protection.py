from pathlib import Path
import hashlib,json,sys
r=Path('I:/WGCombat/CP04BR2-1102-A');result={}
for name,file in [('productAndUser','protected-before.json'),('cp04bHistory','cp04b-history-before.json'),('brHistory','br-history-before.json')]:
 rows=json.loads((r/file).read_text(encoding='utf-8-sig'));bad=[]
 for x in rows:
  p=Path(x['root'])/x['path'] if 'root' in x else Path(x['path']);h=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
  if h!=x['sha256']:bad.append({'path':str(p),'actual':h})
 result[name]={'count':len(rows),'changed':bad}
p=Path('H:/unity/WanxiangGuitu-CP04/Assets/CombatPrototype/CombatAim.cs');result['aimSHA256']=hashlib.sha256(p.read_bytes()).hexdigest();result['sourceFrozen']=result['aimSHA256']=='9f5d9b7d8c1c39b7270839217562033b6425e2af2d357df51e1269558c4e346a'
a=json.loads((r/'assembly-audit.json').read_text(encoding='utf-8-sig'));d={x['run']:x for x in a};result['normalizedAimILSame']=d['BRPure']['aimMethods']==d['BR2Pure']['aimMethods']==d['BR2Mono']['aimMethods'];result['pureTestTypes']=d['BR2Pure']['testTypes'];result['probeTestTypes']=d['BR2Mono']['testTypes'];result['noEditorRefs']=all(not x['editorReferences'] for x in a);(r/'protection-and-il.json').write_text(json.dumps(result,indent=2));print(result)
