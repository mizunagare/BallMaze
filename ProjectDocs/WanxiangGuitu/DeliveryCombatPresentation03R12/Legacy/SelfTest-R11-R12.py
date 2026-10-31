"""Contract binding negative matrix; synthetic receipts, no Unity state changes."""
import argparse,copy,hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parents[2]/'DeliveryCombatPresentation03R11'
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ProcessFixtures import write_process
TOOLS=HERE.parent/'DeliveryCombatPresentation03'

def main():
    a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);o=a.parse_args();o.output.mkdir(exist_ok=False)
    frozen={m:(HERE/'Contracts'/(m+'.json')).read_bytes() for m in ('Editor','Runtime')}
    original={m:json.loads(b) for m,b in frozen.items()}
    def passing(m):
        q=copy.deepcopy(original[m])
        for r in q['rows']:r['status']='PASS'
        return q
    cases=[]
    def add(name,mode='Editor',profile='Editor',contract_mode='Editor',receipt=None,contract_raw=None,expect='INCOMPLETE',code=3,reason=None,omit_contract=False,omit_profile=False,missing_contract=False,missing_receipt=False):
        cases.append(dict(name=name,mode=mode,profile=profile,contract_mode=contract_mode,receipt=receipt,contract_raw=contract_raw,expect=expect,code=code,reason=reason,omit_contract=omit_contract,omit_profile=omit_profile,missing_contract=missing_contract,missing_receipt=missing_receipt))
    add('editor-valid',expect='PASS',code=0)
    add('runtime-valid',mode='Runtime',profile='Runtime',contract_mode='Runtime',expect='PASS',code=0)
    add('contract-omitted',omit_contract=True,reason='CONTRACT_REQUIRED')
    add('profile-omitted',omit_profile=True,reason='PROFILE_REQUIRED')
    add('profile-unknown',profile='native-human',reason='UNKNOWN_PROFILE')
    add('contract-missing-file',missing_contract=True)
    add('receipt-missing-file',missing_receipt=True)
    add('runtime-contract-used-for-editor',contract_mode='Runtime',reason='CONTRACT_SHA_MISMATCH')
    add('editor-contract-used-for-runtime',mode='Runtime',profile='Runtime',reason='CONTRACT_SHA_MISMATCH')
    add('editor-receipt-runtime-context',profile='Runtime',contract_mode='Runtime',reason='RECEIPT_LAYER_MISMATCH')
    add('runtime-receipt-editor-context',mode='Runtime',reason='RECEIPT_LAYER_MISMATCH')
    for mode in ('Editor','Runtime'):
        for field in ('layer','scope'):
            q=passing(mode);q[field]=original['Runtime' if mode=='Editor' else 'Editor']['layer'] if field=='layer' else 'forged native human scope'
            add(mode.lower()+'-receipt-'+field,mode=mode,profile=mode,contract_mode=mode,receipt=q,reason='RECEIPT_'+field.upper()+'_MISMATCH')
        add(mode.lower()+'-contract-whitespace',mode=mode,profile=mode,contract_mode=mode,contract_raw=frozen[mode]+b'\n',reason='CONTRACT_SHA_MISMATCH')
    for mode,field in (('Editor','layer'),('Runtime','scope')):
        q=copy.deepcopy(original[mode]);q[field]='forged frozen '+field
        add(mode.lower()+'-contract-'+field,mode=mode,profile=mode,contract_mode=mode,contract_raw=json.dumps(q).encode(),reason='CONTRACT_SHA_MISMATCH')
    q=copy.deepcopy(original['Editor']);q['rows'][0]['name']='forged assertion';rec=passing('Editor');rec['rows'][0]['name']='forged assertion'
    add('self-consistent-receipt-contract-name-tamper',receipt=rec,contract_raw=json.dumps(q).encode(),reason='CONTRACT_SHA_MISMATCH')
    q=copy.deepcopy(original['Runtime']);q['rows'].pop();rec=passing('Runtime');rec['rows'].pop()
    add('self-consistent-runtime-row-removal',mode='Runtime',profile='Runtime',contract_mode='Runtime',receipt=rec,contract_raw=json.dumps(q).encode(),reason='CONTRACT_SHA_MISMATCH')
    add('contract-empty',contract_raw=b'',reason='CONTRACT_SHA_MISMATCH')
    add('contract-bom-added',contract_raw=b'\xef\xbb\xbf'+frozen['Editor'],reason='CONTRACT_SHA_MISMATCH')
    add('contract-line-ending-tamper',contract_raw=frozen['Editor'].replace(b'\n',b'\r\n'),reason='CONTRACT_SHA_MISMATCH')
    add('byte-identical-contract-relocated',contract_raw=frozen['Editor'],expect='PASS',code=0)
    for mode in ('Editor','Runtime'):
        add(mode.lower()+'-real-open-receipt',mode=mode,profile=mode,contract_mode=mode,receipt=original[mode],expect='BLOCKED',code=2)
    q=passing('Editor');q['rows'][0]['status']='FAIL';q['rows'][1]['status']='UNRESOLVED'
    add('known-fail-stays-fail',receipt=q,expect='FAIL',code=1)
    q=passing('Editor');q['scope']='wrong scope';q['rows'][0]['status']='FAIL'
    add('known-fail-plus-bad-binding',receipt=q,expect='FAIL',code=1,reason='RECEIPT_SCOPE_MISMATCH')
    results=[]
    for c in cases:
        path=o.output/c['name'];path.mkdir();src=path/'presentation.json';contract=path/'frozen-contract.json'
        if not c['missing_receipt']:src.write_bytes(json.dumps(c['receipt'] if c['receipt'] is not None else passing(c['mode'])).encode('utf-8'))
        if not c['missing_contract']:contract.write_bytes(c['contract_raw'] if c['contract_raw'] is not None else frozen[c['contract_mode']])
        pr,ex=write_process(path,c['profile'] if c['profile'] in ('Editor','Runtime') else c['mode'],'PASS',0,False)
        command=[sys.executable,str(TOOLS/'Receipt.py'),'--receipt',str(src),'--output',str(path/'Report'),'--exit-code','0','--process-receipt',str(pr),'--exit-receipt',str(ex)]
        if not c['omit_contract']:command+=['--contract',str(contract)]
        if not c['omit_profile']:command+=['--profile',c['profile']]
        p=subprocess.run(command,capture_output=True,text=True)
        (path/'stdout.txt').write_bytes(p.stdout.encode('utf-8'));(path/'stderr.txt').write_bytes(p.stderr.encode('utf-8'))
        (path/'command.json').write_bytes(json.dumps(dict(scope='synthetic classifier fixture, not an actual Editor/Player run',command=command,exitCode=p.returncode,expectedExit=c['code'])).encode('utf-8'))
        report=json.loads((path/'Report/acceptance.json').read_text(encoding='utf-8'));md=(path/'Report/REPORT.md').read_text(encoding='utf-8')
        ok=p.returncode==c['code']==report['exitCode'] and report['overallStatus']==c['expect'] and '**'+c['expect']+'**' in md and (path/'Report/assertions.csv').is_file()
        if c['reason']:ok=ok and any(c['reason'] in e for e in report['errors'])
        if c['expect']=='PASS':ok=ok and report['binding']['status']=='PASS' and report['counts']==dict(PASS=293)
        if c['expect']=='INCOMPLETE':ok=ok and report['binding']['status']!='PASS' and report['assertionStatus']=='INVALID'
        results.append(dict(name=c['name'],status='PASS' if ok else 'FAIL',actualExit=p.returncode,actualOverall=report['overallStatus'],expectedOverall=c['expect'],errors=report['errors']))
    spec=importlib.util.spec_from_file_location('r11_receipt',TOOLS/'Receipt.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    src=o.output/'editor-valid/presentation.json';contract=HERE/'Contracts/Editor.json'
    for name,kwargs in [('api-no-contract',dict(profile='Editor')),('api-no-profile',dict(contract=contract)),('api-unbound-default',dict())]:
        q=module.evaluate(src,process_receipt=o.output/'editor-valid/process-results.json',exit_receipt=o.output/'editor-valid/CP03Editor.Run.exit.json',**kwargs);results.append(dict(name=name,status='PASS' if q['overallStatus']=='INCOMPLETE' and q['binding']['status']!='PASS' else 'FAIL'))
    # One immutable read per path; the reported digest must bind the bytes actually parsed.
    reads={};original_read=Path.read_bytes
    def read_once(path):
        k=str(path);reads[k]=reads.get(k,0)+1;return original_read(path)
    with patch.object(Path,'read_bytes',read_once):q=module.evaluate(src,contract=contract,profile='Editor',process_receipt=o.output/'editor-valid/process-results.json',exit_receipt=o.output/'editor-valid/CP03Editor.Run.exit.json')
    results.append(dict(name='single-read-digest-binds-parsed-bytes',status='PASS' if q['overallStatus']=='PASS' and reads.get(str(src))==reads.get(str(contract))==1 and q['contractSHA256']==hashlib.sha256(frozen['Editor']).hexdigest() else 'FAIL',reads=reads))
    final=dict(scope='synthetic receipt and API selftests only',counts={s:sum(x['status']==s for x in results) for s in ('PASS','FAIL')},rows=results)
    (o.output/'selftest.json').write_bytes(json.dumps(final,indent=2).encode('utf-8'));print(json.dumps(final['counts']));return 1 if final['counts']['FAIL'] else 0
if __name__=='__main__':raise SystemExit(main())
