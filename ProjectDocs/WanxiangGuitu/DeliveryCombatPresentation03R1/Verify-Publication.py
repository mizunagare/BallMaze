"""Verify direct Git blobs AND resolved LFS bytes; never compare pointers as media."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path

def main():
    a=argparse.ArgumentParser();a.add_argument('repo',type=Path);a.add_argument('--output',type=Path,required=True);o=a.parse_args();repo=o.repo.resolve();d=repo/'ProjectDocs/WanxiangGuitu/DeliveryCombatPresentation03R1';items=[];errors=[];lfs=0
    common=Path(subprocess.check_output(['git','-C',str(repo),'rev-parse','--git-common-dir']).decode().strip());common=common if common.is_absolute() else repo/common
    for folder in (d/'Evidence',d/'Evidence/PostStyle'):
        for x in json.loads((folder/'manifest.json').read_text(encoding='utf-8')):items.append((folder/x['path'],x['publishedSHA256'],x['bytes']))
    data=subprocess.check_output(['git','-C',str(repo),'cat-file','--batch'],input=('\n'.join(':'+f.relative_to(repo).as_posix() for f,h,n in items)+'\n').encode());i=0
    for f,expected,size in items:
        e=data.index(b'\n',i);n=int(data[i:e].split()[2]);blob=data[e+1:e+1+n];i=e+n+2
        if blob.startswith(b'version https://git-lfs.github.com/spec/v1\n'):
            match=re.fullmatch(rb'version https://git-lfs.github.com/spec/v1\noid sha256:([0-9a-f]{64})\nsize ([0-9]+)\n',blob)
            if not match:errors.append(str(f)+' malformed LFS pointer');continue
            oid=match[1].decode();local=common/'lfs/objects'/oid[:2]/oid[2:4]/oid
            if oid!=expected or int(match[2])!=size or not local.is_file() or hashlib.sha256(local.read_bytes()).hexdigest()!=expected:errors.append(str(f)+' LFS mismatch')
            lfs+=1
        elif hashlib.sha256(blob).hexdigest()!=expected:errors.append(str(f)+' direct Git blob mismatch')
        if hashlib.sha256(f.read_bytes()).hexdigest()!=expected:errors.append(str(f)+' published worktree mismatch')
    broken=[]
    for f in list(d.glob('*.md'))+[d/'Evidence/INDEX.md']:
        for link in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8-sig')):
            if '://' not in link and not link.startswith('#') and not (f.parent/link.split('#')[0]).exists():broken.append(dict(file=str(f),link=link))
    q=dict(status='FAIL' if errors or broken else 'PASS',artifacts=len(items),lfsObjects=lfs,directBlobs=len(items)-lfs,errors=errors,brokenLinks=broken,note='Staged Git/LFS content verified; this does not claim product acceptance or remote upload')
    if o.output.exists():raise ValueError('fresh output required')
    o.output.write_text(json.dumps(q,indent=2),encoding='utf-8');print(json.dumps(q));return 1 if q['status']=='FAIL' else 0
if __name__=='__main__':raise SystemExit(main())
