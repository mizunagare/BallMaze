"""Portable published-byte and business-receipt checks; does not rerun Windows or access player saves."""
import argparse,gzip,hashlib,json
from pathlib import Path
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def digest(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('evidence',type=Path);a=ap.parse_args();r=a.evidence
 manifest=load(r/'manifest.json')
 for x in manifest:
  b=(r/x['path']).read_bytes();assert digest(b)==x['publishedSha256'],x['path']
  raw=gzip.decompress(b) if x['compression']=='gzip' else b
  assert digest(raw)==x['rawSha256'],x['path']+' raw'
 origin=load(r/'Inputs/owner.json')['root'].replace('\\','/').rstrip('/')
 def mapped(s):
  path=s.replace('\\','/');assert path.lower().startswith(origin.lower()+'/');return r/path[len(origin)+1:]
 stages=load(r/'Inputs/Story1-stages.json');assert [x['stage'] for x in stages]==['Save','Resume']
 first=mapped(stages[0]['attempt'])/'StorageAfter';second=mapped(stages[1]['attempt'])/'StorageAfter'
 for x in stages:
  native=load(mapped(x['nativeReceipt']));assert native['waitResult']==0 and native['exitCodeKnown'] and native['actualExitCode']==0 and x['wrapperExit']==0
 saved=load(first/'r1-after-f5.json');quit=load(first/'r1-quit-observation-Save.json');ready=load(second/'r1-first-restored-frame.json');quiet=load(second/'r1-after-replay-horizon.json');hit=load(second/'r1-new-hit.json');env=load(first/'WanxiangGuitu/ForestRuins/save.json');data=json.loads(env['payload']);cp=data['activeRun']['checkpoint']
 assert env['version']==9 and digest(env['payload'].encode()).upper()==env['checksum'].upper()
 assert saved['pending']==quit['pending']==1 and saved['actionPhase']=='Startup' and saved['lastReleaseFrame']==quit['lastReleaseFrame']==-1
 assert saved['nodeHP']==quit['nodeHP']==ready['nodeHP']==quiet['nodeHP']==55 and all(x['projectiles']==0 for x in [saved,quit,ready,quiet])
 assert saved['pid']!=ready['pid'] and ready['pending']==ready['actionId']==0
 assert all(saved[k]==ready[k]==quiet[k] for k in ['profileId','runId','region','seed','layout','streams','ledger','gear','profile','bag'])
 assert abs(cp['weaponAttackCooldown']-ready['attackCooldown'])<.002 and quiet['attackCooldown']==0
 assert quiet['simulationTime']-ready['simulationTime']>=3.2 and hit['nodeHP']<quiet['nodeHP']
 close=load(r/'Close3/Observer/exit-observer.json');assert close['childDone'] and close['childKnown'] and close['childCode']==0 and close['hostDone'] and close['hostKnown'] and close['hostCode']==0 and not close['timedOut'] and not close['forcedTermination']
 events=[json.loads(x) for x in (r/'Close3/Observer/timeline.jsonl').read_text().splitlines()];assert any(x['kind']=='pid-not-listed-final' and not x['value']['proofOfExit'] for x in events)
 native=load(r/'Close3/player.desktop-process.json.native-exit.json');assert native['waitResult']==0 and native['exitCodeKnown'] and native['actualExitCode']==0
 audit=[json.loads(x) for x in (r/'Close3/entry-audit.jsonl').read_text().splitlines()];assert any(x['phase']=='title-quit' for x in audit)
 original=load(r/'History/ReleaseSmoke/process.json');assert original['timedOut'] and not original['forcedTermination'] and original['hostExitCode'] is None
 rules=load(r/'Rules/combat01.json');assert rules['status']=='PASS' and len(rules['checks'])==188 and all(x['status']=='PASS' for x in rules['checks'])
 source={x['path']:x['sha256'].upper() for x in load(r/'Inputs/source-files.json')};copies=list((r/'T').glob('*/copied-source-files.json'));assert len(copies)==1
 assert len(source)==1152 and all(x['source']==x['copy'] and x['source'].upper()==source[x['path'].replace('\\','/')] for x in load(copies[0]))
 analysis=load(r/'Analysis2/analysis.json');assert analysis['status']=='PASS' and len(analysis['checks'])==31
 print(json.dumps(dict(status='PASS',publishedFiles=len(manifest),controlledAssertions=188,independentAuditChecks=31,scope='Published bytes and receipt/internal consistency only; not a Windows rerun or current-machine user-file recheck')))
if __name__=='__main__':main()
