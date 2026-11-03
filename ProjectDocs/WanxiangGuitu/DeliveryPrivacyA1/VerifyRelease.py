"""Read-only publication receipt verifier. Never creates a release marker."""
import json,hashlib,sys
from pathlib import Path
PROFILE='Assets/BuildProfiles/WindowsRelease.asset'
FIELDS=('EnableUnityConnect','EnableCrashReporting','EnableInsights','EnableAnalytics','EnablePerformanceReporting')
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def verify(exe,project):
 exe=Path(exe);project=Path(project);r=json.loads(Path(str(exe)+'.release.json').read_text(encoding='utf-8-sig'))
 assert r['profile']==PROFILE,'marker/profile mismatch'
 assert r['profileSHA256']==digest(project/PROFILE),'profile SHA mismatch'
 assert r['unityConnectSHA256']==digest(project/'ProjectSettings/UnityConnectSettings.asset'),'connect SHA mismatch'
 assert r['executableSHA256']==digest(exe),'stale output'
 c=json.loads(Path(str(exe)+'.bee.json').read_text(encoding='utf-8-sig'))['PlayerBuildProgramLibrary.Data.PlayerBuildConfig']
 assert Path(c['DestinationPath']).resolve()==exe.resolve(),'Bee output mismatch'
 assert c['Development'] is False
 assert all(c['Services'][k] is False for k in FIELDS),'Bee services enabled'
 return {'status':'PASS','scope':'publication configuration, not no-network guarantee','exeSHA256':digest(exe)}
if __name__=='__main__':
 try:print(json.dumps(verify(sys.argv[1],sys.argv[2])))
 except Exception as e:print(json.dumps({'status':'FAIL','reason':str(e)}));sys.exit(1)
