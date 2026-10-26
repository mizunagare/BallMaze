"""Fail on concrete runtime null/missing reference errors even if a process exited zero.
Keeps raw logs untouched. This narrow gate is not a claim that every possible error is classified.
"""
import argparse,json,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();findings=[];examined=[]
root=a.run.resolve(strict=True)
if not a.run.is_absolute() or 'locallow' in {x.lower() for x in root.parts} or not (root/'owner.json').is_file():raise ValueError('Explicit owned external test run required')
paths=list((a.run/'Rules').rglob('*.log'))+list((a.run/'Build').glob('*.log'))
for folder in a.run.glob('Normal-*'):paths+=list(folder.glob('*.log'))
for folder in a.run.glob('B09-Title-*'):paths+=list(folder.glob('player.log'))
paths+=list((a.run/'ControlledPlayer').glob('Case-*/player.log'))
for path in sorted(set(paths)):
 lines=path.read_text('utf-8-sig',errors='replace').splitlines();examined.append(path.relative_to(a.run).as_posix())
 for n,line in enumerate(lines):
  if re.match(r'^(NullReferenceException|MissingReferenceException|MissingComponentException):',line):
   context='\n'.join(lines[n:n+18])
   runtime=bool(re.search(r'Assets[\\/]CombatPrototype[\\/](?!Editor[\\/])[^\n]+\.cs:',context))
   if runtime:findings.append(dict(log=path.relative_to(a.run).as_posix(),line=n+1,error=line,stack=context))
result=dict(status='FAIL' if findings or not examined else 'PASS',scope='Concrete runtime null/missing-reference log gate; does not suppress logs, waive other exceptions or infer clean D3D12 exit',logs=examined,findings=findings)
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(dict(status=result['status'],logs=len(examined),runtimeReferenceErrors=len(findings))));raise SystemExit(1 if findings else 0)
