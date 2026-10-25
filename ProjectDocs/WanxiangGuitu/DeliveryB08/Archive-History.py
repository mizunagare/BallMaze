"""Publish explicit B08 attempt roots; preserve all failures separately from final All."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--test-root', type=Path, required=True)
p.add_argument('--target', type=Path, required=True)
a = p.parse_args()
here = Path(__file__).resolve().parent
if a.target.exists():
    p.error('Fresh history directory required')
attempts = [
 ('Before', 'B08Before/20261025-170305-767c88b7', 'Actual missing-contract regression; product source is baseline 638dd9b.'),
 ('Directed1', 'B08Directed1/20261025-171540-7fcac9c7', 'Old-v9 absent tutorial fields materialized by JsonUtility; FAIL retained.'),
 ('Directed2', 'B08Directed2/20261025-172123-1201d04e', 'Post-publish settings comparison treated absent Run as null; FAIL retained.'),
 ('Directed3', 'B08Directed3/20261025-172558-2f89a154', 'Four controlled PASS; normal movement stage deadline FAIL; no forced termination.'),
 ('Directed4', 'B08Directed4/20261025-173304-2e4f7f79', 'CoreCLR/GC initialization tool/environment failure and 150% label visibility FAIL. Cause of GC failure not established.'),
 ('Directed5', 'B08Directed5/20261025-174145-6dec3a7b', 'Eight controlled PASS; normal low-rock bow gather deadline FAIL. Project later reused; do not treat current project as original. PreviousSources in Incremental6 freezes its ended source.'),
 ('Incremental6', 'B08Incremental6', 'Reused ended project. Eight controlled PASS, owned-path tool guard rejected cross-run handoff; subsequent separate normal wrapper Normal PASS / Resume FAIL due snapshot exit ordering. All retained.'),
 ('Normal7', 'B08Normal7', 'Fresh synthetic save; reused ended project, not clean import. Three normal processes PASS after canonical region.Capture snapshot. Sources frozen at launch.')]
records = []
for label, relative, note in attempts:
    root = (a.test_root / relative).resolve(strict=True)
    if not root.is_relative_to(a.test_root.resolve(strict=True)):
        raise ValueError('Outside explicit test root')
    if not (root / 'owner.json').is_file():
        raise ValueError('Missing synthetic-run owner')
    target = a.target / label
    subprocess.run([sys.executable, '-B', str(here / 'Publish-Evidence.py'), '--run', str(root), '--target', str(target)], check=True)
    if label in {'Directed1', 'Directed2', 'Directed3', 'Directed4'}:
        # These projects were never reused. End-of-attempt runtime sources only;
        # actual Editor test drivers have their separate executed-source records.
        manifest = target / 'b08-sources.json'
        sources = json.loads(manifest.read_text(encoding='utf8'))
        for item in sorted((root / 'Project/Assets/CombatPrototype').glob('*.cs')):
            raw = item.read_bytes()
            relative = Path('B08Sources/EndOfAttemptRuntime') / (item.name + '.txt')
            output = target / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(raw)
            sources.append(dict(file=relative.as_posix(), sha256=hashlib.sha256(raw).hexdigest(),
                                bytes=len(raw), scope='Post-run runtime source from never-reused attempt; not a Git/assembly equality claim'))
        manifest.write_text(json.dumps(sources, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    result = json.loads((root / 'results.json').read_text(encoding='utf-8-sig'))
    records.append(dict(label=label, run=str(root), note=note,
                        results=[{k: r.get(k) for k in ['name', 'status', 'exitCode', 'timedOut', 'reason']} for r in result]))
(a.target / 'attempts.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
print('Archived independent attempts:', len(records))
