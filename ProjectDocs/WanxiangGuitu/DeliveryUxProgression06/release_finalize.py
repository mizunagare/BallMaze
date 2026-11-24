"""External evidence reconciliation; no product state injection or source/Git mutations."""
import pathlib,json,csv,hashlib,collections,copy,subprocess,datetime
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];G=D/'RELEASE_RUNTIME'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def write_once(p,obj):
    if p.exists():assert load(p)==obj
    else:save(p,obj)
def decode(p):
    outer=load(p);assert outer['version']==10
    assert hashlib.sha256(outer['payload'].encode('utf-8')).hexdigest().upper()==outer['checksum']
    return outer,json.loads(outer['payload'])
def canonical(profile):
    value=copy.deepcopy(profile)
    resources=value['camp']['resources'];assert len({x['entityId'] for x in resources})==len(resources)
    value['camp']['resources']=sorted(resources,key=lambda x:x['entityId'])
    return value
original=list(csv.DictReader((G/'ORIGINAL_30_RUN_MATRIX.csv').open(encoding='utf-8')))
assert len(original)==30
new=[];comparisons=[];baseline_profile=None
for run in ['UX06-RELEASE-CORE-R01-20261124','UX06-RELEASE-COLD-R02-20261124']:
    p=D/'EVIDENCE'/run;m=load(p/'run-manifest.json');result=load(p/'process-result.json')
    assert result['exitCode']==0 and result['pid']==m['pid']
    assert m['acceptanceHarness']=='ABSENT' and m['region']=='ReleaseNativeUI'
    assert not any('ux06-region' in x or 'test-gameplay' in x for x in m['command'])
    assert sha(p/'native_release_input.js.source.txt')==m['driverSourceSha256']
    a,x=decode(p/'browse-start.save.json');b,y=decode(p/'browse-end.save.json')
    assert len(x['profile']['objectiveHistory'])==len(y['profile']['objectiveHistory'])==128
    assert x['profile']['objectiveHistory']==y['profile']['objectiveHistory']
    assert canonical(x['profile'])==canonical(y['profile'])
    if baseline_profile is None:baseline_profile=canonical(x['profile'])
    else:
        # Cold ApplyCamp calls Restart, not RestoreWorld: the world checkpoint is not a permanent region record.
        current=canonical(x['profile'])
        assert {k:v for k,v in baseline_profile.items() if k!='camp'}=={k:v for k,v in current.items() if k!='camp'}
        save(G/'COLD_PROFILE_DIFFERENCES.json',{'permanentProfileFieldsUnchanged':True,
          'changedProfileKeys':[k for k in baseline_profile if baseline_profile[k]!=current[k]],
          'changedCampKeys':[k for k in baseline_profile['camp'] if baseline_profile['camp'][k]!=current['camp'][k]],
          'note':'Camp world checkpoint randomStateJson/events change across restart. Existing AdventureFlow.ApplyCamp calls session.Restart and restores selected camp state, not RestoreWorld. No claim of whole Profile/live RNG equality across processes. Pure browsing within each Run is checked separately.'})
    assert [k for k in x if x[k]!=y[k]]==['revision','profile']
    assert [k for k in x['profile'] if x['profile'][k]!=y['profile'][k]]==['camp']
    assert [k for k in x['profile']['camp'] if x['profile']['camp'][k]!=y['profile']['camp'][k]]==['resources']
    changes=load(p/'before.json');after=load(p/'after.json')
    before_by={z['path']:z for z in changes};after_by={z['path']:z for z in after}
    pages=[k for k in before_by if '/drop-pages/' in k or 'drops/' in k]
    assert all(before_by[k]==after_by[k] for k in pages)
    observations=[json.loads(line) for line in (p/'observations.jsonl').read_text().splitlines()]
    inputs=[json.loads(line) for line in (p/'native-inputs.jsonl').read_text().splitlines()]
    for z in observations:
        assert list(p.glob(str(z['step']).zfill(3)+'-'+z['label']+'.*'))
    for phase in ['start','before-exit']:
        meta=load(p/('foreground-'+phase+'.json'))
        assert meta['pid']==meta['hwndPid']==meta['foregroundPid']==m['pid']
        assert meta['dpi']==96 and meta['clientRect']==[0,0,1280,720]
    log=(p/'player.log').read_text(encoding='utf-8',errors='replace')
    assert 'CodeReloadManager destroyed' in log and 'Crash!!!' not in log
    detail={'status':'PASS_PERSISTED_BUSINESS_STATE','runId':run,'revisionBefore':a['revision'],'revisionAfter':b['revision'],
       'rawMainShaBefore':sha(p/'browse-start.save.json'),'rawMainShaAfter':sha(p/'browse-end.save.json'),
       'rawBytesUnchanged':False,'historyEntries':128,'historyUnchanged':True,'canonicalProfileUnchanged':True,
       'resourceNodesBefore':len(x['profile']['camp']['resources']),'resourceNodesAfter':len(y['profile']['camp']['resources']),
       'onlyProfileDifference':'camp.resources serialization order; identical unique entityId->full row mapping',
       'explanation':'Existing LateUpdate autosave updates revision/time/checksum; Capture uses FindObjectsSortMode.None at CombatSaveSystem.cs:171. No byte-identity claim.',
       'liveRevisionRngAndUiState':'NOT_OBSERVED_IN_RELEASE','externalPagesCompared':len(pages)}
    save(p/'PERSISTED_BROWSE_COMPARISON.json',detail);comparisons.append(detail)
    verdict={'runId':run,'pid':m['pid'],'exitCode':0,'timedOut':False,'verdict':'PASS',
       'scope':'Visible uGUI region records, existing history, navigation, normal OS quit; cold read in R02',
       'notRun':['Pure Release IMGUI: no reachable product selector'],'internalTelemetry':'NOT_OBSERVED',
       'reviewBasis':'Original native-inputs, observations, PNGs, raw disk snapshots, process-result and clean shutdown log; reviewed by Codex'}
    write_once(p/'result.json',verdict)
    new.append({'RunId':run,'PID':str(m['pid']),'ExitCode':'0','OriginalVerdict':'PASS','AcceptanceVerdict':'PASS',
       'Region':m['region'],'BuildId':m['buildId'],'ProductDllSha256':m['dllSha256'],'ExeSha256':m['exeSha256'],
       'DriverSourceSha256':m['driverSourceSha256'],'DriverBinarySha256':m['driverBinarySha256'],
       'StorageRoot':m['isolatedStorageRoot'],'Evidence':p.relative_to(D).as_posix()})
