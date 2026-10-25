"""Check ended controlled clock runs against explicit Git product/test inputs."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--project', type=Path, required=True)
p.add_argument('--before', type=Path, required=True)
p.add_argument('--after', type=Path, required=True)
p.add_argument('--entry', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def source(root):
    path = root / 'Project/Assets/CombatPrototype/Editor/B06LocalChecks/B08CampPause.cs'
    raw = path.read_bytes()
    return dict(sha256=hashlib.sha256(raw).hexdigest(), normalizedSha256=hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest())
def git(commit):
    raw = subprocess.check_output(['git', '-C', str(a.project), 'show', commit + ':ProjectDocs/WanxiangGuitu/DeliveryB08/Tests/B08CampPause.cs.txt'])
    return hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()
test_commit = 'c7ae847b3f9121236cb5521d4c8fb4a9bc896c05'
entry_commit = 'dcded5b174285550e3fe34506ccf19881c68f939'
b, c, e = source(a.before), source(a.after), source(a.entry)
expected = git(test_commit)
same = b['normalizedSha256'] == c['normalizedSha256'] == expected
def result(root):
    rows = read(root / 'results.json')
    if isinstance(rows, dict):
        rows = [rows]
    return next(r for r in rows if r['name'] == 'B08CampPause.Run')
br, cr, er = map(result, [a.before, a.after, a.entry])
before = read(a.before / 'Rules/b08-camp-clock.json')
after = read(a.after / 'Rules/b08-camp-clock.json')
keys = ['skill', 'attack', 'swap', 'dodge', 'potion']
advanced = all(before[k + 'Before'] > before[k + 'After'] + .1 for k in keys)
paused = all(after[k + 'Before'] == after[k + 'After'] for k in keys)
ok = same and e['normalizedSha256'] == git(entry_commit) and advanced and paused and after['moved'] > .015 and after['elapsed'] == 0 and br['exitCode'] == 1 and cr['exitCode'] == 0 and not br['timedOut'] and not cr['timedOut']
if a.output.exists():
    raise ValueError('Fresh audit output required')
a.output.write_text(json.dumps(dict(status='PASS' if ok else 'FAIL',
    scope='Ended controlled clock fixture and common test-source identity; not native input',
    productBefore='4d48e6e0f0aad67e501f059f9bc5c5053d8eda4b', productAfter=test_commit,
    testCommit=test_commit, beforeTest=b, afterTest=c, commonTestNormalizedSha256=expected,
    sameTest=same, before=before, after=after,
    entryFailure=dict(exitCode=er['exitCode'], timedOut=er['timedOut'], testCommit=entry_commit,
                      source=e, note='Fixture own deadline waiting for initialization intentionally disabled by batch startup; no product conclusion'),
    note='Before product seal deliberately lists one unmatched injected source because the regression postdates that product commit. The common regression is separately verified against its actual test commit here.'),
    ensure_ascii=False, indent=2) + '\n', encoding='utf8')
print(json.dumps(dict(status='PASS' if ok else 'FAIL', sameTest=same, beforeAdvanced=advanced, afterPaused=paused)))
raise SystemExit(0 if ok else 1)
