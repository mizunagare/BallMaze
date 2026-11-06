import pathlib,json,hashlib,csv,math
ROOT=pathlib.Path('I:/WGCombat/C24-1106-A')
OUT=ROOT/'CombatMatrixAudit1'
if OUT.exists(): raise SystemExit('Fresh audit directory required')
OUT.mkdir()
checks=[];inputs=[]
def load(p):
    data=p.read_bytes();inputs.append({'path':str(p),'sha256':hashlib.sha256(data).hexdigest()});return data.decode('utf-8-sig')
def js(p):return json.loads(load(p))
def rows(p):return list(csv.reader(load(p).splitlines(),delimiter='\t'))
def check(name,ok,detail=None):checks.append(dict(name=name,status='PASS' if ok else 'FAIL',detail=detail))
def process(d):
    p=js(d/'process.json');check(d.name+'/process',p['exited'] and p['exitCode']==0 and not p['timedOut'])
    r=rows(d/'assertions.tsv');check(d.name+'/assertions',bool(r) and all(x[1]=='PASS' for x in r))
def vector(s):return [float(x) for x in s.strip('()').split(',')]
for phase,attack in [('p1','Claw'),('p1','Volley'),('p2','Claw'),('p2','Volley'),('p2','CrossLines'),('p2','HollowRing')]:
    outcomes=['hit','inner','outer'] if attack=='HollowRing' else ['hit','evade'];initials=[]
    for outcome in outcomes:
        d=ROOT/f'pair-{phase}-{attack}-{outcome}-A1';process(d);initials.append(js(d/'pair-initial.json'))
        rel=[r for r in rows(d/'pair-releases.tsv') if r[3]==attack and (r[4]=='True')==(phase=='p2')]
        hp=[r for r in rows(d/'pair-health.tsv') if r[2]=='Damage' and r[5]==attack]
        check(d.name+'/releases',len(rel)==(2 if attack=='CrossLines' else 1),rel)
        check(d.name+'/hp',len(hp)==(2 if attack=='CrossLines' else 1) if outcome=='hit' else len(hp)==0,hp)
        if attack=='CrossLines':check(d.name+'/two-distinct-subhits',[r[5] for r in rel]==['0','1'])
        if attack=='HollowRing' and rel:
            frames=rows(d/'pair-frames.tsv');f=next((r for r in frames if int(r[0])>=int(rel[0][0])),None)
            origin=vector(rel[0][6]);p=vector(f[7]);distance=math.hypot(p[0]-origin[0],p[2]-origin[2])
            check(d.name+'/release-zone',2.2<=distance<=6 if outcome=='hit' else distance<2.2 if outcome=='inner' else distance>6,dict(distance=distance,frame=f[0]))
    check(f'{phase}/{attack}/same-initial-position-and-hp',all(x['hero']==initials[0]['hero'] and x['boss']==initials[0]['boss'] and x['hp']==initials[0]['hp'] and x['bossHp']==initials[0]['bossHp'] for x in initials))
for weapon in [0,1,2,3,11,12,13]:process(ROOT/f'PlayerWeapon{weapon}A1')
for weapon in [0,1,11,12,13]:
    fixtures=[]
    for state in ['clear','block']:
        d=ROOT/f'weapon-{state}-{weapon}-A1';process(d);fixture=js(d/'pillar-fixture.json');fixture.pop('blocked');fixtures.append(fixture)
    check(f'weapon-{weapon}/same-pillar-pair-fixture',fixtures[0]==fixtures[1])
(OUT/'inputs.json').write_text(json.dumps(inputs,indent=2),encoding='utf-8')
(OUT/'results.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
summary={s:sum(c['status']==s for c in checks) for s in ['PASS','FAIL']}
summary['scope']='Read-only current raw run audit. Does not close windup A2/B2 INCOMPLETE or human readability.'
(OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary));raise SystemExit(1 if summary['FAIL'] else 0)
