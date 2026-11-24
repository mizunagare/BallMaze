"""Reconcile immutable run/build records into a current UX06 delivery summary."""
import pathlib,json,csv,hashlib,subprocess,collections
D=pathlib.Path(__file__).resolve().parent
R=D.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=list(csv.DictReader((D/'PLAYER_RUN_MATRIX.csv').open(encoding='utf-8')))
cohort=['UX06-'+x+'-20261124' for x in ['F10','F11','F12','R07','R08','R09','C07','C08','C09']]
final=[x for x in rows if x['RunId'] in cohort]
assert len(final)==9 and all(x['AcceptanceVerdict']=='PASS' and x['ExitCode']=='0' for x in final)
assert len({x['ProductDllSha256'] for x in final})==1
assert len({x['DriverSourceSha256'] for x in final})==1
assert collections.Counter(x['Region'] for x in final)=={'ForestRuins':3,'AncientRuins':3,'CrystalCavern':3}
builds=[]
for name in ['BUILD11','BUILD12_RELEASE']:
    item=json.loads((D/name/'RESULT.json').read_text())
    assert item['exitCode']==0
    assert json.loads((D/name/'INPUT_AND_SERVICE_VERIFICATION.json').read_text())['status']=='PASS'
    for a in item['artifacts']:
        p=pathlib.Path(a['path']);assert sha(p)==a['sha256'] and p.stat().st_size==a['bytes']
        builds.append({'Build':name,'BuildId':'UX06-'+item['artifacts'][1]['sha256'][:16], 'Type':'Acceptance' if item['acceptance'] else 'Release','OSExit':item['exitCode'],**a})
with (D/'BUILD_IDENTITY.tsv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(builds[0]),delimiter='\t');w.writeheader();w.writerows(builds)
release=pathlib.Path(builds[-1]['path']).read_bytes()
markers=['RegionRecordsPlayerProbe','PlayerAcceptanceHarness','CavernValidationDriver','UX_ACCEPTANCE','UX06_ACCEPTANCE','RegionRecordsTests','RegionRecordsBuildGuard']
scan={s:any(s.encode(enc) in release for enc in ['utf-8','utf-16le']) for s in markers}
assert not any(scan.values()),scan
(D/'RELEASE_EXCLUSION.json').write_text(json.dumps({'status':'PASS','method':'UTF8 and UTF16LE identifier scan of actual final Release Assembly-CSharp.dll; Editor sources not in Player','dllSha256':sha(pathlib.Path(builds[-1]['path'])),'found':scan},indent=2))
files=[]
git=['git','--no-optional-locks','-c','core.longpaths=true','-C',str(R)]
changed=subprocess.check_output(git+['diff','--name-only'],text=True).splitlines()
new=subprocess.check_output(git+['ls-files','--others','--exclude-standard','Assets'],text=True).splitlines()
for name in sorted(set(changed+new)):
    p=R/name;files.append({'Path':name,'Change':'MODIFIED' if name in changed else 'NEW','Bytes':p.stat().st_size,'Sha256':sha(p)})
with (D/'FILES_CHANGED.tsv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(files[0]),delimiter='\t');w.writeheader();w.writerows(files)
counts=collections.Counter(x['AcceptanceVerdict'] for x in rows)
(D/'FINAL_COHORT.json').write_text(json.dumps({'status':'PASS','finalNine':final,'allRuns':len(rows),'acceptanceCounts':counts,'note':'All raw verdicts preserved. Probe PASS with nonzero OS exit is NOT_ACCEPTED. Partial UI scope is separately stated.'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'finalNine':'PASS','allRuns':len(rows),'counts':counts,'sourceFiles':len(files),'releaseExclusion':scan}))
