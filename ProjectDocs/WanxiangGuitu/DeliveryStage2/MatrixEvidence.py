"""Evidence-only matrix audit. Preserves inputs; hashes files only within the explicit owned synthetic root."""
import collections,hashlib,json,math,statistics
from pathlib import Path
MODES=('Normal','Resume','FinalResume');CORE=('id','build','strategy','seed','weapon','target')
OUTCOMES=('Extracted','Death','Abandoned','TestChallengeComplete')
CONTRACT_VERSION=1
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def text(x):return isinstance(x,str) and bool(x.strip())
def number(x):return type(x) in (int,float) and math.isfinite(x) and x>=0
def stats(xs):return dict(n=len(xs),mean=statistics.mean(xs) if xs else None,stdev=statistics.stdev(xs) if len(xs)>1 else None,sampleInsufficient=len(xs)<2)
def case_contract(data,path,issues):
 """Versioned acceptance semantics only; never backfill or rewrite source JSON/hash."""
 if not isinstance(data,dict):issues.append(path+': case object required');return None
 version=data.get('contractVersion',CONTRACT_VERSION);kind=data.get('contract','economy');expected=data.get('expectedOutcome','Extracted')
 if type(version) is not int or version!=CONTRACT_VERSION:issues.append(path+'.contractVersion: unsupported normalization version');return None
 if type(kind) is not str or kind not in ('economy','terminal'):issues.append(path+'.contract: unsupported');return None
 if type(expected) is not str or expected not in OUTCOMES:issues.append(path+'.expectedOutcome: invalid');return None
 accepted=data.get('acceptedOutcomes',[expected]);modes=data.get('requiredModes',list(MODES) if kind=='economy' else ['Normal'])
 if not isinstance(accepted,list) or not accepted or any(type(x) is not str or x not in OUTCOMES for x in accepted) or len(set(accepted))!=len(accepted):issues.append(path+'.acceptedOutcomes: nonempty unique outcome array required');return None
 if not isinstance(modes,list) or not modes or any(type(x) is not str or x not in MODES for x in modes) or len(set(modes))!=len(modes):issues.append(path+'.requiredModes: nonempty unique stage array required');return None
 if expected not in accepted:issues.append(path+'.expectedOutcome: must belong to acceptedOutcomes')
 for key in ('kind','blockId'):
  if key in data and not text(data[key]):issues.append(path+'.'+key+': nonempty condition identity required when recorded')
 if kind=='economy' and (set(modes)!=set(MODES) or expected!='Extracted' or accepted!=['Extracted']):issues.append(path+': economy requires Extracted and all three independent stages')
 if kind=='terminal' and 'Normal' not in modes:issues.append(path+'.requiredModes: terminal must include Normal')
 return dict(contractVersion=version,contract=kind,expectedOutcome=expected,acceptedOutcomes=sorted(accepted),requiredModes=[x for x in MODES if x in modes],kind=data.get('kind'),blockId=data.get('blockId'))

