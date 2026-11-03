from pathlib import Path
import json,hashlib,re,sys
root=Path(__file__).resolve().parents[1];errors=[];count=0
for stage in ('B1','B2','B3'):
 folder=root/'Evidence'/stage
 for r in json.loads((folder/'manifest.json').read_text(encoding='utf-8-sig')):
  f=folder/r['path'];count+=1
  if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=r['publishedSHA256']:errors.append(str(f))
for md in root.glob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',md.read_text(encoding='utf-8-sig')):
  if '://' not in target and not (md.parent/target.split('#')[0]).exists():errors.append('Missing link: '+str(md)+':'+target)
report={'status':'FAIL' if errors else 'PASS','publishedArtifactsChecked':count,'errors':errors}
Path(sys.argv[1]).write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2));sys.exit(bool(errors))
