"""Synthetic process-evidence negative matrix. No Unity process is simulated as real."""
import argparse,copy,hashlib,importlib.util,inspect,json,subprocess,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ProcessFixtures import write_process, refresh_origin, association_paths, cli_association
HERE=Path(__file__).resolve().parents[1]
TOOLS=HERE.parent/'DeliveryCombatPresentation03'
CONTRACTS=HERE.parent/'DeliveryCombatPresentation03R11/Contracts'

def main():
    a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);o=a.parse_args();o.output.mkdir(exist_ok=False)
    spec=importlib.util.spec_from_file_location('r12_receipt',TOOLS/'Receipt.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    contract=CONTRACTS/'Editor.json';template=json.loads(contract.read_text(encoding='utf-8-sig'));passing=copy.deepcopy(template)
    for row in passing['rows']:row['status']='PASS'
    cases=[]
    def add(name,modify=None,claims=None,files=True,expected='INCOMPLETE',code=3,reason=None,data=None):
        cases.append(dict(name=name,modify=modify,claims=claims or {},files=files,expected=expected,code=code,reason=reason,data=data))
    add('no-exit-code-no-receipts',claims=dict(process_status='PASS'),files=False,reason='PROCESS_RECEIPT_REQUIRED')
    add('no-status-no-receipts',claims=dict(exit_code=0),files=False,reason='PROCESS_RECEIPT_REQUIRED')
    add('no-both-no-receipts',files=False,reason='PROCESS_RECEIPT_REQUIRED')
    add('manual-complete-is-not-proof',claims=dict(process_status='PASS',exit_code=0,timed_out=False),files=False,reason='PROCESS_RECEIPT_REQUIRED')
    add('status-field-missing',lambda r,n:r.pop('status'),reason='INVALID_OR_MISSING_PROCESS_STATUS')
    add('exit-field-missing',lambda r,n:r.pop('exitCode'),reason='INVALID_OR_MISSING_EXIT_CODE')
    add('status-exit-fields-missing',lambda r,n:(r.pop('status'),r.pop('exitCode')),reason='INVALID_OR_MISSING_PROCESS_STATUS')
    add('timedout-field-missing',lambda r,n:r.pop('timedOut'),reason='INVALID_OR_MISSING_TIMED_OUT')
    add('manual-zero-cannot-fill-exit-field',lambda r,n:r.pop('exitCode'),claims=dict(process_status='PASS',exit_code=0,timed_out=False),reason='INVALID_OR_MISSING_EXIT_CODE')
    add('manual-pass-cannot-fill-status-field',lambda r,n:r.pop('status'),claims=dict(process_status='PASS',exit_code=0,timed_out=False),reason='INVALID_OR_MISSING_PROCESS_STATUS')
    add('manual-false-cannot-fill-timeout-field',lambda r,n:r.pop('timedOut'),claims=dict(process_status='PASS',exit_code=0,timed_out=False),reason='INVALID_OR_MISSING_TIMED_OUT')
    add('illegal-status',lambda r,n:r.update(status='UNKNOWN'),reason='INVALID_OR_MISSING_PROCESS_STATUS')
    add('status-whitespace',lambda r,n:r.update(status=' PASS'),reason='INVALID_OR_MISSING_PROCESS_STATUS')
    add('pass-nonzero-contradiction',lambda r,n:(r.update(exitCode=7),n.update(exitCode=7)),reason='PROCESS_STATUS_EXIT_CONTRADICTION')
    add('fail-zero-contradiction',lambda r,n:r.update(status='FAIL'),reason='PROCESS_STATUS_EXIT_CONTRADICTION')
    add('timeout-zero',lambda r,n:r.update(timedOut=True),reason='PROCESS_TIMED_OUT_NOT_ACCEPTABLE')
    add('timeout-null-exit',lambda r,n:(r.update(status='FAIL',exitCode=None,timedOut=True),n.update(exitCode=None)),reason='INVALID_OR_MISSING_EXIT_CODE')
    for name,value in [('string','0'),('bool',False),('float',0.0),('out-of-range',2**40),('null',None)]:
        add('exit-'+name,lambda r,n,value=value:r.update(exitCode=value),reason='INVALID_OR_MISSING_EXIT_CODE')
    for name,value in [('string','false'),('null',None),('number',0)]:
        add('timedout-'+name,lambda r,n,value=value:r.update(timedOut=value),reason='INVALID_OR_MISSING_TIMED_OUT')
    add('native-exit-mismatch',lambda r,n:n.update(exitCode=7),reason='NATIVE_RUNNER_EXIT_MISMATCH')
    add('native-exit-missing',lambda r,n:n.pop('exitCode'),reason='INVALID_NATIVE_EXIT_CODE')
    add('native-exit-bool',lambda r,n:n.update(exitCode=False),reason='INVALID_NATIVE_EXIT_CODE')
    add('native-forced',lambda r,n:n.update(forcedTermination=True),reason='NATIVE_FORCED_OR_UNCONFIRMED_TERMINATION')
    add('native-forced-unknown',lambda r,n:n.pop('forcedTermination'),reason='NATIVE_FORCED_OR_UNCONFIRMED_TERMINATION')
    add('native-pid-zero',lambda r,n:n.update(hostPid=0),reason='INVALID_NATIVE_HOST_PID')
    add('native-pid-bool',lambda r,n:n.update(hostPid=True),reason='INVALID_NATIVE_HOST_PID')
    add('native-no-timezone',lambda r,n:n.update(exitObservedUtc='2026-10-31T00:00:01'),reason='PROCESS_TIMESTAMP_TIMEZONE_REQUIRED')
    add('native-time-outside-stage',lambda r,n:n.update(exitObservedUtc='2026-10-31T00:10:00Z'),reason='NATIVE_EXIT_OUTSIDE_STAGE_INTERVAL')
    add('stage-reverse-time',lambda r,n:r.update(startUtc='2026-10-31T00:00:03Z'),reason='PROCESS_TIME_ORDER_INVALID')
    add('wrong-stage',lambda r,n:r.update(name='OtherStage'),reason='PROCESS_STAGE_MISSING_OR_DUPLICATE')
    add('wrong-scope',lambda r,n:r.update(scope='native-human'),reason='PROCESS_SCOPE_MISMATCH')
    add('wrong-executable',lambda r,n:r.update(command=['C:/bad.exe']),reason='PROCESS_EXECUTABLE_MISMATCH')
    add('wrong-log-prefix',lambda r,n:r.update(log=str(o.output/'another-run')),reason='PROCESS_LOG_PREFIX_MISMATCH')
    add('invalid-claimed-status',claims=dict(process_status='UNKNOWN'),reason='INVALID_PROCESS_STATUS_CLAIM')
    add('claimed-status-mismatch',claims=dict(process_status='FAIL'),reason='PROCESS_STATUS_CLAIM_MISMATCH')
    add('claimed-exit-mismatch',claims=dict(exit_code=7),reason='EXIT_CODE_CLAIM_MISMATCH')
    add('claimed-exit-bool',claims=dict(exit_code=False),reason='INVALID_EXIT_CODE_CLAIM')
    add('claimed-timeout-mismatch',claims=dict(timed_out=True),reason='TIMED_OUT_CLAIM_MISMATCH')
    add('claimed-timeout-string',claims=dict(timed_out='false'),reason='INVALID_TIMED_OUT_CLAIM')
    add('valid-proof-no-scalar-claims',expected='PASS',code=0)
    add('valid-proof-matching-claims',claims=dict(process_status='PASS',exit_code=0,timed_out=False),expected='PASS',code=0)
    add('valid-proof-open-assertions',data=template,expected='BLOCKED',code=2)
    add('valid-failed-process',lambda r,n:(r.update(status='FAIL',exitCode=7),n.update(exitCode=7)),expected='FAIL',code=1)
    add('native-file-absent')
    add('runner-file-absent')
    add('duplicate-stage',reason='PROCESS_STAGE_MISSING_OR_DUPLICATE')
    add('bad-runner-json')
    add('empty-runner-rows',reason='INVALID_RUNNER_RECEIPT')
    add('unknown-runner-filename',reason='UNRECOGNIZED_RUNNER_RECEIPT_NAME')
    add('wrong-exit-pair',reason='PROCESS_EXIT_PAIR_MISMATCH')
    add('other-run-proofs',reason='PROCESS_RECEIPT_RUN_ROOT_MISMATCH')
    bad=copy.deepcopy(passing);bad['rows'][0]['status']='FAIL'
    add('missing-proof-keeps-raw-fail',files=False,data=bad,reason='PROCESS_RECEIPT_REQUIRED')
    results=[]
    for c in cases:
        root=o.output/c['name'];root.mkdir();src=root/'presentation.json';src.write_bytes(json.dumps(c['data'] if c['data'] is not None else passing).encode('utf-8'))
        pr,ex=write_process(root,'Editor','PASS',0,False);row=json.loads(pr.read_text());native=json.loads(ex.read_text())
        if c['modify']:c['modify'](row,native)
        pr.write_bytes(json.dumps(row).encode());ex.write_bytes(json.dumps(native).encode())
        if c['name']=='duplicate-stage':pr.write_bytes(json.dumps([row,row]).encode())
        if c['name']=='bad-runner-json':pr.write_bytes(b'{')
        if c['name']=='empty-runner-rows':pr.write_bytes(b'[]')
        if c['name']=='native-file-absent':ex=root/'absent.exit.json'
        if c['name']=='runner-file-absent':pr=root/'missing'/'process-results.json'
        if c['name']=='unknown-runner-filename':other=root/'arbitrary.json';other.write_bytes(pr.read_bytes());pr=other
        if c['name']=='wrong-exit-pair':other=root/'Wrong.exit.json';other.write_bytes(ex.read_bytes());ex=other
        if c['name']=='other-run-proofs':pr,ex=write_process(root/'OtherRoot','Editor','PASS',0,False)
        refresh_origin(root) # only synthetic fixtures; keep prior test meaning isolated
        original_hash={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (src,pr,ex) if p.is_file()}
        kwargs=dict(contract=contract,profile='Editor',**c['claims'])
        if c['files']:kwargs.update(process_receipt=pr,exit_receipt=ex,**association_paths(pr.parent,'Editor'))
        q=m.evaluate(src,**kwargs);m.write(q,root/'ApiReport')
        # Matching CLI execution validates its actual exit and generated reports too.
        args=[sys.executable,str(TOOLS/'Receipt.py'),'--receipt',str(src),'--profile','Editor','--contract',str(contract),'--output',str(root/'CliReport')]
        if c['files']:args+=['--process-receipt',str(pr),'--exit-receipt',str(ex)]+cli_association(pr.parent,'Editor')
        claims=c['claims']
        if 'process_status' in claims:args+=['--process-status',str(claims['process_status'])]
        if 'exit_code' in claims:args+=['--exit-code',str(claims['exit_code'])]
        if 'timed_out' in claims and type(claims['timed_out']) is bool:args+=['--timed-out' if claims['timed_out'] else '--not-timed-out']
        p=subprocess.run(args,capture_output=True,text=True);(root/'stdout.txt').write_bytes(p.stdout.encode());(root/'stderr.txt').write_bytes(p.stderr.encode())
        actual=json.loads((root/'CliReport/acceptance.json').read_text(encoding='utf-8'))
        ok=q['overallStatus']==c['expected'] and q['exitCode']==c['code']
        # API string timed_out cannot be expressed by Boolean CLI flags.
        # Its CLI invocation is an explicit valid-no-claim control, NOT that negative.
        cli_control=c['name']=='claimed-timeout-string'
        cli_expected='PASS' if cli_control else c['expected'];cli_code=0 if cli_control else c['code']
        ok=ok and p.returncode==actual['exitCode']==cli_code and actual['overallStatus']==cli_expected
        if c['reason']:ok=ok and any(c['reason'] in e for e in q['errors'])
        ok=ok and all(hashlib.sha256(Path(name).read_bytes()).hexdigest()==h for name,h in original_hash.items())
        if c['expected']=='PASS':ok=ok and q['process']['evidenceStatus']=='PASS' and q['process']['reportedStatus']=='PASS' and q['process']['exitCode']==0
        if c['expected']=='INCOMPLETE':ok=ok and q['process']['status']=='INCOMPLETE'
        if c['name']=='missing-proof-keeps-raw-fail':ok=ok and q['counts'].get('FAIL')==1 and q['rawAssertionStatus']=='FAIL'
        if c['expected']=='BLOCKED':ok=ok and q['counts']==dict(PASS=291,UNRESOLVED=2)
        for folder in ('ApiReport','CliReport'):ok=ok and (root/folder/'assertions.csv').is_file() and '**'+json.loads((root/folder/'acceptance.json').read_text(encoding='utf-8'))['overallStatus']+'**' in (root/folder/'REPORT.md').read_text(encoding='utf-8')
        results.append(dict(name=c['name'],status='PASS' if ok else 'FAIL',apiOverall=q['overallStatus'],apiExit=q['exitCode'],cliOverall=actual['overallStatus'],cliExit=p.returncode,expected=c['expected'],expectedExit=c['code'],cliExpected=cli_expected,cliExpectedExit=cli_code,cliPurpose='valid no-claim control; API string type is a separate negative' if cli_control else 'same semantic case',errors=q['errors'],scope='synthetic schema fixtures, not native execution',command=args))
    defaults=inspect.signature(m.evaluate).parameters
    results.append(dict(name='all-process-defaults-unknown',status='PASS' if all(defaults[x].default is None for x in ('process_status','exit_code','timed_out','process_receipt','exit_receipt')) else 'FAIL'))
    root=o.output/'single-read';root.mkdir();src=root/'presentation.json';src.write_bytes(json.dumps(passing).encode());pr,ex=write_process(root,'Editor','PASS',0,False);reads={};raw_read=Path.read_bytes
    def read_once(path):reads[str(path)]=reads.get(str(path),0)+1;return raw_read(path)
    with patch.object(Path,'read_bytes',read_once):q=m.evaluate(src,contract=contract,profile='Editor',process_receipt=pr,exit_receipt=ex,**association_paths(pr.parent,'Editor'))
    results.append(dict(name='same-read-binds-all-source-digests',status='PASS' if q['overallStatus']=='PASS' and all(reads.get(str(p))==1 for p in (src,contract,pr,ex)) else 'FAIL',reads=reads))
    final=dict(scope='tool schema tests only; actual runner proof tests are separately archived',counts={s:sum(x['status']==s for x in results) for s in ('PASS','FAIL')},rows=results)
    (o.output/'selftest.json').write_bytes(json.dumps(final,indent=2).encode());print(json.dumps(final['counts']));return 1 if final['counts']['FAIL'] else 0
if __name__=='__main__':raise SystemExit(main())
