from pathlib import Path
import json,hashlib,re,sys
root=Path(__file__).resolve().parents[1];errors=[];manifest=json.loads((root/'Evidence/manifest.json').read_text(encoding='utf8'))
for row in manifest:
 f=root/'Evidence'/row['path']
 if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=row['publishedSHA256']:errors.append('Artifact mismatch: '+row['path'])
for f in list(root.glob('*.md'))+[root/'Evidence/INDEX.md']:
 for target in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8-sig')):
  if '://' not in target and not (f.parent/target.split('#')[0]).exists():errors.append('Missing link '+str(f)+':'+target)
r={'status':'FAIL' if errors else 'PASS','checkedArtifacts':len(manifest),'errors':errors};Path(sys.argv[1]).write_text(json.dumps(r,indent=2),encoding='utf8');print(json.dumps(r,indent=2));sys.exit(bool(errors))
