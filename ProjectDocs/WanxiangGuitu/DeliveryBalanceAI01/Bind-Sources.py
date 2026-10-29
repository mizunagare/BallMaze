"""Read-only link between shipping sources, exact cloned input, build manifest and user files."""
import pathlib,sys,json,hashlib,subprocess
repo=pathlib.Path(sys.argv[1]);root=pathlib.Path(sys.argv[2]);project=root/'P/Project'
sha=lambda x:hashlib.sha256(x).hexdigest()
canon=lambda x:x.replace(b'\r\n',b'\n')
paths=subprocess.check_output(['git','-C',str(repo),'ls-files','-z','Assets/CombatPrototype']).decode().split('\0')
paths=[p for p in paths if p.endswith('.cs') and '/Editor/' not in p]+['Assets/CombatPrototype/EnemyAttackSignal.cs','Assets/CombatPrototype/ProgressionCurve.cs']
build=root/(sys.argv[3] if len(sys.argv)>3 else 'Final/Build')
inputs=json.loads((build/'build-inputs.json').read_text(encoding='utf-8-sig'));by={r['path'].replace('\\','/'):r for r in inputs}
rows=[];bad=[]
for p in sorted(set(paths)):
 a=(repo/p).read_bytes();b=(project/p).read_bytes();entry=by.get(p)
 row=dict(path=p,sourceRawSHA256=sha(a),runtimeCloneRawSHA256=sha(b),normalizedSHA256=sha(canon(a)),sourceCloneMatch=canon(a)==canon(b),buildInputSHA256=entry['sha256'].lower() if entry else None,buildInputMatch=entry is not None and entry['sha256'].lower()==sha(b));rows.append(row)
 if not row['sourceCloneMatch'] or not row['buildInputMatch']:bad.append(p)
for p in ['Assets/CombatPrototype/BAL01Trace.cs','Assets/CombatPrototype/Editor/B06LocalChecks/BAL01Matrix.cs']:
 if (project/p).exists():bad.append('observation residue:'+p)
scene='Assets/CombatPrototype/ForestRuins.unity';baseline=subprocess.check_output(['git','-C',str(repo),'show','77c4c8c3d11ac87b86ce8999cfb8dbd3e3cfdedf:'+scene]);cloned=(project/scene).read_bytes()
sceneBinding=dict(path=scene,source='baseline tracked scene, NOT user modified working scene',baselineSHA256=sha(baseline),cloneSHA256=sha(cloned),normalizedMatch=canon(baseline)==canon(cloned))
if not sceneBinding['normalizedMatch']:bad.append('baseline scene mismatch')
result=dict(status='FAIL' if bad else 'PASS',scope='Canonical newline source comparison plus exact raw build input hash; this binding targets tracked-scene replay. Original working-scene runs are separately identified, not erased.',buildManifest=str(build/'build-inputs.json'),files=rows,scene=sceneBinding,failures=bad)
(root/'source-bindings.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(result['status'],len(rows),'runtime C# files bound')
if bad:raise SystemExit(1)
