"""Read-only R1.1 cross-check: trust the R1 Git bytes, not supplied receipt metadata."""
import argparse,csv,hashlib,importlib.util,json,subprocess,collections
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE='42cfd3d8f3abd4861cd672dbb8f440fae48e4b65'

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
    a=argparse.ArgumentParser();a.add_argument('root',type=Path);a.add_argument('--output',type=Path,required=True);o=a.parse_args();r=o.root;repo=HERE.parents[2];checks=[];runs=[];pins={}
    def check(n,ok):checks.append(dict(name=n,status='PASS' if ok else 'FAIL'))
    spec=importlib.util.spec_from_file_location('receipt_r11',HERE.parent/'DeliveryCombatPresentation03/Receipt.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    for mode,old in [('Editor','Final2'),('Runtime','Runtime2')]:
        source='ProjectDocs/WanxiangGuitu/DeliveryCombatPresentation03/Evidence/'+old+'/presentation.json'
        raw=subprocess.check_output(['git','-C',str(repo),'show',BASE+':'+source]);q=json.loads(raw);pin=m.FROZEN_CONTRACTS[mode];pins[mode]=dict(sha256=hashlib.sha256(raw).hexdigest(),layer=q['layer'],scope=q['scope'])
        check(mode+' code pin equals immutable R1 Git bytes',pin['sha256']==pins[mode]['sha256'] and pin['layer']==q['layer'] and pin['scope']==q['scope'] and pin['sourceCommit']==BASE and pin['sourcePath']==source)
        check(mode+' snapshot equals immutable R1 bytes',(HERE/'Contracts'/(mode+'.json')).read_bytes()==raw)
        frozen_names={x['name'] for x in q['rows']}
        folder=r/mode;result=read(folder/'Semantic/acceptance.json');data=read(folder/'presentation.json');items=read(folder/'results.json');items=items if isinstance(items,list) else [items];name='CP03Editor.Run' if mode=='Editor' else 'CP03Runtime'
        process=next(x for x in items if x['name']==name);native=read(folder/(name+'.exit.json'));b=result['binding']
        check(mode+' native/Step/semantic process agreement',native['exitCode']==process['exitCode']==result['process']['exitCode']==0 and process['status']=='PASS' and result['process']['status']=='PASS' and not native['forcedTermination'] and not process['timedOut'])
        counts=dict(collections.Counter(x['status'] for x in data['rows']));csv_rows=list(csv.DictReader((folder/'Semantic/assertions.csv').open(encoding='utf-8-sig',newline='')))
        check(mode+' raw/JSON/CSV counts agreement',counts==result['counts']==dict(collections.Counter(x['status'] for x in csv_rows))==dict(PASS=291,UNRESOLVED=2))
        check(mode+' same frozen assertion set',{x['name'] for x in data['rows']}==frozen_names and len(data['rows'])==293)
        check(mode+' explicit profile binding eligible',b['status']=='PASS' and b['profile']==mode and b['contractVerified'] and b['requiredCount']==293)
        check(mode+' expected and actual SHA match immutable pin',b['expectedSHA256']==b['actualSHA256']==result['contractSHA256']==pins[mode]['sha256'])
        check(mode+' receipt/contract/registry layer scope agree',all(b['expected'+field.title()]==b['contract'+field.title()]==b['receipt'+field.title()]==data[field]==pins[mode][field] for field in ('layer','scope')))
        check(mode+' raw receipt digest bound',result['receiptSHA256']==hashlib.sha256((folder/'presentation.json').read_bytes()).hexdigest())
        check(mode+' assertions remain unresolved and overall blocked',result['assertionStatus']=='UNRESOLVED' and result['overallStatus']=='BLOCKED' and result['exitCode']==2 and result['integrity']=='PASS')
        check(mode+' Markdown overall agreement',all('**BLOCKED**' in p.read_text(encoding='utf-8-sig') for p in (folder/'REPORT.md',folder/'Semantic/REPORT.md')))
        if mode=='Runtime':check('runtime semantic-receipt correctly UNRESOLVED',next(x for x in items if x['name']=='semantic-receipt')['status']=='UNRESOLVED')
        runs.append(dict(layer=mode,processExit=native['exitCode'],timedOut=process['timedOut'],forcedTermination=native['forcedTermination'],bindingStatus=b['status'],contractSHA256=result['contractSHA256'],assertionCounts=counts,overallStatus=result['overallStatus'],classifierExit=result['exitCode']))
    check('legacy 50 regression checks retained',read(r/'LegacySelfTestFinal/selftest.json')['counts']==dict(PASS=50))
    check('binding 33 selftests',read(r/'BindingSelfTestFinal/selftest.json')['counts']==dict(PASS=33,FAIL=0))
    prior=read(r/'Before/regressions.json')['rows'];check('5 pre-fix erroneous passes retained',len(prior)==5 and all(x['status']=='FAIL' and x['actualOverall']=='PASS' and x['actualExit']==0 for x in prior))
    cross=read(r/'RealCrossContext/results.json');check('3 real receipt negatives correctly incomplete',len(cross)==3 and all(x['actualExit']==3 and x['overall']=='INCOMPLETE' and x['sourceUnchanged'] for x in cross))
    check('original real receipts unchanged after cross-context tests',all(hashlib.sha256(Path(x['source']).read_bytes()).hexdigest()==x['sourceSHA256'] for x in cross))
    protected=read(r/'protected-after.json');check('protected files and user status preserved',protected['count']==2664 and not protected['changed'] and protected['statusUnchanged'])
    check('current protected bytes still match',all((Path(x['root'])/x['path']).is_file() and hashlib.sha256((Path(x['root'])/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in read(r/'protected-before.json')))
    inputs=read(r/'input-binding.json')
    check('1147 frozen product inputs match',inputs['count']==1147 and not inputs['mismatch'])
    check('current isolated inputs and executable bytes match',all(hashlib.sha256((r/'P/Project'/x['path']).read_bytes()).hexdigest()==x['expected'] for x in inputs['files']) and all(hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()==x['sha256'] for x in inputs['binaries']))
    check('no product source diff',not (r/'product-diff.txt').read_bytes())
    check('locked audit PASS',read(r/'locked-contract.json')['status']=='PASS')
    check('PS syntax PASS',read(r/'powershell-syntax.json')['status']=='PASS')
    result=dict(consistencyStatus='FAIL' if any(x['status']=='FAIL' for x in checks) else 'PASS',checks=checks,runs=runs,contractPins=pins,deliveryOverall='BLOCKED',note='Binding remediation is verified; two historical Staff cases remain UNRESOLVED. Native UI, human playtest and performance NOT_RUN.')
    if o.output.exists():raise ValueError('fresh summary output required')
    o.output.write_bytes(json.dumps(result,indent=2).encode('utf-8'));print(result['consistencyStatus'],len(checks),'consistency checks');return 1 if result['consistencyStatus']=='FAIL' else 0
if __name__=='__main__':raise SystemExit(main())
