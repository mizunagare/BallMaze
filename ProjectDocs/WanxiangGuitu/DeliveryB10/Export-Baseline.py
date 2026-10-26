"""Export an immutable local Git baseline into a fresh external test project, resolving local LFS bytes.
No checkout/reset/network access/deletion; never overwrites a target or user file.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--ref',required=True);p.add_argument('--target',type=Path,required=True);a=p.parse_args();repo=a.repo.resolve();target=a.target.resolve()
if target.exists() or target==repo or repo in target.parents or 'locallow' in str(target).lower():raise SystemExit('Fresh external target required')
sha=subprocess.check_output(['git','-C',str(repo),'rev-parse',a.ref],text=True).strip()
paths=subprocess.check_output(['git','-C',str(repo),'ls-tree','-r','--name-only','-z',sha,'--','Assets','Packages','ProjectSettings']).split(b'\0')
common=Path(subprocess.check_output(['git','-C',str(repo),'rev-parse','--git-common-dir'],text=True).strip());common=common if common.is_absolute() else repo/common
target.mkdir(parents=True);records=[]
with subprocess.Popen(['git','-C',str(repo),'cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE) as proc:
 for raw in paths:
  if not raw:continue
  name=raw.decode('utf-8');rel=Path(name)
  if rel.is_absolute() or '..' in rel.parts or '\n' in name:raise ValueError('Unsafe Git path')
  proc.stdin.write(sha.encode()+b':'+raw+b'\n');proc.stdin.flush();head=proc.stdout.readline().split();size=int(head[2]);body=proc.stdout.read(size);assert proc.stdout.read(1)==b'\n';oid=None
  if body.startswith(b'version https://git-lfs.github.com/spec/v1\n'):
   oid=next(line.split(b':',1)[1].decode() for line in body.splitlines() if line.startswith(b'oid sha256:'));obj=common/'lfs/objects'/oid[:2]/oid[2:4]/oid
   if not obj.is_file():raise FileNotFoundError('Local baseline LFS object missing: '+name)
   body=obj.read_bytes();assert hashlib.sha256(body).hexdigest()==oid
  out=target/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(body);records.append(dict(path=name,bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),lfsOid=oid))
 proc.stdin.close();proc.wait();assert proc.returncode==0
(target.parent/'baseline-export.json').write_text(json.dumps(dict(status='PASS',commit=sha,scope='Exact committed Assets/Packages/ProjectSettings + verified local LFS; tests injected separately',files=records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(commit=sha,files=len(records),lfs=sum(f['lfsOid'] is not None for f in records),target=str(target))))
