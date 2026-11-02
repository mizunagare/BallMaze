import os,json,gzip,hashlib,re,shutil
from pathlib import Path
r=Path('I:/WGCombat/CP04BR-1102-A');out=Path('H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04BR/Evidence/Raw');out.mkdir(exist_ok=True);rows=[]; previous=json.loads((out/"manifest.json").read_text()) if (out/"manifest.json").exists() else []; prior={x["sourceRelative"]:x for x in previous}
for parent,dirs,files in os.walk(r):
 dirs[:]=[d for d in dirs if d not in ['Project','Library','Release','obj','bin','__pycache__']]
 for name in sorted(files):
  f=Path(parent)/name;rel=f.relative_to(r)
  if f.suffix.lower() not in ['.json','.jsonl','.csv','.md','.txt','.log','.stdout','.stderr','.ps1','.cs','.py','.diff','.data','.raw']:continue
  raw=f.read_bytes();h=hashlib.sha256(raw).hexdigest();red=False
  old=prior.get(f.relative_to(r).as_posix())
  if old and old['sourceSHA256']==h:
   rows.append(old);continue
  if old:raise ValueError('Published source changed, preserve version before re-publication: '+str(f))
  if f.suffix.lower() in ['.log','.stdout','.stderr','.jsonl']:
   text=raw.decode('utf-8-sig',errors='strict');clean=re.sub(r'(?i)((?:access[_ ]?token|authorization|client[_ ]?secret)\s*[:=]\s*)(?:Bearer\s+)?(?:"[^"\r\n]*"|[A-Za-z0-9._/+\-=]{8,})',r'\1[REDACTED_CREDENTIAL]',text);red=clean!=text;raw=clean.encode('utf8')
  if f.suffix.lower() in ['.log','.stdout','.stderr','.jsonl','.data','.raw']:raw=gzip.compress(raw,compresslevel=3,mtime=0);rel=rel.with_name(rel.name+'.gz')
  t=out/rel;t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(raw);rows.append(dict(path=rel.as_posix(),sourceRelative=f.relative_to(r).as_posix(),sourceSHA256=h,publishedSHA256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),redacted=red))
(out/'manifest.json').write_text(json.dumps(rows,indent=2));print(len(rows),sum(x['bytes'] for x in rows))

