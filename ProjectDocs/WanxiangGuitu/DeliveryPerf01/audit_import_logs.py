"""Import-time diagnostics stay separate from the 91 BuildReport warnings. Read-only."""
import argparse,json,re
from pathlib import Path
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',required=True,type=Path);ap.add_argument('--output',required=True,type=Path);a=ap.parse_args();rows=[]
 patterns={'JobTempAlloc':r'JobTempAlloc|JobTempMemory|JobTempAllocs','Editor.Search':r'UnityEditor.Search|UnityEditor\.Search','native-target-extension':r'Native extension for .* target not found','assembly-hint-path':r'duplicate hint path','directory-exception':r'DirectoryNotFoundException','native-unknown':r'Got a UNKNOWN while executing native code'}
 for log in sorted(a.root.glob('**/Results/Build01Audit.Run.log')):
  lines=log.read_text(encoding='utf-8-sig',errors='replace').splitlines()
  for n,line in enumerate(lines):
   for category,pattern in patterns.items():
    if re.search(pattern,line):rows.append(dict(log=str(log),line=n+1,category=category,text=line,context=lines[max(0,n-3):n+7],status='UNRESOLVED' if category in ['JobTempAlloc','Editor.Search','directory-exception','native-unknown'] else 'OBSERVED_INFORMATION',scope='Editor import/build log only; not part of 91 release BuildReport warnings; no product root-cause inference'))
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(dict(findings=rows,counts={c:sum(x['category']==c for x in rows) for c in patterns},scope='Raw full logs retained; this is a separate diagnostic index, not filtering'),ensure_ascii=False,indent=2),encoding='utf-8');print('import diagnostic findings',len(rows))
if __name__=='__main__':main()
