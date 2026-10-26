"""Three explicitly synthetic harness probes. Never reads player saves."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
root=a.output.resolve()
if not a.output.is_absolute() or root.exists() or 'locallow' in str(root).lower():
    raise ValueError('Fresh external synthetic probe root required')
root.mkdir(parents=True)
gate=Path(__file__).resolve().parent.parent/'DeliveryB10/Check-RuntimeLogs.py'
rows=[]
for name,content,expected in [
    ('empty',None,1),
    ('nested-runtime-error','NullReferenceException: synthetic expected harness error\n  at Probe () (at Assets/CombatPrototype/SyntheticNeverShipped.cs:1)\n',1),
    ('nested-clean','Synthetic nonempty log; no game launched\n',0)]:
    r=root/name;r.mkdir();(r/'owner.json').write_text('{"kind":"synthetic harness probe; not game evidence"}')
    if content is not None:
        f=r/'Stage2Matrix/case/Normal.log';f.parent.mkdir(parents=True);f.write_text(content)
    cmd=[sys.executable,'-B',str(gate),'--run',str(r),'--output',str(r/'gate.json')]
    run=subprocess.run(cmd,capture_output=True,text=True)
    rows.append(dict(name=name,scope='harness-negative' if expected else 'harness-control',
                     expectedExit=expected,actualExit=run.returncode,
                     status='PASS' if run.returncode==expected else 'FAIL',
                     rawGate=json.loads((r/'gate.json').read_text()),stdout=run.stdout,stderr=run.stderr))
(root/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(dict(assertions=len(rows),failed=sum(r['status']=='FAIL' for r in rows))))
raise SystemExit(1 if any(r['status']=='FAIL' for r in rows) else 0)
