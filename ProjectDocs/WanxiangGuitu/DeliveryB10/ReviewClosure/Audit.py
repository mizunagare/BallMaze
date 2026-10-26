"""Read-only P0 source/evidence review; never launches Unity or reads player saves.

Run with an explicit fresh, external --output root. Historical runtime results
are inspected as historical evidence, never counted as new runtime passes.
"""
import argparse
import collections
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--project', required=True, type=Path)
p.add_argument('--output', required=True, type=Path)
a = p.parse_args()
repo = a.project.resolve(strict=True)
out = a.output.resolve()
if out.exists() or out.is_relative_to(repo) or 'locallow' in str(out).lower():
    raise ValueError('Fresh external audit output required')
out.mkdir(parents=True)
b = repo / 'ProjectDocs/WanxiangGuitu/DeliveryB10'

def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(data):
    return hashlib.sha256(data).hexdigest()

checks = []

def check(name, passed, details):
    checks.append(dict(name=name, status='PASS' if passed else 'FAIL',
                       scope='Current read-only source/evidence audit', details=details))

start = 'b474765dc9c28aaf7d2d267bc0362f828f1902b0'
frozen = '6cad42d535347e0d96ede0e40f3d6a889a846bab'
delivery = '9560b5bb68636fd7783810a6dc4bdead8ed934a3'
head = git('rev-parse', 'HEAD').decode().strip()
for old, new in [(start, frozen), (frozen, delivery), (delivery, head)]:
    rc = subprocess.run(['git', '-C', str(repo), 'merge-base', '--is-ancestor', old, new]).returncode
    check('ancestry:' + old[:8] + ':' + new[:8], rc == 0, dict(old=old, new=new, exitCode=rc))

protected = {
    'Assets/CombatPrototype/ForestRuins.unity': 'ebc46ce7104b6d6ce90b7f510a59a401d7cdf64ae8babc85a7ebbf881c9d16d4',
    'ProjectSettings/ProjectSettings.asset': '7d06ea8265edaaf0a1a7402cff1e94da015450c58899438ebf4a5d97e37fd451',
}
for name, expected in protected.items():
    actual = sha((repo / name).read_bytes())
    staged = git('diff', '--cached', '--name-only', '--', name).decode().strip()
    check('protected:' + name, actual == expected and not staged,
          dict(sha256=actual, expected=expected, staged=bool(staged)))

changed = git('diff', '--name-only', frozen, delivery, '--', 'Assets', 'Packages', 'ProjectSettings').decode().splitlines()
check('delivery-vs-frozen-product', not changed, dict(changed=changed, rule='Documentation delivery must not be called a new build input'))
sources = [n for n in git('ls-tree', '-r', '--name-only', frozen, '--', 'Assets/CombatPrototype').decode().splitlines()
           if n.endswith('.cs') and '/Editor/' not in n]
bad = []
for name in sources:
    old = git('show', frozen + ':' + name).replace(b'\r\n', b'\n')
    current = (repo / name).read_bytes().replace(b'\r\n', b'\n')
    if old != current:
        bad.append(name)
check('current-product-source-vs-frozen', not bad, dict(files=len(sources), differences=bad, normalization='CRLF to LF only'))

closure = load(b / 'Evidence/FinalAudit/closure-summary.json')
check('historical-input-link', closure['inputCommit'] == frozen, dict(input=closure['inputCommit'], historicalCounts=closure['mainCounts'], inheritedAsCurrentPass=False))
inv = load(b / 'ArtBible/ASSET_INVENTORY.json')
missing = []
for item in inv['assets']:
    for rel in item.get('unityPaths', []):
        if not (repo / rel).exists():
            missing.append(dict(asset=item['assetId'], path=rel))
    if not (b / item['conceptImage']).exists():
        missing.append(dict(asset=item['assetId'], concept=item['conceptImage']))
check('asset-reference-paths', not missing, dict(items=len(inv['assets']), missing=missing, statuses=dict(collections.Counter(i['status'] for i in inv['assets'])), provesVisualAcceptance=False))

entry = (repo / 'Assets/CombatPrototype/Editor/FantasySceneMenu.cs').read_text(encoding='utf-8-sig')
readme = (repo / 'README.md').read_text(encoding='utf-8-sig')
contradiction = 'Editor 调试可打开 `Assets/CombatPrototype/ForestRuins.unity` 并 Play，从营地' in readme
check('README-normal-Play-contract', 'playModeStartScene=GameEntry.EditorValidationEntry?null:boot' in entry and not contradiction,
      dict(ordinaryPlay='Boot -> Title -> explicit selection', legacyDirectPlayTextPresent=contradiction, source='Assets/CombatPrototype/Editor/FantasySceneMenu.cs:19'))

log = b / 'Evidence/FinalAll/ExistingFramework/B4Diagnostics/Normal-Bypass/Normal.log'
lines = log.read_text(encoding='utf-8-sig').splitlines()
i = next(i for i, line in enumerate(lines) if line.startswith('ArgumentOutOfRangeException:'))
j = i + 1
while j < len(lines) and lines[j].strip():
    j += 1
stack = lines[i:j]
check('Editor-Search-sample-call-chain', any('SearchDatabase+<EnumerateAll>' in line for line in stack)
      and any('SearchInit.IndexationOnStartup' in line for line in stack),
      dict(log=str(log.relative_to(repo)), line=i+1, fullExceptionBlock=stack, sha256=sha(log.read_bytes()),
           interpretation='Editor startup indexing stack; no product frame in this block. Does not prove no Editor impact or establish engine root cause.'))

unknown = []
for path in (repo / 'ProjectDocs/WanxiangGuitu/DeliveryUI01').rglob('*.log'):
    text = path.read_text(encoding='utf-8-sig', errors='replace')
    marker = 'Got a UNKNOWN while executing native code'
    k = text.find(marker)
    if k >= 0:
        unknown.append(dict(path=path.relative_to(repo).as_posix(), sha256=sha(path.read_bytes()),
                            context=text[max(0,k-350):k+len(marker)+350]))
        if len(unknown) == 3:
            break
check('historical-UNKNOWN-retained', bool(unknown), dict(samples=unknown, rootCause='UNRESOLVED', newExperiment=False))

result = dict(observedUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(), head=head,
              frozenInput=frozen, deliveryCommit=delivery, checks=checks,
              counts=dict(collections.Counter(x['status'] for x in checks)),
              runtime={'rules':'NOT_RUN','normalAI':'NOT_RUN','nondevelopmentBuild':'NOT_RUN',
                       'nativeUI':'NOT_RUN','humanPlay':'NOT_RUN','performanceBenchmark':'NOT_RUN'},
              scope='Evidence/source inspection only. Not independent ChatGPT approval, runtime rerun, native UI or human validation.')
(out / 'audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(dict(output=str(out), counts=result['counts'])))
raise SystemExit(1 if any(x['status']=='FAIL' for x in checks) else 0)
