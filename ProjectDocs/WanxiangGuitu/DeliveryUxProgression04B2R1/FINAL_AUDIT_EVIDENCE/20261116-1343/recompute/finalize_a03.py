from pathlib import Path
import json,csv,hashlib,collections,ast,struct
R=Path.cwd(); O=Path(__file__).parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
hist=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/EVIDENCE/recompute-A03'
h=read(hist/'details.json')['checks']; groups={}
for x in h:
 mode=x.get('mode','asset/session/global')
 groups.setdefault(mode,collections.Counter())[x['status']]+=1
counts=collections.Counter(x['status'] for x in h)
result={'totalRows':len(h),'counts':{k:counts[k] for k in ('PASS','FAIL','INFO')},'byModeIncludingGlobal':{k:{s:v[s] for s in ('PASS','FAIL','INFO')} for k,v in groups.items()},'globalRows':[x for x in h if 'mode' not in x],'correction':'historical_classification.json byMode asset/session empty bucket omitted 14 unscoped checks; full counts were correct. This new report explicitly includes those 14 global PASS rows; no old evidence changed.'}
(O/'historical_recount_complete.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+chr(10),encoding='utf-8')
inputs=[hist/'details.json',hist/'checks.csv',hist/'summary.json',hist.parent.parent/'Tools/recompute_r1.py',R/'Assets/CombatPrototype/B2AttackModel.cs',R/'Assets/CombatPrototype/AdventureLoadout.cs']+list((R/'Evidence/Runs04B2R1/SESSION-20261116-1115/A03').glob('*/run-manifest.json'))
hashes=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in inputs]
(O/'oracle_additional_source_sha256.json').write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+chr(10),encoding='utf-8')
# Test freshly written oracle primitives without running its report side effects.
source=ast.parse((O/'independent_oracle.py').read_text(encoding='utf-8'))
allowed={'f','bit','plus','times','accum','units','fnv','same'}
ns={'struct':struct}; exec(compile(ast.Module(body=[n for n in source.body if isinstance(n,ast.FunctionDef) and n.name in allowed],type_ignores=[]),'<oracle-primitives>','exec'),ns)
tests=[]
def test(name,e,a): tests.append(dict(check=name,expected=e,actual=a,status='PASS' if e==a else 'FAIL'))
test('empty-FNV-offset','cbf29ce484222325',ns['fnv'](''))
test('ASCII-a-known-FNV','af63dc4c8601ec8c',ns['fnv']('a'))
test('astral-UTF16-units',(55357,56832),ns['units'](chr(0x1f600)))
test('binary32-0.1-bits','cdcccc3d',ns['bit'](.1))
test('binary32-0.1plus0.2-bits','9a99993e',ns['bit'](ns['plus'](.1,.2)))
test('spear-power',60.0,ns['times'](48.,1.25))
(O/'oracle_primitive_tests.json').write_text(json.dumps(tests,ensure_ascii=False,indent=2)+chr(10),encoding='utf-8')
print(json.dumps({'historical':result['counts'],'global':result['byModeIncludingGlobal']['asset/session/global'],'primitiveTests':tests},ensure_ascii=False,indent=2))
