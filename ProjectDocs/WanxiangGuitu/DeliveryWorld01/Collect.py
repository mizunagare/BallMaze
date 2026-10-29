"""Publish only this owned run; preserve originals and existing deliveries."""
import pathlib,sys,json,hashlib,gzip,re
root=pathlib.Path(sys.argv[1]).resolve();repo=pathlib.Path(sys.argv[2]).resolve()
if not str(root).lower().replace('\\','/').startswith('i:/wgcombat/') or not (root/'owner.json').is_file():raise SystemExit('owned external root required')
out=repo/'ProjectDocs/WanxiangGuitu/DeliveryWorld01/Evidence';out.mkdir(exist_ok=True)
manifest=[]
def publish(p,d):
 data=p.read_bytes();original=hashlib.sha256(data).hexdigest();d.parent.mkdir(parents=True,exist_ok=True)
 if p.suffix in ('.log','.stdout','.stderr'):
  text=data.decode('utf-8-sig',errors='replace')
  text=re.sub(r'(?i)((?:access[_ ]?token|authorization|client[_ ]?secret)\s*[:=]\s*)(?:Bearer\s+)?[A-Za-z0-9._/+\-=]{8,}',r'\1[REDACTED_CREDENTIAL]',text)
  d=d.with_name(d.name+'.gz');data=gzip.compress(text.encode('utf-8'),mtime=0)
 d.write_bytes(data);manifest.append(dict(path=d.relative_to(out).as_posix(),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),source=str(p),sourceSHA256=original))
phases=[p.name for p in root.iterdir() if p.is_dir() and p.name not in ('P','Prepare','Worker','WorkerSource')]+['Prepare/fixtures']
extensions={'.json','.jsonl','.csv','.txt','.log','.stdout','.stderr','.png','.cs','.bak','.tmp','.held','.published-held','.prior-pending','.archived','.csproj'}
for phase in phases:
 folder=root/phase
 if not folder.exists():continue
 for p in folder.rglob('*'):
  if not p.is_file():continue
  rel=p.relative_to(folder)
  if any(x.lower() in ('library','assets','packages','projectsettings','release','project','runtime','deferred') for x in rel.parts[:-1]):continue
  if p.suffix.lower() in extensions:publish(p,out/phase/rel)
for n in ['owner.json','user-before.json','user-final.json','history-before.json','history-final.json','protection-check.json','build-inputs.json','source-bindings.json','sequence.jsonl','publication-attempts.json','tool-attempts.json','build-input-comparison.json']:
 p=root/n
 if p.exists():publish(p,out/'Bindings'/n)
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(manifest),'owned artifacts published; source histories untouched')
