import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

delivery = Path(sys.argv[1]).resolve()
batch = delivery / 'UX05-IMGUI-R2'
evidence = batch / 'EVIDENCE'


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def json_lines(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines() if line]


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest().upper()


def identity(row):
    return tuple(row[field] for field in (
        'runId', 'objectiveId', 'regionId', 'completedAtUtc', 'committedAtUtc', 'displayNameSnapshot'))


def changed_paths(a, b, prefix=''):
    if type(a) != type(b):
        return [prefix]
    if isinstance(a, dict):
        return sum((changed_paths(a.get(k), b.get(k), prefix+'/'+k) for k in sorted(a.keys() | b.keys())), [])
    return [prefix] if a != b else []


summary = {}
matrix = []
for folder, expected_unknown in [('MIXED-A06', False), ('EMPTY-A03', False), ('UNKNOWN-A03', True)]:
    run = evidence / folder
    manifest = load(run / 'manifest.json')
    actions = json_lines(run / 'actions.jsonl')
    if (run / 'foreign-actions.json').exists():
        foreign = load(run / 'foreign-actions.json')
        assert foreign['status'] == 'NOT_DELIVERED'
        foreign_rows = [a for a in actions if a['step'] in foreign['steps']]
        assert len(foreign_rows) == len(foreign['steps'])
        finished = load(run / 'process-exit.json')['finishedUtc']
        assert all(a['utc'] > finished for a in foreign_rows)
        assert foreign['targetPid'] != manifest['pid']
        actions = [a for a in actions if a['step'] not in foreign['steps']]
    outcomes = {row['step']: row for row in json_lines(run / 'outcomes.jsonl')}
    interruption = load(run / 'input-interruption.json') if (run / 'input-interruption.json').exists() else None
    states = [row['after'] for row in outcomes.values() if row['after']]
    opened = [state for state in states if state['open']]
    assert opened and {state['ui'] for state in opened} == {'imgui', 'ugui'}
    assert len({state['saveSha256'] for state in states}) == 1
    assert len({state['profileJson'] for state in states}) == 1
    storage_files = [row for row in load(run / 'before.json') if row['path'].startswith('WanxiangGuitu')]
    for row in storage_files:
        path = run / row['path']
        if path.name in ('save.json', 'save.json.bak'):
            continue  # OnApplicationQuit performs the existing SaveBeforeExit publication; audit below.
        assert path.stat().st_size == row['bytes'] and sha(path) == row['sha256']
    main = run / 'WanxiangGuitu/ForestRuins-v10/save.json'
    backup = main.with_name('save.json.bak')
    before_main = next(row for row in storage_files if row['path'].endswith('save.json'))
    assert sha(backup) == before_main['sha256']
    old_envelope, new_envelope = load(backup), load(main)
    old_payload, new_payload = json.loads(old_envelope['payload']), json.loads(new_envelope['payload'])
    assert old_envelope['checksum'] == hashlib.sha256(old_envelope['payload'].encode()).hexdigest().upper()
    assert new_envelope['checksum'] == hashlib.sha256(new_envelope['payload'].encode()).hexdigest().upper()
    assert new_envelope['revision'] == old_envelope['revision'] + 1
    exit_delta = changed_paths(old_payload, new_payload)
    assert exit_delta == ['/profile/camp/events', '/profile/camp/randomStateJson', '/profile/camp/resources', '/revision']
    assert changed_paths(old_envelope, new_envelope) == ['/checksum', '/payload', '/revision', '/savedAtUtc']
    for state in states:
        assert not state['preparing']
        assert state['unknown'] == expected_unknown
        assert state['inventoryPage'] == 'Camp'
    observed = {}
    consumed = 0
    focus_count = 0
    for action in actions:
        native = action['window']
        assert native['playerPid'] == native['hwndPid'] == native['foregroundPid'] == manifest['pid']
        assert native['foregroundVerified'] and native['converted'] and native['dpiScale'] > 0
        focus_count += 1
        outcome = outcomes.get(action['step'])
        if not outcome:
            if interruption and action['step'] == interruption['step']:
                assert interruption['status'] == 'NOT_DELIVERED'
                continue
            # Alt+F4 ends the process before a new screenshot can be captured.
            assert '结束' in action['label']
            continue
        state = outcome['after']
        if not action['label'].startswith(('IMGUI', 'uGUI')):
            continue
        assert state is not None
        if '末条滚动' in action['label']:
            if state['ui']=='imgui':
                assert state['imguiScroll']['y'] > action['before']['imguiScroll']['y']
            else:
                assert state['uguiScroll'] < action['before']['uguiScroll']
        if '地区' in action['label']:
            suffix = action['label'].split('地区')[-1]
            assert state['regionFilter'] == {'全部': 0, '森林': 1, '遗迹': 2, '洞窟': 3}[suffix]
            assert state['page'] == 1
        if '类型' in action['label']:
            suffix = action['label'].split('类型')[-1]
            assert state['typeFilter'] == {'全部': 0, '采集': 1, '寻宝': 2, '讨伐': 3, '首领': 4, '特殊': 5}[suffix]
            assert state['page'] == 1
        expected = sorted(state['query'], key=lambda row: (row['runId'], row['objectiveId']))
        expected.sort(key=lambda row: (row['completedAtUtc'], row['committedAtUtc']), reverse=True)
        assert [identity(row) for row in state['query']] == [identity(row) for row in expected]
        if '关闭' in action['label']:
            assert not state['open']
        else:
            assert state['open']
            assert [identity(row) for row in state['visible']] == [identity(row) for row in expected[(state['page']-1)*20:state['page']*20]]
            if state['ui'] == 'imgui':
                assert state['repaintCount'] > 0
            else:
                assert any(state['notice'] in text for text in state['text'])
                for row in state['visible']:
                    assert any(row['runId'] in text and row['displayNameSnapshot'] in text for text in state['text'])
            key = (state['regionFilter'], state['typeFilter'], state['page'])
            observed[(state['ui'], key)] = ([identity(row) for row in state['query']], [identity(row) for row in state['visible']])
        consumed += 1
    pair_keys = {key for ui, key in observed if ui == 'imgui'}
    assert pair_keys == {key for ui, key in observed if ui == 'ugui'}
    for key in pair_keys:
        assert observed[('imgui', key)] == observed[('ugui', key)]
    if folder.startswith('MIXED'):
        for ui in ('imgui', 'ugui'):
            page_rows = [observed[(ui, (0, 0, page))][1] for page in range(1, 8)]
            assert [len(rows) for rows in page_rows] == [20]*6 + [8]
            all_rows = sum(page_rows, [])
            assert len({row[0] for row in all_rows}) == 128
            assert all_rows[-1][1] == 'ruins.challenge'
        assert all('R2 当前新名称' not in state['notice'] for state in opened)
    else:
        assert all(not state['query'] and state['pages'] == 1 for state in opened)
        assert all(('旧版目标历史未知' in state['notice']) == expected_unknown for state in opened)
    exit_receipt = load(run / 'process-exit.json') if (run / 'process-exit.json').exists() else None
    if exit_receipt:
        assert exit_receipt['exitCode'] == 0 and not exit_receipt['timedOut']
        assert exit_receipt['pid'] == manifest['pid']
    assert exit_receipt is not None
    result = {'runId': manifest['runId'], 'status': 'PASS' if exit_receipt else 'PASS_INTERACTION_INCOMPLETE_EXIT', 'focusVerifiedOperations': focus_count,
              'deliveredOperations': len(actions) - (1 if interruption else 0),
              'undeliveredOperations': 1 if interruption else 0,
              'unchangedAssociatedFiles': len(storage_files)-2,
              'exitSaveAudit': {'beforeSha256': before_main['sha256'], 'afterSha256': sha(main),
                               'backupEqualsBeforeMain': True, 'payloadChangedPaths': exit_delta,
                               'historySettlementAndRewardsUnchanged': True,
                               'reason': 'Existing OnApplicationQuit -> SaveBeforeExit -> SaveProgress captures current camp world'},
              'historyControlConsumption': consumed, 'pairedQueryStates': len(pair_keys),
              'imguiConsumption': sum(1 for a in actions if a['label'].startswith('IMGUI') and a['step'] in outcomes),
              'uguiConsumption': sum(1 for a in actions if a['label'].startswith('uGUI') and a['step'] in outcomes),
              'saveSha256DuringInteraction': states[0]['saveSha256'], 'profileUnchangedDuringInteraction': True,
              'sixFieldsAndOrderEqual': True, 'unknown': expected_unknown,
              'exitCode': exit_receipt['exitCode'] if exit_receipt else 'NOT_CAPTURED',
              'exitObservation': 'Monitored process receipt' if exit_receipt else 'Native Alt+F4; window disappeared; no numeric process exit receipt'}
    (run / 'verified-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    summary[folder] = result

original = load(evidence / 'history-before.json')
for row in original['files']:
    path = Path('\\\\?\\' + str(delivery / row['path']).replace('/', '\\'))
    assert path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], row['path']
before = load(evidence / 'source-before.json')
changed = []
for row in before:
    path = Path(row['path'])
    if sha(path) != row['sha256']:
        changed.append(row['path'])
assert changed == ['Assets/CombatPrototype/AdventureFlow.UI.cs'], changed
summary['protection'] = {'historicalRuns': 147, 'historicalFilesVerified': len(original['files']),
                         'changedProductFiles': changed, 'sourceFilesVerified': len(before)}
(evidence / 'independent-review.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
