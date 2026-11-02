"""Publish new BR2 evidence only; preserve source bytes/hashes and redact credential values in text logs."""
from pathlib import Path
import os,json,gzip,hashlib,re,shutil
root=Path('I:/WGCombat/CP04BR2-1102-A');out=Path('H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04BR2/Evidence/Raw')
if json.loads((root/'owner.json').read_text(encoding='utf-8-sig'))['task']!='CP04-BR2':raise ValueError('Wrong owned root')
out.mkdir(exist_ok=True);manifest=[];old=json.loads((out/"manifest.json").read_text()) if (out/"manifest.json").exists() else [];prior={x["sourceRelative"]:x for x in old}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
for parent,dirs,files in os.walk(root):
 dirs[:]=[x for x in dirs if x not in ['Project','Library','Release','PythonLib','bin','obj','__pycache__']]
 for name in sorted(files):
  p=Path(parent)/name;rel=p.relative_to(root);ext=p.suffix.lower()
  if ext not in ['.json','.jsonl','.csv','.md','.txt','.log','.stdout','.stderr','.ps1','.py','.cs','.cpp','.data','.dll']:continue
  if ext=='.dll' and rel.as_posix()!='Native/BR2AllocationNative.dll':continue
  original=sha(p);old=prior.get(rel.as_posix())
  if old and old["sourceSHA256"]==original:manifest.append(old);continue
  if old:raise ValueError("Published source changed; preserve a new version: "+str(p))
  red=False;target=out/rel;target.parent.mkdir(parents=True,exist_ok=True)
  if ext=='.data':
   target=target.with_name(target.name+'.gz')
   with p.open('rb') as source,target.open('wb') as dest,gzip.GzipFile(filename='',mode='wb',fileobj=dest,compresslevel=6,mtime=0) as zipped:shutil.copyfileobj(source,zipped,4*1024*1024)
  else:
   data=p.read_bytes()
   if ext in ['.log','.stdout','.stderr','.jsonl']:
    text=data.decode('utf-8-sig');clean=re.sub(r'(?i)((?:access[_ ]?token|authorization|client[_ ]?secret)\s*[:=]\s*)(?:Bearer\s+)?(?:"[^"\r\n]*"|[A-Za-z0-9._/+\-=]{8,})',r'\1[REDACTED_CREDENTIAL]',text);red=clean!=text;data=clean.encode('utf8')
   if ext in ['.log','.stdout','.stderr','.jsonl','.dll']:target=target.with_name(target.name+'.gz');data=gzip.compress(data,compresslevel=6,mtime=0)
   target.write_bytes(data)
  manifest.append({'path':target.relative_to(out).as_posix(),'sourceRelative':rel.as_posix(),'sourceSHA256':original,'publishedSHA256':sha(target),'sourceBytes':p.stat().st_size,'publishedBytes':target.stat().st_size,'redacted':red})
(out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8');print(len(manifest),'artifacts',sum(x['publishedBytes'] for x in manifest),'bytes')

