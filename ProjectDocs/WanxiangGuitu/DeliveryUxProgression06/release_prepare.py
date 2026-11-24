import pathlib,json,hashlib,subprocess,csv,shutil,datetime
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];G=D/'RELEASE_RUNTIME'
G.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git','--no-optional-locks','-c','core.longpaths=true',*a],cwd=R).decode()
assert git('branch','--show-current').strip()=='feature/ux-progression-06-region-records'
assert git('rev-parse','HEAD').strip()=='1c3fb90bf5902c147fda35252dc59e3b3a5f8872'
assert not git('diff','--cached','--name-only').strip()
for row in json.loads((D/'BUILD12_RELEASE/FROZEN_INPUT_MANIFEST.json').read_text()):assert sha(R/row['path'])==row['sha256'],row['path']
build=json.loads((D/'BUILD12_RELEASE/RESULT.json').read_text())
for a in build['artifacts']:assert sha(pathlib.Path(a['path']))==a['sha256'] and pathlib.Path(a['path']).stat().st_size==a['bytes']
for row in csv.DictReader((D/'PROTECTION_SHA256.tsv').open(encoding='utf-8'),delimiter='\t'):assert sha(R/row['Path'])==row['CurrentSha256'],row['Path']
for row in csv.DictReader((D/'FILES_CHANGED.tsv').open(encoding='utf-8'),delimiter='\t'):assert sha(R/row['Path'])==row['Sha256'],row['Path']
shutil.copyfile(D/'PLAYER_RUN_MATRIX.csv',G/'ORIGINAL_30_RUN_MATRIX.csv')
shutil.copyfile(D/'EVIDENCE/INDEX.json',G/'INDEX_BEFORE_RELEASE.json')
old=json.loads((D/'EVIDENCE/INDEX.json').read_text())
protected=[x for x in old['files'] if x['path'].startswith('EVIDENCE/')]
assert all(sha(D/x['path'])==x['sha256'] for x in protected)
refs=git('show-ref');index=pathlib.Path(git('rev-parse','--git-path','index').strip());index=index if index.is_absolute() else R/index
state={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':git('rev-parse','HEAD').strip(),'branch':git('branch','--show-current').strip(),
 'indexSha256':sha(index),'trackedDiff':git('diff','--name-status'),'status':git('status','--porcelain=v1','--untracked-files=all'),
 'sparseCheckout':subprocess.run(['git','config','--get','core.sparseCheckout'],cwd=R,capture_output=True,text=True).stdout.strip(),'refs':refs,'build':build,'oldEvidence':protected}
(G/'START.json').write_text(json.dumps(state,indent=2))
source=D/'EVIDENCE/STORAGE/UI_REUSED_UX05_CAPACITY/WanxiangGuitu'
target=D/'EVIDENCE/STORAGE/RELEASE_FINAL_COPY01/WanxiangGuitu'
assert not target.exists();target.parent.mkdir(parents=True,exist_ok=False)
finger=[]
for p in sorted(source.rglob('*')):
    assert not p.is_symlink()
    if not p.is_file():continue
    rel=p.relative_to(source);q=target/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
    assert q.read_bytes()==p.read_bytes()
    finger.append({'path':rel.as_posix(),'size':p.stat().st_size,'sha256':sha(p),'sourceMtimeNs':p.stat().st_mtime_ns})
(G/'SAMPLE_COPY.json').write_text(json.dumps({'source':str(source),'target':str(target),'files':finger,'note':'Registered isolated UX06 UI sample; no original UX05 or user storage accessed.'},indent=2))
print(json.dumps({'status':'PASS','copiedFiles':len(finger),'protectedExistingEvidence':len(protected),'releaseDllSha256':build['artifacts'][1]['sha256']}))
