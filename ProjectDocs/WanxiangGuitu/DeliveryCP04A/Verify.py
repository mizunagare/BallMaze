"""Final readonly CP04 evidence/protection verification, not a product fix verdict."""
import argparse,hashlib,json,subprocess,collections
from pathlib import Path
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('repo',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=a.root;rows=[]
def check(n,ok):rows.append(dict(name=n,status='PASS' if ok else 'FAIL'))
check('2329 protected original bytes',all(digest(Path(x['root'])/x['path'])==x['sha256'] for x in load(r/'protected-before.json')))
check('five historical raw sources',all(digest(Path(x['path']))==x['sha256'] for x in load(r/'historical-before.json')))
check('user status exact',subprocess.check_output(['git','-C','H:/unity/WanxiangGuitu','status','--porcelain'])==(r/'main-status-before.txt').read_bytes())
check('no product diff',not subprocess.check_output(['git','-C',str(a.repo),'diff','72db192a527bd256e2ba18cd7ab334d8334051da','--','Assets','Packages','ProjectSettings']))
x=load(r/'product-input-binding.json');check('1163 frozen products',x['count']==1163 and not x['mismatch'] and all(digest(r/'P/Project'/x['path'])==x['expected'] for x in x['files']))
check('original24 exact',load(r/'paired-24.json')['count']==24 and all(x['originEqual'] and x['directionEqual'] for x in load(r/'paired-24.json')['rows']))
check('six analysis checks',load(r/'Analysis/verification.json')['counts']==dict(PASS=6))
for folder,name in [('Historical','CP03Editor.Run'),('Matrix','CP04Editor.Run'),('CameraWall','CP04Editor.CameraWall')]:
 d=r/folder;items=load(d/'results.json');items=items if isinstance(items,list) else [items];row=next(x for x in items if x['name']==name);cmd=load(d/(name+'.command.json'));native=load(d/(name+'.exit.json'));desktop=load(d/(name+'.desktop-process.json'))
 check(folder+' native process chain',row['status']=='PASS' and row['exitCode']==native['exitCode']==0 and row['timedOut'] is False and native['forcedTermination'] is False and cmd['hostPid']==native['hostPid'] and Path(cmd['exe']).resolve()==Path(desktop['exe']).resolve()==Path(row['command'][0]).resolve() and cmd['arguments']==row['command'][1:] and desktop['inputDesktopActive'] is False)
 check(folder+' no diagnostic exception',not (d/'exception.txt').exists())
q=load(r/'CameraWall/diagnosis.json');check('actual camera wall ray hits',len(q['cases'])==2 and len(q['shots'])==2 and all(x['hpLoss']==0 and x['remainingProjectiles']==0 for x in q['cases']) and all(x['reason']=='CAMERA_SURFACE_BEHIND_MUZZLE' and x['rayHits'][0]['name']=='CP04-camera-wall-verified' and x['rayHits'][0]['legal'] for x in q['shots']))
q=load(r/'Historical/Semantic/acceptance.json');check('R13 binding and historical UR retained',q['process']['source']['associationStatus']=='PASS' and q['counts']==dict(PASS=291,UNRESOLVED=2) and q['overallStatus']=='BLOCKED' and q['exitCode']==load(r/'Historical/classifier-exit.json')['exitCode']==2)
check('wrapper final parse',load(r/'wrapper-parse-final.json')['status']=='PASS')
q=dict(scope='Evidence consistency only; historical aim defects remain UNRESOLVED',counts=dict(collections.Counter(x['status'] for x in rows)),rows=rows);a.output.write_text(json.dumps(q,indent=2),encoding='utf-8');print(json.dumps(q['counts']));raise SystemExit(any(x['status']=='FAIL' for x in rows))
