from pathlib import Path
import json,collections,struct
O=Path(__file__).parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
rows=read(O/'oracle_details.json'); risks=read(O/'oracle_nonmain_risks.json')
counts=collections.Counter(r['status'] for r in rows)
groups={}
for r in rows:
 key=r['check'].split('.')[0]
 groups.setdefault(key,collections.Counter())[r['status']]+=1
mains={}
for r in rows:
 if r['check'].startswith('Main.') and '.keys' not in r['check']:
  mains.setdefault(r['mode'],{})[r['check']]=dict(expected=r['expected'],actual=r['actual'],status=r['status'])
nonmain=[]
for r in risks:
 mismatches=[]
 for section in ('before','after'):
  for k,e in r['asImplemented'][section].items():
   a=r['recorded'][section][k]
   if (struct.pack('<f',e)!=struct.pack('<f',a)) if isinstance(e,float) else (e!=a): mismatches.append(section+'.'+k)
 for k in ('deltaAttackPower','deltaBasicPower','deltaLoadoutAttack'):
  if struct.pack('<f',r['asImplemented'][k])!=struct.pack('<f',r['recorded'][k]): mismatches.append(k)
 nonmain.append(dict(mode=r['mode'],seq=r['seq'],role=r['role'],candidateId=r['candidate']['id'],candidateDefinition=r['candidate']['definitionId'],candidateType=r['candidate']['type'],feasible=r['recorded']['feasible'],reason=r['recorded']['reason'],asImplementedMismatches=mismatches,intendedAfterDifferences=r['intendedAfterDifferences'],recordedAfter=r['recorded']['after']))
hist=read(Path.cwd()/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/EVIDENCE/recompute-A03/details.json')['checks']
hg={}
for r in hist: hg.setdefault(r['check'].split('.')[0].split(':')[0],collections.Counter())[r['status']]+=1
result=dict(counts={k:counts[k] for k in ('PASS','FAIL','INFO')},checkGroups=groups,historicalCheckFamilies=hg,MainEvaluations=mains,nonMainDiagnostics=nonmain,FNVComparisons=sum(r['check'].startswith('FNV.') for r in rows),nineUnchangedComparisons=sum(r['check'].startswith('C06.hash.unchanged.') for r in rows),sortPublishedComparisons=sum(r['check']=='sort.publishedIds' for r in rows),sortRenderedComparisons=sum(r['check']=='sort.renderedIds' for r in rows),sha256Comparisons=sum(r['check'].startswith('file.sha256.') for r in rows))
(O/'oracle_metrics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+chr(10),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('MainEvaluations','historicalCheckFamilies','nonMainDiagnostics')},indent=2))
print(json.dumps(nonmain,ensure_ascii=False,indent=2))
