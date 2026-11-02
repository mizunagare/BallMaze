import json,hashlib
from pathlib import Path
r=Path('I:/WGCombat/CP04BR-1102-A');p=r/'Fixed/Project/Library/PackageCache/com.unity.inputsystem@7a4e1a2a8194/InputSystem/Editor/Internal/BuildProviderHelpers.cs';q=p.parent.parent/'ProjectWideActions/ProjectWideActionsBuildProvider.cs'
out=[]
for x in [p,q]:out.append({'path':str(x),'sha256':hashlib.sha256(x.read_bytes()).hexdigest(),'lines':[{'line':i+1,'text':s.strip()} for i,s in enumerate(x.read_text().splitlines()) if any(z in s for z in ['OnPreprocessBuild','OnPostprocessBuild','SetPreloadedAssets','GetPreloadedAssets','PreloadAsset','RemovePreloadedAsset'])]})
(r/'input-preload-source-audit.json').write_text(json.dumps(out,indent=2))
# exact stage and binary comparisons, without restoring isolated inputs
j=json.loads((r/'build-phase-analysis.json').read_text());summary={}
for b in j:
 if b['build']:
  before=next(x for x in b['stages'] if x['phase']=='execute-before-BuildPipeline');after=next(x for x in b['stages'] if x['phase']=='execute-after-BuildPipeline');summary[b['run']]={'changed':[a['path'] for a,c in zip(before['files'],after['files']) if a['sha256']!=c['sha256']],'before':before['connect'],'after':after['connect']}
a=json.loads((r/'assembly-audit.json').read_text(encoding='utf-8-sig'));d={x['build']:x for x in a};summary['pureBinaryComparison']={'exeSame':d['FixedBuildAudit']['exeSHA256']==d['FixedWarmPureBuild']['exeSHA256'],'assemblySame':d['FixedBuildAudit']['assemblySHA256']==d['FixedWarmPureBuild']['assemblySHA256'],'note':'Same exe is a generic Unity bootstrap; not proof of serialized/data equivalence'}
(r/'build-comparison.json').write_text(json.dumps(summary,indent=2));print(summary)
