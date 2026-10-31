"""Cross-check actual raw process receipts, semantic summaries and frozen inputs."""
import argparse,hashlib,json,collections,subprocess
from pathlib import Path

def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
    a=argparse.ArgumentParser();a.add_argument('root',type=Path);a.add_argument('output',type=Path);o=a.parse_args();r=o.root;checks=[];runs=[]
    def check(n,b):checks.append(dict(name=n,status='PASS' if b else 'FAIL'))
    for name,process in [('EditorFinal','CP03Editor.Run'),('EditorDiagnosis','CP03Editor.Run'),('RuntimeFinal','CP03Runtime')]:
        folder=r/name;q=load(folder/'Semantic/acceptance.json');raw=load(folder/'presentation.json');results=load(folder/'results.json');results=results if isinstance(results,list) else [results]
        os=load(folder/(process+'.exit.json'));row=next(x for x in results if x['name']==process)
        check(name+' OS/Step/semantic process exit consistent',os['exitCode']==row['exitCode']==q['process']['exitCode']==0 and not os['forcedTermination'] and not row['timedOut'])
        counts=dict(collections.Counter(x['status'] for x in raw['rows']));check(name+' raw/assertion counts',q['counts']==counts==dict(PASS=291,UNRESOLVED=2))
        check(name+' blocking and receipt hash',q['overallStatus']=='BLOCKED' and q['assertionStatus']=='UNRESOLVED' and q['exitCode']==2 and q['receiptSHA256']==hashlib.sha256((folder/'presentation.json').read_bytes()).hexdigest())
        check(name+' semantic Markdown agreement','**BLOCKED**' in (folder/'Semantic/REPORT.md').read_text(encoding='utf-8'))
        if name!='EditorDiagnosis':check(name+' root Markdown agreement','**BLOCKED**' in (folder/'REPORT.md').read_text(encoding='utf-8-sig'))
        if name=='RuntimeFinal':check('runtime semantic-receipt is UNRESOLVED',next(x for x in results if x['name']=='semantic-receipt')['status']=='UNRESOLVED')
        runs.append(dict(name=name,processStatus=row['status'],processExit=os['exitCode'],timedOut=row['timedOut'],forcedTermination=os['forcedTermination'],counts=counts,overallStatus=q['overallStatus'],classifierExit=q['exitCode']))
    check('selftest 50 PASS',load(r/'SelfTestDelivery/selftest.json')['counts']==dict(PASS=50))
    check('frozen product input no mismatch',not load(r/'frozen-build-product-binding.json')['mismatch'])
    check('1802 protected files no change',load(r/'protected-after.json')['count']==1802 and not load(r/'protected-after.json')['changed'] and load(r/'protected-after.json')['statusUnchanged'])
    check('no product Git diff',not (r/'product-diff.txt').read_bytes())
    check('strict audit PASS',load(r/'locked-contract-delivery.json')['status']=='PASS')
    result=dict(consistencyStatus='FAIL' if any(x['status']=='FAIL' for x in checks) else 'PASS',checks=checks,runs=runs,
                deliveryOverall='BLOCKED',open=['two near Staff cases UNRESOLVED','CombatAim change WAITING_AUTHORIZATION','historical engine issues UNRESOLVED'],NOT_RUN=['Profiler CPU/GC/GPU/particles/pools/audio/long-duration/load-unload','native input/U16','independent human feel/readability/audio/playtest','fresh pure release build in R1'])
    if o.output.exists():raise ValueError('fresh verification output required')
    o.output.write_text(json.dumps(result,indent=2),encoding='utf-8');print(result['consistencyStatus'],len(checks),'consistency checks');return 1 if result['consistencyStatus']=='FAIL' else 0
if __name__=='__main__':raise SystemExit(main())
