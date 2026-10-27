"""Read-only equality checks on the actual sampled chain, no business/save mutation."""
import argparse,hashlib,json
from pathlib import Path
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ident(s):return {k:s.get(k) for k in ['profileId','runId','region','seed','layout','streams','ledger','gear']}
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();checks=[];cases=a.root/'Runtime/Cases'
 for d in sorted(cases.glob('Loop-*')):
  if not (d/'case-result.json').exists() or load(d/'case-result.json')['exitCode']!=0:continue
  before=load(d/'snapshot-Observe-perf-entered.json');after=load(d/'snapshot-Observe-perf-final.json');pending=load(d/'snapshot-Observe-perf-pending.json');committed=load(d/'snapshot-Observe-perf-committed.json')
  ps=load_str(pending['settlement']);cs=load_str(committed['settlement']);r=load_str(after['run'])
  conditions=dict(newRun=before['runId']!=after['runId'],sameProfile=before['profileId']==after['profileId'],forest=r['mode']==2,actualExtracted=ps['outcome']==0,pending=ps['status']==0,committed=cs['status']==1,sameSettlement=ps['settlementId']==cs['settlementId'])
  checks.append(dict(case=d.name,kind='actual-loop',status='PASS' if all(conditions.values()) else 'FAIL',conditions=conditions,oldRun=before['runId'],newRun=after['runId'],seed=after['seed']))
 for d in sorted(cases.glob('Resume-*')):
  if not (d/'case-result.json').exists() or load(d/'case-result.json')['exitCode']!=0:continue
  c=load(d/'perf-config.json');source=cases/Path(c['fixture'].replace('\\','/')).parent.name;expect=load(source/'snapshot-Observe-perf-final.json');actual=load(d/'snapshot-Observe-perf-resumed.json');ei=ident(expect);ai=ident(actual)
  equal={k:ei[k]==ai[k] for k in ei};checks.append(dict(case=d.name,kind='actual-new-process-restore',status='PASS' if all(equal.values()) else 'FAIL',equal=equal,expectedSha256=hashlib.sha256(json.dumps(ei,sort_keys=True).encode()).hexdigest(),actualSha256=hashlib.sha256(json.dumps(ai,sort_keys=True).encode()).hexdigest(),source=str(source),run=actual['runId'],seed=actual['seed']))
 passed=len(checks)==6 and all(c['status']=='PASS' for c in checks)
 (a.root/'runtime-chain-audit.json').write_text(json.dumps(dict(status='PASS' if passed else 'FAIL',checks=checks,scope='Actual loop and restore snapshots; frame/AI motion may progress, immutable identities/layout/streams/ledger/gear compared without editing saves'),ensure_ascii=False,indent=2),encoding='utf-8');print([(c['case'],c['status']) for c in checks])
 if not passed:raise SystemExit(1)
def load_str(v):return json.loads(v) if isinstance(v,str) else v
if __name__=='__main__':main()
