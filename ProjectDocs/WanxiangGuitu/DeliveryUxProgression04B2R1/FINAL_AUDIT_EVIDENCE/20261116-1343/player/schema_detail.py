import json,pathlib
r=pathlib.Path('Evidence/Runs04B2R1/SESSION-20261116-1115/A03')
def jl(p):return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
for m in ['strength3','sort-ugui','preview9','restart']:
 rows=jl(r/m/'r1-observations.jsonl')
 print(m)
 for o in rows:
  if o['stage'] in ['strength','preview9','sort','restart']:
   print('flow',o['flow'],'extra keys',list(o.keys())[26:]);
   if o['flow'] in ['ugui-AttackDesc','role-Main']:print(json.dumps({k:v for k,v in o.items() if k not in ['raw','note','canonicalBeforeJson','canonicalAfterJson']},ensure_ascii=False)[:1600])
 print('raw sample',json.dumps({k:v for k,v in rows[-1]['raw'].items() if k not in ['items','warehouse','canonical']},ensure_ascii=False)[:2000])
 print('checks',[(d['name'],d['detail'][:100]) for d in json.loads((r/m/'result.json').read_text(encoding='utf-8-sig'))['detail']])
print('collection first snapshot other', {k:v for k,v in jl(r/'collection'/'r1-state-changes.jsonl')[0]['before'].items() if k!='raw'})
print('restart state',json.dumps(jl(r/'restart'/'r1-state-changes.jsonl')[0],ensure_ascii=False)[-1800:])
print('restart manifest input',json.loads((r/'restart'/'run-manifest.json').read_text(encoding='utf-8-sig'))['restartInput'])
