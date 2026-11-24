"""Run Unity synchronously; retain the actual OS result and immutable build records."""
import pathlib,subprocess,os,json,datetime,hashlib,sys
DEV=pathlib.Path('I:/unity/WanxiangGuitu-UX06')
DELIVERY=DEV/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression06'
PROJECT=pathlib.Path('I:/UX06_BUILD_20261124/Project')
record=sys.argv[1]
acceptance=sys.argv[2]=='acceptance'
evidence=DELIVERY/record
evidence.mkdir(exist_ok=True)
assert not (evidence/'LAUNCH.json').exists(),'Do not reuse build record'
output=pathlib.Path('I:/UX06_BUILD_20261124/OUTPUT')/record/'WanxiangGuitu.exe'
env=os.environ.copy()
env.update(UX06_OUTPUT=str(output),UX06_ACCEPTANCE='1' if acceptance else '0',UX06_SCRATCH='1',
           UX06_BUILD_EVIDENCE=str(evidence/'SETTINGS'),
           UPM_CACHE_ROOT=str(PROJECT/'Library/IsolatedUpmCache'))
command=['C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe','-batchmode','-nographics',
         '-projectPath',str(PROJECT),'-executeMethod','RegionRecordsBuild.Run','-logFile',str(evidence/'unity.log')]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
data={'record':record,'command':command,'project':str(PROJECT),'output':str(output),'acceptance':acceptance,'startUtc':now()}
with (evidence/'bootstrap.log').open('wb') as log:
    proc=subprocess.Popen(command,cwd=PROJECT,env=env,stdout=log,stderr=subprocess.STDOUT)
    data['pid']=proc.pid
    (evidence/'LAUNCH.json').write_text(json.dumps(data,indent=2))
    print(json.dumps(data),flush=True)
    data['exitCode']=proc.wait()
data['endUtc']=now()
data['artifacts']=[]
for p in [output,output.parent/'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll']:
    if p.exists():data['artifacts'].append({'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)})
fixture=PROJECT/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression06/FIXTURE_RESULT.json'
if fixture.exists():(evidence/'FIXTURE_RESULT.json').write_bytes(fixture.read_bytes())
(evidence/'RESULT.json').write_text(json.dumps(data,indent=2))
print(json.dumps(data),flush=True)
sys.exit(0 if data['exitCode']==0 else 1)
