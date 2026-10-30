import json,csv,math
from pathlib import Path
import sys
root=Path(sys.argv[1]);out=Path(__file__).parent
pairs={};allrows=[];contacts=[]
for variant,phase in [('old','BeforeMatrix'),('new','AfterMatrix')]:
 d=json.loads((root/phase/'matrix.json').read_text());assert len(d['runs'])==9 and len({x['run']for x in d['runs']})==9 and len(d['rows'])==216
 pairs[variant]={x['sample']:x for x in d['rows']};types={r['run']:{e['id']:('Warden'if e.get('boss')==1 else'Tide'if e.get('boss')==2 else['Melee','Ranged','Elite','Boss'][e['type']])for e in json.loads(r['layout'])['encounters']}for r in d['runs']}
 for row in d['rows']:
  row=dict(row);row['variant']=variant;row['effectivePolicy']='WrongDodge'if row['rep']==2 and row['type']=='Mixed'else row['policy'];allrows.append(row)
  path=root/phase/'Samples'/row['sample']/'events.jsonl';owners={}
  if not path.exists():continue
  for line in path.read_text().splitlines():
   e=json.loads(line)
   if e['kind']in ['telegraph','projectile']and e['entity']!='projectile':owners[e['attack']]=e['entity']
   if e['kind']!='contact':continue
   applied=e['before']-e['after'];entity=e['entity']if e['entity']!='projectile'else owners.get(e['attack'],'UNRESOLVED_SOURCE')
   contacts.append(dict(variant=variant,sample=row['sample'],run=row['run'],seed=row['seed'],tier=row['tier'],type=row['type'],policy=row['effectivePolicy'],attack=e['attack'],entity=entity,attackerType=types.get(row['run'],{}).get(entity,'UNRESOLVED_TYPE'),frame=e['frame'],time=e['time'],raw=e['raw'],defense=e['defense'],before=e['before'],after=e['after'],applied=applied,invulnerable=e['invulnerable'],reduction=1-applied/e['raw']if e['raw']else None,nonOverkill=e['after']>0 and applied>0))
with(out/'BALANCE_MATRIX.csv').open('w',encoding='utf-8-sig',newline='')as f:
 w=csv.DictWriter(f,fieldnames=allrows[0]);w.writeheader();w.writerows(allrows)
with(out/'HIT_EVENTS.csv').open('w',encoding='utf-8-sig',newline='')as f:
 w=csv.DictWriter(f,fieldnames=contacts[0]);w.writeheader();w.writerows(contacts)
summary={}
for v in ['old','new']:
 rows=[r for r in allrows if r['variant']==v];hits=[e for e in contacts if e['variant']==v];high=[e for e in hits if e['tier']==3 and e['type']in ['Melee','Ranged']and e['nonOverkill']];summary[v]=dict(runs=9,samples=len(rows),outcomes={o:sum(r['outcome']==o for r in rows)for o in sorted({r['outcome']for r in rows})},contacts=len(hits),highNormalContacts=len(high),highNormalFloorRate=sum(abs(e['applied']-1)<.001 for e in high)/len(high)if high else None,damage=sum(r['damage']for r in rows),heals=sum(r['heals']for r in rows),xp=sum(r['experience']for r in rows),xpCheckedSurvivors=sum(r['outcome']!='PLAYER_DEAD'for r in rows),xpDeathNotChecked=sum(r['outcome']=='PLAYER_DEAD'for r in rows),xpSourceMismatch=sum(not r['xpMatchesWhenSurviving']for r in rows if r['outcome']!='PLAYER_DEAD'))
# Conditional comparison; independent profiles and entity UUIDs are expected to differ.
comparison=[]
for k,a in pairs['old'].items():
 b=pairs['new'][k];comparison.append(dict(sample=k,initialDefenseEqual=abs(a['initialDefense']-b['initialDefense'])<1e-4,initialHPEqual=a['initialHP']==b['initialHP'],initialPowerEqual=a['initialPower']==b['initialPower'],initialRanksEqual=a['initialRanks']==b['initialRanks'],initialPositionsEqual=a['initialPositions']==b['initialPositions'],initialRNGEqual=a['initialStreams']==b['initialStreams'],oldOutcome=a['outcome'],newOutcome=b['outcome'],oldDamage=a['damage'],newDamage=b['damage'],oldElapsed=a['elapsed'],newElapsed=b['elapsed']))
(out/'PAIRED_INPUTS.json').write_text(json.dumps(comparison,indent=2),encoding='utf-8');(out/'SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2));print('conditional input mismatches',sum(not all(r[n]for n in ['initialDefenseEqual','initialHPEqual','initialPowerEqual','initialRanksEqual','initialPositionsEqual','initialRNGEqual'])for r in comparison))