def terminal_result(tx,settled,settled_present,departures,metric,issues):
 """A failed successor may keep a trusted first outcome; identity conflicts may not."""
 problems=[];claims=[];identities=[]
 for event in departures:
  identity={k:event.get(k) for k in ('run','profile','region')}
  if all(text(v) for v in identity.values()):identities.append(identity)
  else:problems.append('depart: complete recorded run/profile/region required for terminal attribution')
 anchor=identities[0] if identities else None
 if any(x!=anchor for x in identities):problems.append('depart: conflicting Run identities')
 if anchor and any(text(metric.get(k)) and metric[k]!=anchor[k] for k in anchor):problems.append('metrics/depart: conflicting Run identity')
 pending=[x for x in tx if isinstance(x,dict) and x.get('label')=='settlement-pending']
 for i,event in enumerate(pending):
  path='stage2-transactions.jsonl/settlement-pending['+str(i)+']';value=event.get('outcome');claims.append(dict(source=path,outcome=value,outcomeRecorded='outcome' in event,identity={k:event.get(k) for k in ('run','profile','region')}))
  for k in ('run','profile','region'):
   if not anchor or not text(event.get(k)) or event[k]!=anchor[k]:problems.append(path+'.'+k+': terminal identity missing/conflicting')
  # The real Stage2 Snapshot class never recorded outcome; its independent
  # b4-first-settlement record supplies it. Absence is not an invented value.
  # Explicit null/invalid values remain conflicts, even if another file is valid.
  if 'outcome' in event and (type(value) is not str or value not in OUTCOMES):problems.append(path+'.outcome: invalid')
 for i,event in enumerate(x for x in tx if isinstance(x,dict) and x.get('label')=='acknowledged'):
  if not anchor or event.get('profile')!=anchor['profile'] or any(text(event.get(k)) and event[k]!=anchor[k] for k in ('run','region')):problems.append('acknowledged['+str(i)+']: terminal identity conflicting')
 if settled_present:
  if not isinstance(settled,dict):problems.append('b4-first-settlement.json: settlement object required')
  else:
   value=OUTCOMES[settled['outcome']] if type(settled.get('outcome')) is int and 0<=settled['outcome']<len(OUTCOMES) else None
   claims.append(dict(source='b4-first-settlement.json',outcome=value,identity=dict(run=settled.get('runId'))))
   if not anchor or settled.get('runId')!=anchor['run']:problems.append('b4-first-settlement.json.runId: terminal identity conflicting')
   if value is None:problems.append('b4-first-settlement.json.outcome: invalid')
 values={x['outcome'] for x in claims if type(x['outcome']) is str and x['outcome'] in OUTCOMES}
 if len(values)>1:problems.append('terminal evidence: conflicting outcomes; no last-file override')
 if claims and not anchor:problems.append('terminal evidence: no complete independent depart identity')
 # A partial metric cannot erase independent evidence, nor can later evidence
 # silently repair an already conflicting terminal identity/outcome.
 confirmed=bool(claims and anchor and len(values)==1 and not problems)
 if claims:issues.extend(problems)
 return dict(businessOutcome=next(iter(values)) if confirmed else 'Unknown',declaredTerminalEvidence=claims,terminalIdentityConfirmed=confirmed,terminalConflict=bool(claims and problems),terminalIssues=problems if claims else [],trustedRunIdentity=anchor)

def snapshot(root):
 return {p.relative_to(root).as_posix():digest(p) for p in root.rglob('*') if p.is_file() and p.suffix in ('.json','.jsonl','.txt') and not any(x in ('WanxiangGuitu','Project','Library','Worker','Deferred') for x in p.relative_to(root).parts)}
