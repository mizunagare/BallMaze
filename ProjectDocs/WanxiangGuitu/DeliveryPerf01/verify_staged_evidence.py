"""Check index bytes or exact local LFS object against every raw archive manifest entry."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
def h(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',required=True,type=Path);p.add_argument('--archive',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args();repo=a.repo.resolve();archive=a.archive.resolve();base=archive.relative_to(repo).as_posix();m=json.loads((archive/'MANIFEST.json').read_text(encoding='utf-8'))
 names=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=repo).decode().split('\0');allowed=['ProjectDocs/WanxiangGuitu/DeliveryBuild01/Invoke-Diagnostic.ps1','ProjectDocs/WanxiangGuitu/DEVELOPMENT_PLAN.md'];assert all(not n or n.startswith('ProjectDocs/WanxiangGuitu/DeliveryPerf01/') or n in allowed for n in names)
 gitdir=Path(subprocess.check_output(['git','rev-parse','--absolute-git-dir'],cwd=repo,text=True).strip());proc=subprocess.Popen(['git','cat-file','--batch'],cwd=repo,stdin=subprocess.PIPE,stdout=subprocess.PIPE);checked=0;lfs=0
 try:
  for e in m['entries']:
   name=base+'/'+e['path'];proc.stdin.write((':'+name+'\n').encode());proc.stdin.flush();header=proc.stdout.readline().decode().strip().split();assert len(header)==3 and header[1]=='blob',(name,header)
   raw=proc.stdout.read(int(header[2]));assert proc.stdout.read(1)==b'\n'
   if raw.startswith(b'version https://git-lfs.github.com/spec/v1'):
    text=raw.decode();oid=re.search(r'oid sha256:([a-f0-9]{64})',text)[1];size=int(re.search(r'size (\d+)',text)[1]);assert oid==e['storedSha256'] and size==e['storedBytes'];obj=gitdir/'lfs/objects'/oid[:2]/oid[2:4]/oid;content=obj.read_bytes();assert h(content)==oid and len(content)==size;lfs+=1
   else:assert h(raw)==e['storedSha256'] and len(raw)==e['storedBytes'],name
   checked+=1
 finally:proc.stdin.close();proc.wait(timeout=30)
 a.output.write_text(json.dumps(dict(status='PASS',archiveEntries=checked,lfsPointersChecked=lfs,manifestSha256=h((archive/'MANIFEST.json').read_bytes()),scope='Every archived manifest file in Git index or exact local LFS object matches stored SHA/size. Does not prove remote upload; remote SHA and push receipt checked separately. Own receipt excluded from this manifest.',onlyAuthorizedStagedPaths=True),indent=2),encoding='utf-8');print('Staged archive integrity PASS',checked,'LFS',lfs)
if __name__=='__main__':main()
