from pathlib import Path
import json,collections
r=Path.cwd(); out=Path(__file__).parent
rows=[]
for p in sorted((r/'Evidence/Runs04B2R1/SESSION-20261116-1115/A03').glob('*/r1-observations.jsonl')):
 obs=[json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
 rows.append({'mode':p.parent.name,'count':len(obs),'stages':dict(collections.Counter(o['stage'] for o in obs)),'special':[{'seq':o['seq'],'stage':o['stage'],'keys':list(o),'eval':json.loads(o['evaluationJson']) if isinstance(o.get('evaluationJson'),str) else o.get('evaluationJson'),'spec':o.get('spec'),'FilterKey':o.get('FilterKey'),'rawkeys':list(o.get('raw',{}))} for o in obs if 'evaluationJson' in o or o['stage']=='sort'][:3]})
(out/'raw_schema.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{k:v for k,v in x.items() if k!='special'} for x in rows]))
