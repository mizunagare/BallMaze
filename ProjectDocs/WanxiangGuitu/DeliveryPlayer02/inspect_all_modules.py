"""Supplement PE metadata with byte-aligned token checks in every built managed module."""
import argparse,hashlib,json
from pathlib import Path
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',required=True,type=Path);ap.add_argument('--output',required=True,type=Path);a=ap.parse_args()
 owner=json.loads((a.build/'owner.json').read_text(encoding='utf-8-sig'));assert owner['kind']=='BUILD-01 diagnostic using existing coordinator';assert owner['variant'] in ('Release','Acceptance')
 tokens=['PlayerAcceptanceDriver','-p02-mode','-p02-expect','PLAYER02 isolated acceptance driver'];modules=[]
 for p in sorted((a.build/'Results/Release/WanxiangGuitu_Data/Managed').glob('*.dll')):
  blob=p.read_bytes();hits=[t for t in tokens if t.encode() in blob or t.encode('utf-16-le') in blob]
  modules.append(dict(module=p.name,bytes=len(blob),sha256=hashlib.sha256(blob).hexdigest(),tokens=hits))
 matches=[m for m in modules if m['tokens']];assert modules
 passed=not matches if owner['variant']=='Release' else len(matches)==1 and matches[0]['module']=='Assembly-CSharp.dll' and set(matches[0]['tokens'])==set(tokens)
 result=dict(status='PASS' if passed else 'FAIL',variant=owner['variant'],modules=modules,toolSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scope='Read-only all managed modules raw UTF8/UTF16LE substring scan; pair with PE type/reference and source/scene proofs')
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(dict(status=result['status'],variant=owner['variant'],modules=len(modules),matched=[m['module'] for m in matches])))
 if not passed:raise SystemExit(1)
if __name__=='__main__':main()
