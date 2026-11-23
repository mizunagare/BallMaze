import pathlib, json, hashlib, csv, datetime, collections, re
R=pathlib.Path.cwd()
D=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation'
O=D/'EVIDENCE/R2'
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def utc(v): return datetime.datetime.fromisoformat(v.replace('Z','+00:00'))
def save(p):
    e=load(p)
    assert e['version']==10
    assert hashlib.sha256(e['payload'].encode()).hexdigest().upper()==e['checksum']
    return e,json.loads(e['payload'])
fields={'runId','objectiveId','regionId','completedAtUtc','committedAtUtc','displayNameSnapshot'}
rows=[]
source=D/'EVIDENCE/CAPACITY-A02/WanxiangGuitu/ForestRuins-v10/save.json'
seed,seedp=save(source)
assert len(seedp['profile']['objectiveHistory'])==128 and len(seedp['profile']['committedRuns'])==129
for folder in sorted(O.glob('UX05-R2-CLOSURE-*')):
    m=load(folder/'run-manifest.json')
    run=m['runId']; interrupted=(folder/'instrument-interruption.json').exists()
    before,b=save(folder/'save.before.json')
    exe=pathlib.Path(m['exe']); dll=pathlib.Path(m.get('productDll',m.get('dll')))
    assert h(exe)==m['exeSha256'] and h(dll)==m.get('productDllSha256',m.get('dllSha256'))
    root=pathlib.Path(m.get('isolatedStorageRoot',m.get('storageRoot')))
    assert root.is_relative_to(O)
    result={'runId':run,'status':'INSTRUMENT_INTERRUPTED' if interrupted else 'PASS','pid':m['pid'],'buildId':m['buildId'],'exeSha256':h(exe),'productDllSha256':h(dll),'storageRoot':str(root),'instrumentation':'NONE_IN_PRODUCT; native @oai/sky only','beforeSaveSha256':h(folder/'save.before.json'),'historyCount':len(b['profile']['objectiveHistory']),'committedRunCount':len(b['profile']['committedRuns']),'exitCode':None,'nativeExitReceipt':False}
    assert b['profile']['objectiveHistory']==seedp['profile']['objectiveHistory']
    assert b['profile']['committedRuns']==seedp['profile']['committedRuns']
    inputlines=[json.loads(v) for v in (folder/'inputs.jsonl').read_text().splitlines()] if (folder/'inputs.jsonl').exists() else []
    result['inputAttempts']=len(inputlines)
    result['inputErrors']=len((folder/'input-errors.jsonl').read_text().splitlines()) if (folder/'input-errors.jsonl').exists() else 0
    if not interrupted:
        exit=load(folder/'host-exit.json'); assert exit['exitCode']==0 and exit['pid']==m['pid']
        result.update(exitCode=exit['exitCode'],nativeExitReceipt=True)
        after,a=save(folder/'save.after.json')
        assert a['profile']['objectiveHistory']==b['profile']['objectiveHistory']
        assert a['profile']['committedRuns']==b['profile']['committedRuns']
        protected=[k for k in b['profile'] if k!='camp']
        assert all(a['profile'][k]==b['profile'][k] for k in protected)
        assert all(set(x)==fields for x in a['profile']['objectiveHistory'])
        entries=[json.loads(v) for v in (root/'entry-audit.jsonl').read_text().splitlines()]
        start=utc(m.get('startedUtc',m.get('startUtc')));end=utc(exit.get('endedUtc',exit.get('endUtc')))
        entries=[v for v in entries if start<=utc(v['utc'])<=end]
        phases=[v['phase'] for v in entries]
        assert 'continue-selected' in phases and 'game-ready' in phases and any(v['phase']=='title-ready' and v['canContinue'] for v in entries)
        (folder/'entry-events.json').write_text(json.dumps(entries,ensure_ascii=True,indent=2))
        screens=list(folder.glob('*history*.jpg'))+list(folder.glob('*history*.png'))
        assert screens
        result.update(afterSaveSha256=h(folder/'save.after.json'),historyUnchanged=True,committedRunsUnchanged=True,otherProfileFieldsUnchanged=True,revisionBefore=before['revision'],revisionAfter=after['revision'],entryPhases=phases,historyScreens=[z.relative_to(D).as_posix() for z in screens],logSha256=h(folder/'Player.log'))
        log=(folder/'Player.log').read_text(errors='replace')
        result['logExceptionLines']=[v for v in log.splitlines() if re.search(r'Exception:|NullReferenceException|B09_ISOLATION_REJECTED',v)]
        assert not result['logExceptionLines']
        result['logKnownWarnings']=[v for v in log.splitlines() if ('not supported' in v or 'warning' in v.lower() or 'failed' in v.lower())][:30]
        if (folder/'save.history-view.json').exists():
            # Initial A01 audit assumed whole-session byte equality. Existing
            # unscaled-time/focus autosave makes that assumption invalid. Preserve
            # that failed audit and verify every changed business field instead.
            viewed,v=save(folder/'save.history-view.json')
            changed=[k for k in b if b[k]!=v[k]]
            assert set(changed)<= {'revision','profile'}
            assert all(v['profile'][k]==b['profile'][k] for k in protected)
            camp_changed=[k for k in b['profile']['camp'] if b['profile']['camp'][k]!=v['profile']['camp'][k]]
            assert set(camp_changed)<= {'randomStateJson','events','resources'}
            assert viewed['revision']>=before['revision']
            result.update(historyViewWholeSaveUnchanged=h(folder/'save.history-view.json')==h(folder/'save.before.json'),historyViewSha256=h(folder/'save.history-view.json'),historyViewChangedPayloadKeys=changed,historyViewChangedCampKeys=camp_changed,historyViewProtectedBusinessUnchanged=True)
        if (folder/'storage.before.json').exists():
            bef={v['path']:v for v in load(folder/'storage.before.json')};aft={v['path']:v for v in load(folder/'storage.after.json')}
            pages=[k for k in bef if 'ground-loot' in k]
            assert all(k in aft and bef[k]['sha256']==aft[k]['sha256'] for k in pages)
            result['unchangedPageFiles']=len(pages)
    (folder/'result.json').write_text(json.dumps(result,ensure_ascii=True,indent=2))
    rows.append({'run_id':run,'build_id':m['buildId'],'pid':m['pid'],'exit_code':result['exitCode'],'status':result['status'],'exe_sha256':h(exe),'product_dll_sha256':h(dll),'launcher_sha256':m.get('driverSha256','N/A inline launch, original manifest retained'),'storage_root':str(root.relative_to(R)),'history_count':result['historyCount'],'committed_run_count':result['committedRunCount'],'manifest':(folder/'run-manifest.json').relative_to(D).as_posix(),'result':(folder/'result.json').relative_to(D).as_posix(),'input_errors':result['inputErrors'],'notes':'No injected harness/probe; 1280x720 DPI96; original errors retained' if not interrupted else 'Node timeout terminated child tree; no normal exit code inferred'})
with (D/'NODEFINE_RELEASE_RUN_MATRIX.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={'newRunCount':len(rows),'statuses':dict(collections.Counter(x['status'] for x in rows)),'rows':rows,'seedSaveSha256':h(source),'seedHistoryCount':128,'seedCommittedRunCount':129,'interpretation':'New targeted runtime evidence only; no modification of historical 159 Run classifications'}
(O/'run-verification.json').write_text(json.dumps(summary,ensure_ascii=True,indent=2))
print(json.dumps({'newRuns':len(rows),'statuses':summary['statuses']}))
