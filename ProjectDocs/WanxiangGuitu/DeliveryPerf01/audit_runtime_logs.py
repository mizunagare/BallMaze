"""Index complete runtime diagnostics separately from BuildReport and from frame metrics."""
import argparse,collections,json,re
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();rows=[]
 patterns={'URP-feature-shader-unavailable':r"Shader '.*(?:not supported|stripped)", 'exception':r'\b\w*Exception\b','native-unknown':r'Got a UNKNOWN while executing native code','JobTempAlloc':r'JobTempAlloc|JobTempMemory|JobTempAllocs','runtime-error':r'\b(?:ERROR|Error:)'}
 for f in sorted((a.root/'Runtime/Attempts').glob('*/player.log')):
  lines=f.read_text(encoding='utf-8-sig',errors='replace').splitlines()
  for i,line in enumerate(lines):
   for category,pattern in patterns.items():
    if re.search(pattern,line):rows.append(dict(file=str(f.relative_to(a.root)),line=i+1,category=category,text=line,context=lines[max(0,i-2):i+4],status='UNRESOLVED',scope='Observed raw runtime diagnostic; not one of 91 BuildReport warnings, not causal proof of product defect or performance bottleneck'))
 a.output.write_text(json.dumps(dict(findings=rows,counts=dict(collections.Counter(x['category'] for x in rows)),note='Absence of a target diagnostic in this D3D11 sample does not close historic D3D12/Editor issues. All full logs retained, no filtering in raw evidence.'),ensure_ascii=False,indent=2),encoding='utf-8')
 print(dict(collections.Counter(x['category'] for x in rows)))
if __name__=='__main__':main()
