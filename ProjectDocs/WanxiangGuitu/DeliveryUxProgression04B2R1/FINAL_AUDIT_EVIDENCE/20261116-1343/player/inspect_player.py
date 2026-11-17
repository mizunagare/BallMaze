import json,pathlib
r=pathlib.Path('Evidence/Runs04B2R1/SESSION-20261116-1115/A03')
for m in sorted(x for x in r.iterdir() if x.is_dir()):
 print('MODE',m.name)
 mf=json.loads((m/'run-manifest.json').read_text(encoding='utf-8-sig'));print('MANIFEST',{k:v for k,v in mf.items() if k not in ['files','result']})
 for n in ['r1-observations.jsonl','r1-state-changes.jsonl']:
  rows=[json.loads(l) for l in (m/n).read_text(encoding='utf-8-sig').splitlines() if l.strip()]
  print(n,'count',len(rows))
  if rows:
   print('SCHEMA',list(rows[min(1,len(rows)-1)]));print('RAW SCHEMA',list(rows[min(1,len(rows)-1)].get('raw',{})))
  for i,o in enumerate(rows):
   if n=='r1-state-changes.jsonl':
    print(i+1,o.get('tag'),'keys',list(o),'before keys',list(o.get('before',{})), 'before raw keys',list(o.get('before',{}).get('raw',{})))
   else: print(i+1,{k:v for k,v in o.items() if k!='raw'})
