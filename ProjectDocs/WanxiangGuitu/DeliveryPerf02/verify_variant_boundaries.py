"""Exact custom-type expectations using existing PLAYER02 metadata, no build mutation."""
import argparse,json
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();rows=[]
 for variant in 'ABC':
  d=json.loads((a.root/'BuildProof'/f'{variant}-pe.json').read_text(encoding='utf-8-sig'));types=[t.lstrip('.') for t in d['types']];checks={'P02Present':'PlayerAcceptanceDriver' in types,'FullSampler':'PerfSampler' in types,'MinimalSampler':'Perf02Minimal' in types,'Probe':'Perf02Probe' in types,'Dxgi':'Perf02Dxgi' in types,'NoEditorReference':not any(x.startswith('UnityEditor') for x in d['assemblyReferences'])};expected={'A':(False,False,False,False),'B':(False,True,False,False),'C':(True,False,True,True)}[variant]
  assert tuple(checks[k] for k in ['FullSampler','MinimalSampler','Probe','Dxgi'])==expected and checks['P02Present'] and checks['NoEditorReference']
  rows.append(dict(variant=variant,status='PASS',checks=checks,hashes=d['hashes'],buildResult=d['buildResult'],warnings=d['warnings'],errors=d['errors']))
 out=dict(status='PASS',rows=rows,normalization='Strip only leading empty-namespace dot from existing reader, exact custom type expectations unchanged',scope='All temporary acceptance builds, not unobserved release; common P02/boundary harness remains in all')
 (a.root/'BuildProof/variant-boundaries-rechecked.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('Variant boundaries PASS')
if __name__=='__main__':main()
