"""Publish only owned synthetic evidence; never copy user project/cache/build binaries."""
from pathlib import Path
import sys,json,hashlib,gzip,re
root=Path(sys.argv[1]).resolve();repo=Path(sys.argv[2]).resolve()
assert str(root).lower().replace('\\','/').startswith('i:/wgcombat/') and (root/'owner.json').is_file()
out=repo/'ProjectDocs/WanxiangGuitu/DeliveryUXTech01/Evidence';out.mkdir(exist_ok=True)
skip={'P','F','DeferredUserInputs','DeferredAfterUserInputs','DeferredFreshUserInputs','Library','Assets','Packages','ProjectSettings','Release','Project','Host','HostSource','bin','obj'}
ext={'.json','.jsonl','.csv','.txt','.log','.stdout','.stderr','.png','.cs','.bak','.tmp','.held','.published-held','.prior-pending','.archived','.csproj','.ps1'}
manifest=[]
for p in root.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(root)
 if any(part in skip for part in rel.parts[:-1]) or p.suffix.lower() not in ext:continue
 data=p.read_bytes();original=hashlib.sha256(data).hexdigest();d=out/rel;d.parent.mkdir(parents=True,exist_ok=True)
 if p.suffix in {'.log','.stdout','.stderr'} or p.name=='hp.csv' or p.suffix=='.jsonl':
  text=data.decode('utf-8-sig',errors='replace');text=re.sub(r'(?i)((?:access[_ ]?token|authorization|client[_ ]?secret)\s*[:=]\s*)(?:Bearer\s+)?(?:\"[^\"\r\n]*\"|[A-Za-z0-9._/+\-=]{8,})',r'\1[REDACTED_CREDENTIAL]',text);data=gzip.compress(text.encode('utf-8'),mtime=0);d=d.with_name(d.name+'.gz')
 d.write_bytes(data);manifest.append(dict(path=d.relative_to(out).as_posix(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),source=str(p),sourceSHA256=original))
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');print(len(manifest),'owned artifacts')
