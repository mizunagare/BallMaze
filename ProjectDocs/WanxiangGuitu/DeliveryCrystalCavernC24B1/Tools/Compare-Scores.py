import pathlib,json,hashlib,math
root=pathlib.Path('I:/WGCombat/C24B1-1107-A');out=root/'ScoreComparison1'
if out.exists():raise SystemExit('Fresh audit required')
out.mkdir();inputs=[];report=[];differences=[]
def load(p):
 b=p.read_bytes();inputs.append(dict(path=str(p),sha256=hashlib.sha256(b).hexdigest()));return json.loads(b.decode('utf-8-sig'))
def compare(a,b,path):
 if isinstance(a,bool) or isinstance(b,bool):ok=type(a)==type(b) and a==b
 elif isinstance(a,(int,float)) and isinstance(b,(int,float)):
  delta=abs(a-b);relative=delta/max(abs(a),abs(b),1e-30);ok=(a==b) if isinstance(a,int) and isinstance(b,int) else delta<=0.0001 or relative<=0.00001
  if a!=b:differences.append(dict(path=path,reference=a,candidate=b,absolute=delta,relative=relative,accepted=ok))
  return ok
 elif isinstance(a,dict) and isinstance(b,dict):return set(a)==set(b) and all([compare(a[k],b[k],path+'/'+k) for k in a])
 elif isinstance(a,list) and isinstance(b,list):return len(a)==len(b) and all([compare(x,y,path+f'/{i}') for i,(x,y) in enumerate(zip(a,b))])
 else:ok=a==b
 if not ok:differences.append(dict(path=path,reference=a,candidate=b,accepted=False))
 return ok
for map in ['Forest','Ruins','C21','C22','C23Closed','C23Open']:
 a=root/f'Reference{map}2';b=root/f'Candidate{map}1'
 try:
  pa=load(a/'process.json');pb=load(b/'process.json');process=all(p['exited'] and p['exitCode']==0 and not p['timedOut'] for p in [pa,pb])
  fa=load(a/'fixture.json');fb=load(b/'fixture.json');same_files=fa['files']==fb['files']
  wa=load(a/'input-restored.json');wb=load(b/'input-restored.json')
  keys=['forest','heroPosition','heroYaw','enemies','materials','gear','events','loot','resources']
  same_world=all([compare(wa['activeRun']['checkpoint'][k],wb['activeRun']['checkpoint'][k],map+'/input/'+k) for k in keys])
  sa=load(a/'scores.json')['rows'];sb=load(b/'scores.json')['rows'];da={r['poiId']:r for r in sa};db={r['poiId']:r for r in sb}
  if set(da)!=set(db):raise RuntimeError('POI identity mismatch')
  ordering=(a/'ordering.txt').read_text(encoding='utf-8-sig')==(b/'ordering.txt').read_text(encoding='utf-8-sig')
  for poi in sorted(da):
   equal=compare(da[poi],db[poi],map+'/'+poi)
   report.append(dict(map=map,poi=poi,status='PASS' if process and same_files and same_world and ordering and equal else 'FAIL',process=process,sameInputFiles=same_files,sameRestoredWorld=same_world,sameRanking=ordering,allFieldsEqualWithinRegisteredPolicy=equal,reference=da[poi],candidate=db[poi]))
 except Exception as e:report.append(dict(map=map,status='INCOMPLETE',error=str(e)))
(out/'inputs.json').write_text(json.dumps(inputs,indent=2),encoding='utf-8')
(out/'per-poi.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
(out/'differences.json').write_text(json.dumps(differences,indent=2,ensure_ascii=False),encoding='utf-8')
counts={s:sum(r['status']==s for r in report) for s in ['PASS','FAIL','INCOMPLETE']}
(out/'summary.json').write_text(json.dumps(counts,indent=2),encoding='utf-8');print(counts)
raise SystemExit(3 if counts['INCOMPLETE'] else 1 if counts['FAIL'] else 0)
