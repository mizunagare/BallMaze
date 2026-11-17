"""Verify all pre-FIX originals and unchanged protected calculator methods."""
from pathlib import Path
import json,csv,hashlib,subprocess,argparse
R=Path.cwd();D=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX';S=Path('I:/unity/WanxiangGuitu-UX04B2R2FIX-snapshot-20261116-1536')
ALLOWED={'Assets/CombatPrototype/B2AttackModel.cs':'ComputeAttack authorized precision restoration + pure replacement preview','Assets/CombatPrototype/AdventureLoadout.cs':'shared geometry/transaction preview helpers','Assets/CombatPrototype/CatInventoryPresenter.cs':'explicit read-only preview UI','Assets/CombatPrototype/ContainerInventoryView.cs':'shared explicit preview workspace'}
def xp(p):return Path(chr(92)*2+'?'+chr(92)+str(p.absolute()))
def info(p):
 p=xp(p)
 if not p.is_file():return 'MISSING',None
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest(),p.stat().st_size

def method(data,signature):
 start=data.index(signature);i=data.index(b'{',start);depth=1;j=i+1
 while depth:
  if data[j:j+1]==b'{':depth+=1
  elif data[j:j+1]==b'}':depth-=1
  j+=1
 return data[start:j]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=R/a.out;assert not out.exists();out.mkdir(parents=True)
 base=json.loads((S/'PRECHANGE_FIX_SHA256.json').read_text(encoding='utf-8'))['files'];rows=[];errors=[];authorized=[]
 for b in base:
  cur=info(R/b['path']);snap=info(S/'workspace'/b['path']);same=cur==(b['sha256'],b['bytes']);snapok=snap==(b['sha256'],b['bytes']);allow=b['path'] in ALLOWED
  status='UNCHANGED' if same else 'AUTHORIZED_FIX_EDIT' if allow else 'UNAUTHORIZED_CHANGE'
  row={'path':b['path'],'baselineSHA256':b['sha256'],'baselineBytes':b['bytes'],'snapshotSHA256':snap[0],'snapshotBytes':snap[1],'currentSHA256':cur[0],'currentBytes':cur[1],'classification':status,'scope':ALLOWED.get(b['path'],'PROTECTED')};rows.append(row)
  if not snapok or (not same and not allow) or cur[0]=='MISSING':errors.append(row)
  if not same and allow:authorized.append(b['path'])
 p=out/'PROTECTION_SHA256.tsv'
 with p.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0],delimiter='\t');w.writeheader();w.writerows(rows)
 source=Path('Assets/CombatPrototype/B2AttackModel.cs');before=(S/'workspace'/source).read_bytes();now=(R/source).read_bytes();guard={}
 for name in [b'public static float ComputeDefense',b'public static IEnumerable<GearItem> Active']:
  left=method(before,name);right=method(now,name);guard[name.decode()]={'byteIdentical':left==right,'beforeSHA256':hashlib.sha256(left).hexdigest(),'afterSHA256':hashlib.sha256(right).hexdigest()}
 if not all(x['byteIdentical'] for x in guard.values()):errors.append({'protectedMethods':guard})
 attack=method(now,b'public static float ComputeAttack');attackOK=b'Active(list, mainId).Sum(i => i.Attack)' in attack and b'i.Defense' not in attack and b'foreach' not in attack
 g=lambda *x:subprocess.run(['git',*x],capture_output=True,text=True)
 frozenPaths=['ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/SUBMIT_WHITELIST.txt','ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/SUBMIT_WHITELIST.csv']
 frozenUnchanged=all(info(R/p)==info(S/'workspace'/p) for p in frozenPaths)
 summary={'baselineFileCount':len(rows),'authorizedProductEdits':authorized,'errors':errors,'methodGuards':guard,'computeAttackRestoredSingleChain':attackOK,'historical961ListFilesByteIdentical':frozenUnchanged,'head':g('rev-parse','HEAD').stdout.strip(),'branch':g('branch','--show-current').stdout.strip(),'staged':g('diff','--cached','--name-status').stdout.strip(),'diffCheckExitCode':g('diff','--check').returncode,'result':'PASS' if not errors and frozenUnchanged and attackOK else 'FAIL'}
 (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(summary,ensure_ascii=False,indent=2));raise SystemExit(summary['result']!='PASS')
if __name__=='__main__':main()
