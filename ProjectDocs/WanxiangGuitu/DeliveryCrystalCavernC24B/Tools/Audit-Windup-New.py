"""Audit A2/B2 only. Missing source attribution cannot be inferred from frame equality."""
import csv, hashlib, json, pathlib, sys
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p): return list(csv.reader(p.open(encoding='utf-8-sig'),delimiter='\t'))
def js(p): return json.loads(p.read_text(encoding='utf-8-sig'))
source,out=map(pathlib.Path,sys.argv[1:3]);out.mkdir(exist_ok=False)
results=[]
for name,cross in [('PlayerWindupA2',False),('PlayerWindupB2',True)]:
    p=source/name
    files=sorted(p.glob('windup-*'))+[p/'Player.command.json',p/'Player.exit.json',p/'process.json',p/'cavern-test.txt']
    command=js(p/'Player.command.json');exit_receipt=js(p/'Player.exit.json')
    assert command['hostPid']==exit_receipt['hostPid']
    assert name in ' '.join(command['arguments'])
    assert (p/'cavern-test.txt').read_text().strip()==('windup-b' if cross else 'windup-a')
    summary=js(p/'windup-summary.json');timeline=rows(p/'windup-timeline.tsv')
    release=rows(p/'windup-release.tsv');boss=rows(p/'windup-health.tsv');hero=rows(p/'windup-hero-health.tsv')
    assert len(release)==1
    r=release[0];warning=float(timeline[0][1]);released=float(r[1])
    damage=[v for v in boss if v[2]=='Damage' and warning<=float(v[1])<released]
    threshold= len(damage)==1 and (float(damage[0][3])>180>=float(damage[0][4]) if cross else float(damage[0][4])>180)
    locked=[v for v in timeline if v[2]=='Warning' and float(v[4])<=.75]
    before=[v for v in timeline if float(v[1])<released][-1]
    after=next(v for v in timeline if float(v[1])>=released)
    # No fitted tolerance: bracket the deadline in the actual adjacent frames.
    deadline=summary['deadline']
    timing=float(before[1])<=deadline<=released and float(after[1])==released
    direction=bool(locked) and all(v[5]==r[7] for v in locked)
    player_damage=[v for v in hero if v[2]=='Damage']
    transition=rows(p/'windup-transition.tsv') if (p/'windup-transition.tsv').exists() else []
    result=dict(sample=name,runIdentity=command,process=exit_receipt,
        inputs=[dict(path=str(f),sha256=sha(f)) for f in files],
        checks=dict(bossThreshold='PASS' if threshold else 'FAIL',
            releaseFrameBracket='PASS' if timing else 'FAIL',
            recordedDirection='PASS' if direction else 'FAIL',
            playerDamageAttribution='INCOMPLETE',recoveryTransitionOrder='INCOMPLETE'),
        observed=dict(bossDamage=damage,playerDamage=player_damage,release=r,
            warning=warning,warningToRelease=released-warning,deadline=deadline,
            previousFrame=before,releaseFrame=after,transition=transition,
            releaseToTransition=float(transition[0][1])-released if transition else None),
        limitations=['Hero Damage has no shared attackId; matching frame alone does not exclude other sources.',
            'Direction vectors serialized to two decimals; subprecision turning is not established.',
            'B summary recoveryObserved and transition were assigned together by driver, not independent events.',
            'Recovery-to-Transition adjacent states observed, but no ordered recovery-end event recorded.'],
        status='FAIL' if not(threshold and timing and direction) else 'INCOMPLETE')
    results.append(result)
report=dict(scope='P1 Claw crossing half-health only',toolVersion='2.0',toolSHA256=sha(pathlib.Path(__file__)),samples=results,status='FAIL' if any(r['status']=='FAIL' for r in results) else 'INCOMPLETE')
dest=out/'audit.json';dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
assert js(dest)==report
sys.exit(1 if report['status']=='FAIL' else 3)
