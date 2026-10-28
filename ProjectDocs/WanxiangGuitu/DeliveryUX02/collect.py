"""Archive owned UX02 evidence; never include full projects, Player binaries or real saves."""
import argparse,gzip,hashlib,json,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',required=True,type=Path);p.add_argument('--out',required=True,type=Path);a=p.parse_args()
root=a.root.resolve();out=a.out.resolve()
if json.loads((root/'owner.json').read_text(encoding='utf-8-sig'))['kind']!='UX02 owned isolated validation':raise ValueError('Owned UX02 root required')
if out.exists():raise ValueError('Fresh archive directory required; preserve earlier snapshots')
out.mkdir(parents=True);manifest=[]
for base in root.iterdir():
 if base.is_dir() and base.name in {'A','B','Before2-ProductSources','FinalExtrasShared','ExtrasShared'}:continue
 for f in ([base] if base.is_file() else base.rglob('*')):
  if any(x.is_symlink() or getattr(x,'is_junction',lambda:False)() for x in [f,*f.parents]):continue
  if not f.is_file() or any(x in ['Release','Library','Project','Deferred'] or x.startswith('ExecutedDrivers-') for x in f.relative_to(root).parts):continue
  if f.suffix.lower() not in ['.json','.jsonl','.csv','.txt','.log','.stdout','.stderr','.png']:continue
  raw=f.read_bytes();dest=out/f.relative_to(root);dest.parent.mkdir(parents=True,exist_ok=True);redactions=0
  if f.suffix.lower() in ['.log','.stdout','.stderr']:
   text,redactions=re.subn(r'(?im)(access token[^\r\n]*?:\s*)"[^"\r\n]*"',r'\1"[REDACTED LICENSING TOKEN]"',raw.decode('utf-8',errors='replace'))
   dest=dest.with_name(dest.name+'.gz');dest.write_bytes(gzip.compress(text.encode('utf-8'),mtime=0))
  else:dest.write_bytes(raw)
  manifest.append(dict(localSource=str(f),published=dest.relative_to(out).as_posix(),sourceBytes=len(raw),sourceSha256=hashlib.sha256(raw).hexdigest(),publishedSha256=hashlib.sha256(dest.read_bytes()).hexdigest(),credentialRedactions=redactions,liveAttemptSnapshot=(base.name=='Normal-Gather')))
(out/'collection-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');print('archived',len(manifest))
