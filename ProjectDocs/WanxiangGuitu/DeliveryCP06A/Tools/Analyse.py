from pathlib import Path
import json,sys,hashlib
r=Path(sys.argv[1]);out=Path(sys.argv[2]);checks=[]
def c(name,ok,detail):checks.append(dict(name=name,status='PASS' if ok else 'FAIL',detail=detail))
for before,after in [('BeforeEditor2','AfterEditorFinal'),('BeforePlayer','PlayerFinal')]:
 a=json.loads((r/before/'legacy.json').read_text())['rows'];b=json.loads((r/after/'legacy.json').read_text())['rows'];diff=[]
 for x,y in zip(a,b):
  for key in ['weapon','skill','accepted','spawns']:
   if x[key]!=y[key]:diff.append([x['weapon'],x['skill'],key,x[key],y[key]])
  for key in ['loss','cooldown']:
   if abs(x[key]-y[key])>.01:diff.append([x['weapon'],x['skill'],key,x[key],y[key]])
 c(after+'-legacy-8-paired',len(a)==len(b)==8 and not diff,str(diff))
for name in ['AfterEditorFinal','ExtraEditorFinal','SaveEditorFinal','ResumeEditorFinal','CP05RegressionEditor','RegressionFormalEditor','PlayerFinal','ExtraPlayer','SavePlayer','ResumePlayer','CP05RegressionPlayer','RegressionFormalPlayer']:
 f=r/name/'probe.json'
 if not f.exists():c(name,False,'missing receipt');continue
 d=json.loads(f.read_text());rows=d['rows'];valid=len(rows)>0 and all(x.get('status')=='PASS' and x.get('name') for x in rows) and len({x['name'] for x in rows})==len(rows) and not d.get('error');c(name,valid,str(len(rows))+' actual assertions, unique names, no semantic errors')
for before,after in [('I:/WGCombat/CP05C-1104-A/BeforeFormal2','RegressionFormalEditor'),('I:/WGCombat/CP05C-1104-A/BeforePlayerFormal','RegressionFormalPlayer')]:
 a=json.loads((Path(before)/'formal-rules.json').read_text());b=json.loads((r/after/'formal-rules.json').read_text());c(after+'-480-rules',len(a['rows'])==480 and a==b,'old quality/affix/three-stream factory matrix')
 a=json.loads((Path(before)/'formal-death.json').read_text());b=json.loads((r/after/'formal-death.json').read_text());keys=['targetId','run','region','seed','wave','randomBefore','randomAfter','bagBefore','bagAfter','xpBefore','xpAfter','levelBefore','levelAfter'];diff=[k for k in keys if a.get(k)!=b.get(k)];c(after+'-actual-death',not diff,str(diff));normalize=lambda d:[{k:v for k,v in x.items() if k!='actualId'} for x in d['drops']];c(after+'-actual-drop-semantics',normalize(a)==normalize(b),'new actual IDs separately recorded; no duplicate reward')
result=dict(status='FAIL' if any(x['status']=='FAIL' for x in checks) else 'PASS',checks=checks,scope='Paired data and semantic audit; checks overlap runtime rows, do not add to function counts');out.write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result));sys.exit(any(x['status']=='FAIL' for x in checks))
