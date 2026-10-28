from pathlib import Path
import json,gzip,hashlib,shutil,re,csv,argparse
ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--repository',required=True);ap.add_argument('--compiler-root');args=ap.parse_args();repo=Path(args.repository);root=Path(args.root);assert (root/'owner.json').is_file();out=repo/'ProjectDocs/WanxiangGuitu/DeliveryCombat02R1/Evidence';out.mkdir(exist_ok=True);(out/'.gitattributes').write_bytes(b'* -text\n');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();manifest=[]
def copy(p,d):
 d=out/d;d.parent.mkdir(parents=True,exist_ok=True);original=sha(p)
 if p.suffix.lower() in ['.log','.jsonl','.stdout','.stderr']:
  text=p.read_text(encoding='utf-8-sig',errors='replace');text=re.sub(r'(?i)((?:access[_ ]?token|authorization|client[_ ]?secret)\s*[:=]\s*)(?:Bearer\s+)?[A-Za-z0-9._/+\-=]{8,}',r'\1[REDACTED_CREDENTIAL]',text);d=d.with_name(d.name+'.gz');d.write_bytes(gzip.compress(text.encode('utf-8'),mtime=0))
 else:shutil.copyfile(p,d)
 manifest.append({'source':str(p),'path':str(d.relative_to(out)).replace('\\','/'),'originalSHA256':original,'publishedSHA256':sha(d),'bytes':d.stat().st_size})
for phase in ['Observed','Fixed','Canonical','Integrated']:
 for n in range(1,4):
  base=(root/'Observed' if (root/'Observed').is_dir() else root) if phase=='Observed' else root/phase
  for category in ['Runs','Stores']:
   folder=base/category/f'{n:02}'
   for p in folder.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in ['.json','.jsonl','.csv','.txt','.log','.stdout','.stderr']:continue
    # Saved fixture JSONs are synthetic and explicitly scoped; no projects, caches or binaries.
    copy(p,Path(phase)/f'{n:02}'/category/p.relative_to(folder))
for folder in ['Compile','Analysis','Batch']:
 if not (root/folder).exists():continue
 for p in (root/folder).rglob('*'):
  if p.is_file():copy(p,Path(folder)/p.relative_to(root/folder))
for name in ['owner.json','original-lock.json','original-lock-after.json','original-raw-vs-published.json','original-save-metadata.json','product-before.json','product-inputs-after.json','product-csharp-binding.json','protected-before.json','protected-after.json','patch-manifest.json','ready-fix-manifest.json','process-summary.json','product-editor-assemblies.json','prepare-link.json','Invoke-Rules-before.ps1']:
 copy(root/name,Path('Bindings')/name)
copy(root/'Fixed/process-summary.json',Path('Bindings/Fixed-process-summary.json'))
a=Path(args.compiler_root) if args.compiler_root else root/'NoCompilerFailure'
for p in (a/'Runs/01').glob('*'):
 if p.is_file() and p.suffix.lower() in ['.json','.csv','.txt','.log','.stdout','.stderr']:copy(p,Path('CompilerFailure')/p.name)
for name in ['Trace-before-api-fix.cs.txt','Executed-OwnedAbort.cs.txt','cleanup-close.json','cleanup-exit.json','cleanup-guard.json']:
 if (a/name).exists():copy(a/name,Path('CompilerFailure')/name)
old=repo/'ProjectDocs/WanxiangGuitu/DeliveryCombat02/Evidence/Runs'
copy(old/'Recovery/storage-audit.jsonl',Path('OriginalReference/storage-audit.jsonl'))
for folder in ['Recovery-Run','Recovery-Resume','Recovery-PendingResume','Recovery-CommittedResume']:
 for p in (old/folder).glob('*.exit.json'):copy(p,Path('OriginalReference')/folder/p.name)
copy(repo/'ProjectDocs/WanxiangGuitu/DeliveryCombat02/Evidence/aggregate-status.json',Path('OriginalReference/aggregate-status.json'))
(out/'manifest.json').write_bytes(json.dumps(manifest,ensure_ascii=False,indent=2).encode('utf-8'));print('files',len(manifest),'published bytes',sum(x['bytes'] for x in manifest))
# Same original assertions/predicates, not weakened for readiness.
def calls(s,token):
 result=[];start=0
 while True:
  pos=s.find(token+'(',start)
  if pos<0:return result
  i=pos+len(token);depth=0;quote=False;escape=False
  while i<len(s):
   c=s[i]
   if quote:
    if escape:escape=False
    elif c=='\\':escape=True
    elif c=='"':quote=False
   elif c=='"':quote=True
   elif c=='(':depth+=1
   elif c==')':
    depth-=1
    if depth==0:result.append(s[pos:i+1]);start=i+1;break
   i+=1
original=(repo/'ProjectDocs/WanxiangGuitu/DeliveryCombat02/Evidence/B07Rules-before-diagnostic.cs.txt').read_text(encoding='utf-8-sig');observed=(repo/'ProjectDocs/WanxiangGuitu/DeliveryCombat02R1/Tests/B07RulesObserved.cs.txt').read_text(encoding='utf-8');ready=(repo/'ProjectDocs/WanxiangGuitu/DeliveryCombat02R1/Tests/B07RulesReady.cs.txt').read_text(encoding='utf-8')
contract={t:{'count':len(calls(original,t)),'identicalObserved':calls(original,t)==calls(observed,t),'identicalReady':calls(original,t)==calls(ready,t),'identicalStable':calls(original,t)==calls((repo/'ProjectDocs/WanxiangGuitu/DeliveryCombat02R1/Tests/B07RulesStable.cs.txt').read_text(encoding='utf-8'),t)} for t in ['Need','Single']};(out/'assertion-contract.json').write_bytes(json.dumps(contract,indent=2).encode());print(contract)
assert all(x['identicalObserved'] and x['identicalReady'] and x['identicalStable'] for x in contract.values())