def summarize(root,plan,legacy=False):
 initial=snapshot(root);errors=[];rows=[];seen_case=set();seen_attempt=set();seen_run=set();seen_successor=set()
 if not isinstance(plan,dict):errors.append('plan: root object required');plan={}
 cases=plan.get('cases')
 if not isinstance(cases,list) or not cases:errors.append('plan.cases: nonempty array required');cases=[]
 ended=root/'preserved-processes.json'
 if not ended.exists():errors.append('preserved-processes.json: finalization receipt missing; evidence may still be running')
 else:
  try:
   if read(ended)!=[]:errors.append('preserved-processes.json: live/preserved processes; final acceptance refused')
  except (ValueError,OSError):errors.append('preserved-processes.json: unreadable finalization receipt')
 try:
  steps=read(root/'results.json')
  if isinstance(steps,dict):steps=[steps]
  elif not isinstance(steps,list):errors.append('results.json: result array/object required');steps=[]
  if any(not isinstance(x,dict) or not text(x.get('name')) for x in steps):errors.append('results.json: result rows require objects and names')
 except (ValueError,OSError):steps=[];errors.append('results.json: missing/unreadable process ledger')
 for case in cases:
  issues=[];warnings=[];files=[];d={};tx=[];attempt={};outcome='Unknown'
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
  def object_file(name,required=False):
   value=load(name,required)
   if not isinstance(value,dict):
    if required or (folder/name).exists():issues.append(name+': root object required; got '+type(value).__name__)
    return None
   return value
  relevant=[x for x in steps if isinstance(x,dict) and text(x.get('name')) and x['name'].startswith(ident+'.')]
  tp=folder/'stage2-transactions.jsonl'
  if tp.exists():
   files.append(dict(path=tp.relative_to(root).as_posix(),sha256=digest(tp)))
   try:tx=[json.loads(line) for line in tp.read_text(encoding='utf-8-sig').splitlines() if line.strip()]
   except (ValueError,OSError) as e:issues.append('stage2-transactions.jsonl: invalid '+str(e))
  raw=load('stage2-metrics.json');d=raw if isinstance(raw,dict) else {}
  if raw is not None and not isinstance(raw,dict):issues.append('stage2-metrics.json: object required')
  attempt=object_file('attempt.json') or {}
  sidecar=root/(ident+'.attempt.json')
  if sidecar.exists():
   files.append(dict(path=sidecar.relative_to(root).as_posix(),sha256=digest(sidecar)))
   try:
    registration=read(sidecar)
    if not isinstance(registration,dict):issues.append(sidecar.name+': root object required')
    elif attempt and registration!=attempt:issues.append(sidecar.name+': registration conflicts with copied attempt')
    elif not attempt:attempt=registration
   except (ValueError,OSError) as e:issues.append(sidecar.name+': invalid JSON '+str(e))
  registered=text(attempt.get('attemptId'))
  departures=[x for x in tx if isinstance(x,dict) and x.get('label')=='depart']
  process_evidence=[]
  for mode in MODES:
   path=folder/('process-result-'+mode+'.json')
   if path.exists():
    try:
     receipt=read(path)
     if isinstance(receipt,dict) and receipt.get('mode')==mode and (type(receipt.get('exitCode')) is int or receipt.get('timedOut') is True):process_evidence.append(path.name)
    except (ValueError,OSError):pass # Required-object validation below records the real path/error.
  launch_steps=[x for x in relevant if x.get('status')!='NOT_RUN' and (type(x.get('exitCode')) is int or x.get('timedOut') is True)]
  started=bool(departures or launch_steps or process_evidence or d)
  departed=any(all(text(x.get(k)) for k in ('run','profile','region')) for x in departures)
  technical=any(x.get('status')=='FAIL' for x in relevant)
  declared_contract=case_contract(case,'plan.case['+ident+']',issues);frozen_contract=None
  terminal=dict(businessOutcome='Unknown',declaredTerminalEvidence=[],terminalIdentityConfirmed=False,terminalConflict=False,terminalIssues=[],trustedRunIdentity=None)
  if started:
   if not d:issues.append('stage2-metrics.json: final metrics missing/unreadable')
   input_data=load('stage2-input.json',True)
   if not isinstance(input_data,dict) or any(type(input_data.get(k)) is not type(case.get(k)) or input_data.get(k)!=case.get(k) for k in CORE):issues.append('stage2-input.json: configuration mismatch')
   if not isinstance(d.get('input'),dict) or any(type(d['input'].get(k)) is not type(case.get(k)) or d['input'].get(k)!=case.get(k) for k in CORE):issues.append('stage2-metrics.json.input: configuration mismatch')
   frozen_contract=case_contract(input_data,'stage2-input.json',issues);metric_contract=case_contract(d.get('input'),'stage2-metrics.json.input',issues)
   if declared_contract!=frozen_contract:issues.append('plan.case['+ident+']: acceptance contract differs from frozen stage2-input.json')
   if metric_contract!=frozen_contract:issues.append('stage2-metrics.json.input: acceptance contract differs from frozen stage2-input.json')
   effective=frozen_contract or declared_contract
   modes=list(MODES) if not effective or effective['contract']=='economy' else effective['requiredModes']
   if not legacy:
    for field in ('attemptId','blockId','configSha256','codeInput','driverInput','caseId'):
     if not text(attempt.get(field)):issues.append('attempt.json.'+field+': missing/empty identity')
    identity=plan.get('inputIdentity')
    if not isinstance(identity,dict) or any(not text(identity.get(k)) or attempt.get(k)!=identity.get(k) for k in ('codeInput','driverInput')):issues.append('attempt.json: code/driver differs from frozen plan inputIdentity')
    if attempt.get('schemaVersion')!=2 or attempt.get('caseId')!=ident:issues.append('attempt.json: schema/case mismatch')
    if frozen_contract and frozen_contract['blockId'] is not None and attempt.get('blockId')!=frozen_contract['blockId']:issues.append('attempt.json.blockId: differs from frozen case condition')
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
   settled=object_file('b4-first-settlement.json')
   terminal=terminal_result(tx,settled,(folder/'b4-first-settlement.json').exists(),departures,d,issues);outcome=terminal['businessOutcome']
   for mode in modes:
    proc=object_file('process-result-'+mode+'.json',True)
    if proc is None:technical=True
    else:
     if proc.get('mode')!=mode or type(proc.get('exitCode')) is not int or type(proc.get('timedOut')) is not bool:issues.append('process-result-'+mode+'.json: invalid mode/exit/timeout types');technical=True
     if proc.get('exitCode')!=0 or proc.get('timedOut') is not False:issues.append('process-result-'+mode+'.json: nonzero/timeout');technical=True
    if not legacy:
     stage=object_file('stage-result-'+mode+'.json',True)
     if not isinstance(stage,dict):continue
     for key in ('attemptId','caseId','blockId','configSha256','codeInput','driverInput'):
      if stage.get(key)!=attempt.get(key):issues.append('stage-result-'+mode+'.json.'+key+': identity/input conflict')
     if type(stage.get('schemaVersion')) is not int or stage['schemaVersion']!=2:issues.append('stage-result-'+mode+'.json.schemaVersion: unsupported/missing')
     if stage.get('mode')!=mode or stage.get('complete') is not True or stage.get('profile')!=d.get('profile') or stage.get('firstRun')!=run:issues.append('stage-result-'+mode+'.json: invalid completion/identity')
     expected_stage=1 if mode=='Normal' else 2;expected_run=run if mode=='Normal' else d.get('secondRun')
     if type(stage.get('stage')) is not int or stage['stage']!=expected_stage or stage.get('run')!=expected_run:issues.append('stage-result-'+mode+'.json: stage/run mismatch')
   if (folder/'validation-interruption.json').exists():issues.append('validation-interruption.json: explicit interruption');technical=True
   contract=effective['contract'] if effective else 'economy';accepted=effective['acceptedOutcomes'] if effective else ['Extracted']
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
  row=dict(d);row.update(input=case,status='PASS' if complete else 'FAIL' if started or issues or technical else 'NOT_RUN',attemptId=attempt.get('attemptId'),blockId=attempt.get('blockId'),registered=registered,registrationTimestampSource=attempt.get('launchedUtc'),registrationTimestampMeaning='Original pre-launch registration field; never sufficient proof of actual launch',launchEvidence=dict(processReceipts=process_evidence,executedSteps=[x.get('name') for x in launch_steps],departTransactions=len(departures),metricsObject=bool(d)),started=started,departed=departed,run=run,technicalInterrupted=technical,measurementCompleteness=completeness,normalizedContract=frozen_contract or declared_contract,issues=issues,warnings=warnings,evidence=files,legacyProjection=legacy,**terminal)
  if d and number(d.get('elapsedSeconds')):row['partialWindowSeconds']=d['elapsedSeconds'] if not complete else None
  if complete:
   row['materialRetentionByKind']=[None if n==0 else d['kept'][i]/n for i,n in enumerate(d['obtained'])]
   if all(isinstance(d.get(k),list) and len(d[k])==6 for k in ('assetsStart','assetsEnd')):
    row['materialNetAfterCampGrowth']=[n-d['assetsStart'][i] for i,n in enumerate(d['assetsEnd'])];row['netPerFirstRunSimulationSecondAfterCampGrowthByKind']=[n/d['elapsedSeconds'] for n in row['materialNetAfterCampGrowth']] if d['elapsedSeconds']>0 else None
  rows.append(row)
 final=snapshot(root)
 if final!=initial:errors.append('evidence inputs changed during audit; final acceptance refused')
 full=[r for r in rows if r['measurementCompleteness']=='complete'];known=[r for r in rows if r['started'] and r['terminalIdentityConfirmed'] and r['businessOutcome']!='Unknown'];extract=[r for r in known if r['businessOutcome']=='Extracted'];started=[r for r in rows if r['started']];departed=[r for r in rows if r['departed']]
 def grouped(sample):
  return {build:{k:stats([r[k] for r in sample if r["input"]["build"]==build and number(r.get(k))]) for k in ('elapsedSeconds','damageTaken','potionsUsed','meters')} for build in ('Safety','Gather','Boss')}
 status='FAIL' if errors or any(r['status']=='FAIL' for r in rows) else 'PASS' if rows and len(full)==len(rows) else 'NOT_RUN'
 return dict(contractNormalizationVersion=CONTRACT_VERSION,materials=['MonsterHide','CrystalShard','BossCore','Wood','Stone','Ore'],valuation='Quantity vectors only; post-camp-growth net / first-Run simulation seconds is not whole-cycle per-minute income.',finalAcceptanceEligible=status=='PASS',statisticsDiagnosticOnly=bool(errors or any(r['issues'] or r['technicalInterrupted'] for r in rows)),status=status,scope='Evidence audit only; no native/human acceptance. Legacy mode is an explicit read-only re-audit projection, not backfilled source.',planned=len(cases),registered=sum(r['registered'] for r in rows),started=len(started),departed=len(departed),knownTerminal=len(known),terminalConflicts=sum(r['terminalConflict'] for r in rows),extracted=len(extract),died=sum(r['businessOutcome']=='Death' for r in known),abandoned=sum(r['businessOutcome']=='Abandoned' for r in known),technicalInterrupted=sum(r['technicalInterrupted'] for r in rows),unknown=sum(r['businessOutcome']=='Unknown' for r in started),notStarted=sum(not r['started'] for r in rows),validSorties=len(departed),counts=dict(collections.Counter(r['status'] for r in rows)),extractionSuccessRate=len(extract)/len(known) if known else None,extractionRateDenominator='identity-confirmed knownTerminal ONLY; publish unknown, terminalConflicts and technicalInterrupted alongside; no inference of death',groupsDescriptiveOnly=grouped(full),completeTerminalStatistics=grouped(full),successfulExtractionStatistics=grouped([r for r in full if r['businessOutcome']=='Extracted']),deathStatistics=grouped([r for r in full if r['businessOutcome']=='Death']),abandonedStatistics=grouped([r for r in full if r['businessOutcome']=='Abandoned']),partialWindows=[dict(caseId=r['input']['id'],elapsedSeconds=r.get('partialWindowSeconds'),completeness=r['measurementCompleteness'],issues=r['issues']) for r in rows if r['started'] and r['measurementCompleteness']!='complete'],groupsMeaning='Complete windows only; per-condition n remains explicit, no broad balance inference. Partial windows never pooled with complete ones.',globalIssues=errors,rows=rows,inputManifest=initial,inputManifestAfter=final,nativeUI='NOT_RUN',independentHumanFourWeapons='NOT_RUN')
