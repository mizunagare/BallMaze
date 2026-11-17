"""Launch ONE explicitly requested FIX replacement UI run; never build a Player.
Use six distinct --run-id values, fresh roots, and the replacement sidecar receipt.
"""
import argparse, base64, datetime, hashlib, json, os, pathlib, re, shutil, subprocess

MODES = ('accessory', 'arms', 'main', 'board-insufficient', 'legal-swap', 'illegal-swap')
NINE = {'GearItem','Inventory','EquipmentGrid','Main','Reserve','Worn','Overflow','AttackPower','Container'}

def sha(p):
    with pathlib.Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def dump(path, data):
    with pathlib.Path(path).open('x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fnv_utf16(s):
    h = 14695981039346656037
    b = s.encode('utf-16-le', errors='surrogatepass')
    for i in range(0,len(b),2):
        h = ((h ^ (b[i] | b[i+1]<<8))*1099511628211) & ((1<<64)-1)
    return f'{h:016x}'

def lines(path):
    return [json.loads(s) for s in path.read_text(encoding='utf-8-sig').splitlines() if s.strip()]

def validate_states(ev):
    """Integer/hash/raw kernel validation, NOT a second product float implementation."""
    faults=[]
    transitions=lines(ev/'state-changes.jsonl')
    for t in transitions:
        for side in ('before','after'):
            s=t[side]
            if set(s['canonical']) != NINE or set(s['fingerprints']) != NINE:
                faults.append(t['tag']+': nine keys missing')
            for key, raw in s['canonical'].items():
                if fnv_utf16(raw) != s['fingerprints'][key]:
                    faults.append(t['tag']+': cannot recompute '+key)
                json.loads(raw) # all complete canonical domains are raw JSON, no opaque summary
            for save in s['saveFiles']:
                raw=base64.b64decode(save['base64'], validate=True)
                if len(raw)!=save['bytes'] or hashlib.sha256(raw).hexdigest()!=save['sha256']:
                    faults.append('save original bytes cannot be independently rehashed')
        a,b=t['before'],t['after']
        equal=(a['canonical']==b['canonical'] and a['random']==b['random'] and a['saveFiles']==b['saveFiles'])
        if t['tag']=='UI-Evaluate' or t['tag'].startswith('ADDITIONAL-API-'):
            if not equal:faults.append(t['tag']+': read-only mutation')
    ui=[t for t in transitions if t['tag'] in ('UI-Evaluate','UI-Commit')]
    if [t['tag'] for t in ui] != ['UI-Evaluate','UI-Commit']:
        faults.append('must have one actual UI Evaluate and one UI Commit')
    return faults, transitions

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--receipt',required=True)
    ap.add_argument('--session',required=True)
    ap.add_argument('--mode',required=True,choices=MODES)
    ap.add_argument('--run-id',required=True)
    ap.add_argument('--timeout',type=int,default=240)
    a=ap.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,119}',a.run_id):
        raise SystemExit('run-id must be a single safe unique basename')
    if a.timeout<=0:raise SystemExit('positive timeout required')
    receipt_path=pathlib.Path(a.receipt).absolute()
    receipt=json.loads(receipt_path.read_text(encoding='utf-8-sig'))
    if receipt['assembly']!='B2R2FixReplacementDriver' or receipt['namespace']!='B2R2FixReplacement':
        raise SystemExit('need the REPLACEMENT driver receipt, not FloatGate or historical PASS')
    player=pathlib.Path(receipt['copy']).absolute()
    exe=player/'WanxiangGuitu.exe';managed=player/'WanxiangGuitu_Data/Managed'
    dll=managed/'Assembly-CSharp.dll';driver=managed/(receipt['assembly']+'.dll')
    expected={'productDLLSHA256':sha(dll),'driverSHA256':sha(driver),'exeSHA256':sha(exe)}
    if receipt['compileExitCode']!=0 or any(receipt[k]!=v for k,v in expected.items()):
        raise SystemExit('Player inputs differ from immutable build receipt')
    compiled_source=pathlib.Path(receipt['executedSource'])
    if sha(compiled_source)!=receipt['executedSourceSHA256'] or receipt['executedSourceSHA256']!=receipt['sourceSHA256']:
        raise SystemExit('compiled observer source lineage mismatch')
    session=pathlib.Path(a.session).absolute();ev=session/a.run_id;root=session/'_roots'/a.run_id
    if ev.exists() or root.exists():raise SystemExit('Refuse overwrite: evidence and storage root must BOTH be new')
    ev.mkdir(parents=True);root.mkdir(parents=True)
    config=dict(runId=a.run_id,mode=a.mode,buildId=receipt['buildId'],dllSHA256=expected['productDLLSHA256'],driverSHA256=expected['driverSHA256'],exeSHA256=expected['exeSHA256'])
    dump(root/'replacement-config.json',config)
    env=os.environ.copy();env['UNITY_TEST_ROOT']=str(root)
    args=[str(exe),'-logFile',str(root/'Player.log'),'-screen-width','1280','-screen-height','800','-screen-fullscreen','0','-force-d3d12','-wanxiang-storage-root',str(root)]
    dump(ev/'Player.command.json',dict(config,arguments=args,storageRoot=str(root),receipt=str(receipt_path),scope='actual product UI replacement; setup and authority API observations separately labelled'))
    shutil.copyfile(receipt_path,ev/'build-receipt.json')
    shutil.copyfile(compiled_source,ev/'ReplacementDriver.compiled.cs')
    shutil.copyfile(driver,ev/driver.name)
    shutil.copyfile(dll,ev/'Assembly-CSharp.input.dll')
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();timed_out=False
    with (root/'Player.stdout').open('wb') as out,(root/'Player.stderr').open('wb') as err:
        proc=subprocess.Popen(args,cwd=player,env=env,stdout=out,stderr=err)
        dump(ev/'process-start.json',dict(pid=proc.pid,startUtc=start,**config))
        try:code=proc.wait(timeout=a.timeout)
        except subprocess.TimeoutExpired:
            timed_out=True;proc.terminate()
            try:code=proc.wait(timeout=15)
            except subprocess.TimeoutExpired:proc.kill();code=proc.wait()
    # Preserve every original event/state/screenshot/save byte, also on failed attempts.
    shutil.copytree(root,ev/'original-root')
    for name in ('input-events.jsonl','observations.jsonl','state-changes.jsonl','checks.jsonl','result.json','Player.log'):
        if (root/name).is_file():shutil.copyfile(root/name,ev/name)
    if (root/'screenshots').is_dir():shutil.copytree(root/'screenshots',ev/'screenshots')
    faults=[];result=None;transitions=[]
    try:
        result=json.loads((ev/'result.json').read_text(encoding='utf-8-sig'))
        if any(result.get(k)!=config[k] for k in ('runId','mode','buildId')):faults.append('result identity mismatch')
        if result.get('pid')!=proc.pid:faults.append('PID mismatch')
        if any(result.get(k)!=v for k,v in expected.items()):faults.append('runtime DLL/driver/exe hashes mismatch')
        if not result.get('isMono') or result.get('isEditor'):faults.append('not actual standalone Mono')
        if code!=result.get('requestedExitCode'):faults.append('actual exit differs from result requested exit')
        if result.get('result')!='PASS' or result.get('failed')!=0 or result.get('checks',0)<=0:faults.append('driver checks failed')
        f,transitions=validate_states(ev);faults+=f
        events=lines(ev/'input-events.jsonl')
        for action in ('Candidate:','Replaced:','Role:','Evaluate','Commit'):
            for kind in ('ugui-raycast','mouse-down','mouse-up'):
                if not any(e['kind']==kind and ('ReplacementPreview:'+action) in e['detail'] for e in events):
                    faults.append('missing real input '+kind+' '+action)
        if a.mode!='main':
            for action in ('XPlus','XMinus','YPlus','YMinus'):
                if not any(e['kind']=='mouse-up' and ('ReplacementPreview:'+action) in e['detail'] for e in events):faults.append('position not physically selected '+action)
        for name in ('01-selection.png','02-evaluated.png','03-committed.png'):
            if not (ev/'screenshots'/name).is_file():faults.append('missing screenshot '+name)
        if a.mode in ('illegal-swap','board-insufficient') and transitions:
            t=next(t for t in transitions if t['tag']=='UI-Commit')
            if t['before']['canonical']!=t['after']['canonical'] or t['before']['random']!=t['after']['random'] or t['before']['saveFiles']!=t['after']['saveFiles']:faults.append('rejected Commit changed actual kernel')
    except (OSError,ValueError,KeyError,TypeError,StopIteration) as ex:
        faults.append('incomplete evidence: '+repr(ex))
    if timed_out:faults.append('actual Player timeout')
    if code!=0:faults.append('actual Player exit '+str(code))
    # Recheck input files after the process; observer must not replace product bytes.
    if any(sha(p)!=expected[k] for k,p in [('productDLLSHA256',dll),('driverSHA256',driver),('exeSHA256',exe)]):faults.append('execution modified input binary')
    verdict='PASS' if not faults else 'FAIL'
    manifest=dict(config,**{'productDLLSHA256':expected['productDLLSHA256']},pid=proc.pid,exitCode=code,timedOut=timed_out,startUtc=start,endUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),verdict=verdict,faults=faults,result=result,arguments=args,runRoot=str(root),evidenceDir=str(ev),receiptSHA256=sha(receipt_path),files={p.relative_to(ev).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(ev.rglob('*')) if p.is_file()})
    dump(ev/'run-manifest.json',manifest)
    print(json.dumps({k:manifest[k] for k in ('runId','mode','pid','exitCode','buildId','verdict','faults')},ensure_ascii=False,indent=2))
    return 0 if verdict=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
