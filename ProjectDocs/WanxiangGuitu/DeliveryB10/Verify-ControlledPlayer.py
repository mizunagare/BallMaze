"""Strict receipt/log/storage audit for separate controlled Player, never native UI."""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--case',required=True);a=p.parse_args()
root=a.root.resolve();r=json.loads((root/'b10-controlled-result.json').read_text('utf-8-sig'))
events=[json.loads(x) for x in (root/'entry-audit.jsonl').read_text('utf-8-sig').splitlines()]
storage=[json.loads(x) for x in (root/'storage-audit.jsonl').read_text('utf-8-sig').splitlines()]
log=(root/f'player-{a.case}.log').read_text('utf-8-sig',errors='replace')
save=json.loads((root/'WanxiangGuitu/ForestRuins/save.json').read_text('utf-8-sig'));data=json.loads(save['payload'])
def within(name):
 path=Path(name).resolve();return path==root or root in path.parents
checks={'completed':r['status']=='PASS' and r['quitRequested'],'quitRequest':any(x['phase']=='title-exit-request' for x in events),'quitAudit':any(x['phase']=='title-quit' for x in events),'storageIsolated':all(within(x['path']) for x in storage),'saveChecksum':hashlib.sha256(save['payload'].encode()).hexdigest().upper()==save['checksum'],'profileMatches':data['profile']['profileId']==r['profile'],'revisionMatches':save['revision']==r['revision'],'noNativeCrash':not any(x in log for x in ['Got a UNKNOWN','Native Crash Reporting','Crash!!!','Unhandled Exception:']),'noRuntimeException':not any(x in log for x in ['NullReferenceException:','MissingReferenceException:','InvalidOperationException:','System.Exception:'])}
if a.case in ('read','continue'):checks['actualActiveRun']=data.get('hasActiveRun') and bool(r['run']) and data['activeRun']['runId']==r['run']
result=dict(status='PASS' if all(checks.values()) else 'FAIL',scope='Controlled nondevelopment Player callbacks + strict audit, NOT native input/titlebar/human',checks=checks,scenario=a.case,revision=save['revision'],saveSha256=hashlib.sha256((root/'WanxiangGuitu/ForestRuins/save.json').read_bytes()).hexdigest())
(root/f'b10-verification-{a.case}.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');print(json.dumps(result));raise SystemExit(0 if result['status']=='PASS' else 1)
