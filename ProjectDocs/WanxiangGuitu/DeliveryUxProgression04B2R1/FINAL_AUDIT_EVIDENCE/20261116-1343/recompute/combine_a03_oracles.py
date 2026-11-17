from pathlib import Path
import json,csv,collections
O=Path(__file__).parent
read=lambda name:json.loads((O/name).read_text(encoding='utf-8-sig'))
numeric=read('oracle_details.json'); structural=read('supplemental_structure_details.json'); prior=read('historical_oracle_mapping.json')['mapping']; supplement={r['historicalRowIndex']:r for r in read('supplemental_structure_mapping.json')}
merged=[]
for old in prior:
 n=old['historicalRowIndex']; entries=old['oracleEvidence']; source='oracle_details.json'; data=numeric
 if old['classification']=='NOT_REASSERTED_BY_NEW_ORACLE': entries=supplement[n]['evidence']; source='supplemental_structure_details.json'; data=structural
 if not entries and old['classification']=='INFO_PRESERVED': entries=[dict(oracleRowIndex=i,status=r['status']) for i,r in enumerate(numeric) if r.get('mode')==old.get('mode') and r.get('seq')==old.get('seq') and r['check']==old['check']]
 if not entries: raise RuntimeError('No independent evidence for old row '+str(n))
 newrows=[data[r['oracleRowIndex']] for r in entries]; statuses={r['status'] for r in newrows}
 if len(statuses)!=1: raise RuntimeError('Inconsistent independent evidence')
 status=next(iter(statuses))
 merged.append(dict(historicalRowIndex=n,mode=old.get('mode'),seq=old.get('seq'),historicalCheck=old['check'],independentStatus=status,source=source,evidence=entries))
counts=collections.Counter(r['independentStatus'] for r in merged)
assert len(merged)==23211 and counts=={'PASS':23191,'INFO':20}
assert len({r['historicalRowIndex'] for r in merged})==23211
allcounts=collections.Counter(r['status'] for r in numeric+structural)
summary=dict(originalRowCoverage=23211,independentlyReassertedOriginalCounts={k:counts[k] for k in ('PASS','FAIL','INFO')},newOracleAllAssertions={k:allcounts[k] for k in ('PASS','FAIL','INFO')},numericalOracleMappedOriginalPASS=15298,structuralSupplementMappedOriginalPASS=7893,unmappedOriginalRows=0,extraCrossCountAssertions=5,infoNeverPass=True,limitations=['Supplied Inventory canonical UTF16 plaintext is hashed and checked read-only, but full Inventory raw fields are absent: independent canonical reconstruction remains impossible.','Current assets do not by themselves prove built Player provenance.','Non-Main container first-worn replacement numerical risk remains; C06 only read-only.'],auxiliaryNotIncluded={'primitiveTestsPASS':6,'staticRiskINFOExamples':2})
for name,data in [('A03_COMBINED_SUMMARY.json',summary),('A03_COMPLETE_ORIGINAL_CHECK_MAPPING.json',merged)]:
 p=O/name
 if p.exists(): raise RuntimeError('Refuse overwrite')
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+chr(10),encoding='utf-8')
with (O/'A03_COMPLETE_ORIGINAL_CHECK_MAPPING.csv').open('x',encoding='utf-8-sig',newline='') as s:
 w=csv.DictWriter(s,fieldnames=list(merged[0])); w.writeheader()
 for r in merged: w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()})
print(json.dumps(summary,ensure_ascii=False,indent=2))
