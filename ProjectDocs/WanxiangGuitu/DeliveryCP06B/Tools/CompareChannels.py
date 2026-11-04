from pathlib import Path
import json,sys
a=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8-sig'));b=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8-sig'));out=Path(sys.argv[3]);keys=['run','region','entity','content','seed','before','after','xpBefore','xpAfter'];different=[k for k in keys if a[k]!=b[k]]
def canonical(d):return sorted(json.dumps({k:v for k,v in x.items() if k!='actualID'},sort_keys=True,separators=(',',':')) for x in d['legacy'])
legacy=canonical(a)==canonical(b);globals_ok=a['globalBefore']==a['globalAfter'] and b['globalBefore']==b['globalAfter'];valid=not different and legacy and globals_ok and a['additional']==0 and b['additional']==1
result=dict(status='PASS' if valid else 'FAIL',different=different,legacyMultisetIdentical=legacy,globalInvariant=globals_ok,controlAdditional=a['additional'],normalAdditional=b['additional'],scope='Exact old drop payload multiset and RNG checkpoints. FindObjectsByType order is not spawn order. Only newly generated UUID fields excluded, all raw UUIDs retained. No data or tolerances changed.')
out.write_text(json.dumps(result,indent=2),encoding='utf-8');print(result);sys.exit(not valid)
