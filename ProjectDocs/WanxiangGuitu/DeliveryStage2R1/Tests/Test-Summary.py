"""Real subprocess regressions of the existing matrix CLI; synthetic evidence only."""
import argparse,copy,hashlib,json,shutil,subprocess,sys,threading,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
if a.output.exists() or not a.output.is_absolute():raise ValueError('Fresh absolute test output required')
background=[]
a.output.mkdir(parents=True);source=Path(__file__).resolve().parents[2]/'DeliveryStage2';results=[]
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,sort_keys=True)+'\n',encoding='utf8')
def fixture(work,ident='one',outcome='Extracted',contract='economy'):
 c=dict(id=ident,build='Safety',strategy='Gather',seed=1,weapon=3,target=4)
 if contract!='economy':c.update(contract=contract,expectedOutcome=outcome)
 f=work/'matrix'/ident;f.mkdir(parents=True);write(f/'stage2-input.json',c);h=hashlib.sha256((f/'stage2-input.json').read_bytes()).hexdigest();attempt='attempt-'+ident
 meta=dict(schemaVersion=2,caseId=ident,attemptId=attempt,blockId='block1',configSha256=h,codeInput='a'*64,driverInput='b'*64,launchedUtc='2026-10-27T00:00:00Z')
 write(f/'attempt.json',meta)
 metric=dict(input=c,status='PASS',profile='profile-'+ident,run='run-'+ident,region='run-'+ident+':ForestRuins:1',secondRun='second-'+ident,secondRegion='second-'+ident+':ForestRuins:1',extracted=outcome=='Extracted',committed=True,acknowledged=True,secondForest=True,elapsedSeconds=60,damageTaken=0,potionsUsed=0,meters=90,obtained=[0,0,0,9,0,0],kept=[0,0,0,7,0,0],lost=[0]*6,measurementCompleteness='complete')
 write(f/'stage2-metrics.json',metric)
 tx=[dict(label='depart',run=metric['run'],profile=metric['profile'],region=metric['region']),dict(label='settlement-pending',run=metric['run'],profile=metric['profile'],outcome=outcome),dict(label='acknowledged',profile=metric['profile'],settlementStatus='Committed',ack=True),dict(label='verified-new-process-second-forest',run=metric['secondRun'],profile=metric['profile'],region=metric['secondRegion'])]
 (f/'stage2-transactions.jsonl').write_text(''.join(json.dumps(t)+'\n' for t in tx),encoding='utf8')
 for mode in ('Normal','Resume','FinalResume'):
  write(f/f'process-result-{mode}.json',dict(mode=mode,exitCode=0,timedOut=False))
  write(f/f'stage-result-{mode}.json',dict(meta,mode=mode,profile=metric['profile'],firstRun=metric['run'],run=metric['run'] if mode=='Normal' else metric['secondRun'],stage=1 if mode=='Normal' else 2,complete=True))
 return c,f,metric

def test(name,mutate,assertion):
 w=a.output/name;w.mkdir();shutil.copyfile(source/'Summarize-Matrix.py',w/'Summarize-Matrix.py')
 if (source/'MatrixEvidence.py').exists():shutil.copyfile(source/'MatrixEvidence.py',w/'MatrixEvidence.py')
 c,f,m=fixture(w);plan={'cases':[c],'inputIdentity':{'codeInput':'a'*64,'driverInput':'b'*64}};write(w/'matrix/owner.json',{'kind':'synthetic-offline-R1-only'});write(w/'matrix/preserved-processes.json',[]);write(w/'matrix/results.json',[])
 mutate(w,plan,c,f,m);write(w/'MATRIX_INPUTS.json',plan)
 child=subprocess.run([sys.executable,'-B',str(w/'Summarize-Matrix.py'),'--matrix',str((w/'matrix').resolve()),'--output',str((w/'summary').resolve())],capture_output=True,text=True)
 for stop,thread in background:stop.set();thread.join(2)
 background.clear()
 (w/'stdout.txt').write_text(child.stdout,encoding='utf8');(w/'stderr.txt').write_text(child.stderr,encoding='utf8')
 try:s=json.loads((w/'summary/matrix-summary.json').read_text(encoding='utf-8-sig'));ok=bool(assertion(child.returncode,s));error=''
 except Exception as e:ok=False;s={};error=repr(e)
 results.append(dict(name=name,status='PASS' if ok else 'FAIL',exitCode=child.returncode,summaryStatus=s.get('status'),error=error));write(w/'assertion.json',results[-1])

