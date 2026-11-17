"""Trace historical assertions to newly computed checks; never infer truth from old PASS."""
from pathlib import Path
import json,csv,collections,re
R=Path.cwd(); O=Path(__file__).parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
old=read(R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/EVIDENCE/recompute-A03/details.json')['checks']; new=read(O/'oracle_details.json')
index=collections.defaultdict(list)
for i,x in enumerate(new): index[(x.get('mode'),x.get('seq'),x['check'])].append((i,x))
def renamed(x):
 k=x['check']
 if k in ('live.attackPower','live.basicPower'): return 'D24.'+k
 if k=='live.bonus': return 'Strength.bonus'
 if k.startswith('published.'): return 'D24.'+k
 m=re.fullmatch(r'(items|warehouse)[[]([0-9]+):[^]]*[]][.](derivedAttack|derivedDefense|asset[.]savedAttack|asset[.]savedDefense)',k)
 if m: return m[1]+'.'+m[2]+'.'+m[3]
 if k.startswith(('rig.asset.','bag.asset.')): return k
 if k.startswith('sort.'): return k
 if k.startswith('nine.'):
  rules={'nine.unchanged.':'C06.hash.unchanged.','nine.canonical.unchanged.':'C06.plaintext.unchanged.','nine.fnv.before.':'FNV.before.','nine.fnv.after.':'FNV.after.','nine.rawCanonical.':'C06.rawCanonical.'}
  for prefix,target in rules.items():
   if k.startswith(prefix): return target+k[len(prefix):]
  keys={'beforeJson':'before','afterJson':'after','canonicalBefore':'canonicalBefore','canonicalAfter':'canonicalAfter','raw.canonical':'rawCanonical'}
  for a,b in keys.items():
   if k=='nine.'+a+'.keys': return 'C06.keys.'+b
 if k.startswith('preview.'):
  if k=='preview.candidateId': return k
  # Main-only full evaluation vs non-Main limited before/metadata.
  role=next((r['actual'] for r in old if r.get('mode')==x.get('mode') and r.get('seq')==x.get('seq') and r['check']=='preview.role'),None)
  suffix=k[len('preview.'):]
  suffix=suffix[:-len('.fields')]+'.keys' if suffix.endswith('.fields') else 'keys' if suffix=='fields' else suffix
  return ('Main.' if role==1 else 'nonMain.')+suffix
 if k.startswith(('file.safe:','file.bytes:','file.sha256:')): return k.replace(':','.',1)
 if k=='manifest.files.coverage': return 'manifest.coverage'
 if k in ('manifest.exitCode','manifest.completeFlag','manifest.timedOut','manifest.forcedTermination','manifest.verdict'): return k
 return None
mapped=[]
for n,x in enumerate(old):
 target=renamed(x); matches=index.get((x.get('mode'),x.get('seq'),target),[])
 # Historical non-observation checks have no seq, matching own manifest checks.
 evidence=[{'oracleRowIndex':i,'status':v['status'],'check':v['check']} for i,v in matches]
 classification='INFO_PRESERVED' if x['status']=='INFO' else 'INDEPENDENTLY_RECOMPUTED' if evidence and all(z['status']=='PASS' for z in evidence) else 'NOT_REASSERTED_BY_NEW_ORACLE'
 mapped.append(dict(historicalRowIndex=n,mode=x.get('mode'),seq=x.get('seq'),check=x['check'],historicalStatus=x['status'],classification=classification,oracleTarget=target,oracleEvidence=evidence))
counts=dict(collections.Counter(x['classification'] for x in mapped))
unmapped=collections.Counter(x['check'].split('.')[0].split(':')[0] for x in mapped if x['classification']=='NOT_REASSERTED_BY_NEW_ORACLE')
summary=dict(counts=counts,unmappedFamilies=unmapped,scope='Mapped means original check has separately calculated raw/asset/manifest assertion in new oracle; original status/expected/actual values are not used to compute oracle truth. Unmapped schema/source-presence, execution receipts, driver result and input claims remain coverage boundaries. INFO remains INFO. Auxiliary primitive selftests and static risk examples excluded from 15303 count.')
(O/'historical_oracle_mapping.json').write_text(json.dumps({'summary':summary,'mapping':mapped},ensure_ascii=False,indent=2)+chr(10),encoding='utf-8')
with (O/'historical_oracle_mapping.csv').open('x',encoding='utf-8-sig',newline='') as s:
 w=csv.DictWriter(s,fieldnames=list(mapped[0])); w.writeheader()
 for r in mapped: w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})
print(json.dumps(summary,ensure_ascii=False,indent=2))
