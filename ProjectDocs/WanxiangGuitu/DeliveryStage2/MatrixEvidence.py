"""Evidence-only matrix audit. Never opens player saves or modifies source evidence."""
import collections,hashlib,json,math,statistics
from pathlib import Path
MODES=('Normal','Resume','FinalResume');CORE=('id','build','strategy','seed','weapon','target')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def text(x):return isinstance(x,str) and bool(x.strip())
def number(x):return type(x) in (int,float) and math.isfinite(x) and x>=0
def stats(xs):return dict(n=len(xs),mean=statistics.mean(xs) if xs else None,stdev=statistics.stdev(xs) if len(xs)>1 else None,sampleInsufficient=len(xs)<2)
def snapshot(root):
 return {p.relative_to(root).as_posix():digest(p) for p in root.rglob('*') if p.is_file() and p.suffix in ('.json','.jsonl','.txt') and not any(x in ('WanxiangGuitu','Project','Library','Worker','Deferred') for x in p.relative_to(root).parts)}
def summarize(root,plan,legacy=False):
 initial=snapshot(root);errors=[];rows=[];cases=plan.get('cases');seen_case=set();seen_attempt=set();seen_run=set();seen_successor=set()
 if not isinstance(cases,list) or not cases:errors.append('plan.cases: nonempty array required');cases=[]
 ended=root/'preserved-processes.json'
 if not ended.exists():errors.append('preserved-processes.json: finalization receipt missing; evidence may still be running')
 else:
  try:
   if read(ended)!=[]:errors.append('preserved-processes.json: live/preserved processes; final acceptance refused')
  except (ValueError,OSError):errors.append('preserved-processes.json: unreadable finalization receipt')
 try:
  steps=read(root/'results.json');steps=steps if isinstance(steps,list) else [steps]
 except (ValueError,OSError):steps=[];errors.append('results.json: missing/unreadable process ledger')
 for case in cases:
  issues=[];warnings=[];files=[];d={};tx=[];attempt={};source_runs=[];outcome='Unknown'
  if not isinstance(case,dict) or not text(case.get('id')) or any(k not in case for k in CORE):errors.append('plan case: invalid structure');continue
  ident=case['id'];folder=root/ident
  if Path(ident).name!=ident or ident in ('.','..') or not folder.resolve().is_relative_to(root):errors.append('plan case: unsafe id '+ident);continue
  if type(case.get('seed')) is not int or case['seed']<=0 or type(case.get('weapon')) is not int or not 0<=case['weapon']<=3 or type(case.get('target')) is not int or case.get('build') not in ('Safety','Gather','Boss'):errors.append('plan case: invalid field types/ranges '+ident)
  if ident in seen_case:errors.append('duplicate caseId: '+ident)
  seen_case.add(ident)
  def load(name,required=False):
   p=folder/name
   if not p.exists():
    if required:issues.append(name+': missing')
    return None
   files.append(dict(path=p.relative_to(root).as_posix(),sha256=digest(p)))
   try:return read(p)
   except (ValueError,OSError) as e:issues.append(name+': invalid JSON '+str(e));return None
  relevant=[x for x in steps if isinstance(x,dict) and x.get('name','').startswith(ident+'.')]
  tp=folder/'stage2-transactions.jsonl'
  if tp.exists():
   files.append(dict(path=tp.relative_to(root).as_posix(),sha256=digest(tp)))
   try:tx=[json.loads(line) for line in tp.read_text(encoding='utf-8-sig').splitlines() if line.strip()]
   except (ValueError,OSError) as e:issues.append('stage2-transactions.jsonl: invalid '+str(e))
  raw=load('stage2-metrics.json');d=raw if isinstance(raw,dict) else {}
  if raw is not None and not isinstance(raw,dict):issues.append('stage2-metrics.json: object required')
  attempt=load('attempt.json') or {}
  if not isinstance(attempt,dict):issues.append('attempt.json: object required');attempt={}
  departures=[x for x in tx if isinstance(x,dict) and x.get('label')=='depart']
  started=bool(departures or relevant or text(attempt.get('launchedUtc')) or d)
  departed=bool(departures or text(d.get('run')))
  technical=any(x.get('status')=='FAIL' for x in relevant)
  modes=case.get('requiredModes',list(MODES))
  if not isinstance(modes,list) or not modes or len(set(modes))!=len(modes) or any(m not in MODES for m in modes):issues.append('plan.requiredModes: invalid');modes=list(MODES)
  if started:
   if not d:issues.append('stage2-metrics.json: final metrics missing/unreadable')
   input_data=load('stage2-input.json',True)
   if not isinstance(input_data,dict) or any(type(input_data.get(k)) is not type(case.get(k)) or input_data.get(k)!=case.get(k) for k in CORE):issues.append('stage2-input.json: configuration mismatch')
   if not isinstance(d.get('input'),dict) or any(type(d['input'].get(k)) is not type(case.get(k)) or d['input'].get(k)!=case.get(k) for k in CORE):issues.append('stage2-metrics.json.input: configuration mismatch')
   if not legacy:
    for field in ('attemptId','blockId','configSha256','codeInput','driverInput','caseId'):
     if not text(attempt.get(field)):issues.append('attempt.json.'+field+': missing/empty identity')
    identity=plan.get('inputIdentity')
    if not isinstance(identity,dict) or any(not text(identity.get(k)) or attempt.get(k)!=identity.get(k) for k in ('codeInput','driverInput')):issues.append('attempt.json: code/driver differs from frozen plan inputIdentity')
    if attempt.get('schemaVersion')!=2 or attempt.get('caseId')!=ident:issues.append('attempt.json: schema/case mismatch')
    cfg=folder/'stage2-input.json'
    if cfg.exists() and attempt.get('configSha256')!=digest(cfg):issues.append('attempt.json.configSha256: input hash mismatch')
    aid=attempt.get('attemptId')
    if text(aid):
     if aid in seen_attempt:issues.append('attempt.json.attemptId: duplicate '+aid)
     seen_attempt.add(aid)
   else:warnings.append('LEGACY_PROJECTION: no actual attemptId/blockId/hash stage schema recorded; only existing config/transactions/checkpoints/process receipts are audited, never backfilled')
   for field in ('profile','run','region'):
    if not text(d.get(field)):issues.append('stage2-metrics.json.'+field+': missing/empty identity')
   for field in ('extracted','committed','acknowledged','secondForest'):
    if type(d.get(field)) is not bool:issues.append('stage2-metrics.json.'+field+': bool required')
   for field in ('elapsedSeconds','damageTaken','potionsUsed','meters'):
    if not number(d.get(field)):issues.append('stage2-metrics.json.'+field+': finite nonnegative number required')
   for field in ('obtained','kept'):
    v=d.get(field)
    if not isinstance(v,list) or len(v)!=6 or any(type(x) is not int or x<0 for x in v):issues.append('stage2-metrics.json.'+field+': six nonnegative integer quantities required')
   if not departures:issues.append('stage2-transactions.jsonl: actual depart evidence missing')
   for event in departures:
    for k in ('run','profile','region'):
     if not text(event.get(k)) or event.get(k)!=d.get(k):issues.append('depart.'+k+': conflicts with metrics or missing')
   run=d.get('run') or next((x.get('run') for x in departures if text(x.get('run'))),None)
   if text(run):
    if run in seen_run:issues.append('run: reused across cases '+run)
    seen_run.add(run)
   for event in tx:
    if not isinstance(event,dict):issues.append('transaction: object required');continue
    if event.get('profile') and d.get('profile') and event['profile']!=d['profile']:issues.append('transaction.profile: identity conflict')
    if event.get('label')=='settlement-pending' and event.get('outcome') in ('Extracted','Death','Abandoned','TestChallengeComplete'):outcome=event['outcome']
   pending_events=[x for x in tx if isinstance(x,dict) and x.get('label')=='settlement-pending']
   if any(x.get('run')!=run for x in pending_events):issues.append('settlement-pending.run: conflicts with first Run')
   if len({x.get('outcome') for x in pending_events if x.get('outcome')})>1:issues.append('multiple conflicting terminal outcomes for same Run')
   committed_evidence=any(isinstance(x,dict) and x.get('settlementStatus')=='Committed' for x in tx)
   terminal_receipts=[x for x in tx if isinstance(x,dict) and x.get('label') in ('settlement-pending','acknowledged')]
   if any(x.get('profile')!=d.get('profile') or (text(x.get('run')) and x['run']!=run) or (text(x.get('region')) and x['region']!=d.get('region')) for x in terminal_receipts):issues.append('terminal receipt: run/profile/region identity mismatch')
   ack_evidence=any(isinstance(x,dict) and x.get('label')=='acknowledged' and x.get('ack') is True for x in tx)
   second_evidence=any(isinstance(x,dict) and x.get('label')=='verified-new-process-second-forest' for x in tx)
   for flag,evidence in (('committed',committed_evidence),('acknowledged',ack_evidence),('secondForest',second_evidence)):
    if type(d.get(flag)) is bool and d[flag]!=evidence:issues.append('metrics.'+flag+': conflicts with actual lifecycle transactions')
   settled=load('b4-first-settlement.json')
   if isinstance(settled,dict):
    mapping={0:'Extracted',1:'Death',2:'Abandoned',3:'TestChallengeComplete'};observed=mapping.get(settled.get('outcome'),'Unknown')
    if settled.get('runId')!=run:issues.append('b4-first-settlement.json.runId: mismatch')
    if outcome!='Unknown' and outcome!=observed:issues.append('terminal evidence conflicts')
    outcome=observed
   for mode in modes:
    proc=load('process-result-'+mode+'.json',True)
    if not isinstance(proc,dict):technical=True;continue
    if proc.get('mode')!=mode or type(proc.get('exitCode')) is not int or type(proc.get('timedOut')) is not bool:issues.append('process-result-'+mode+'.json: invalid mode/exit/timeout types');technical=True
    if proc.get('exitCode')!=0 or proc.get('timedOut') is not False:issues.append('process-result-'+mode+'.json: nonzero/timeout');technical=True
    if not legacy:
     stage=load('stage-result-'+mode+'.json',True)
     if not isinstance(stage,dict):continue
     for key in ('attemptId','caseId','configSha256','codeInput','driverInput'):
      if stage.get(key)!=attempt.get(key):issues.append('stage-result-'+mode+'.'+key+': identity/input conflict')
     if stage.get('mode')!=mode or stage.get('complete') is not True or stage.get('profile')!=d.get('profile') or stage.get('firstRun')!=run:issues.append('stage-result-'+mode+': invalid completion/identity')
     expected_stage=1 if mode=='Normal' else 2;expected_run=run if mode=='Normal' else d.get('secondRun')
     if type(stage.get('stage')) is not int or stage['stage']!=expected_stage or stage.get('run')!=expected_run:issues.append('stage-result-'+mode+': stage/run mismatch')
   if (folder/'validation-interruption.json').exists():issues.append('validation-interruption.json: explicit interruption');technical=True
   contract=case.get('contract','economy');expected=case.get('expectedOutcome','Extracted')
   if contract not in ('economy','terminal') or expected not in ('Extracted','Death','Abandoned','TestChallengeComplete'):issues.append('plan.contract/expectedOutcome: unsupported explicit contract')
   accepted=case.get('acceptedOutcomes',[expected])
   if not isinstance(accepted,list) or not accepted or any(x not in ('Extracted','Death','Abandoned','TestChallengeComplete') for x in accepted):issues.append('plan.acceptedOutcomes: invalid explicit outcomes');accepted=[expected]
   if outcome not in accepted:issues.append('terminal outcome: '+outcome+' does not satisfy '+str(accepted))
   if type(d.get('extracted')) is bool and outcome!='Unknown' and d['extracted']!=(outcome=='Extracted'):issues.append('metrics.extracted: contradicts actual terminal')
   if contract=='economy':
    for field in ('extracted','committed','acknowledged','secondForest'):
     if d.get(field) is not True:issues.append('economy.'+field+': completion not true')
    for field in ('secondRun','secondRegion'):
     if not text(d.get(field)):issues.append(field+': missing successor identity')
    if d.get('secondRun')==run or d.get('secondRegion')==d.get('region'):issues.append('successor equals first Run/region')
    successor=d.get('secondRun')
    if text(successor):
     if successor in seen_successor:issues.append('successor: reused across cases '+successor)
     seen_successor.add(successor)
    ack=[x for x in tx if isinstance(x,dict) and x.get('label')=='acknowledged']
    if not any(x.get('ack') is True and x.get('settlementStatus')=='Committed' for x in ack):issues.append('acknowledged: actual committed/ACK transaction absent')
    if not any(x.get('label')=='verified-new-process-second-forest' and x.get('run')==d.get('secondRun') and x.get('region')==d.get('secondRegion') for x in tx if isinstance(x,dict)):issues.append('successor: actual new-process transaction absent')
    if legacy:
     cp1=load('b4-checkpoint-1.json',True);cp2=load('b4-checkpoint-2.json',True)
     for cp,expected_run in ((cp1,run),(cp2,d.get('secondRun'))):
      if not isinstance(cp,dict) or cp.get('profile')!=d.get('profile') or cp.get('run')!=expected_run or cp.get('firstRun')!=run:issues.append('legacy checkpoint: identity conflict/missing')
     marks=folder/'normal-results.txt';lines=marks.read_text(encoding='utf-8-sig') if marks.exists() else ''
     for marker in ('NEW_PROCESS_FULL_STATE_PASS stage=1','NEW_PROCESS_FULL_STATE_PASS stage=2','ALL_PASS'):
      if marker not in lines:issues.append('legacy process stage assertion missing: '+marker)
   if d.get('status')!='PASS':issues.append('metrics.status: not completed PASS')
  else:run=None
  complete=started and not issues and not technical
  completeness='complete' if complete else 'missing' if not d else 'conflict' if issues and d.get('status')=='PASS' else 'partial'
  row=dict(d);row.update(input=case,status='PASS' if complete else 'FAIL' if started else 'NOT_RUN',attemptId=attempt.get('attemptId'),blockId=attempt.get('blockId'),started=started,departed=departed,run=run,businessOutcome=outcome,technicalInterrupted=technical,measurementCompleteness=completeness,issues=issues,warnings=warnings,evidence=files,legacyProjection=legacy)
  if d and number(d.get('elapsedSeconds')):row['partialWindowSeconds']=d['elapsedSeconds'] if not complete else None
  if complete:
   row['materialRetentionByKind']=[None if n==0 else d['kept'][i]/n for i,n in enumerate(d['obtained'])]
   if all(isinstance(d.get(k),list) and len(d[k])==6 for k in ('assetsStart','assetsEnd')):
    row['materialNetAfterCampGrowth']=[n-d['assetsStart'][i] for i,n in enumerate(d['assetsEnd'])];row['netPerFirstRunSimulationSecondAfterCampGrowthByKind']=[n/d['elapsedSeconds'] for n in row['materialNetAfterCampGrowth']] if d['elapsedSeconds']>0 else None
  rows.append(row)
 final=snapshot(root)
 if final!=initial:errors.append('evidence inputs changed during audit; final acceptance refused')
 full=[r for r in rows if r['measurementCompleteness']=='complete'];known=[r for r in rows if r['businessOutcome']!='Unknown'];extract=[r for r in known if r['businessOutcome']=='Extracted'];started=[r for r in rows if r['started']];departed=[r for r in rows if r['departed']]
 def grouped(sample):
  return {build:{k:stats([r[k] for r in sample if r["input"]["build"]==build and number(r.get(k))]) for k in ('elapsedSeconds','damageTaken','potionsUsed','meters')} for build in ('Safety','Gather','Boss')}
 status='FAIL' if errors or any(r['status']=='FAIL' for r in rows) else 'PASS' if rows and len(full)==len(rows) else 'NOT_RUN'
 return dict(materials=['MonsterHide','CrystalShard','BossCore','Wood','Stone','Ore'],valuation='Quantity vectors only; post-camp-growth net / first-Run simulation seconds is not whole-cycle per-minute income.',finalAcceptanceEligible=status=='PASS',statisticsDiagnosticOnly=bool(errors),status=status,scope='Evidence audit only; no native/human acceptance. Legacy mode is an explicit read-only re-audit projection, not backfilled source.',planned=len(cases),started=len(started),departed=len(departed),knownTerminal=len(known),extracted=len(extract),died=sum(r['businessOutcome']=='Death' for r in known),abandoned=sum(r['businessOutcome']=='Abandoned' for r in known),technicalInterrupted=sum(r['technicalInterrupted'] for r in rows),unknown=sum(r['businessOutcome']=='Unknown' for r in started),notStarted=sum(not r['started'] for r in rows),validSorties=len(departed),counts=dict(collections.Counter(r['status'] for r in rows)),extractionSuccessRate=len(extract)/len(known) if known else None,extractionRateDenominator='knownTerminal ONLY; publish unknown and technicalInterrupted alongside; no inference of death',groupsDescriptiveOnly=grouped(full),completeTerminalStatistics=grouped(full),successfulExtractionStatistics=grouped([r for r in full if r['businessOutcome']=='Extracted']),deathStatistics=grouped([r for r in full if r['businessOutcome']=='Death']),abandonedStatistics=grouped([r for r in full if r['businessOutcome']=='Abandoned']),partialWindows=[dict(caseId=r['input']['id'],elapsedSeconds=r.get('partialWindowSeconds'),completeness=r['measurementCompleteness'],issues=r['issues']) for r in rows if r['started'] and r['measurementCompleteness']!='complete'],groupsMeaning='Complete windows only; per-condition n remains explicit, no broad balance inference. Partial windows never pooled with complete ones.',globalIssues=errors,rows=rows,inputManifest=initial,inputManifestAfter=final,nativeUI='NOT_RUN',independentHumanFourWeapons='NOT_RUN')
