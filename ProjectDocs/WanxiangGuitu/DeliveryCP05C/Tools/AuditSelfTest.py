from pathlib import Path
import json,runpy,sys
m=runpy.run_path(str(Path(__file__).with_name('Audit.py')));repo=m['repo'];names=['AdventureItems.cs','AdventureRandom.cs','CombatEnemy.cs'];data={n:(repo/'Assets/CombatPrototype'/n).read_text(encoding='utf-8-sig') for n in names};rows=[]
def test(name,mutate,expected):
 d=data.copy();mutate(d);errors=m['source_checks'](d);ok=(not errors)==expected;rows.append(dict(name=name,status='PASS' if ok else 'FAIL',expectedAccepted=expected,errors=errors))
def replace(n,a,b):
 def f(d):
  assert d[n].count(a)==1,(n,a);d[n]=d[n].replace(a,b)
 return f
test('exact-current-control',lambda d:None,True)
test('quality-threshold-tamper',replace('AdventureItems.cs','.005f + luck * .1f','.015f + luck * .1f'),False)
test('formal-luck-tamper',replace('AdventureItems.cs','wave * .004f','wave * .005f'),False)
test('training-luck-tamper',replace('AdventureItems.cs','Value(owner:owner),0,false,false','Value(owner:owner),.2f,false,false'),False)
test('formal-drop-wave-tamper',replace('CombatEnemy.cs','ByType<CombatSession>().Wave','ByType<CombatSession>().Wave+1'),False)
test('drop-extra-draw',replace('CombatEnemy.cs','DropLootCore(training);','DropLootCore(training); AdventureRandom.Value(owner:this);'),False)
test('random-fallback-tamper',replace('AdventureRandom.cs','return training.Streams;','return null;'),False)
test('extra-item-business',replace('AdventureItems.cs','public const int BagWidth = 12','public const int BagWidth = 13'),False)
Path(sys.argv[1]).write_text(json.dumps(dict(rows=rows),indent=2),encoding='utf8');print(json.dumps(rows));sys.exit(any(r['status']=='FAIL' for r in rows))