def patch_metric(f,m,**values):m.update(values);write(f/'stage2-metrics.json',m)
def nochange(*args):pass
def rejected(code,s):return code!=0 and s['status']!='PASS'
test('R01-complete',nochange,lambda c,s:c==0 and s['status']=='PASS' and s.get('started',s.get('validSorties'))==1)
def grouped_fixture(w,p,c,f,m):
 c2,f2,m2=fixture(w,'two');c2['build']='Boss';p['cases'].append(c2);write(f2/'stage2-input.json',c2);m2.update(input=c2,elapsedSeconds=90);write(f2/'stage2-metrics.json',m2);meta=json.loads((f2/'attempt.json').read_text());meta['configSha256']=hashlib.sha256((f2/'stage2-input.json').read_bytes()).hexdigest();write(f2/'attempt.json',meta)
 for mode in ('Normal','Resume','FinalResume'):
  stage=json.loads((f2/f'stage-result-{mode}.json').read_text());stage.update(meta);write(f2/f'stage-result-{mode}.json',stage)
test('R01-build-separation',grouped_fixture,lambda c,s:c==0 and s['groupsDescriptiveOnly']['Safety']['elapsedSeconds']['mean']==60 and s['groupsDescriptiveOnly']['Boss']['elapsedSeconds']['mean']==90 and s['groupsDescriptiveOnly']['Gather']['elapsedSeconds']['n']==0)
test('R02-null-run',lambda w,p,c,f,m:patch_metric(f,m,run=None),rejected)
for flag in ('extracted','committed','acknowledged','secondForest'):
 test('R03-'+flag,lambda w,p,c,f,m,flag=flag:patch_metric(f,m,**{flag:False}),rejected)
test('R04-input-hash',lambda w,p,c,f,m:write(f/'attempt.json',dict(json.loads((f/'attempt.json').read_text()),configSha256='0'*64)),rejected)
test('R04-code-hash',lambda w,p,c,f,m:write(f/'attempt.json',dict(json.loads((f/'attempt.json').read_text()),codeInput='c'*64)),rejected)
test('R04-config',lambda w,p,c,f,m:patch_metric(f,m,input=dict(c,weapon=0)),rejected)
test('R05-stage',lambda w,p,c,f,m:(f/'stage-result-Resume.json').unlink(),rejected)
test('R05-process',lambda w,p,c,f,m:(f/'process-result-Resume.json').unlink(),rejected)
for fault in ('nonzero','timeout','interrupt'):
 def bad(w,p,c,f,m,fault=fault):
  if fault=='interrupt':write(f/'validation-interruption.json',{'reason':'synthetic'})
  else:write(f/'process-result-Normal.json',{'mode':'Normal','exitCode':1 if fault=='nonzero' else None,'timedOut':fault=='timeout'})
 test('R06-'+fault,bad,rejected)
def missing(w,p,c,f,m):
 c2,f2,m2=fixture(w,'two');p['cases'].append(c2);(f2/'stage2-metrics.json').unlink();write(w/'matrix/results.json',[{'name':'two.Normal','status':'FAIL'}]);(f2/'stage2-transactions.jsonl').write_text(json.dumps({'label':'depart','run':'run-two','profile':'profile-two','region':'run-two:ForestRuins:1'})+'\n',encoding='utf8')
test('R07-missing',missing,lambda c,s:rejected(c,s) and s.get('started')==2 and s.get('unknown')==1 and s.get('knownTerminal')==1 and s.get('technicalInterrupted')==1)
for field,value in [('elapsedSeconds','60'),('committed',1),('obtained',[0]),('profile',None)]:
 test('R08-type-'+field,lambda w,p,c,f,m,field=field,value=value:patch_metric(f,m,**{field:value}),rejected)
