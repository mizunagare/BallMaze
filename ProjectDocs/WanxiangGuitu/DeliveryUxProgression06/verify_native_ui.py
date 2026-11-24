"""Read-only independent assertions over native input and observed product state."""
import pathlib,json,hashlib
D=pathlib.Path(__file__).resolve().parent
records=[]
for short in ['REAL-A03','CAPACITY-A01','UNKNOWN-A01','EMPTY-A01']:
    run='UX06-UI-'+short+'-20261124';p=D/'EVIDENCE'/run/'probe'
    baseline=json.loads((p/'readonly-baseline.json').read_text(encoding='utf-8'))
    final=json.loads((p/'readonly-final.json').read_text(encoding='utf-8'))
    for k in ['revision','profile','globalRng','attack','defense','saveSha']:assert baseline[k]==final[k],(run,k)
    steps={x.stem:json.loads(x.read_text(encoding='utf-8')) for x in sorted((p/'native-steps').glob('*.json'))}
    for name,s in steps.items():
        for k in ['revision','profile','globalRng','attack','defense']:assert s[k]==baseline[k],(name,k)
    inputs=[json.loads(x) for x in (p/'native-inputs.jsonl').read_text(encoding='utf-8').splitlines()]
    assert len(inputs)==len(steps)
    metadata=json.loads((p/'foreground.json').read_text()) if (p/'foreground.json').exists() else None
    full=[json.loads(x.read_text()) for x in p.glob('*foreground*.json') if 'foregroundPid' in json.loads(x.read_text())]
    for m in full:
        assert m['pid']==m['hwndPid']==m['foregroundPid']
        assert m['dpi']==96 and m['clientRect']==[0,0,1280,720]
    if not full and metadata:assert metadata['method']=='sky.activate_window'
    record={'runId':run,'nativeAttempts':len(inputs),'steps':len(steps),'readOnly':True,
            'nativeMetadataSamples':len(full),'focusEvidence':'full Win32 sample' if full else 'native input window + product focus gate; no full Win32 metadata sample in this Run',
            'activationArtifactPresent':metadata is not None}
    if short=='REAL-A03':
        assert len(steps)==20
        expected=[(0,0),(0,1),(1,0),(1,1),(1,2),(1,1),(2,0),(2,1)]
        observed=[(s['regionIndex'],s['regionPage']) for s in list(steps.values())[1:9]]
        assert expected==observed,(expected,observed)
        assert steps['019-imgui-region-history-jump']['historyRegion']==2
        assert not steps['020-imgui-close-no-clickthrough']['historyOpen']
        for a,b in [('004-ruins-screen-one','016-imgui-switch-ruins'),('005-ruins-screen-two','017-imgui-ruins-recent'),('006-ruins-screen-three','018-imgui-ruins-revisit'),('009-cavern-objectives-screen','014-imgui-cavern-next-screen')]:
            for k in ['profile','regionIndex','regionPage']:assert steps[a][k]==steps[b][k]
        record['pairedRendererStates']=4
    elif short=='CAPACITY-A01':
        assert [s['historyPage'] for s in list(steps.values())[:7]]==list(range(7))
        assert steps['008-ugui-previous6']['historyPage']==5
        assert steps['009-ugui-filter-forest']['historyRegion']==1
        assert steps['010-ugui-filter-gather-empty']['historyType']==1
        assert steps['012-ugui-jump-resets-type']['historyType']==0
        assert [steps[str(i).zfill(3)+'-imgui-page'+str(i-13)]['historyPage'] for i in range(15,20)]==[1,2,3,4,5]
        assert steps['020-imgui-page7']['historyPage']==5 # original unconsumed click retained
        assert steps['021-imgui-page7-retry']['historyPage']==6
        assert steps['022-imgui-previous6']['historyPage']==5
        assert steps['023-imgui-filter-ruins']['historyRegion']==2
        record['unconsumedAttempts']=['020-imgui-page7']
        record['notice']='Seven logical pages verified; all offscreen rows were not individually scrolled/read in this batch.'
    else:
        unknown=short.startswith('UNKNOWN')
        assert ('旧版目标历史未知' in steps[next(iter(steps))]['visibleText'])==unknown
        profile=json.loads(baseline['profile'])
        assert len(profile['objectiveHistory'])==0 and profile['objectiveHistoryLegacyUnknown']==unknown
        assert steps[list(steps)[1]]['regionRecordsOpen']
    records.append(record)
(D/'NATIVE_UI_RECOMPUTATION.json').write_text(json.dumps({'status':'FUNCTIONAL_PASS_METADATA_PARTIAL','nativeAttempts':sum(x['nativeAttempts'] for x in records),'unconsumed':1,'records':records},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':'FUNCTIONAL_PASS_METADATA_PARTIAL','runs':len(records),'attempts':sum(x['nativeAttempts'] for x in records),'unconsumed':1}))
