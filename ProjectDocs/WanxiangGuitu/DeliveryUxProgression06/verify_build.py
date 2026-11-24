import pathlib,json,hashlib,sys,re
DEV=pathlib.Path('I:/unity/WanxiangGuitu-UX06')
D=DEV/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression06'
P=pathlib.Path('I:/UX06_BUILD_20261124/Project')
record=sys.argv[1];e=D/record
result=json.loads((e/'RESULT.json').read_text(encoding='utf-8'));assert result['exitCode']==0
manifest=json.loads((e/'FROZEN_INPUT_MANIFEST.json').read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
dev_drift=[x['path'] for x in manifest if sha(DEV/x['path'])!=x['sha256']]
source_drift=[x['path'] for x in manifest if (x['path'].endswith(('.cs','.cs.meta')) or x['path'].startswith('Packages/')) and sha(P/x['path'])!=x['sha256']]
assert not dev_drift and not source_drift,(dev_drift,source_drift)
bee=json.loads((e/'SETTINGS/ACTUAL_BEE_INPUT.json').read_text(encoding='utf-8'))
services=bee['PlayerBuildProgramLibrary.Data.PlayerBuildConfig']['Services']
assert all(services[k] is False for k in ['EnableUnityConnect','EnablePerformanceReporting','EnableAnalytics','EnableCrashReporting','EnableInsights'])
effective=[]
for name in ['PC_RPAsset.asset','UniversalRenderPipelineGlobalSettings.asset']:
    a=(e/'SETTINGS'/ (name+'.baseline-effective.json')).read_bytes()
    b=(e/'SETTINGS'/ (name+'.imported-effective.json')).read_bytes()
    assert a==b,name
    effective.append({'asset':name,'baselineImportedEffectiveEqual':True,'sha256':hashlib.sha256(a).hexdigest()})
graphics=(e/'SETTINGS/PACKAGING/ProjectSettings/GraphicsSettings.asset').read_text(encoding='utf-8-sig')
base=(D/'SETTINGS_GATE/BASELINE/ProjectSettings/GraphicsSettings.asset').read_text(encoding='utf-8-sig')
guid=lambda s:sorted(re.findall(r'guid: ([0-9a-f]{32})',s))
assert guid(graphics)==guid(base),'Graphics external refs changed'
out={'status':'PASS','osExitCode':result['exitCode'],'devInputDrift':dev_drift,'scratchSourcePackageDrift':source_drift,
     'actualBeeServices':services,'urpEffectiveSettings':effective,'graphicsExternalReferencesUnchanged':True}
(e/'INPUT_AND_SERVICE_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out),flush=True)
