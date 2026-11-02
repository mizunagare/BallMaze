import json,hashlib,collections
from pathlib import Path
r=Path('I:/WGCombat/CP04BR-1102-A');summary=[]
for n in ['FixedOpen2','FixedBuildAudit','FixedWarmPureBuild','FixedAcceptanceBuild','BaselineAcceptanceBuild']:
 stages=[]
 for p in sorted((r/n/'Stages').glob('*/snapshot.json')):
  j=json.loads(p.read_text(encoding="utf-8-sig"));stages.append({'phase':j['phase'],'utc':j['utc'],'files':j['files'],'connect':j['connect'],'packages':j['packages']})
 build=json.loads((r/n/'build.json').read_text(encoding="utf-8-sig")) if (r/n/'build.json').exists() else None
 if build:build={'result':build['result'],'options':build['options'],'errors':build['errors'],'warnings':build['warnings'],'seconds':build['seconds'],'shaderCallbacks':len(build['shaders']),'sumCallbackVariants':sum(x['variants'] for x in build['shaders']),'note':'Callback variants are pass/snippet observations, not distinct final shader-blob count'}
 summary.append({'run':n,'build':build,'stages':stages})
(r/'build-phase-analysis.json').write_text(json.dumps(summary,indent=2))
meta=[]
for pattern in ['**/ShaderBuildPreprocessor.cs','**/RenderPipelineGraphicsSettingsContainer.cs','**/UniversalRenderPipelineAssetPrefiltering.cs']:
 for p in (r/'Fixed/Project/Library/PackageCache').glob(pattern):
  lines=p.read_text(encoding='utf-8-sig').splitlines();hits=[{'line':i+1,'text':s.strip()} for i,s in enumerate(lines) if any(t in s for t in ['UpdateShaderPrefilteringDataBeforeBuild()','GatherShaderFeatures();','SaveAssetIfDirty','OnBeforeSerialize','OnAfterDeserialize','BuildPipeline.isBuildingPlayer','m_RuntimeSettings','UpdateShaderKeywordPrefiltering'])];meta.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'matches':hits})
(r/'package-source-audit.json').write_text(json.dumps(meta,indent=2));print([(x['run'],x['build']) for x in summary])