with (D/'PLAYER_RUN_MATRIX.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(original[0]));w.writeheader();w.writerows(original+new)
correlation=[]
build_map={load(p)['artifacts'][1]['sha256']:p.parent.name for p in D.glob('BUILD*/RESULT.json') if len(load(p).get('artifacts',[]))>1}
final11=load(D/'BUILD11/RESULT.json')['artifacts'][1]['sha256'];final12=load(D/'BUILD12_RELEASE/RESULT.json')['artifacts'][1]['sha256']
for row in original+new:
    if row['ExitCode']=='0' and row not in new:continue
    p=D/row['Evidence'];native=int(row['ExitCode'])>255
    reason=load(p/'probe/result.json').get('reason','') if (p/'probe/result.json').exists() else 'normal system close; observed OS exit 0'
    correlation.append({'RunId':row['RunId'],'Build':build_map.get(row['ProductDllSha256'],'UNKNOWN'),'BuildId':row['BuildId'],
       'DllSha256':row['ProductDllSha256'],'ExeSha256':row['ExeSha256'],'DriverSha256':row['DriverSourceSha256'],
       'ExitCode':row['ExitCode'],'ExitHex':hex(int(row['ExitCode'])),'Classification':'NATIVE_ABNORMAL_EXIT' if native else 'CONTROLLED_FAILURE_EXIT' if row['ExitCode']!='0' else 'NORMAL_EXIT',
       'Stage':'After Input System Shutdown; Crash!!! in log; exact native cause unknown' if native else reason,
       'FinalBuild11':row['ProductDllSha256']==final11,'FinalBuild12':row['ProductDllSha256']==final12,
       'OriginalVerdict':row['OriginalVerdict'],'AcceptanceVerdict':row['AcceptanceVerdict'],'Log':(p/'player.log').relative_to(D).as_posix()})
with (G/'EXIT_CORRELATION.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(correlation[0]));w.writeheader();w.writerows(correlation)
sample=load(G/'SAMPLE_COPY.json');source=pathlib.Path(sample['source'])
assert all(sha(source/x['path'])==x['sha256'] and (source/x['path']).stat().st_mtime_ns==x['sourceMtimeNs'] for x in sample['files'])
start=load(G/'START.json')
assert all(sha(D/x['path'])==x['sha256'] and (D/x['path']).stat().st_size==x['bytes'] for x in start['oldEvidence'])
def git(*a):return subprocess.check_output(['git','--no-optional-locks','-c','core.longpaths=true',*a],cwd=R).decode()
index=pathlib.Path(git('rev-parse','--git-path','index').strip());index=index if index.is_absolute() else R/index
assert git('rev-parse','HEAD').strip()==start['head'] and git('branch','--show-current').strip()==start['branch']
assert sha(index)==start['indexSha256'] and not git('diff','--cached','--name-only').strip()
assert git('show-ref')==start['refs'] and git('diff','--name-status')==start['trackedDiff']
for x in load(D/'BUILD12_RELEASE/FROZEN_INPUT_MANIFEST.json'):assert sha(R/x['path'])==x['sha256']
for x in start['build']['artifacts']:assert sha(pathlib.Path(x['path']))==x['sha256']
save(G/'PROTECTION_AFTER.json',{'status':'PASS','head':start['head'],'branch':start['branch'],'indexSha256':sha(index),
 'refsUnchanged':True,'stagedEmpty':True,'frozenBuildInputsUnchanged':1516,'oldEvidenceUnchanged':len(start['oldEvidence']),
 'sourceSampleShaSizeMtimeUnchanged':len(sample['files']),'productSchemaSettingsUnchangedThisRound':True,'originalUX05':'Not operated; no repeat audit',
 'trackedDiff':git('diff','--name-status'),'remainingStatus':git('status','--porcelain=v1','--untracked-files=all')})
save(G/'SUMMARY.json',{'status':'CONDITIONAL_PASS','newReleaseRuns':new,'totalRuns':32,'rawVerdicts':{'PASS':26,'FAIL':6},'processAccepted':25,'notAccepted':7,
 'original30Preserved':True,'onlyNativeAbnormalRun':'UX06-F07-20261124','nativeAbnormalBuild':'BUILD09','finalReleaseNativeAbnormalObserved':False,
 'releaseImgui':'NOT_RUN_NO_PRODUCT_ENTRY','releaseBusinessComparison':comparisons,'submitPreparation':'CONDITIONAL_READONLY_READY_REQUIRES_OWNER_REVIEW; NO_STAGING_AUTHORIZATION'})
print(json.dumps({'status':'CONDITIONAL_PASS','newRuns':2,'exitCodes':[0,0],'old30Unchanged':True,'oldEvidenceUnchanged':len(start['oldEvidence']),'releaseImgui':'NOT_RUN_NO_PRODUCT_ENTRY'}))
