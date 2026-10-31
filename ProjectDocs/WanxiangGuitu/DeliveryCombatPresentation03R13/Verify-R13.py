"""Independent consistency checks; no modification of source evidence."""
import argparse,collections,csv,hashlib,inspect,importlib.util,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=a.root;checks=[]
def check(name,ok):checks.append(dict(name=name,status='PASS' if ok else 'FAIL'))
for mode in ('Editor','Runtime'):
 s=a.source/mode;q=load(r/'Reaudit'/mode/'Semantic/acceptance.json');pr=q['process'];proof=pr['source'];name='CP03Editor.Run' if mode=='Editor' else 'CP03Runtime';raw=load(s/'process-results.json');raw=raw if isinstance(raw,list) else [raw];row=next(x for x in raw if x['name']==name);native=load(s/(name+'.exit.json'));cmd=load(s/(name+'.command.json'));origin=load(s/'process-origin.json');desktop=load(s/(name+'.desktop-process.json'))
 check(mode+' process and association',pr['evidenceStatus']==proof['associationStatus']=='PASS' and pr['status']=='PASS' and row['exitCode']==native['exitCode']==0 and row['timedOut'] is False)
 check(mode+' host PID pair',type(cmd['hostPid']) is int and cmd['hostPid']==native['hostPid']==proof['commandHostPid'])
 check(mode+' full exe triple',Path(cmd['exe']).resolve()==Path(row['command'][0]).resolve()==Path(desktop['exe']).resolve())
 check(mode+' exact arguments',cmd['arguments']==row['command'][1:]==proof['arguments'])
 check(mode+' origin paths',Path(origin['source']).resolve()==(s/'results.json').resolve() and Path(origin['snapshot']).resolve()==(s/'process-results.json').resolve())
 check(mode+' origin double hash',origin['snapshotSHA256'].lower()==origin['sourceSHA256AtSnapshot'].lower()==digest(s/'process-results.json'))
 for key,file in [('runnerReceipt','process-results.json'),('exitReceipt',name+'.exit.json'),('commandReceipt',name+'.command.json'),('originReceipt','process-origin.json'),('desktopReceipt',name+'.desktop-process.json')]:check(mode+' '+key,Path(proof[key]['path']).resolve()==(s/file).resolve() and proof[key]['sha256']==digest(s/file))
 counts=dict(collections.Counter(x['status'] for x in load(s/'presentation.json')['rows']));csvrows=list(csv.DictReader((r/'Reaudit'/mode/'Semantic/assertions.csv').open(encoding='utf-8-sig',newline='')))
 check(mode+' raw JSON CSV agreement',counts==q['counts']==dict(collections.Counter(x['status'] for x in csvrows))==dict(PASS=291,UNRESOLVED=2))
 check(mode+' semantic exit and report',q['overallStatus']=='BLOCKED' and q['exitCode']==load(r/'Reaudit'/mode/'actual-exit.json')['exitCode']==2 and '**BLOCKED**' in (r/'Reaudit'/mode/'Semantic/REPORT.md').read_text(encoding='utf-8-sig'))
 check(mode+' frozen contract',q['binding']['status']=='PASS' and q['binding']['profile']==mode and q['contractSHA256']==digest(HERE.parent/'DeliveryCombatPresentation03R11/Contracts'/(mode+'.json')))
 check(mode+' original receipt unchanged',q['receiptSHA256']==digest(s/'presentation.json'))
for folder,count in [('Legacy50-First',50),('Legacy33-First',33),('Legacy60-First',60),('Association-First',35)]:
 result=load(r/folder/'selftest.json');check(folder,result['counts'].get('PASS')==count and result['counts'].get('FAIL',0)==0 and len(result['rows'])==count)
check('old failures retained',load(r/'Before/regressions.json')['counts']==dict(PASS=1,FAIL=10))
x=load(r/'protected-after.json');check('3476 plus3191 protected',x['count']==3476 and not x['changed'] and x['statusUnchanged'] and x['extraCount']==3191 and not x['extraChanged'])
check('current3476',all(digest(Path(x['root'])/x['path'])==x['sha256'] for x in load(r/'protected-before.json')))
check('current3191',all(digest(Path(x['path']))==x['sha256'] for x in load(r/'extra-protected-before.json')))
x=load(r/'input-binding.json');check('1147 input and binaries',x['count']==1147 and not x['mismatch'] and not x['binaryMismatch'] and all(digest(a.source/'P/Project'/x['path'])==x['expected'] for x in x['files']) and all(digest(Path(x['path']))==x['sha256'] for x in x['binaries']))
check('product diff empty',not (r/'product-diff.txt').read_bytes());check('locked audit',load(r/'locked-contract.json')['status']=='PASS');check('PS syntax',all(x['status']=='PASS' for x in load(r/'powershell-parse.json')))
for f in ['Invoke-Runtime.ps1','Invoke-ReviewEditor.ps1']:
 text=(HERE.parent/'DeliveryCombatPresentation03'/f).read_text(encoding='utf-8-sig');check(f+' explicit sources',all(flag in text for flag in ['--command-receipt','--process-origin','--desktop-receipt']))
result=dict(counts={s:sum(x['status']==s for x in checks) for s in ('PASS','FAIL')},rows=checks);a.output.write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result['counts']));raise SystemExit(bool(result['counts']['FAIL']))
