"""Reuse existing audit and add B09 runtime/test exclusion checks."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--project',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--target',type=Path,required=True);p.add_argument('--baseline',required=True);a=p.parse_args();here=Path(__file__).resolve().parent
subprocess.run([sys.executable,'-B',str(here.parent/'DeliveryB08/Audit-Release.py'),'--project',str(a.project),'--run',str(a.run),'--target',str(a.target),'--baseline',a.baseline],check=True)
raw=(a.run/'Build/Release/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll').read_bytes()
runtime={k:k.encode() in raw for k in ['GameEntry','SaveCatalog','NewProfileTransaction','TitleMenu','ScenePresentation','FantasyActorVisual']}
excluded={k:k.encode() in raw for k in ['EntryInterruption','B09Rules','B09Visual','B09Cases','WGNormalAICheck','SetNextSeedForValidation']}
result={'status':'PASS' if all(runtime.values()) and not any(excluded.values()) else 'FAIL','scope':'Static release managed metadata; not UI acceptance','runtime':runtime,'excludedTestNamesPresent':excluded,'sha256':hashlib.sha256(raw).hexdigest()}
(a.target/'release-entry-check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');print(json.dumps(result));raise SystemExit(0 if result['status']=='PASS' else 1)
