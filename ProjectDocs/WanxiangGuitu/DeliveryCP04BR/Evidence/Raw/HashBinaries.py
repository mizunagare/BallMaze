from pathlib import Path
import json,hashlib
r=Path('I:/WGCombat/CP04BR-1102-A');out=[]
for run in ['FixedBuildAudit','FixedWarmPureBuild','FixedAcceptanceBuild','BaselineAcceptanceBuild']:
 d=r/run/'Release';files=[]
 for p in sorted(d.rglob('*')):
  if p.is_file():files.append({'path':p.relative_to(d).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 out.append({'run':run,'files':files})
(r/'binary-manifests.json').write_text(json.dumps(out,indent=2));print([(x['run'],len(x['files'])) for x in out])