test('R08-input-type',lambda w,p,c,f,m:patch_metric(f,m,input=dict(c,seed=True)),rejected)
test('R08-attempt-array',lambda w,p,c,f,m:write(f/'attempt.json',[1]),rejected)
def wrong_ack(w,p,c,f,m):
 tx=[json.loads(x) for x in (f/'stage2-transactions.jsonl').read_text().splitlines()];tx[2]['run']='other-run';(f/'stage2-transactions.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in tx),encoding='utf8')
test('R03-ack-identity',wrong_ack,rejected)
test('R08-json',lambda w,p,c,f,m:(f/'stage2-metrics.json').write_text('{',encoding='utf8'),lambda c,s:rejected(c,s) and s.get('started')==1)
def partial(w,p,c,f,m):
 c2,f2,m2=fixture(w,'two');p['cases'].append(c2);patch_metric(f2,m2,status='FAIL',elapsedSeconds=2,extracted=False,measurementCompleteness='partial');write(f2/'process-result-Normal.json',{'mode':'Normal','exitCode':1,'timedOut':False});(f2/'stage2-transactions.jsonl').write_text(json.dumps({'label':'depart','run':'run-two','profile':'profile-two','region':'run-two:ForestRuins:1'})+'\n',encoding='utf8')
test('R09-partial',partial,lambda c,s:rejected(c,s) and s['groupsDescriptiveOnly']['Safety']['elapsedSeconds']['mean']==60 and s['groupsDescriptiveOnly']['Safety']['elapsedSeconds']['n']==1 and s.get('partialWindows',[{}])[0].get('elapsedSeconds')==2)
for outcome in ('Death','Abandoned'):
 def terminal(w,p,c,f,m,outcome=outcome):
  c.update(contract='terminal',expectedOutcome=outcome);write(f/'stage2-input.json',c);meta=json.loads((f/'attempt.json').read_text());meta['configSha256']=hashlib.sha256((f/'stage2-input.json').read_bytes()).hexdigest();write(f/'attempt.json',meta)
  patch_metric(f,m,input=c,extracted=False)
  tx=[json.loads(x) for x in (f/'stage2-transactions.jsonl').read_text().splitlines()];tx[1]['outcome']=outcome;(f/'stage2-transactions.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in tx),encoding='utf8')
  for mode in ('Normal','Resume','FinalResume'):
   stage=json.loads((f/f'stage-result-{mode}.json').read_text());stage.update(meta);write(f/f'stage-result-{mode}.json',stage)
 test('R10-'+outcome,terminal,lambda c,s:c==0 and s['knownTerminal']==1 and (s['died']+s['abandoned'])==1 and s['extracted']==0)
test('R11-case',lambda w,p,c,f,m:p['cases'].append(dict(c)),rejected)
test('R11-same-successor',lambda w,p,c,f,m:patch_metric(f,m,secondRun=m['run']),rejected)
def duplicate(w,p,c,f,m,kind):
 c2,f2,m2=fixture(w,'two');p['cases'].append(c2)
 if kind=='attempt':write(f2/'attempt.json',dict(json.loads((f2/'attempt.json').read_text()),attemptId='attempt-one'))
 else:patch_metric(f2,m2,run=m['run'])
for kind in ('attempt','run'):test('R11-'+kind,lambda w,p,c,f,m,kind=kind:duplicate(w,p,c,f,m,kind),rejected)
test('R12-empty',lambda w,p,c,f,m:p.update(cases=[]),rejected)
def notstarted(w,p,c,f,m):
 for x in list(f.iterdir()):x.unlink()
test('R12-notstarted',notstarted,lambda c,s:c!=0 and s['status']!='PASS' and s.get('notStarted')==1 and s['extractionSuccessRate'] is None)
test('R14-not-finalized',lambda w,p,c,f,m:(w/'matrix/preserved-processes.json').unlink(),rejected)
def moving(w,p,c,f,m):
 stop=threading.Event()
 def mutate():
  i=0;end=time.monotonic()+15
  while not stop.is_set() and time.monotonic()<end:
   (w/'matrix/changing.txt').write_text(str(i),encoding='utf8');i+=1;time.sleep(.001)
 thread=threading.Thread(target=mutate,daemon=True);thread.start();background.append((stop,thread))
test('R14-changing-input',moving,rejected)
write(a.output/'results.json',{'scope':'Offline synthetic regression assertions; negative child FAILs expected; not Unity/game tests','sourceSha256':hashlib.sha256((source/'Summarize-Matrix.py').read_bytes()).hexdigest(),'results':results})
print(json.dumps({'PASS':sum(x['status']=='PASS' for x in results),'FAIL':sum(x['status']=='FAIL' for x in results),'failed':[x['name'] for x in results if x['status']=='FAIL']}));raise SystemExit(1 if any(x['status']=='FAIL' for x in results) else 0)
