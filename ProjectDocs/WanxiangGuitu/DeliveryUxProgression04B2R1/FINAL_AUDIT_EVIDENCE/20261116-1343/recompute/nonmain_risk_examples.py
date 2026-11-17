"""Static numerical counterexamples only: not a Player run, never acceptance FAIL."""
from pathlib import Path
import json,copy
root=Path.cwd(); out=Path(__file__).parent
observations=[json.loads(x) for x in (root/'Evidence/Runs04B2R1/SESSION-20261116-1115/A03/preview9/r1-observations.jsonl').read_text(encoding='utf-8-sig').splitlines()]
r=next(o['raw'] for o in observations if o['stage']=='preview9')
def scalar(path,key):
 for line in path.read_text(encoding='utf-8-sig').splitlines():
  if line.startswith('  '+key+':'): return float(line.split(':',1)[1].strip())
 raise KeyError(key)
examples=[]
for slot,typ,definition,role in [('bag',10,'bag_relic',7),('rig',9,'rig_heavy',6)]:
 existing=next(i for i in r['items'] if i['worn'] and i['type']==typ)
 selected=existing['definitionId']
 original_asset=root/'Assets/CombatPrototype/Resources/ContainerData'/(selected+'.asset')
 candidate_asset=root/'Assets/CombatPrototype/Resources/ContainerData'/(definition+'.asset')
 fields={}
 for key in ('attackBonus','defenseBonus'):
  old=scalar(original_asset,key); new=scalar(candidate_asset,key)
  fields[key]=dict(current=old,appendedFirstWornSelection=old,actualReplacement=new,missedDelta=new-old)
 examples.append(dict(status='INFO',kind='STATIC_COUNTEREXAMPLE_NOT_OBSERVED_PLAYER_FAILURE',baseObservationSeq=next(o['seq'] for o in observations if o['stage']=='preview9'),role=role,existing=selected,hypotheticalCandidate=definition,fields=fields,explanation='Source Preview appends worn candidate without unwearing existing same type; first-worn selector retains existing container. This counterexample is not A03 measured mismatch.'))
(out/'nonmain_static_risk_examples.json').write_text(json.dumps(examples,ensure_ascii=False,indent=2)+chr(10),encoding='utf-8')
print(json.dumps(examples,ensure_ascii=False,indent=2))
