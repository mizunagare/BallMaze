import argparse,csv,gzip,hashlib,json,re,shutil,statistics
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--run-root',required=True);ap.add_argument('--repository',required=True);a=ap.parse_args();root=Path(a.run_root).resolve();repo=Path(a.repository).resolve()
assert str(root).lower().replace('\\','/').startswith('i:/wgcombat/') and (root/'owner.json').is_file()
out=repo/'ProjectDocs/WanxiangGuitu/DeliveryCombat02/Evidence';out.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
# Publish raw logs with credential-value redaction only, never error/severity filtering.
manifest=[]
for folder in ['Comparison','Slope','Before','BeforeBoundary','After','AfterBoundary','Contracts','VisualBefore','VisualAfter','LegacyOriginal','LegacyAdapted','Regression','RecoveryProbe','RecoveryProbe-Resume','RecoveryProbe-PendingResume','RecoveryProbe-CommittedResume','Recovery-Run','Recovery-Resume','Recovery-PendingResume','Recovery-CommittedResume','Recovery','Build']:
 base=root/folder
 if not base.exists():continue
 for p in base.rglob('*'):
  if not p.is_file():continue
  rel=p.relative_to(base)
  if any(part.lower() in {'project','assets','library','packages','projectsettings','synthetic','b07-save','release','temp','obj','deferred'} for part in rel.parts[:-1]):continue
  if p.suffix.lower() not in {'.json','.jsonl','.csv','.txt','.md','.png','.log','.stdout','.stderr'}:continue
  dest=out/'Runs'/folder/rel;dest.parent.mkdir(parents=True,exist_ok=True)
  original=sha(p)
  if p.suffix.lower() in {'.log','.stdout','.stderr'}:
   text=p.read_text(encoding='utf-8',errors='replace')
   text=re.sub(r'(?i)((?:access[_ ]?token|authorization|client[_ ]?secret)\s*[:=]\s*)(?:Bearer\s+)?[A-Za-z0-9._/+\-=]{8,}',r'\1[REDACTED_CREDENTIAL]',text)
   dest=dest.with_name(dest.name+'.gz');dest.write_bytes(gzip.compress(text.encode('utf-8'),mtime=0))
  else:shutil.copyfile(p,dest)
  manifest.append({'source':str(p),'path':str(dest.relative_to(out)).replace('\\','/'),'originalSHA256':original,'publishedSHA256':sha(dest),'bytes':dest.stat().st_size})
for name in ['owner.json','protected-before.json']:
 shutil.copyfile(root/name,out/name)
protected=json.loads((root/'protected-before.json').read_text(encoding='utf-8-sig'));checks=[]
for x in protected:
 actual=sha(repo/x['path']);checks.append({**x,'afterSHA256':actual,'status':'PASS' if actual.upper()==x['sha256'].upper() else 'FAIL'})
write(out/'protected-after.json',checks)
# Freeze product sources and packages, recording any clone/source differences without overwriting either.
inputs=[]
for top in ['Assets','Packages','ProjectSettings']:
 for p in sorted((repo/top).rglob('*')):
  if p.is_file() and (top!='Assets' or p.suffix in {'.cs','.unity','.prefab','.asset','.shader'}):
   rel=p.relative_to(repo);clone=root/'P/Project'/rel
   inputs.append({'path':str(rel).replace('\\','/'),'sourceSHA256':sha(p),'cloneSHA256':sha(clone) if clone.is_file() else None})
write(out/'product-inputs.json',inputs)
rows={k:list(csv.DictReader((root/k/'matrix.csv').open())) for k in ['Before','After']}
key=lambda x:tuple(x[c] for c in ['weapon','action','body','distance','angle','height','duplicate','wall'])
before={key(x):x for x in rows['Before']};pairs=[]
for row in rows['After']:
 old=before[key(row)];pairs.append({**{k:row[k] for k in ['weapon','action','body','distance','angle','height','duplicate','wall']},**{f'{phase}_{c}':x[c] for phase,x in [('before',old),('after',row)] for c in ['hit','applied','cooldown','releaseLatency','hitLatency','damageEvents']}})
with (out/'paired-matrix.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(pairs[0]));w.writeheader();w.writerows(pairs)
summary={}
for phase in ['Before','After']:
 duels=list(csv.DictReader((root/phase/'duels.csv').open()));stats=[]
 for w in range(4):
  for body in ['normal','elite','boss']:
   sample=[x for x in duels if x['weapon']==str(w) and x['body']==body]
   record={'weapon':w,'body':body,'n':len(sample),'terminals':[x['terminal'] for x in sample]}
   for c in ['seconds','killWindowDPS','receivedDamage','acceptedAttacks','damageEvents']:
    values=[float(x[c]) for x in sample];record[c]={'mean':statistics.mean(values),'min':min(values),'max':max(values),'stdev':statistics.stdev(values) if len(values)>1 else None}
   stats.append(record)
 summary[phase]=stats
write(out/'paired-duels-summary.json',summary)
write(out/'published-manifest.json',manifest)
print(json.dumps({'published':len(manifest),'protected':checks,'pairs':len(pairs)},ensure_ascii=False))
