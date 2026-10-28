"""Publish completed, explicitly owned R1 test evidence, never product binaries or real saves."""
import argparse,gzip,hashlib,json,re,subprocess
from pathlib import Path
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 if a.out.exists() or load(a.root/'owner.json')['kind']!='PLAYER-02 isolated runtime acceptance':raise ValueError('Fresh publication and owned root required')
 if load(a.root/'owned-processes.json'):raise ValueError('New run processes still active; preserve, do not clean')
 if load(a.root/'Analysis2/analysis.json')['status']!='PASS':raise ValueError('Independent final audit not PASS')
 a.out.mkdir(parents=True);records=[]
 def publish(data,rel,source,compress=False):
  dest=a.out/rel;dest.parent.mkdir(parents=True,exist_ok=True)
  if compress:dest=dest.with_suffix(dest.suffix+'.gz');encoded=gzip.compress(data,mtime=0)
  else:encoded=data
  dest.write_bytes(encoded);records.append(dict(path=dest.relative_to(a.out).as_posix(),source=source,rawSha256=sha(data),publishedSha256=sha(encoded),bytes=len(data),compression='gzip' if compress else 'none'))
 folders=['Attempts','Story1','Close1','Close2','Close3','Rules','Analysis1','Analysis2','ProductIdentity','HostSource','ObserverSource','ObserverSource2','ObserverSource3','Observer','Observer2','Observer3','Host']
 folders += [str(x.relative_to(a.root)) for x in (a.root/'T').glob('*') if x.is_dir()]
 for name in folders:
  folder=a.root/name
  if not folder.exists():continue
  for f in sorted(folder.rglob('*')):
   if not f.is_file():continue
   relative=f.relative_to(folder)
   if any(x in relative.parts for x in ['Project','Library','Temp','Release','bin','obj','fixtures','legacy-forest-v9']):continue
   if f.suffix.lower() not in ['.json','.jsonl','.csv','.txt','.md','.png','.log','.stdout','.stderr','.ps1','.py','.cs','.csproj']:continue
   publish(f.read_bytes(),Path(name)/relative,str(f),f.suffix=='.log')
 for name in ['owner.json','source-files.json','protected-inputs.json','worktree-before.txt','task.md','owned-processes.json','release-provenance.json','warning-inventory.json','tool-binary-hashes.json','Story1-stages.json','full-release-hashes.json']:
  f=a.root/name
  if f.exists():publish(f.read_bytes(),Path('Inputs')/name,str(f))
 prefix='ProjectDocs/WanxiangGuitu/DeliveryCombat01/'
 legacy=['ACCEPTANCE.md','Evidence/Run-1028-093640/ReleaseSmoke/process.json','Evidence/Run-1028-093640/ReleaseSmoke/results.json','Evidence/Run-1028-093640/ReleaseSmoke/player.log.gz','Evidence/Run-1028-093640/Baseline3/results.json','Evidence/Run-1028-093640/SaveRun/results.json']
 for name in legacy:
  repoPath=prefix+name;blob=subprocess.check_output(['git','show','be448f56cb629022047c5de35ca3bfb03eac7604:'+repoPath],cwd=a.repo)
  data=blob
  if blob.startswith(b'version https://git-lfs.github.com/spec/v1'):
   data=(a.repo/repoPath).read_bytes();oid=re.search(rb'oid sha256:([0-9a-f]+)',blob).group(1).decode();assert sha(data)==oid
  rel=Path('History')/name.replace('Evidence/Run-1028-093640/','');publish(data,rel,'git:be448f56cb629022047c5de35ca3bfb03eac7604:'+repoPath);records[-1]['gitBlobSha256']=sha(blob)
 (a.out/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(dict(status='PASS',files=len(records),bytes=sum(x['bytes'] for x in records),evidence=str(a.out))))
if __name__=='__main__':main()
