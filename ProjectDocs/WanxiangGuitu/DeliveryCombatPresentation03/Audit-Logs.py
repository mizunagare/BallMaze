from pathlib import Path
import re,json,sys
root=Path(sys.argv[1]);rows=[]
for p in sorted(root.glob('*/*.log')):
 lines=p.read_text(encoding='utf-8-sig',errors='replace').splitlines();events=[]
 for i,line in enumerate(lines):
  if re.search(r'Exception:|error CS\d+|Got a UNKNOWN|JobTempAlloc',line):
   context='\n'.join(lines[max(0,i-2):i+15]);kind='compiler/tool' if re.search(r'error CS\d+',line) else 'exception/unclassified'
   if 'UnityEditor.Search.' in context:kind='UnityEditor.Search history root UNRESOLVED'
   elif 'JobTempAlloc' in context:kind='JobTempAlloc history root UNRESOLVED'
   elif 'Got a UNKNOWN' in context:kind='UNKNOWN UNRESOLVED'
   events.append(dict(line=i+1,kind=kind,context=context))
 rows.append(dict(path=p.relative_to(root).as_posix(),events=events))
(root/'log-analysis.json').write_text(json.dumps(dict(scope='Raw exception index, no clean-exit claim or log filtering; original process results unchanged',logs=rows),ensure_ascii=False,indent=2),encoding='utf-8')
print('indexed',sum(len(x['events']) for x in rows),'events in',len(rows),'logs')
