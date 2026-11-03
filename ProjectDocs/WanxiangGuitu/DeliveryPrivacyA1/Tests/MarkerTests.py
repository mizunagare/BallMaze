from pathlib import Path
import json,shutil,importlib.util,sys
r=Path(sys.argv[1]);src=r/'ReleaseBuild2/Release/WanxiangGuitu.exe';spec=importlib.util.spec_from_file_location('verify',Path(__file__).parents[1]/'VerifyRelease.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);test=r/'MarkerTests';test.mkdir(exist_ok=False);exe=test/src.name
receipt=json.loads(Path(str(src)+'.release.json').read_text(encoding='utf-8-sig'));bee=json.loads(Path(str(src)+'.bee.json').read_text(encoding='utf-8-sig'));bee['PlayerBuildProgramLibrary.Data.PlayerBuildConfig']['DestinationPath']=str(exe);Path(str(exe)+'.bee.json').write_text(json.dumps(bee),encoding='utf8');rows=[]
for name in ['positive','marker-profile-mismatch','stale-executable','missing-marker']:
 Path(str(exe)+'.release.json').write_text(json.dumps(receipt),encoding='utf8');shutil.copy2(src,exe)
 if name=='marker-profile-mismatch':
  x=dict(receipt);x['profile']='Assets/Wrong.asset';Path(str(exe)+'.release.json').write_text(json.dumps(x),encoding='utf8')
 if name=='stale-executable':exe.write_bytes(b'old build')
 if name=='missing-marker':Path(str(exe)+'.release.json').unlink()
 try:m.verify(exe,r/'Project');accepted=True;reason='accepted'
 except Exception as e:accepted=False;reason=str(e)
 rows.append({'case':name,'status':'PASS' if accepted==(name=='positive') else 'FAIL','accepted':accepted,'classification':'PASS' if accepted else 'FAIL','exitCode':0 if accepted else 1,'reason':reason})
(r/'marker-tests.json').write_text(json.dumps(rows,indent=2),encoding='utf8');print(rows);sys.exit(any(x['status']!='PASS' for x in rows))

