"""One evidence-owned isolated run; immutable run directories, no real saves."""
import pathlib, hashlib, json, subprocess, sys, datetime, shutil, os

ROOT=pathlib.Path(__file__).resolve().parent
PROJECT=ROOT.parents[2]
EXE=pathlib.Path(os.environ['UX06_EXE']).resolve()
DLL=EXE.parent/'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'
DRIVER=PROJECT/'Assets/CombatPrototype/Acceptance/RegionRecordsPlayerProbe.cs'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fingerprints(root):
    return [{'path':p.relative_to(root).as_posix(),'size':p.stat().st_size,'sha256':sha(p)}
            for p in sorted(root.rglob('*')) if p.is_file() and p.suffix!='.lock']

region,runid,storage=sys.argv[1:4]
if region=='CrystalCavern' and (ROOT/'CAVERN_PREFLIGHT_HOLD.json').exists() and not (ROOT/'CAVERN_PREFLIGHT_RESOLVED.json').exists():
    print('PRELAUNCH_HOLD: cavern waypoint source correction required; no Player Run created',flush=True)
    sys.exit(3)
evidence=ROOT/'EVIDENCE'/runid
evidence.mkdir(parents=True,exist_ok=False)
storage=(ROOT/'EVIDENCE'/'STORAGE'/storage).resolve()
storage.mkdir(parents=True,exist_ok=True)
before=fingerprints(storage)
(evidence/'before.json').write_text(json.dumps(before,indent=2))
command=[str(EXE),'-wanxiang-storage-root',str(storage),'-wanxiang-entry-evidence',
         '-screen-fullscreen','0','-screen-width','1280','-screen-height','720',
         '-logFile',str(evidence/'player.log'),'-ux06-region',region,runid]
manifest={'runId':runid,'region':region,'command':command,'isolatedStorageRoot':str(storage),
          'buildId':'UX06-'+sha(DLL)[:16],'exeSha256':sha(EXE),'dllSha256':sha(DLL),
          'driverSourceSha256':sha(DRIVER),'driverBinarySha256':sha(DLL),
          'launcherSha256':sha(pathlib.Path(__file__)),'startedUtc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(evidence/'launcher-source.py.txt').write_bytes(pathlib.Path(__file__).read_bytes())
(evidence/'driver-source.cs.txt').write_bytes(DRIVER.read_bytes())
process=subprocess.Popen(command,cwd=PROJECT)
manifest['pid']=process.pid
(evidence/'run-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'pid':process.pid,'runId':runid,'storage':str(storage)}),flush=True)
timedout=False
try:code=process.wait(timeout=1900 if region=='ui' else 420)
except subprocess.TimeoutExpired:
    timedout=True;process.kill();code=process.wait()
source=storage/'ux06-results'/runid
if source.exists():shutil.copytree(source,evidence/'probe')
result={'runId':runid,'pid':process.pid,'exitCode':code,'timedOut':timedout,
        'verdict':'NOT_COMPLETED' if timedout or not (source/'result.json').exists() else json.loads((source/'result.json').read_text(encoding='utf-8'))['verdict']}
result['probeVerdict']=result['verdict']
if code!=0 and result['verdict']=='PASS':result['verdict']='PROCESS_FAILED'
(evidence/'result.json').write_text(json.dumps(result,indent=2))
(evidence/'after.json').write_text(json.dumps(fingerprints(storage),indent=2))
print(json.dumps(result),flush=True)
sys.exit(0 if result['verdict']=='PASS' else 1)
