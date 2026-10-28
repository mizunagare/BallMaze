"""Read only a declared UX synthetic session. Disk facts are NOT evidence of native input/human understanding."""
import argparse,hashlib,json
from pathlib import Path
from ux_pack import safe,load,now
def inspect(session):
 session=safe(session);meta=load(session/'session.json');pack=safe(meta['packageRoot']);storage=safe(meta['storageRoot'])
 if load(pack/'owner.json')['kind']!='UX01 preparation only' or storage!=session/'Storage' or pack not in session.parents:raise ValueError('Owned UX session only')
 main=storage/'WanxiangGuitu/ForestRuins/save.json';result=dict(utc=now(),scope='Read-only disk identity, not native input or human PASS',sessionId=meta['sessionId'],humanVerdict='NOT_EVALUATED',saveState='MISSING')
 if main.exists():
  safe(main);env=load(main)
  if env.get('version')!=9:result['saveState']='INCOMPATIBLE';return result
  payload=env.get('payload','')
  if hashlib.sha256(payload.encode()).hexdigest().upper()!=env.get('checksum','').upper():result['saveState']='CORRUPT_CHECKSUM';return result
  data=json.loads(payload);profile=data.get('profile') or {};run=data.get('activeRun') or {};settlement=data.get('settlement') or {};cp=run.get('checkpoint') or profile.get('camp') or {}
  result.update(saveState='CHECKSUM_VALID_NOT_PRODUCT_CATALOG_VERDICT',revision=env.get('revision'),profileId=profile.get('profileId'),runId=run.get('runId'),regionInstance=run.get('regionInstanceId'),seed=run.get('seed'),runPhase=run.get('phase'),settlementId=settlement.get('settlementId'),settlementStatus=settlement.get('status'),gearIds=[x.get('id') for x in cp.get('gear',[])],bagMaterials=cp.get('materials'),warehouseMaterials=profile.get('materials'),randomStreamsSha256=hashlib.sha256(json.dumps(run.get('randomStreams'),sort_keys=True).encode()).hexdigest())
 if main.exists() and result.get('saveState')=='CHECKSUM_VALID_NOT_PRODUCT_CATALOG_VERDICT':
  result['stateDigests']={key:hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest() for key,value in dict(forest=cp.get('forest'),forestWorld=cp.get('forestWorld'),broughtRemaining=run.get('broughtRemaining'),earnedRemaining=run.get('earnedRemaining'),pending=profile.get('pending'),badges=profile.get('badges'),bossHunts=profile.get('bossHunts')).items()}
 prefs=storage/'WanxiangGuitu/preferences.json'
 if prefs.exists():safe(prefs);result['preferencesOnDisk']=load(prefs)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--session',required=True,type=Path);a=p.parse_args();print(json.dumps(inspect(a.session),ensure_ascii=False,indent=2))
