"""Cross-check native evidence, immutable snapshots and all retained tests."""
import argparse,collections,csv,hashlib,importlib.util,inspect,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    a=argparse.ArgumentParser();a.add_argument('root',type=Path);a.add_argument('--output',type=Path,required=True);o=a.parse_args();r=o.root;repo=HERE.parents[2];checks=[];runs=[]
    def check(name,ok):checks.append(dict(name=name,status='PASS' if ok else 'FAIL'))
    spec=importlib.util.spec_from_file_location('r12_verify_receipt',HERE.parent/'DeliveryCombatPresentation03/Receipt.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    check('no successful process defaults',all(inspect.signature(m.evaluate).parameters[x].default is None for x in ('process_status','exit_code','timed_out','process_receipt','exit_receipt')))
    for mode in ('Editor','Runtime'):
        folder=r/mode;q=load(folder/'Semantic/acceptance.json');raw=load(folder/'presentation.json');snapshot=load(folder/'process-results.json');items=snapshot if isinstance(snapshot,list) else [snapshot]
        name='CP03Editor.Run' if mode=='Editor' else 'CP03Runtime';scope='controlled-editor' if mode=='Editor' else 'nondevelopment-acceptance-player-controlled-combat-API'
        row=next(x for x in items if x['name']==name);native=load(folder/(name+'.exit.json'));p=q['process'];origin=load(folder/'process-origin.json')
        check(mode+' real status/exit/timeout',row['status']==p['reportedStatus']==p['status']=='PASS' and type(row['exitCode']) is int and row['exitCode']==native['exitCode']==p['exitCode']==0 and row['timedOut'] is False and p['timedOut'] is False and native['forcedTermination'] is False)
        check(mode+' file evidence eligible',p['evidenceStatus']=='PASS' and p['source']['kind']=='runner-result-and-native-exit' and p['source']['stage']==name and row['scope']==scope)
        check(mode+' no scalar success claims',p['claims']==dict(status=None,exitCode=None,timedOut=None))
        check(mode+' actual source paths',Path(p['source']['runnerReceipt']['path']).resolve()==(folder/'process-results.json').resolve() and Path(p['source']['exitReceipt']['path']).resolve()==(folder/(name+'.exit.json')).resolve())
        check(mode+' source receipt SHA',p['source']['runnerReceipt']['sha256']==digest(folder/'process-results.json')==origin['snapshotSHA256'].lower()==origin['sourceSHA256AtSnapshot'].lower() and p['source']['exitReceipt']['sha256']==digest(folder/(name+'.exit.json')))
        rawresults=load(folder/'results.json');allrows=rawresults if isinstance(rawresults,list) else [rawresults]
        check(mode+' snapshot process row unchanged',row==next(x for x in allrows if x['name']==name))
        check(mode+' raw assertion digest',q['receiptSHA256']==digest(folder/'presentation.json'))
        counts=dict(collections.Counter(x['status'] for x in raw['rows']));csvrows=list(csv.DictReader((folder/'Semantic/assertions.csv').open(encoding='utf-8-sig',newline='')))
        check(mode+' raw JSON/CSV counts',counts==q['counts']==dict(collections.Counter(x['status'] for x in csvrows))==dict(PASS=291,UNRESOLVED=2))
        pin=m.FROZEN_CONTRACTS[mode];contract=HERE.parent/'DeliveryCombatPresentation03R11/Contracts'/(mode+'.json')
        check(mode+' frozen contract and role still bound',q['binding']['status']=='PASS' and q['binding']['profile']==mode and q['contractSHA256']==pin['sha256']==digest(contract) and raw['layer']==pin['layer'] and raw['scope']==pin['scope'])
        check(mode+' unresolved stays blocked',q['overallStatus']=='BLOCKED' and q['exitCode']==2 and q['assertionStatus']=='UNRESOLVED')
        check(mode+' root/semantic Markdown agreement',all('**BLOCKED**' in f.read_text(encoding='utf-8-sig') for f in (folder/'REPORT.md',folder/'Semantic/REPORT.md')))
        if mode=='Runtime':check('runtime semantic not process success',next(x for x in allrows if x['name']=='semantic-receipt')['status']=='UNRESOLVED')
        runs.append(dict(mode=mode,processExit=p['exitCode'],processStatus=p['status'],evidenceStatus=p['evidenceStatus'],counts=counts,overall=q['overallStatus'],classifierExit=q['exitCode'],source=p['source']))
    check('old50 retained and pass',load(r/'Legacy50-Final/selftest.json')['counts']==dict(PASS=50))
    check('R11 33 retained and pass',load(r/'Legacy33-Final/selftest.json')['counts']==dict(PASS=33,FAIL=0))
    check('new60 process tests pass',load(r/'ProcessTests-Delivery/selftest.json')['counts']==dict(PASS=60,FAIL=0))
    before=load(r/'Before/regressions.json');check('pre-fix failures and controls retained',before['counts']==dict(PASS=2,FAIL=6) and len(before['rows'])==8)
    real=load(r/'RealEvidenceChecks/results.json');check('8 real proof reader checks pass',real['counts']==dict(PASS=8,FAIL=0))
    source_rows=real['rows'];check('original actual receipts never edited',all(digest(Path(path))==h for x in source_rows for path,h in x['originalSourceSHA256'].items()))
    protection=load(r/'protected-after.json');check('protected original files unchanged',protection['count']==3476 and not protection['changed'] and protection['statusUnchanged'])
    check('protected current bytes',all(digest(Path(x['root'])/x['path'])==x['sha256'] for x in load(r/'protected-before.json')))
    inputs=load(r/'input-binding.json');check('frozen1147 no diff',inputs['count']==1147 and not inputs['mismatch'])
    check('current frozen products and binaries',all(digest(r/'P/Project'/x['path'])==x['expected'] for x in inputs['files']) and all(digest(Path(x['path']))==x['sha256'] for x in inputs['binaries']))
    check('no Assets Packages ProjectSettings diff',not (r/'product-diff.txt').read_bytes())
    oldtests=['ProjectDocs/WanxiangGuitu/DeliveryCombatPresentation03/SelfTest-R1.py','ProjectDocs/WanxiangGuitu/DeliveryCombatPresentation03R11/SelfTest-R11.py']
    check('original legacy harness sources unchanged',not subprocess.check_output(['git','-C',str(repo),'diff','00a8d740','--']+oldtests))
    check('locked13 sampling and spawns',load(r/'locked-contract.json')['status']=='PASS')
    check('PS syntax',load(r/'powershell-syntax.json')['status']=='PASS')
    result=dict(consistencyStatus='FAIL' if any(x['status']=='FAIL' for x in checks) else 'PASS',checks=checks,runs=runs,deliveryOverall='BLOCKED',note='143 synthetic tool checks and 8 actual-exit reader checks do not replace actual gameplay/native UI/human validation.')
    if o.output.exists():raise ValueError('fresh output required')
    o.output.write_bytes(json.dumps(result,indent=2).encode());print(result['consistencyStatus'],len(checks),'consistency checks');return 1 if result['consistencyStatus']=='FAIL' else 0
if __name__=='__main__':raise SystemExit(main())
