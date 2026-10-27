"""Finite S2-R2 CLI tests, reusing S2-R1's synthetic fixture functions only.
No Unity, game execution, player save, network or historical-input mutation.
"""
import argparse,ast,copy,hashlib,json,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--source',type=Path);a=p.parse_args()
if not a.output.is_absolute() or a.output.exists():raise ValueError('Fresh absolute output required')
here=Path(__file__).resolve().parent;source=a.source or here.parent/'DeliveryStage2';original=here.parent/'DeliveryStage2R1/Tests/Test-Summary.py'
tree=ast.parse(original.read_text(encoding='utf-8-sig'));defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('write','fixture','patch_metric')];exec(compile(ast.Module(body=defs,type_ignores=[]),str(original),'exec'))
a.output.mkdir(parents=True);results=[]
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def txwrite(f,tx):(f/'stage2-transactions.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in tx),encoding='utf8')
def txread(f):return [json.loads(x) for x in (f/'stage2-transactions.jsonl').read_text().splitlines()]
def sync(f,c,m):
 write(f/'stage2-input.json',c);m['input']=copy.deepcopy(c);write(f/'stage2-metrics.json',m)
 meta=load(f/'attempt.json');meta['configSha256']=hashlib.sha256((f/'stage2-input.json').read_bytes()).hexdigest();write(f/'attempt.json',meta)
 for mode in ('Normal','Resume','FinalResume'):
  file=f/f'stage-result-{mode}.json'
  if file.exists():stage=load(file);stage.update(meta);write(file,stage)
def test(name,mutate,assertion,expectation,legacy=False):
 w=a.output/name;w.mkdir();tool=w/'Tool';tool.mkdir()
 for n in ('Summarize-Matrix.py','MatrixEvidence.py'):shutil.copyfile(source/n,tool/n)
 c,f,m=fixture(w);tx=txread(f);tx[1]['region']=m['region'];txwrite(f,tx)
 plan=dict(cases=[c],inputIdentity=dict(codeInput='a'*64,driverInput='b'*64));write(w/'matrix/owner.json',dict(kind='S2-R2 synthetic fixture only'));write(w/'matrix/preserved-processes.json',[]);write(w/'matrix/results.json',[])
 mutate(w,plan,c,f,m);write(w/'plan.json',plan)
 command=[sys.executable,'-B',str(tool/'Summarize-Matrix.py'),'--matrix',str(w/'matrix'),'--plan',str(w/'plan.json'),'--output',str(w/'summary')]
 if legacy:command.append('--legacy-audit')
 child=subprocess.run(command,capture_output=True,text=True,encoding='utf8');(w/'stdout.txt').write_text(child.stdout,encoding='utf8');(w/'stderr.txt').write_text(child.stderr,encoding='utf8')
 try:s=load(w/'summary/matrix-summary.json');ok=bool(assertion(child.returncode,s));error=''
 except Exception as e:s={};ok=False;error=repr(e)
 row=dict(name=name,status='PASS' if ok else 'FAIL',expectation=expectation,exitCode=child.returncode,observedStatus=s.get('status'),finalAcceptanceEligible=s.get('finalAcceptanceEligible'),command=command,error=error);results.append(row);write(w/'assertion.json',row)
def noop(*args):pass
def reject(code,s):return code!=0 and s['status']!='PASS' and s['finalAcceptanceEligible'] is False
def row(s):return s['rows'][0]
test('R2-01-economy',noop,lambda c,s:c==0 and s['status']=='PASS' and s['knownTerminal']==1,'Valid economy three-stage PASS')
for outcome in ('Death','Abandoned'):
 def terminal(w,p,c,f,m,outcome=outcome):
  c.update(contract='terminal',expectedOutcome=outcome,acceptedOutcomes=[outcome],requiredModes=['Normal']);m.update(extracted=False,secondForest=False,secondRun='',secondRegion='');sync(f,c,m)
  tx=txread(f);tx[1]['outcome']=outcome;txwrite(f,[x for x in tx if x['label']!='verified-new-process-second-forest'])
  for mode in ('Resume','FinalResume'):
   (f/f'process-result-{mode}.json').unlink();(f/f'stage-result-{mode}.json').unlink()
 test('R2-02-terminal-'+outcome,terminal,lambda c,s:c==0 and s['knownTerminal']==1 and s['died']+s['abandoned']==1,'Terminal legitimately requires Normal only')
for mode in ('Normal','Resume','FinalResume'):
 for label,value in [('null',None),('array',[]),('string','complete'),('boolean',False)]:
  file='stage-result-'+mode+'.json'
  test('R2-03-'+mode+'-'+label,lambda w,p,c,f,m,file=file,value=value:write(f/file,value),lambda c,s,file=file:reject(c,s) and any(file in x for x in row(s)['issues']),'Required stage root object rejected with file path')
 for label in ('empty-object','missing-field','broken-json','missing-file'):
  file='stage-result-'+mode+'.json'
  def broken(w,p,c,f,m,file=file,label=label):
   if label=='empty-object':write(f/file,{})
   elif label=='missing-field':d=load(f/file);del d['attemptId'];write(f/file,d)
   elif label=='broken-json':(f/file).write_text('{',encoding='utf8')
   else:(f/file).unlink()
  test('R2-04-'+mode+'-'+label,broken,lambda c,s,file=file:reject(c,s) and any(file in x for x in row(s)['issues']),'Required object/fields/JSON/existence independently validated')
def shrink(w,p,c,f,m):
 p['cases']=[dict(c,requiredModes=['Normal'])]
 for mode in ('Resume','FinalResume'):
  (f/f'process-result-{mode}.json').unlink();(f/f'stage-result-{mode}.json').unlink()
test('R2-05-plan-shrink',shrink,reject,'Changing plan cannot reduce frozen economy evidence')
def shrink_all(w,p,c,f,m):shrink(w,p,c,f,m);c['requiredModes']=['Normal'];sync(f,c,m);p['cases']=[copy.deepcopy(c)]
test('R2-05-economy-all-shrink',shrink_all,reject,'Even matching declarations cannot redefine economy as one stage')
for field,value in [('contract','terminal'),('expectedOutcome','Death'),('acceptedOutcomes',['Extracted','Death']),('contractVersion',2)]:
 test('R2-06-plan-'+field,lambda w,p,c,f,m,field=field,value=value:p.update(cases=[dict(c,**{field:value})]),reject,'Acceptance semantic drift rejected')
def metric_shrink(w,p,c,f,m):patch_metric(f,m,input=dict(c,requiredModes=['Normal']))
test('R2-06-metric-contract',metric_shrink,reject,'Metric embedded contract is also frozen-bound')
test('R2-06-condition-kind',lambda w,p,c,f,m:p.update(cases=[dict(c,kind='Lake')]),reject,'Recorded target kind is a stable condition, not a descriptive label')
def terminal_expected_drift(w,p,c,f,m):
 c.update(contract='terminal',expectedOutcome='Extracted',acceptedOutcomes=['Extracted','Death'],requiredModes=['Normal']);sync(f,c,m);p['cases']=[dict(c,expectedOutcome='Death')]
test('R2-06-terminal-expected-drift',terminal_expected_drift,reject,'Expected outcome must bind even when actual outcome remains in the accepted set')
def no_schema_downgrade(w,p,c,f,m):terminal(w,p,c,f,m,outcome='Death');write(f/'stage-result-Normal.json',None)
test('R2-06-no-schema-downgrade',no_schema_downgrade,reject,'Explicit legacy mode cannot waive existing modern frozen identity/stage evidence',legacy=True)
def explicit_defaults(w,p,c,f,m):p['cases']=[dict(c,contractVersion=1,contract='economy',expectedOutcome='Extracted',acceptedOutcomes=['Extracted'],requiredModes=['Normal','Resume','FinalResume'])]
test('R2-07-explicit-plan-defaults',explicit_defaults,lambda c,s:c==0 and s['status']=='PASS','Implicit frozen defaults match equivalent explicit plan defaults')
def explicit_input(w,p,c,f,m):original=copy.deepcopy(c);explicit_defaults(w,p,c,f,m);c.update(p['cases'][0]);sync(f,c,m);p['cases']=[original]
test('R2-07-explicit-input-defaults',explicit_input,lambda c,s:c==0 and s['status']=='PASS','Equivalent explicit frozen defaults match implicit plan')
test('R2-07-description-metadata',lambda w,p,c,f,m:p.update(cases=[dict(c,description='Read-only label, not acceptance conditions')]),lambda c,s:c==0 and s['status']=='PASS','Descriptive metadata does not change the normalized acceptance contract')
def not_run(w,p,c,f,m,registered=False):
 for x in list(f.iterdir()):
  if not registered or x.name!='attempt.json':x.unlink()
 write(w/'matrix/results.json',[dict(name=c['id']+'.'+mode,status='NOT_RUN',exitCode=None,timedOut=False,reason='Project occupied before launch') for mode in ('Normal','Resume','FinalResume')])
test('R2-08-all-not-run',not_run,lambda c,s:c!=0 and s['started']==0 and s['departed']==0 and s['notStarted']==1 and s['extractionSuccessRate'] is None,'NOT_RUN notes are not execution')
def registered_only(w,p,c,f,m):not_run(w,p,c,f,m,True);write(w/'matrix/results.json',[])
for name,fn in [('registration-only',registered_only),('registration-not-run',lambda w,p,c,f,m:not_run(w,p,c,f,m,True))]:
 test('R2-09-'+name,fn,lambda c,s:c!=0 and s.get('registered')==1 and s['started']==0 and s['departed']==0 and s['notStarted']==1,'Registration is retained independently of launch')
def missing_metrics(w,p,c,f,m):
 (f/'stage2-metrics.json').unlink();txwrite(f,[txread(f)[0]]);write(w/'matrix/results.json',[dict(name=c['id']+'.Normal',status='FAIL',exitCode=1,timedOut=False)])
test('R2-10-departed-no-metrics',missing_metrics,lambda c,s:reject(c,s) and s['started']==1 and s['departed']==1 and s['unknown']==1 and s['technicalInterrupted']==1,'Actual departed identity retained without inventing terminal')
def conflict(w,p,c,f,m,key,missing=False):
 tx=txread(f)
 if missing:del tx[1][key]
 else:tx[1][key]='another-'+key
 txwrite(f,tx)
for key in ('run','profile','region'):
 for missing in (False,True):
  test('R2-11-'+key+('-missing' if missing else '-conflict'),lambda w,p,c,f,m,key=key,missing=missing:conflict(w,p,c,f,m,key,missing),lambda c,s:reject(c,s) and s['knownTerminal']==0 and s['extracted']==0 and s['unknown']==1 and s['statisticsDiagnosticOnly'] is True,'Invalid terminal identity is not a known extraction')
def two_outcomes(w,p,c,f,m):tx=txread(f);tx.append(dict(tx[1],outcome='Death'));txwrite(f,tx)
test('R2-11-inconsistent-outcomes',two_outcomes,lambda c,s:reject(c,s) and s['knownTerminal']==0 and s['extractionSuccessRate'] is None,'Conflicting outcomes cannot overwrite one another')
def later_valid(w,p,c,f,m):conflict(w,p,c,f,m,'run');write(f/'b4-first-settlement.json',dict(runId=m['run'],outcome=0))
test('R2-11-later-file-no-override',later_valid,lambda c,s:reject(c,s) and s['knownTerminal']==0,'Later valid file does not erase earlier conflict')
def wrong_settlement(w,p,c,f,m):write(f/'b4-first-settlement.json',dict(runId='other-run',outcome=0))
test('R2-11-settlement-conflict',wrong_settlement,lambda c,s:reject(c,s) and s['knownTerminal']==0,'Independent settlement cannot belong to another Run')
def snapshot_no_outcome(w,p,c,f,m,backing=True,explicit_null=False):
 tx=txread(f)
 if explicit_null:tx[1]['outcome']=None
 else:del tx[1]['outcome']
 txwrite(f,tx)
 if backing:write(f/'b4-first-settlement.json',dict(runId=m['run'],outcome=0))
test('R2-15-real-snapshot-outcome-source',snapshot_no_outcome,lambda c,s:c==0 and s['knownTerminal']==1,'Real old Snapshot omitted outcome; actual matching settlement supplies it, never metric inference')
test('R2-11-explicit-null-no-override',lambda w,p,c,f,m:snapshot_no_outcome(w,p,c,f,m,True,True),lambda c,s:reject(c,s) and s['knownTerminal']==0,'Explicit null is invalid, not legacy omission or last-file repair')
test('R2-11-missing-outcome-no-source',lambda w,p,c,f,m:snapshot_no_outcome(w,p,c,f,m,False),lambda c,s:reject(c,s) and s['knownTerminal']==0,'Absent outcome without independent source stays unknown')
def late_failure(w,p,c,f,m):write(f/'process-result-Resume.json',dict(mode='Resume',exitCode=1,timedOut=False))
test('R2-12-trusted-terminal-late-failure',late_failure,lambda c,s:reject(c,s) and s['knownTerminal']==1 and s['extracted']==1 and s['technicalInterrupted']==1 and s['statisticsDiagnosticOnly'] is True and s['groupsDescriptiveOnly']['Safety']['elapsedSeconds']['n']==0,'Confirmed terminal kept despite later tool failure; complete statistics excluded')
def partial(w,p,c,f,m):
 c2,f2,m2=fixture(w,'two');p['cases'].append(c2);patch_metric(f2,m2,status='FAIL',elapsedSeconds=2,extracted=False);txwrite(f2,[txread(f2)[0]]);write(f2/'process-result-Normal.json',dict(mode='Normal',exitCode=1,timedOut=False))
test('R2-13-complete-plus-partial',partial,lambda c,s:reject(c,s) and s['groupsDescriptiveOnly']['Safety']['elapsedSeconds']['mean']==60 and s['groupsDescriptiveOnly']['Safety']['elapsedSeconds']['n']==1 and s['partialWindows'][0]['elapsedSeconds']==2 and s['statisticsDiagnosticOnly'] is True,'Only complete windows enter 60-second mean')
write(a.output/'results.json',dict(scope='Finite offline synthetic assertion matrix; not gameplay PASS or supplied ZIP execution',source=[dict(file=n,sha256=hashlib.sha256((source/n).read_bytes()).hexdigest()) for n in ('MatrixEvidence.py','Summarize-Matrix.py')],fixtureSourceSha256=hashlib.sha256(original.read_bytes()).hexdigest(),results=results))
print(json.dumps(dict(PASS=sum(r['status']=='PASS' for r in results),FAIL=sum(r['status']=='FAIL' for r in results),cases=len(results),failed=[r['name'] for r in results if r['status']=='FAIL'])));raise SystemExit(1 if any(r['status']=='FAIL' for r in results) else 0)
