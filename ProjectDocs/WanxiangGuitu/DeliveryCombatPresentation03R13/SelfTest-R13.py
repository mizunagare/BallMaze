"""R1.3 synthetic association tests. Never evidence of an executed game process."""
import argparse,copy,hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
from ProcessFixtures import write_process,refresh_origin,association_paths,cli_association
HERE=Path(__file__).resolve().parent;TOOLS=HERE.parent/'DeliveryCombatPresentation03';CONTRACTS=HERE.parent/'DeliveryCombatPresentation03R11/Contracts'
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(exist_ok=False)
 s=importlib.util.spec_from_file_location('receipt',TOOLS/'Receipt.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 cases=[('native-hostpid','native','hostPid',9),('command-hostpid','command','hostPid',9),('command-exe','command','exe','D:/Other/Unity.exe'),('command-args','command','arguments',['wrong']),('origin-source-sha','origin','sourceSHA256AtSnapshot','0'*64),('origin-snapshot-sha','origin','snapshotSHA256','0'*64),('origin-source-path','origin','source','I:/Other/results.json'),('origin-snapshot-path','origin','snapshot','I:/Other/process-results.json'),('desktop-exe','desktop','exe','D:/Other/Unity.exe'),('desktop-pid-bool','desktop','pid',True),('command-pid-bool','command','hostPid',True),('command-relative-exe','command','exe','Unity.exe'),('desktop-relative-exe','desktop','exe','Unity.exe'),('origin-bad-sha','origin','snapshotSHA256','bad'),('command-time','command','startUtc','2026-10-31T00:00:03Z'),('desktop-time','desktop','utc','2026-10-31T00:00:03Z'),('origin-time','origin','utc','2026-10-31T00:00:01Z')]
 for name in ['foreign-native-content','foreign-native-path','foreign-command-path','foreign-origin-path','foreign-desktop-path','runner-args','snapshot-modified','missing-command','missing-origin','missing-desktop','missing-source','omit-command','omit-origin','omit-desktop','positive-editor','positive-runtime','open-editor','open-runtime']:cases.append((name,None,None,None))
 rows=[]
 for name,target,key,value in cases:
  root=a.output/name;profile='Runtime' if name.endswith('runtime') else 'Editor';pr,ex=write_process(root,profile,'PASS',0,False);assoc=association_paths(root,profile)
  paths=dict(native=ex,command=assoc['command_receipt'],origin=assoc['process_origin'],desktop=assoc['desktop_receipt'])
  contract=CONTRACTS/(profile+'.json');data=json.loads(contract.read_text(encoding='utf-8-sig'))
  if not name.startswith('open-'):
   for row in data['rows']:row['status']='PASS'
  src=root/'presentation.json';src.write_text(json.dumps(data),encoding='utf-8')
  if target:
   obj=json.loads(paths[target].read_text());obj[key]=value;paths[target].write_text(json.dumps(obj),encoding='utf-8')
  if name.startswith('foreign-'):
   fp,fe=write_process(root/'ForeignRun',profile,'PASS',0,False);fa=association_paths(fp.parent,profile)
   if name=='foreign-native-content':
    obj=json.loads(fe.read_text());obj['hostPid']=999;ex.write_text(json.dumps(obj))
   elif name=='foreign-native-path':ex=fe
   else:assoc[{'foreign-command-path':'command_receipt','foreign-origin-path':'process_origin','foreign-desktop-path':'desktop_receipt'}[name]]=fa[{'foreign-command-path':'command_receipt','foreign-origin-path':'process_origin','foreign-desktop-path':'desktop_receipt'}[name]]
  if name=='runner-args':
   obj=json.loads(pr.read_text());obj['command'].append('extra');pr.write_text(json.dumps(obj));refresh_origin(root)
  if name=='snapshot-modified':pr.write_bytes(pr.read_bytes()+b'\n')
  for part in ('command','origin','desktop'):
   if name=='missing-'+part:paths[part].unlink()
   if name=='omit-'+part:assoc[{'command':'command_receipt','origin':'process_origin','desktop':'desktop_receipt'}[part]]=None
  if name=='missing-source':(root/'results.json').unlink()
  before={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in root.rglob('*.json')}
  result=m.evaluate(src,contract=contract,profile=profile,process_receipt=pr,exit_receipt=ex,**assoc);m.write(result,root/'ApiReport')
  args=[sys.executable,str(TOOLS/'Receipt.py'),'--receipt',str(src),'--contract',str(contract),'--profile',profile,'--process-receipt',str(pr),'--exit-receipt',str(ex),'--output',str(root/'CliReport')]
  for k,flag in [('command_receipt','--command-receipt'),('process_origin','--process-origin'),('desktop_receipt','--desktop-receipt')]:
   if assoc[k]:args += [flag,str(assoc[k])]
  run=subprocess.run(args,capture_output=True,text=True);(root/'command.json').write_text(json.dumps(args));(root/'stdout.txt').write_text(run.stdout);(root/'stderr.txt').write_text(run.stderr);(root/'actual-exit.json').write_text(json.dumps({'exitCode':run.returncode}))
  cli=json.loads((root/'CliReport/acceptance.json').read_text(encoding='utf-8-sig'))
  expected,code=('PASS',0) if name.startswith('positive-') else ('BLOCKED',2) if name.startswith('open-') else ('INCOMPLETE',3)
  ok=result['overallStatus']==cli['overallStatus']==expected and result['exitCode']==cli['exitCode']==run.returncode==code and result['errors']==cli['errors'] and all(hashlib.sha256(Path(f).read_bytes()).hexdigest()==h for f,h in before.items())
  for folder in ['ApiReport','CliReport']:
   ok=ok and (root/folder/'assertions.csv').is_file() and expected in (root/folder/'REPORT.md').read_text(encoding='utf-8-sig')
  rows.append(dict(name=name,status='PASS' if ok else 'FAIL',expected=expected,actual=cli['overallStatus'],exitCode=run.returncode,errors=cli['errors']))
 result=dict(kind='SYNTHETIC TOOL TESTS; no game process executed',counts={x:sum(r['status']==x for r in rows) for x in ('PASS','FAIL')},rows=rows)
 (a.output/'selftest.json').write_text(json.dumps(result,indent=2));print(json.dumps(result['counts']));return bool(result['counts']['FAIL'])
if __name__=='__main__':raise SystemExit(main())
