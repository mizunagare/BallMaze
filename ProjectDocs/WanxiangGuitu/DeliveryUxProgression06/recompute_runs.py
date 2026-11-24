"""Independent, read-only recomputation from original Player events and manifests."""
import pathlib,json,hashlib,csv,sys
D=pathlib.Path(__file__).resolve().parent
rows=[];checks=[]
for folder in sorted((D/'EVIDENCE').glob('UX06-*')):
    if not (folder/'result.json').exists():continue
    result=json.loads((folder/'result.json').read_text(encoding='utf-8'))
    manifest=json.loads((folder/'run-manifest.json').read_text(encoding='utf-8'))
    assert result['runId']==manifest['runId'] and result['pid']==manifest['pid']
    events=[json.loads(line) for line in (folder/'probe/events.jsonl').read_text(encoding='utf-8').splitlines()] if (folder/'probe/events.jsonl').exists() else []
    gameplay=manifest['region'] not in ['ui','ReleaseNativeUI']
    assertion={'runId':result['runId'],'rawVerdict':result['verdict'],'gameplay':gameplay}
    if result['verdict']=='PASS' and result['exitCode']!=0:
        assertion['status']='PROBE_PASS_OS_FAILURE_NOT_ACCEPTED'
    elif result['verdict']=='PASS' and manifest['region']=='ReleaseNativeUI':
        comparison=json.loads((folder/'PERSISTED_BROWSE_COMPARISON.json').read_text(encoding='utf-8'))
        assert result['exitCode']==0 and manifest['acceptanceHarness']=='ABSENT'
        assert comparison['historyUnchanged'] and comparison['canonicalProfileUnchanged']
        assertion.update(status='PASS_SCOPED_RELEASE_UGUI',internalTelemetry='NOT_OBSERVED',releaseImgui='NOT_RUN_NO_PRODUCT_ENTRY')
    elif result['verdict']=='PASS' and gameplay:
        cold=json.loads(next(x['data'] for x in events if x['name']=='cold-published-profile'))
        pending=json.loads(next(x['data'] for x in events if x['name']=='pending'))
        committed=json.loads(next(x['data'] for x in events if x['name']=='committed'))
        settlement=committed['settlement'];run=settlement['runId'];region=manifest['region']
        assert result['exitCode']==0 and not result['timedOut']
        assert settlement['outcome']==0 and settlement['status']==1
        assert pending['settlement']['status']==0
        old=cold.get('objectiveHistory',[]);history=committed['profile']['objectiveHistory']
        added=[x for x in history if x['runId']==run]
        assert len(added)==1 and added[0]['regionId']==region
        assert not any(x['runId']==run for x in pending['profile']['objectiveHistory'])
        assert added[0]==next(x for x in pending['settlement']['plan']['objectiveHistory'] if x['runId']==run)
        assert committed['profile']['committedRuns'].count(run)==1
        assert len(history)==min(128,len(old)+1)
        interactions=[x for x in events if x['name']=='product-interaction' and 'used=True' in x['data']]
        assert len(interactions)>=(4 if region=='AncientRuins' else 3 if region=='ForestRuins' else 4)
        assert any(x['name']=='movement-input' and 'focused=True' in x['data'] for x in events)
        assertion.update({'status':'PASS','objectiveId':added[0]['objectiveId'],'runIdentity':run,
                          'coldHistoryCount':len(old),'committedHistoryCount':len(history),
                          'pendingHistoryAbsent':True,'frozenPendingRowMatchesCommitted':True,
                          'permanentCommitIdentityExactlyOnce':True,'successfulInteractions':len(interactions)})
    elif result['verdict']=='PASS' and not gameplay:
        first=json.loads((folder/'probe/readonly-baseline.json').read_text(encoding='utf-8'))
        last=json.loads((folder/'probe/readonly-final.json').read_text(encoding='utf-8'))
        for key in ['revision','profile','globalRng','attack','defense','saveSha']:assert first[key]==last[key],(folder.name,key)
        assertion.update(status='PASS',readOnlyWindowVerified=True)
    else:assertion['status']='RAW_FAILURE_PRESERVED_NOT_RECLASSIFIED'
    checks.append(assertion)
    rows.append({'RunId':result['runId'],'PID':result['pid'],'ExitCode':result['exitCode'],'OriginalVerdict':result['verdict'],'AcceptanceVerdict':('PASS' if result['verdict']=='PASS' and result['exitCode']==0 and not result['timedOut'] else 'NOT_ACCEPTED'),
                 'Region':manifest['region'],'BuildId':manifest['buildId'],'ProductDllSha256':manifest['dllSha256'],
                 'ExeSha256':manifest['exeSha256'],'DriverSourceSha256':manifest['driverSourceSha256'],
                 'DriverBinarySha256':manifest['driverBinarySha256'],'StorageRoot':manifest['isolatedStorageRoot'],
                 'Evidence':folder.relative_to(D).as_posix()})
if (D/'RELEASE_RUNTIME/ORIGINAL_30_RUN_MATRIX.csv').exists():
    baseline=list(csv.DictReader((D/'RELEASE_RUNTIME/ORIGINAL_30_RUN_MATRIX.csv').open(encoding='utf-8')))
    by_id={x['RunId']:{k:str(v) for k,v in x.items()} for x in rows} # CSV cells are strings
    assert all(by_id[x['RunId']]==x for x in baseline),'Original Run classification drift'
    original_ids={x['RunId'] for x in baseline}
    rows=baseline+[x for x in rows if x['RunId'] not in original_ids]
with (D/'PLAYER_RUN_MATRIX.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ['RunId']);writer.writeheader();writer.writerows(rows)
(D/'INDEPENDENT_RUN_RECOMPUTATION.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'runs':len(rows),'pass':sum(x['AcceptanceVerdict']=='PASS' for x in rows),'fail':sum(x['OriginalVerdict']=='FAIL' for x in rows)}))
