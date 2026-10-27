"""Read-only publication of owned synthetic PLAYER-02 evidence. Never copies game assets/binaries."""
import argparse, csv, hashlib, json, shutil, subprocess
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone

def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def flat(src,dst):
    dst.mkdir(parents=True,exist_ok=True)
    for p in src.iterdir():
        if p.is_file() and p.suffix.lower() not in ('.dll','.exe','.pdb'): shutil.copy2(p,dst/p.name)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',required=True,type=Path);ap.add_argument('--source',required=True,type=Path);ap.add_argument('--evidence',required=True,type=Path);a=ap.parse_args();r=a.run;e=a.evidence
    owner=load(r/'owner.json');assert owner['kind']=='PLAYER-02 isolated runtime acceptance'
    assert not e.exists(),'Evidence publishing is append-only: choose a new target'
    e.mkdir(parents=True);shutil.copy2(r/'owner.json',e/'owner.json')
    for name in ('ReadOnlyAudit','ProductIdentity','Preflight'):
        if (r/name).exists():shutil.copytree(r/name,e/name)
    for name in ('worker-build.log','worker2-build.log'):
        if (r/name).exists():shutil.copy2(r/name,e/name)
    # Build collector already filters executable output, Library, source bodies, junctions.
    for b in ('R','T'):
        subprocess.run([__import__('sys').executable,'-B',str(a.source/'ProjectDocs/WanxiangGuitu/DeliveryBuild01/collect_results.py'),'--root',str(r/b),'--evidence',str(e/('Build-'+b))],check=True)
    rows=[]
    for d in sorted((r/'Attempts').iterdir()):
        if not d.is_dir():continue
        target=e/'Attempts'/d.name;flat(d,target)
        if (d/'StorageAfter').exists():shutil.copytree(d/'StorageAfter',target/'StorageAfter')
        if not (d/'results.json').exists():
            rows.append(dict(attempt=d.name,mode='LAUNCH',status='FAIL',exitCode=None,timedOut=False,terminal='PRELAUNCH_TOOL_REJECTION',checks=0,source='No runtime claimed; see failure history'))
            continue
        o=load(d/'owner.json');mode=o['mode'];runtime=next((x for x in load(d/'results.json') if x['name']=='runtime.'+mode),None)
        result=d/'StorageAfter'/('result-'+mode+'.json');v=load(result) if result.exists() else {}
        # Original events can be cumulative; distinguish immutable stage receipt and process return.
        rows.append(dict(attempt=d.name,mode=mode,status=v.get('status','NOT_RUN'),exitCode=runtime.get('exitCode') if runtime else None,timedOut=runtime.get('timedOut') if runtime else None,terminal=v.get('terminal','NO_RECEIPT'),checks=len(v.get('checks',[])),source=str(target.relative_to(e)),assemblySha256=o['assemblySha256']))
    original=load(r/'ReadOnlyAudit/source-files.json');changed=[x['path'] for x in original if not (a.source/x['path']).exists() or sha(a.source/x['path'])!=x['sha256']]
    assert not changed, 'User/product input changed; stop and investigate rather than overwrite'
    proofs=[load(p) for p in (r/'ProductIdentity').glob('*.json') if p.name.startswith('proof-')]
    assert proofs and all(p['status']=='PASS' for p in proofs)
    builds=[]
    for b in ('R','T'):builds+=load(e/('Build-'+b)/'RESULTS.json')['runs']
    # Full warnings are retained; compare final release against the first completed release in this run.
    release=next(x for x in builds if '/R/' in x['root'].replace('\\','/'))
    summary=dict(utc=datetime.now(timezone.utc).isoformat(),startSha=owner['head'],sourceFiles=len(original),sourceChanges=changed,productChangesCommitted=subprocess.check_output(['git','diff','--name-only',owner['head'],'HEAD','--','Assets','Packages','ProjectSettings'],cwd=a.source,text=True).splitlines(),attempts=rows,attemptCounts=dict(Counter(x['status'] for x in rows)),builds=builds,exclusionProofs=proofs,releaseWarnings=release['build']['warnings'],native='NOT_RUN',human='NOT_RUN',performance='NOT_RUN',historicalUnresolved=['D3D12 UNKNOWN','Editor cyan frame','Editor.Search','JobTempAlloc'],scope='Acceptance non-development Player automation; virtual devices and queued window messages; not native/human')
    assert not summary['productChangesCommitted']
    dump(e/'RESULTS.json',summary)
    with (e/'RESULTS.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    manifest=[dict(path=p.relative_to(e).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(e.rglob('*')) if p.is_file()]
    dump(e/'manifest.json',manifest)
    print(json.dumps(dict(attempts=summary['attemptCounts'],builds=len(builds),sourceChanges=changed)))
if __name__=='__main__':main()
