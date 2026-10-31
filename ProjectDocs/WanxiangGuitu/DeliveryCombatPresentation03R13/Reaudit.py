"""Readonly reclassification of original real receipts; does not launch Unity."""
import argparse,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False);rows=[]
for mode in ('Editor','Runtime'):
 src=a.source/mode;out=a.output/mode;out.mkdir();name='CP03Editor.Run' if mode=='Editor' else 'CP03Runtime'
 args=[sys.executable,str(HERE.parent/'DeliveryCombatPresentation03/Receipt.py'),'--receipt',str(src/'presentation.json'),'--profile',mode,'--contract',str(HERE.parent/'DeliveryCombatPresentation03R11/Contracts'/(mode+'.json')),'--process-receipt',str(src/'process-results.json'),'--exit-receipt',str(src/(name+'.exit.json')),'--command-receipt',str(src/(name+'.command.json')),'--process-origin',str(src/'process-origin.json'),'--desktop-receipt',str(src/(name+'.desktop-process.json')),'--output',str(out/'Semantic')]
 run=subprocess.run(args,capture_output=True,text=True)
 for file,text in [('command.json',json.dumps(args)),('stdout.txt',run.stdout),('stderr.txt',run.stderr),('actual-exit.json',json.dumps(dict(exitCode=run.returncode)))]: (out/file).write_text(text,encoding='utf-8')
 q=json.loads((out/'Semantic/acceptance.json').read_text(encoding='utf-8-sig'));rows.append(dict(mode=mode,exitCode=run.returncode,overall=q['overallStatus'],counts=q['counts'],errors=q['errors']))
(a.output/'results.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows));raise SystemExit(0 if all(x['exitCode']==2 and x['overall']=='BLOCKED' and not x['errors'] and x['counts']==dict(PASS=291,UNRESOLVED=2) for x in rows) else 1)
