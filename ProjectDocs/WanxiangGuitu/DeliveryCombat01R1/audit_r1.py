"""Independent read-only reconciliation of runtime, saved bytes, native handles and frozen inputs."""
import argparse,csv,hashlib,json
from pathlib import Path
from datetime import datetime

def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 if a.out.exists():raise ValueError('Fresh output required; preserve every prior result')
 checks=[]
 def need(v,name):checks.append(dict(name=name,status='PASS' if v else 'FAIL'))
 stages=load(a.root/'Story1-stages.json');need([x['stage'] for x in stages]==['Save','Resume'],'two prescribed stages')
 for stage in stages:
  d=Path(stage['attempt']);result=load(d/'StorageAfter'/('result-R1'+stage['stage']+'.json'))
  native=load(Path(stage['nativeReceipt']));need(result['status']=='PASS' and native['waitResult']==0 and native['exitCodeKnown'] and native['actualExitCode']==0 and stage['wrapperExit']==0,stage['stage']+' actual runtime receipt and retained native exit code')
 first=Path(stages[0]['attempt'])/'StorageAfter';second=Path(stages[1]['attempt'])/'StorageAfter'
 before=load(first/'r1-before-input.json');accepted=load(first/'r1-startup.json');saved=load(first/'r1-after-f5.json');quit=load(first/'r1-quit-observation-Save.json');ready=load(second/'r1-first-restored-frame.json');quiet=load(second/'r1-after-replay-horizon.json');new=load(second/'r1-new-accepted.json');hit=load(second/'r1-new-hit.json')
 need(accepted['actionId']>before['actionId'] and accepted['pending']==saved['pending']==quit['pending']==1 and accepted['actionPhase']==saved['actionPhase']=='Startup','accepted action still pending in F5 and real quit callback')
 need(saved['lastReleaseFrame']==quit['lastReleaseFrame']==before['lastReleaseFrame']==-1,'release never happened before exit')
 need(all(x['nodeHP']==before['nodeHP'] and x['heroHP']==before['heroHP'] and x['projectiles']==0 for x in [accepted,saved,quit]),'no HP or projectile committed during startup')
 need(all(x[k]==before[k] for x in [accepted,saved,quit] for k in ['bag','ledger','streams','gear','profile']),'no inventory source ledger RNG gear or Profile mutation during startup save')
 files=list((first/'WanxiangGuitu/ForestRuins').glob('save.json'));assert len(files)==1;env=load(files[0]);payload=json.loads(env['payload']);run=payload['activeRun'];cp=run['checkpoint'];resource=next(x for x in cp['resources'] if x['entityId']==saved['nodeId'])
 need(env['version']==9 and hashlib.sha256(env['payload'].encode()).hexdigest().upper()==env['checksum'].upper(),'actual final exit v9 envelope checksum valid')
 need(resource['health']==before['nodeHP'] and cp['health']==before['heroHP'] and cp['materials']==before['bag'],'final exit disk has unchanged HP and inventory')
 need(cp['weaponAttackCooldown']>0 and abs(cp['weaponAttackCooldown']-quit['attackCooldown'])<.00001,'exit disk cooldown equals real quit observation')
 need(saved['revision']>before['revision'] and env['revision']>=saved['revision'],'normal F5 published a new revision and exit retained it')
 need(ready['pid']!=saved['pid'] and ready['pid']==hit['pid'],'new OS process identity')
 need(all(ready[k]==saved[k] for k in ['profileId','runId','region','seed','layout','streams','ledger','gear','profile','bag']),'same Profile Run region seed layout random streams gear and ledger')
 need(ready['actionId']==0 and ready['pending']==0 and ready['projectiles']==0 and ready['nodeHP']==before['nodeHP'],'restored no transient action or projectile')
 need(abs(ready['attackCooldown']-cp['weaponAttackCooldown'])<.002,'first restored frame cooldown equals saved cooldown once')
 need(quiet['simulationTime']-ready['simulationTime']>=3.2,'observe beyond startup plus full projectile lifetime')
 need(quiet['pending']==quiet['projectiles']==0 and quiet['nodeHP']==before['nodeHP'] and quiet['heroHP']==before['heroHP'],'no replay or delayed damage')
 need(quiet['attackCooldown']==0 and all(quiet[k]==saved[k] for k in ['bag','ledger','streams','gear','profile']),'no repeated cooldown debit reward consumption or random draw')
 need(new['pending']==1 and new['actionId']>0 and new['attackCooldown']>0 and hit['nodeHP']<quiet['nodeHP'] and hit['lastReleaseFrame']>=new['frame'],'subsequent legitimate input attack releases and damages')
 need(hit['bag']==saved['bag'] and hit['ledger']==saved['ledger'],'new damage does not inject materials')
 case=a.root/'Close3';v=load(case/'Observer/exit-observer.json');timeline=[json.loads(x) for x in (case/'Observer/timeline.jsonl').read_text().splitlines()];request=next(x for x in timeline if x['kind']=='close-request');identity=next(x for x in timeline if x['kind']=='identity')['value'];audit=[json.loads(x) for x in (case/'entry-audit.jsonl').read_text().splitlines()];exitAudit=next(x for x in audit if x['phase']=='title-quit');host=load(case/'player.desktop-process.json.native-exit.json')
 need(v['queued'] and v['responsive'] and v['windowGone'],'exact owned responsive window request and destruction independently observed')
 need(v['childDone'] and v['childKnown'] and v['childCode']==0 and host['exitCodeKnown'] and host['actualExitCode']==0 and host['pid']==identity['pid'],'held child handle exit agrees with native launcher receipt')
 need(v['pidGone'] and any(x['kind']=='pid-not-listed-final' for x in timeline),'PID absence separately observed after native exit (not exit oracle)')
 need(v['hostDone'] and v['hostKnown'] and v['hostCode']==0 and not v['timedOut'] and not v['forcedTermination'],'host independently exits normally without force kill')
 need(datetime.fromisoformat(exitAudit['utc'].replace('Z','+00:00'))>=datetime.fromisoformat(request['utc'].replace('Z','+00:00')) and exitAudit['scene']=='Title','product title quit audit follows close request')
 need(not any(x in (case/'player.log').read_text(errors='replace') for x in ['Got a UNKNOWN','Native Crash Reporting','Unhandled Exception','Crash!!!']),'complete new D3D11 shutdown log has no crash marker (not historical root-cause proof)')
 release=load(a.root/'release-provenance.json');need(release['sourceExe']==release['copyExe']==identity['sha256'] and release['sourceAssembly']==release['copyAssembly'],'pure release bit identity and observed process image SHA')
 inputs=load(a.root/'source-files.json');changed=[x['path'] for x in inputs if sha(a.repo/x['path']).upper()!=x['sha256'].upper()];need(not changed,'all 1152 product inputs unchanged')
 protected=load(a.root/'protected-inputs.json');need(all(sha(a.repo/x['path']).upper()==x['sha256'].upper() for x in protected),'all user uncommitted file hashes protected')
 build=list((a.root/'T').glob('*/copied-source-files.json'));assert len(build)==1;copy=load(build[0]);need(len(copy)==len(inputs) and all(x['source']==x['copy'] and x['source'].upper()==sha(a.repo/x['path'].replace('\\','/')).upper() for x in copy),'acceptance build input copy matches unchanged product source')
 rules=load(a.root/'Rules/combat01.json');need(rules['status']=='PASS' and len(rules['checks'])==188 and all(x['status']=='PASS' for x in rules['checks']),'direct COMBAT01 rule regression 188 new PASS')
 a.out.mkdir(parents=True);summary=dict(status='FAIL' if any(x['status']=='FAIL' for x in checks) else 'PASS',checks=checks,changedProductInputs=changed,protectedFiles=len(protected),productInputs=len(inputs),saved= {k:saved[k] for k in ['pid','frame','actionId','actionPhase','pending','nodeHP','attackCooldown','revision']},exitDisk=dict(revision=env['revision'],cooldown=cp['weaponAttackCooldown']),restored={k:ready[k] for k in ['pid','frame','pending','actionId','nodeHP','attackCooldown']},newHitHP=hit['nodeHP'],closeObservation=v)
 (a.out/'analysis.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 with (a.out/'checks.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=['name','status']);w.writeheader();w.writerows(checks)
 samples=[before,accepted,saved,quit,ready,quiet,new,hit]
 with (a.out/'startup-timeline.csv').open('w',encoding='utf-8-sig',newline='') as f:
  fields=['label','utc','pid','frame','simulationTime','actionId','actionPhase','pending','lastReleaseFrame','heroHP','nodeHP','attackCooldown','projectiles','revision'];w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(samples)
 print(json.dumps(dict(status=summary['status'],checks=len(checks),failures=[x['name'] for x in checks if x['status']=='FAIL'])));raise SystemExit(0 if summary['status']=='PASS' else 1)
if __name__=='__main__':main()
