"""Publish only owned synthetic validation evidence; no user source bodies/caches/Players."""
import argparse,ast,hashlib,json,re,shutil,subprocess
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone

def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def copy_flat(src,dest):
 dest.mkdir(parents=True,exist_ok=True)
 for f in src.iterdir():
  if f.is_file() and f.suffix.lower() not in ['.dll','.exe','.pdb']:shutil.copy2(f,dest/f.name)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--evidence',type=Path,required=True);a=ap.parse_args();r=a.run;ev=a.evidence
 owner=load(r/'owner.json');assert owner['kind']=='PLAYER-01 isolated vertical-slice validation'
 assert load(r/'preserved-processes.json')==[], 'Do not collect live runs'
 ev.mkdir(parents=True,exist_ok=True);copy_flat(r,ev/'Run')
 for name in ['ReadOnlyAudit','ExecutedTools','ProductIdentity']:
  shutil.copytree(r/name,ev/name,dirs_exist_ok=True)
 for name in ['C','Confirmation','Fixture','Gather']:
  if (r/name).exists():copy_flat(r/name,ev/'Run'/name)
 if (r/'Gather').exists():
  for d in (r/'Gather').glob('ExecutedDrivers-*'):shutil.copytree(d,ev/'Run/Gather'/d.name,dirs_exist_ok=True)
 players=[]
 for d in sorted(r.glob('Player-*')):
  copy_flat(d,ev/'Run'/d.name);analysis=load(d/'b09-title-analysis.json');events=[json.loads(x) for x in (d/'entry-audit.jsonl').read_text(encoding='utf-8-sig').splitlines()]
  save=d/'WanxiangGuitu/ForestRuins';afterFiles={f.relative_to(save).as_posix():sha(f).upper() for f in save.rglob('*') if f.is_file()} if save.exists() else {}
  dump(ev/'Run'/d.name/'save-after-readonly.json',dict(observedUtc=datetime.now(timezone.utc).isoformat(),scope='Post-test read-only fingerprint; original verifier also compared immediately after close',files=afterFiles,equalBefore=afterFiles==load(d/'save-before.json')))
  assert afterFiles==load(d/'save-before.json')
  boot=next(x for x in events if x['phase']=='boot-start');shown=next(x for x in events if x['phase']=='title-rendered')
  parse=lambda x:datetime.fromisoformat(x.replace('Z','+00:00'))
  players.append(dict(case=d.name,analysis=analysis,bootToTitleRenderedSeconds=(parse(shown['utc'])-parse(boot['utc'])).total_seconds(),timingScope='Observed entry latency only, NOT a gameplay/performance benchmark'))
 # Existing BUILD-01 collector handles this run's new child build receipts.
 py=str(Path(__import__('sys').executable));collector=a.source/'ProjectDocs/WanxiangGuitu/DeliveryBuild01/collect_results.py'
 subprocess.run([py,'-B',str(collector),'--root',str(r/'B'),'--evidence',str(ev/'Build')],check=True)
 build=load(ev/'Build/RESULTS.json')['runs'][0]['build'];warnings=build['warningCategories']
 old=load(a.source/'ProjectDocs/WanxiangGuitu/DeliveryBuild01/Evidence/Runs/20261027-175503-Repeat-d42b8bc9/Results/build-report-messages.json')
 current=load(next((r/'B').glob('*/Results/build-report-messages.json')))
 before=Counter(x['text'] for x in old['messages'] if x['type']=='Warning');after=Counter(x['text'] for x in current['messages'] if x['type']=='Warning')
 warningReview=dict(categories=warnings,stillPresent=sum((before&after).values()),disappeared=sum((before-after).values()),added=sum((after-before).values()),interpretation={'CS0618':'86 warnings in Player-compiled code: obsolete API use, potential Player relevance; not automatically harmless or Editor-only','CS0414':'3 unused-field warnings in Player code; not removed in this batch','scene serialized version':'2 Boot/Title format warnings: possible initialization concern; six title observations are limited evidence, not an upgrade'},editorImportDiagnostics='Raw Editor logs retained separately (JobTempAlloc etc). These are not silently merged into 91 BuildReport warnings.')
 dump(ev/'WARNING_REVIEW.json',warningReview)
 original=load(r/'ReadOnlyAudit/source-files.json');changes=[x['path'] for x in original if not (a.source/x['path']).exists() or sha(a.source/x['path'])!=x['sha256']]
 initial=load(r/'ReadOnlyAudit/inputs-history.json')
 stage1=load(r/'Gather/b4-checkpoint-1.json');stage2=load(r/'Gather/b4-checkpoint-2.json')
 normalLog=(r/'Gather/normal-results.txt').read_text(encoding='utf-8-sig')
 processes=[]
 for m in ['Normal','Resume','FinalResume']:
  receipt=load(r/'Gather'/('process-result-'+m+'.json'));log=(r/'Gather'/(m+'.log')).read_text(encoding='utf-8-sig',errors='replace');ids=sorted(set(re.findall(r'"processId":(\d+)',log)));receipt['unityProcessIdsFromRawUTPLog']=ids;receipt['processIdEvidence']='Unity raw ##utp log processId, separate from worker/pwsh host PID';processes.append(receipt)
 gather=dict(scope='Editor normal AI, never formal Player adventure',stage1=stage1,stage2=stage2,processes=processes,actualWoodPickup=int(re.findall(r'ACTUAL_WOOD_PICKUP wood=(\d+)',normalLog)[-1]),ferryWoodCost=2,ferryStoneCost=1,woodAfterRepair=int(stage1['ledger'].split('/')[1].split(',')[3]),withdrawWoodForCraft=2,finalWarehouseWood=int(stage2['warehouse'].split('/')[0].split(',')[3]),newRun=stage1['run']!=stage2['run'],sameProfile=stage1['profile']==stage2['profile'],newEquipmentIds=sorted(set(stage2['gear'].split(','))-set(stage1['gear'].split(','))))
 assert all(x['exitCode']==0 and not x['timedOut'] for x in gather['processes'])
 bindings=dict(scope='Editor virtual InputSystem/uGUI only',rules=load(r/'C/input01-rules.json') if (r/'C/input01-rules.json').exists() else None,play=load(r/'C/input01-play-normal.json'),resume=load(r/'C/input01-play-resume.json'))
 rows=load(r/'results.json');counts=dict(Counter(x['status'] for x in rows))
 matrix=[dict(id='P01-01',status='PASS',scope='Fresh non-development build and artifact identity'),dict(id='P01-02',status='NOT_RUN',scope='Six final Player title/catalog/WM_CLOSE cases PASS; actual Continue/Load/settings/new-game interaction not executed in final Player'),dict(id='P01-03',status='NOT_RUN',scope='Formal Player full adventure cannot reuse Editor-only Gather driver; three Editor AI stages PASS separately'),dict(id='P01-04',status='NOT_RUN',scope='No final Player virtual/native binding driver; Editor 239+11 assertions do not substitute'),dict(id='P01-05',status='PASS',scope='Explicitly allowed controlled regression: candidate save failure/rollback, changed confirmation, Pending/Committed new-process restoration and positive-yield duplicate commit; final Player corrupt/incompatible files protected'),dict(id='P01-06',status='NOT_RUN',scope='No authorized independent interactive Windows environment or human tester; zero native input sent'),dict(id='P01-07',status='NOT_RUN',scope='Hardware/title latency only; CPU/GPU frame time, gameplay memory/VRAM and controlled loads not measured')]
 summary=dict(utc=datetime.now(timezone.utc).isoformat(),startSha=owner['head'],productInputSha=owner['head'],testToolFreeze='4a48a30c97c9ac92adc3d9bd493c496e687c6455',overall='NOT_RUN: final Player full vertical slice and native/human requirements remain open',matrix=matrix,matrixCounts=dict(Counter(x['status'] for x in matrix)),orchestrationCounts=counts,orchestrationCountsAreNotPlayerExperiments=True,players=players,build=build,warningReview=warningReview,gather=gather,controlledInput=dict(ruleAssertions=len(bindings['rules']['checks']) if bindings['rules'] and 'checks' in bindings['rules'] else None,playAssertions=len(bindings['play']['checks']),resumeAssertions=len(bindings['resume']['checks'])),confirmation=load(r/'Confirmation/confirmation-result.json'),sourceFilesAtFreeze=len(original),sourceFilesChanged=changes,protectedInputs=initial['inputs'],progressVersion='v9 unchanged',userOverlay='ForestRuins.unity, ProjectSettings.asset and three untracked _Recovery files copied/hash-recorded; user content not published',native=load(r/'Player-Missing/native-environment.json'),historicalUnresolved=['D3D12 UNKNOWN','Editor cyan frame','Editor.Search root cause','JobTempAlloc root cause'],productFilesCommittedChanged=subprocess.check_output(['git','diff','--name-only',owner['head'],'HEAD','--','Assets','Packages','ProjectSettings'],cwd=a.source,text=True).splitlines())
 assert not changes
 assert not summary['productFilesCommittedChanged']
 assert all(p['analysis']['status']=='PASS' for p in players) and len(players)==6
 assert build['errors']==0 and build['packageDirectoryNotFoundCount']==0
 assert summary['native']['status']=='NOT_RUN' and not any('SendInput' in e.get('method','') for e in summary['native']['events'])
 assert gather['actualWoodPickup']==4 and gather['woodAfterRepair']==2 and gather['finalWarehouseWood']==0 and gather['newRun'] and gather['sameProfile']
 dump(ev/'RESULTS.json',summary)
 print(json.dumps(dict(matrix=summary['matrixCounts'],orchestration=counts,formalTitleProcesses=len(players),buildErrors=build['errors'],sourceChanges=changes)))
if __name__=='__main__':main()
