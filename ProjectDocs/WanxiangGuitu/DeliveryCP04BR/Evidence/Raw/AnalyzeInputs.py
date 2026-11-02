import json,hashlib,difflib
from pathlib import Path
r=Path('I:/WGCombat/CP04BR-1102-A'); stages=r/'FixedBuildAudit/Stages'
a=stages/'0002-execute-before-BuildPipeline'; b=stages/'0010-execute-after-BuildPipeline'
rows=[]
for f in a.glob('*.txt'):
 g=b/f.name
 rows.append({'file':f.name,'beforeSHA256':hashlib.sha256(f.read_bytes()).hexdigest(),'afterSHA256':hashlib.sha256(g.read_bytes()).hexdigest(),'diff':list(difflib.unified_diff(f.read_text(encoding="utf-8-sig").splitlines(),g.read_text(encoding="utf-8-sig").splitlines(),fromfile='before',tofile='after',n=3))})
(r/'field-differences.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False))
(r/'field-differences.diff').write_text('\n'.join('\n'.join(x['diff']) for x in rows),encoding='utf8')
p=r/'Fixed/Project/Library/Bee/Playerb2f5140b-inputdata.json'
j=json.loads(p.read_text(encoding="utf-8-sig"));out=[]
def walk(v,path=''):
 if isinstance(v,dict):
  for k,x in v.items():
   if k=='Services':out.append({'path':path+'/'+k,'value':x})
   else:walk(x,path+'/'+k)
 elif isinstance(v,list):
  for n,x in enumerate(v):walk(x,path+'/'+str(n))
walk(j)
(r/'bee-services.json').write_text(json.dumps({'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'services':out},indent=2))
print((r/'field-differences.diff').read_text(encoding="utf-8-sig"));print(out)

