"""Read-only COMBAT01 provenance and evidence publication; never starts Unity or edits saves."""
import argparse,csv,gzip,hashlib,json,subprocess
from pathlib import Path
from datetime import datetime,timezone

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 if not (a.root/'owner.json').is_file() or a.output.exists():raise ValueError('Owned root and fresh publication required')
 owner=load(a.root/'owner.json');assert Path(owner['source']).resolve()==a.repo.resolve()
 rows=[]
 original=load(a.root/'source-files.json');allowed={f'Assets/CombatPrototype/{n}.cs' for n in ['AdventureCombat','CombatFeedback','FantasyActorVisual','HeroDodge']}
 changes=[]
 for x in original:
  p=a.repo/x['path'];current=sha(p);old=x['sha256'];changed=current.upper()!=old.upper()
  if changed:changes.append(dict(path=x['path'],before=old,after=current))
  if changed and x['path'] not in allowed:raise ValueError('Unexpected product input change: '+x['path'])
 protected=[dict(path=x['path'],before=x['sha256'],after=sha(a.repo/x['path'])) for x in load(a.root/'protected-inputs.json')]
 if any(x['before'].upper()!=x['after'].upper() for x in protected):raise ValueError('Protected user input changed; inspect without overwriting')
 buildproof=[]
 for kind in ['R2','T3']:
  builds=list((a.root/kind).glob('*/owner.json'));assert len(builds)==1
  b=builds[0].parent;inputs=load(b/'copied-source-files.json');mismatches=[]
  for item in inputs:
   path=item['path'].replace('\\','/');actual=sha(a.repo/path)
   if actual.upper()!=item['source'].upper() or item['source']!=item['copy']:mismatches.append(path)
  assert not mismatches,(kind,mismatches)
  buildproof.append(dict(kind=kind,sourceFiles=len(inputs),matchesCurrentProductInputs=True,report=load(b/'Results/build-report-messages.json')))
 final=load(a.root/'After4/combat01.json');assert final['status']=='PASS'
 before=load(a.root/'Baseline2/combat01.json');after={x['name']:x for x in final['checks']}
 comparison=[dict(name=x['name'],before=x['status'],after=after.get(x['name'],{}).get('status','NOT_RUN')) for x in before['checks']]
 rows.extend(dict(layer='controlled-final',name=x['name'],status=x['status']) for x in final['checks'])
 for item in load(a.root/'Regression1/results.json'):rows.append(dict(layer=item['scope'],name=item['name'],status=item['status']))
 business=load(a.root/'ProductIdentity/story-business.json');assert business['status']=='PASS'
 attempts=[]
 for p in sorted((a.root/'Attempts').glob('*/owner.json')):
  attempt=p.parent;data=load(p);results=load(attempt/'results.json')
  if isinstance(results,dict):results=[results]
  for x in results:
   if x['name'].startswith('runtime.'):
    attempts.append(dict(path=str(attempt),mode=data['mode'],storage=data['storage'],build=data['build'],status=x['status'],exitCode=x['exitCode'],timedOut=x['timedOut']))
 for x in attempts:rows.append(dict(layer='acceptance-player-attempt',name=x['path'],status=x['status']))
 # All attempts stay visible, not just the final six.
 assert len([x for x in attempts if Path(x['storage']).name=='Story2' and x['status']=='PASS'])==6
 a.output.mkdir(parents=True)
 summary=dict(utc=datetime.now(timezone.utc).isoformat(),baseline=owner['head'],productFileCount=len(original),changes=changes,protectedInputs=protected,buildProof=buildproof,baselineCounts={k:sum(x['status']==k for x in before['checks']) for k in ['PASS','FAIL']},finalControlledCounts={k:sum(x['status']==k for x in final['checks']) for k in ['PASS','FAIL']},comparison=comparison,attempts=attempts,business=business)
 write(a.output/'analysis.json',summary)
 with (a.output/'results.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['layer','name','status']);w.writeheader();w.writerows(rows)
 sources=['Baseline','Baseline2','Baseline3','After1','After2','After3','After4','SaveRun','SaveResume','Regression1','ReleaseSmoke','Attempts','Story','Story2','ProductIdentity']
 sources += [str(p.relative_to(a.root)) for variant in ['R','T','R2','T2','T3'] for p in (a.root/variant).glob('*') if p.is_dir()]
 manifest=[]
 for rel in sources:
  source=a.root/rel
  if not source.exists():continue
  for p in sorted(source.rglob('*')):
   if not p.is_file():continue
   sub=p.relative_to(source)
   if any(t in sub.parts for t in ['Project','Library','Temp','Release','Worker','Deferred']):continue
   if p.suffix.lower() not in ['.json','.jsonl','.csv','.txt','.md','.png','.log','.stdout','.stderr','.ps1','.py','.cs','.gitattributes']:continue
   dest=a.output/rel/sub;dest.parent.mkdir(parents=True,exist_ok=True);raw=p.read_bytes()
   if p.suffix=='.log':dest=dest.with_suffix('.log.gz');dest.write_bytes(gzip.compress(raw,mtime=0))
   else:dest.write_bytes(raw)
   manifest.append(dict(source=str(p),path=dest.relative_to(a.output).as_posix(),sourceBytes=len(raw),sourceSha256=hashlib.sha256(raw).hexdigest(),publishedSha256=sha(dest),partialSnapshot=rel in ['Baseline3','SaveRun','SaveResume']))
 for name in ['owner.json','source-files.json','protected-inputs.json','protected-inputs-check.json','worktree-before.txt','task.md','owned-processes.json']:
  p=a.root/name
  if p.exists():
   dest=a.output/'Inputs'/name;dest.parent.mkdir(exist_ok=True);dest.write_bytes(p.read_bytes());manifest.append(dict(source=str(p),path=dest.relative_to(a.output).as_posix(),sourceBytes=p.stat().st_size,sourceSha256=sha(p),publishedSha256=sha(dest)))
 write(a.output/'manifest.json',manifest)
 print(json.dumps(dict(evidence=str(a.output),files=len(manifest),controlled=summary['finalControlledCounts'],business=business['status']),ensure_ascii=False))
if __name__=='__main__':main()
