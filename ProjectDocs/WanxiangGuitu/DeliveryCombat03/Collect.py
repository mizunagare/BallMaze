"""Publish owned test artifacts only. Never edits historical deliveries or saves."""
import pathlib,hashlib,gzip,json,sys,re
root=pathlib.Path(sys.argv[1]).resolve();repo=pathlib.Path(sys.argv[2]).resolve()
if not str(root).lower().replace('\\','/').startswith('i:/wgcombat/') or not (root/'owner.json').exists():raise SystemExit('owned root required')
out=repo/'ProjectDocs/WanxiangGuitu/DeliveryCombat03/Evidence';out.mkdir(exist_ok=True);manifest=[]
phases=['Preflight','Before','BeforeReadability','BeforePaired','AfterReadability','After','Contracts','Legacy','Regression','Build','Area','VisualAfter','BeforeVerified','VisualBefore','FinalReadability','FixedBefore','FixedAfter','FrozenProduct','BaselineInputs']
def publish(p,d):
 data=p.read_bytes();d.parent.mkdir(parents=True,exist_ok=True)
 if p.suffix in ('.log','.stdout','.stderr'):
  text=data.decode('utf-8-sig',errors='replace');text=re.sub(r'(?i)((?:access[_ ]?token|authorization|client[_ ]?secret)\s*[:=]\s*)(?:Bearer\s+)?[A-Za-z0-9._/+\-=]{8,}',r'\1[REDACTED_CREDENTIAL]',text)
  d=d.with_name(d.name+'.gz');data=gzip.compress(text.encode('utf-8'),mtime=0)
 d.write_bytes(data);manifest.append({'path':d.relative_to(out).as_posix(),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'source':str(p),'sourceSHA256':hashlib.sha256(p.read_bytes()).hexdigest()})
for phase in phases:
 folder=root/phase
 if not folder.exists():continue
 for p in folder.rglob('*'):
  if not p.is_file():continue
  rel=p.relative_to(folder)
  # Exclude project copies, built binaries, package caches and machine runtime.
  if any(x.lower() in ('library','assets','packages','projectsettings','release','project','runtime','deferred') for x in rel.parts[:-1]):continue
  if p.suffix.lower() not in ('.json','.jsonl','.csv','.txt','.log','.stdout','.stderr','.png','.cs'):continue
  publish(p,out/phase/rel)
for n in ['owner.json','status-before.txt','user-before.json','history-before.json','sequence.jsonl','completion.jsonl','fixed-pair.jsonl','comparison.json','changed-source-input.json','user-midcheck.json','user-final.json','history-final.json','source-copy.json','build-inputs.json','sequence-first-failure.json','sequence-copy-failure.json','Invoke-Measure-before-freeze-fix.ps1.txt']:
 p=root/n
 if p.exists():publish(p,out/'Bindings'/n)
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(manifest),'published; original source files untouched')
