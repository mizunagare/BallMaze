from pathlib import Path
import json,sys,csv,collections,statistics,hashlib,re
root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(exist_ok=False)
editor=['TwinEditor3','FinalHeavy2','FinalScythe2','FinalBoundary3','PerformanceEditor3','CancelAfter1','StorageEditor3','ResumeEditorData2','BossData1','ChannelControlData2','ChannelNormalData2','ChannelGroundData2','ChannelPickedData2','FinalLegacyExpanded2','LegacyExtraEditor1','LegacyTrainingEditor1','LegacyFormalData2','NearEditor3','UpgradeEditorData1']
player=['PlayerTwin2','PlayerHeavy2','PlayerScythe2','PlayerBoundary2','PlayerPerformance2','PlayerCancel2','PlayerSave2','PlayerResume2','PlayerDrop2','PlayerBoss2','PlayerChannelControl2','PlayerChannelNormal2','PlayerChannelGround2','PlayerChannelPicked2','LegacyExpandedPlayer2','LegacyExtraPlayer2','LegacySavePlayer2','LegacyResumePlayer2','LegacyTrainingPlayer2','LegacyFormalPlayer2','NearPlayer3','UpgradePlayer1']
rows=[];trials=[];errors=[]
for layer,names in [('Editor',editor),('nondevelopment Player',player)]:
 for name in names:
  f=root/name/'probe.json'
  if not f.exists():errors.append('missing '+str(f));continue
  data=json.loads(f.read_text(encoding='utf-8-sig'));items=data.get('rows',[])
  if not items or data.get('error'):errors.append('invalid '+name+' '+str(data.get('error')))
  for i,item in enumerate(items):
   if not item.get('name') or item.get('status') not in ['PASS','FAIL']:errors.append('bad row '+name+str(i))
   rows.append(dict(rowId=name+':'+str(i),layer=layer,trial=name,assertion=item.get('name'),status=item.get('status'),detail=item.get('detail')))
  counts=dict(collections.Counter(x['status'] for x in items));trials.append(dict(name=name,layer=layer,source=str(f.relative_to(root)),counts=counts))
  if counts.get('FAIL'):errors.append('functional failure '+name)
counts={layer:dict(collections.Counter(x['status'] for x in rows if x['layer']==layer)) for layer in ['Editor','nondevelopment Player']}
open_items=[('native-U16','NOT_RUN'),('new-weapon-physical-input','NOT_RUN'),('independent-human-feel-readability-audio','NOT_RUN'),('final-balance','NOT_RUN'),('whole-frame-concurrent-workload-and-performance-budget','NOT_RUN'),('long-duration-soak','NOT_RUN'),('UI01-D3D12-UNKNOWN','UNRESOLVED'),('Editor-cyan-root-cause','UNRESOLVED'),('Editor-Search-internal-exception','UNRESOLVED'),('historical-C15-shutdown-root-cause','UNRESOLVED'),('external-diagnostic-send-paths','UNRESOLVED')]
summary=dict(status='FAIL' if errors else 'AUTOMATED_FUNCTIONS_PASS_WITH_OPEN_ITEMS',sourceProductSHA='bc06154cc3e7d5d619048efcafbb009e49b6d37b',counts=counts,trials=trials,openItems=[dict(name=n,status=s) for n,s in open_items],errors=errors,scope='Row instances have canonical trial+index identity; repeated setup assertions counted as real separate fixtures, never deduplicated by human label. Process, functional, performance and human classifications are separate. No inherited historical PASS.')
(out/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8');(out/'results.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
with (out/'results.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ['rowId']);w.writeheader();w.writerows(rows)
# Preserve all directly available initial failing semantic rows. These are history, not silently folded into final PASS.
history=[]
for f in root.glob('*/probe.json'):
 try:d=json.loads(f.read_text(encoding='utf-8-sig'))
 except Exception:continue
 for i,x in enumerate(d.get('rows',[])):
  if x.get('status')=='FAIL':history.append(dict(source=str(f.relative_to(root)),rowIndex=i,**x))
f=root/'B1Before/before.json'
if f.exists():
 d=json.loads(f.read_text(encoding='utf-8-sig'))
 if isinstance(d,dict):
  for i,x in enumerate(d.get('rows',[])):
   if x.get('status')=='FAIL':history.append(dict(source=str(f.relative_to(root)),rowIndex=i,**x))
(out/'historical-failing-rows.json').write_text(json.dumps(history,indent=2,ensure_ascii=False),encoding='utf-8')
# Actual calibrated allocation events; report main-thread order160..180 intervals only, not total attack/frame cost.
perf=[]
for name in ['PerformanceEditor3','PlayerPerformance2']:
 d=json.loads((root/name/'performance.json').read_text(encoding='utf-8-sig'));groups=collections.defaultdict(list)
 for s in d.get('samples',[]):
  scenario=s.get('scenario');weapon=s.get('weapon');stage=s.get('stage')
  if scenario and weapon and scenario.startswith(weapon+'/') and stage in ['Startup','Release','Recovery']:groups[scenario].append(s)
 report=dict(source=name,status=d.get('status'),calibrated=d.get('calibrated'),scope=d.get('scope'),rawSamples=len(d.get('samples',[])),groups=[])
 for key,items in sorted(groups.items()):
  ns=sorted(s['ns'] for s in items);report['groups'].append(dict(scenario=key,frames=len(items),p50ms=statistics.median(ns)/1e6,p95ms=ns[min(len(ns)-1,int(.95*len(ns)))]/1e6,maxms=max(ns)/1e6,totalGCBytes=sum(s['bytes'] for s in items),invalidEvents=sum(s['invalid'] for s in items)))
 perf.append(report)
(out/'performance-summary.json').write_text(json.dumps(perf,indent=2),encoding='utf-8')
# No filtering of build warnings: keep matching raw lines plus original complete logs and reported count.
builds=[]
for name in ['B1TestBuild','B1PureBuild','B2TestBuild','B2PureBuild','B3TestBuild','FinalTestBuild','FinalTestBuild2','FinalPureBuild2','NearTestBuild1','NearTestBuild2','NearTestBuild3','UpgradeTestBuild1']:
 b=root/name/'Release';exe=b/'WanxiangGuitu.exe'
 if not exe.exists():continue
 side=Path(str(exe)+'.summary.txt');identity=json.loads(Path(str(exe)+'.release.json').read_text(encoding='utf-8-sig'));bee=json.loads(Path(str(exe)+'.bee.json').read_text(encoding='utf-8-sig'))['PlayerBuildProgramLibrary.Data.PlayerBuildConfig'];warnings=[];log=root/name/'Unity.log'
 if log.exists():
  for line,text in enumerate(log.read_text(encoding='utf-8-sig',errors='replace').splitlines(),1):
   if re.search(r'warning|JobTempAlloc|MemoryLeaks|Exception:',text,re.I):warnings.append(dict(line=line,text=text))
 values=dict(x.split('=',1) for x in side.read_text(encoding='utf-8-sig').splitlines() if '=' in x)
 builds.append(dict(name=name,summary=values,identity=identity,services=bee['Services'],development=bee['Development'],executableSHA256=hashlib.sha256(exe.read_bytes()).hexdigest(),assemblySHA256=hashlib.sha256((b/'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll').read_bytes()).hexdigest(),rawWarningLines=warnings))
(out/'builds-and-warnings.json').write_text(json.dumps(builds,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(dict(counts=counts,open=collections.Counter(s for n,s in open_items),errors=errors),ensure_ascii=False));sys.exit(bool(errors))
