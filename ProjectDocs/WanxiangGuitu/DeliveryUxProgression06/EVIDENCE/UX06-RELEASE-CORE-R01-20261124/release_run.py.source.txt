"""External process observer only. No process injection, state construction or input automation."""
import pathlib,json,hashlib,subprocess,datetime,sys,time,shutil
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
run=sys.argv[1];e=D/'EVIDENCE'/run;e.mkdir(exist_ok=False)
root=D/'EVIDENCE/STORAGE/RELEASE_FINAL_COPY01'
build=json.loads((D/'BUILD12_RELEASE/RESULT.json').read_text());exe=pathlib.Path(build['output'])
for a in build['artifacts']:assert sha(pathlib.Path(a['path']))==a['sha256']
def fingerprint():return [{'path':p.relative_to(root).as_posix(),'size':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file()]
(e/'before.json').write_text(json.dumps(fingerprint(),indent=2))
for name in ['release_run.py','native_release_input.js','window_metadata.py']:shutil.copyfile(D/name,e/(name+'.source.txt'))
args=[str(exe),'-wanxiang-storage-root',str(root),'-screen-fullscreen','0','-screen-width','1280','-screen-height','720','-logFile',str(e/'player.log')]
m={'runId':run,'region':'ReleaseNativeUI','buildId':'UX06-'+build['artifacts'][1]['sha256'][:16],
   'exeSha256':build['artifacts'][0]['sha256'],'dllSha256':build['artifacts'][1]['sha256'],
   'driverSourceSha256':sha(D/'native_release_input.js'),'driverBinarySha256':'NOT_APPLICABLE_EXTERNAL_NATIVE_INPUT_ONLY',
   'inputTool':'@oai/sky via computer-use 26.1117.41037','launcherSha256':sha(pathlib.Path(__file__)),
   'command':args,'isolatedStorageRoot':str(root),'acceptanceHarness':'ABSENT','internalState':'NOT_OBSERVED',
   'startedUtc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
p=subprocess.Popen(args,cwd=R);m['pid']=p.pid
(e/'run-manifest.json').write_text(json.dumps(m,indent=2));print(json.dumps({'runId':run,'pid':p.pid}),flush=True)
last=None
while p.poll() is None:
    time.sleep(1)
    main=root/'WanxiangGuitu/ForestRuins-v10/save.json'
    if main.exists():
        try:
            content=main.read_bytes();h=hashlib.sha256(content).hexdigest()
            if h!=last:
                snapshot=e/'save-observations';snapshot.mkdir(exist_ok=True)
                (snapshot/(h+'.json')).write_bytes(content)
                with (e/'save-changes.jsonl').open('a') as f:f.write(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':h,'bytes':len(content)})+'\n')
                last=h
        except OSError:pass
code=p.wait();(e/'after.json').write_text(json.dumps(fingerprint(),indent=2))
(e/'process-result.json').write_text(json.dumps({'runId':run,'pid':p.pid,'exitCode':code,'endedUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'note':'Exit observed directly; UI verdict requires separate visible evidence review.'},indent=2))
print(json.dumps({'runId':run,'pid':p.pid,'exitCode':code}),flush=True)
