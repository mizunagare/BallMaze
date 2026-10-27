"""Read-only reconciliation of snapshots produced by actual runtime inputs. No save generation."""
import argparse,hashlib,json
from pathlib import Path
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--story',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();p=a.story;rows=[]
 def snap(n):return load(p/('snapshot-'+n+'.json'))
 def profile(s):return json.loads(s['profile'])
 def need(b,n):rows.append(dict(name=n,status='PASS' if b else 'FAIL'))
 dep=snap('Main-departed');paid=snap('Main-repaired');pending=snap('Main-pending');failed=snap('Pending-commit-failed');committed=snap('Pending-committed');repeat=snap('Committed-verified-committed');withdraw=snap('Manufacture-withdrawn');made=snap('Manufacture-manufactured');next_run=snap('Manufacture-successor');resumed=snap('Successor-verified-successor')
 picked=snap('Main-picked-Ore');cost=[0,0,0,2,1,0];craft=[0,0,0,2,1,2]
 need(all(picked['bag'][i]-paid['bag'][i]==cost[i] for i in range(6)),'ferry actual inventory cost wood2 stone1')
 exits=json.loads(paid['layout'])['exits'];receipt=next(x['repairReceipt'] for x in exits if x['id']=='exit:ferry')
 need(bool(receipt) and next(x for x in exits if x['id']=='exit:ferry')['repaired'],'paid repaired exit has stable receipt')
 need(next(x['repairReceipt'] for x in json.loads(pending['layout'])['exits'] if x['id']=='exit:ferry')==receipt,'extraction cancel/retry did not replace repair receipt')
 need(paid['bag']==pending['bag'],'cancel and extraction do not charge again')
 for name,k in [('Wood',3),('Stone',4),('Ore',5)]:
  g=snap('Main-ground-'+name);v=snap('Main-picked-'+name)
  need(len(g['ground'])>0 and g['bag'][k]<v['bag'][k] and profile(g)['materials']==profile(dep)['materials'],'ground '+name+' not credited to bag/warehouse before E pickup')
 need(profile(pending)['materials']==profile(failed)['materials']==profile(dep)['materials'],'Pending/rejected commit do not publish warehouse income')
 st=json.loads(committed['settlement']);earned=[st['keptMaterials'][i]+st['returnedMaterials'][i] for i in range(6)]
 need(all(profile(committed)['materials'][i]-profile(pending)['materials'][i]==earned[i] for i in range(6)),'real Commit warehouse equals actual settlement yield')
 need(profile(committed)==profile(repeat) and committed['settlement']==repeat['settlement'],'Committed new process no repeat award')
 need(profile(committed)['committedRuns'].count(pending['runId'])==1,'exactly one committed Run identity')
 need(withdraw['bag']==craft and all(profile(committed)['materials'][i]-profile(withdraw)['materials'][i]==craft[i] for i in range(6)),'real warehouse withdraw matches white sword recipe materials')
 need(made['bag']==[0]*6 and profile(made)['materials']==profile(withdraw)['materials'],'craft consumes carried materials, not warehouse twice')
 new_ids=sorted(set(made['gear'].split(','))-set(withdraw['gear'].split(',')))
 need(len(new_ids)==1,'exactly one manufactured equipment identity')
 need(next_run['profileId']==pending['profileId'] and next_run['runId']!=pending['runId'] and json.loads(next_run['run'])['mode']==2,'successor is actual new forest Run in same Profile')
 for key in ['profileId','runId','region','seed','layout','streams','gear','ledger']:
  need(next_run[key]==resumed[key],'new process retains successor '+key)
 audit=dict(status='PASS' if all(x['status']=='PASS' for x in rows) else 'FAIL',story=str(p),checks=rows,profile=pending['profileId'],firstRun=pending['runId'],successorRun=next_run['runId'],firstRegion=pending['region'],successorRegion=next_run['region'],seed=pending['seed'],successorSeed=next_run['seed'],actualHarvest=picked['bag'],ferryCost=cost,settlementYield=earned,committedWarehouse=profile(committed)['materials'],withdrawn=withdraw['bag'],craftedCost=craft,finalWarehouse=profile(made)['materials'],newEquipmentIds=new_ids,repairReceipt=receipt,scope='Read-only reconciliation of runtime snapshots, not a new gameplay execution or a universal value estimate')
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(dict(status=audit['status'],checks=len(rows),actualHarvest=audit['actualHarvest'],finalWarehouse=audit['finalWarehouse'])))
 if audit['status']!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
