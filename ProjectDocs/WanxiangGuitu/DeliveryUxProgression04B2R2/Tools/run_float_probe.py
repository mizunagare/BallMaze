"""One real Unity Standalone Mono float probe. No product formula in Python."""
import pathlib,json,argparse,subprocess,os,hashlib,datetime,shutil
R=pathlib.Path.cwd()
def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def dump(p,obj):
    if p.exists():raise RuntimeError('Refuse overwriting '+str(p))
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--session',required=True);ap.add_argument('--run-id',required=True);a=ap.parse_args();session=(R/a.session).absolute();receipt=json.loads((session/'_build/build-receipt.json').read_text(encoding='utf-8'));player=pathlib.Path(receipt['copy']);exe=player/'WanxiangGuitu.exe';managed=player/'WanxiangGuitu_Data/Managed'
    ev=session/a.run_id;root=session/'_roots'/a.run_id
    if ev.exists() or root.exists():raise SystemExit('Every run and evidence destination must be NEW')
    ev.mkdir(parents=True);root.mkdir(parents=True)
    config={'runId':a.run_id,'buildId':receipt['buildId'],'dllSHA256':sha(managed/'Assembly-CSharp.dll'),'exeSHA256':sha(exe),'driverSHA256':sha(managed/'B2R2FloatProbe.dll')}
    dump(root/'r2-float-config.json',config);dump(ev/'Player.command.json',dict(config,mode='R03-FLOAT-STOP-GATE',scope='actual Mono math only; not replacement UI acceptance'))
    env=os.environ.copy();env['UNITY_TEST_ROOT']=str(root)
    args=[str(exe),'-logFile',str(root/'Player.log'),'-screen-width','1280','-screen-height','720','-screen-fullscreen','0','-force-d3d12','-wanxiang-storage-root',str(root)]
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();timed_out=False
    with (root/'Player.stdout').open('wb') as stdout,(root/'Player.stderr').open('wb') as stderr:
        proc=subprocess.Popen(args,cwd=player,env=env,stdout=stdout,stderr=stderr)
        try:code=proc.wait(timeout=90)
        except subprocess.TimeoutExpired:
            timed_out=True;proc.terminate()
            try:code=proc.wait(timeout=15)
            except subprocess.TimeoutExpired:proc.kill();code=proc.wait()
    for p in root.iterdir():
        if p.is_file():shutil.copyfile(p,ev/p.name)
    result=json.loads((ev/'result.json').read_text(encoding='utf-8')) if (ev/'result.json').is_file() else None
    runtime=ev/'runtime';runtime.mkdir()
    for p in [managed/'System.Core.dll',player/'MonoBleedingEdge/EmbedRuntime/mono-2.0-bdwgc.dll']:
        if p.is_file():shutil.copyfile(p,runtime/p.name)
    valid=(not timed_out and result is not None and result['runId']==a.run_id and result['pid']==proc.pid and result['buildId']==config['buildId'] and result['identityMatches'] and result['isMono'] and not result['isEditor'] and result['inputsMatch'] and result['fixturesUnchanged'] and result['randomStateUnchanged'] and result['tracesMatch'] and code==result['requestedExitCode'])
    if result is not None:
        # Integer bit-pattern consistency ONLY; Python does not calculate the float outputs.
        ulp=abs(int(result['oldActualBitsHex'],16)-int(result['newActualBitsHex'],16));valid=valid and result['ulpDifference']==ulp
    verdict='INVALID_PROBE' if not valid else result['verdict']
    manifest=dict(config,mode='R03-FLOAT-STOP-GATE',pid=proc.pid,exitCode=code,timedOut=timed_out,startUtc=start,endUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),arguments=args,runRoot=str(root),evidenceDir=str(ev),verdict=verdict,result=result,files={p.relative_to(ev).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(ev.rglob('*')) if p.is_file()})
    dump(ev/'run-manifest.json',manifest)
    print(json.dumps({'runId':a.run_id,'pid':proc.pid,'exitCode':code,'buildId':config['buildId'],'verdict':verdict,'oldBits':None if result is None else result['oldActualBitsHex'],'newBits':None if result is None else result['newActualBitsHex'],'ulp':None if result is None else result['ulpDifference'],'stopRequired':verdict=='BIT_DIFFERENCE_STOP'},indent=2))
    return 0 if valid and verdict in ('BIT_DIFFERENCE_STOP','BITWISE_EQUAL') else 1
if __name__=='__main__':raise SystemExit(main())
