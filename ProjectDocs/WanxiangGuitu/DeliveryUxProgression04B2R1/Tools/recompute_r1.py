#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent UX04-B2-R1 evidence verifier. Standard library only; never launches Unity.

--session may be absolute, workspace-relative, or relative to this delivery directory.
--output MUST NOT exist. Reports preserve every individual failure, including failed runs.
The asset files are parsed as data, never imported/executed. Decimal JSON numbers are
rounded back to IEEE754 single before comparisons; arithmetic rounds each operation.
"""
import argparse
import copy
import csv
import hashlib
import json
import re
import struct
from collections import Counter
from pathlib import Path

NINE = ('GearItem', 'Inventory', 'EquipmentGrid', 'Main', 'Reserve', 'Worn',
        'Overflow', 'AttackPower', 'Container')
WEAPONS = {0, 1, 2, 3, 11, 12, 13}
POWERS = (8, 19, 43, 78, 132)
TYPES = ('Sword', 'Spear', 'Staff', 'Bow', 'Armor', 'Trousers', 'Arms', 'Boots',
         'Accessory', 'ChestRig', 'Backpack', 'TwinBlades', 'Greatsword', 'Scythe')
SORTS = ('None', 'AttackDesc', 'AttackAsc', 'QualityDesc', 'QualityAsc', 'TypeAsc', 'NameAsc')
ROLES = ('None', 'Main', 'Reserve', 'Board', 'Overflow', 'Worn', 'ContainerRig', 'ContainerBag')
ITEM_FIELDS = ('origin originRunId id affixes type quality x y board legacyTier definitionId '
               'dataRevision rotation widthOverride heightOverride overflow worn savedAttack savedDefense').split()
RAW_FIELDS = ('items warehouse rig bag baseDamage rank bonus attackPower basicPower main reserve canonical').split()


def f32(v):
    return struct.unpack('<f', struct.pack('<f', float(v)))[0]


def bits(v):
    return struct.pack('<f', f32(v)).hex()


def add(a, b):
    return f32(f32(a) + f32(b))


def mul(a, b):
    return f32(f32(a) * f32(b))


def total(values):
    out = 0.0
    for v in values:
        out = add(out, v)
    return out


def ordinal(s):
    b = (s or '').encode('utf-16-le', errors='surrogatepass')
    return tuple(b[k] | b[k + 1] << 8 for k in range(0, len(b), 2))


def fnv(s):
    h = 14695981039346656037
    for unit in ordinal(s):
        h = ((h ^ unit) * 1099511628211) & 0xffffffffffffffff
    return '%016x' % h


def decoded(v):
    return json.loads(v) if isinstance(v, str) else v


def enum(v, names):
    return names.index(v) if isinstance(v, str) and v in names else int(v)


def weapon(i):
    return int(i['type']) in WEAPONS


def inbag(i):
    return not any(i[k] for k in ('board', 'worn', 'overflow'))


def stats(i):
    if i['dataRevision'] > 0:
        return f32(i['savedAttack']), f32(i['savedDefense'])
    t, tier = int(i['type']), int(i['legacyTier'])
    p = POWERS[int(i['quality'])]
    a = tier * 15 if tier > 0 and weapon(i) else p if weapon(i) else mul(p, .35 if t == 6 else .5) if t in (6, 8) else 0
    d = tier * 5 if tier > 0 and not weapon(i) else mul(p, .4 if t == 4 else .3 if t == 5 else .2) if not weapon(i) and t not in (9, 10) else 0
    return f32(a), f32(d)


def snapshot(raw):
    items = raw['items']
    main = next((i for i in items if i and i['id'] == raw['main'] and raw['main'] and inbag(i) and weapon(i)), None)
    active, seen = [], set()
    for i in items:
        if i is None or (i['id'] or '') in seen:
            continue
        seen.add(i['id'] or '')
        if not i['worn'] and not i['overflow'] and (i['board'] or i is main):
            active.append(i)
    rb, bb = raw['rig'] or {}, raw['bag'] or {}
    a = add(add(total(stats(i)[0] for i in active), rb.get('attackBonus', 0)), bb.get('attackBonus', 0))
    d = add(add(total(stats(i)[1] for i in active if i['board']), rb.get('defenseBonus', 0)), bb.get('defenseBonus', 0))
    bonus = f32(int(raw['rank']) * 5)
    ap = add(add(raw['baseDamage'], a), bonus)
    wt = int(main['type']) if main else 0
    return dict(baseDamage=f32(raw['baseDamage']), progressionBonus=bonus, loadoutAttack=a,
                loadoutDefense=d, attackPower=ap, basicPower=mul(ap, 1.25 if wt == 1 else 1),
                mainContribution=total(stats(i)[0] for i in active if i is main),
                reserveContribution=total(stats(i)[0] for i in active if raw['reserve'] and i['id'] == raw['reserve']),
                accessoryContribution=total(stats(i)[0] for i in active if int(i['type']) == 8),
                armsContribution=total(stats(i)[0] for i in active if int(i['type']) == 6),
                boardContribution=total(stats(i)[0] for i in active if i['board']),
                containerBonus=add(rb.get('attackBonus', 0), bb.get('attackBonus', 0)),
                weaponType=wt, activeCount=len(active))


class Audit:
    def __init__(self):
        self.rows = []
        self.context = {}

    def check(self, name, ok, expected=None, actual=None, detail=''):
        self.rows.append(dict(self.context, check=name, status='PASS' if ok else 'FAIL',
                              expected=expected, actual=actual, detail=detail))

    def equal(self, name, expected, actual, numeric=False):
        try:
            ok = bits(expected) == bits(actual) if numeric else expected == actual
        except (TypeError, ValueError, OverflowError, struct.error):
            ok = False
        detail = ('float32 expectedBits=' + bits(expected)) if numeric else ''
        self.check(name, ok, expected, actual, detail)

    def error(self, name, ex):
        self.check(name, False, detail=type(ex).__name__ + ': ' + str(ex))


def asset_scalars(path):
    # Only the scalar fields needed by this independent oracle; no YAML code execution.
    out = {}
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        m = re.match(r'^  ([A-Za-z][A-Za-z0-9_]*):\s*(.*?)\s*$', line)
        if not m:
            continue
        key, value = m.groups()
        if value.startswith('"'):
            try:
                value = json.loads(value)
            except ValueError:
                pass
        else:
            try:
                value = float(value) if any(c in value for c in '.eE') else int(value)
            except ValueError:
                pass
        out[key] = value
    return out


class Assets:
    def __init__(self, root, audit):
        self.items, self.qualities, self.containers = {}, {}, {}
        self.files = []
        for folder, target, key in (('ItemData', self.items, 'definitionId'),
                                    ('QualityData', self.qualities, 'quality'),
                                    ('ContainerData', self.containers, 'definitionId')):
            paths = sorted((root / 'Assets/CombatPrototype/Resources' / folder).glob('*.asset'))
            audit.check('asset-source-' + folder, bool(paths), 'nonempty', len(paths))
            for p in paths:
                try:
                    d = asset_scalars(p)
                    target[d[key]] = d
                    self.files.append(dict(path=str(p), bytes=p.stat().st_size,
                                           sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
                except Exception as ex:
                    audit.error('asset-parse:' + str(p), ex)

    def containers_for(self, items, t):
        chosen = next((i for i in items if i['worn'] and int(i['type']) == t), None)
        key = chosen['definitionId'] if chosen else 'rig_standard' if t == 9 else 'bag_standard'
        if key not in self.containers:
            raise ValueError('missing ContainerData definition ' + str(key))
        return self.containers[key]

    def name(self, i):
        return str(self.qualities[int(i['quality'])]['displayName']) + '·' + str(self.items[i['definitionId']]['displayName'])


def preview(raw, candidate, role, assets):
    before = snapshot(raw)
    ev = dict(before=before, after=before, deltaAttackPower=0., deltaBasicPower=0.,
              deltaLoadoutAttack=0., itemAttack=stats(candidate)[0] if candidate else 0.,
              itemDefense=stats(candidate)[1] if candidate else 0., role=role, feasible=True, reason='')
    if candidate is not None and role != 0:
        state, c = copy.deepcopy(raw), copy.deepcopy(candidate)
        state['items'] = [i for i in state['items'] if i['id'] != c['id']]
        if role == 1:
            if not weapon(c):
                ev.update(feasible=False, reason='候选不是武器，不能设为主武器')
            else:
                c.update(board=False, worn=False, overflow=False)
                if c['id'] == state['reserve']:
                    state['reserve'] = state['main']
                state['main'] = c['id']
        elif role == 2:
            if not weapon(c) or c['id'] == state['main']:
                ev.update(feasible=False, reason='候选不能设为备用武器')
            else:
                c.update(board=False, worn=False, overflow=False)
                state['reserve'] = c['id']
        elif role == 3:
            if int(c['type']) in (9, 10) or c['id'] in (state['main'], state['reserve']):
                ev.update(feasible=False, reason='容器或携带中的武器不能放入装备盘')
            else:
                c.update(board=True, worn=False, overflow=False)
        elif role == 4:
            c.update(board=False, worn=False, overflow=True, x=-1, y=-1)
        elif role in (5, 6, 7):
            if int(c['type']) not in (9, 10):
                ev.update(feasible=False, reason='候选不是容器，不能穿戴')
            else:
                c.update(board=False, worn=True, overflow=False, x=-1, y=-1)
        if not ev['feasible']:
            return ev
        state['items'].append(c)
        state['rig'] = assets.containers_for(state['items'], 9)
        state['bag'] = assets.containers_for(state['items'], 10)
        ev['after'] = snapshot(state)
    for delta, field in (('deltaAttackPower', 'attackPower'), ('deltaBasicPower', 'basicPower'),
                         ('deltaLoadoutAttack', 'loadoutAttack')):
        ev[delta] = add(ev['after'][field], -ev['before'][field])
    return ev


def compare_tree(audit, name, expected, actual):
    if isinstance(expected, dict):
        audit.check(name + '.fields', isinstance(actual, dict) and set(expected) <= set(actual), list(expected), list(actual) if isinstance(actual, dict) else actual)
        if not isinstance(actual, dict):
            return
        for key, value in expected.items():
            compare_tree(audit, name + '.' + key, value, actual.get(key))
    else:
        audit.equal(name, expected, actual, isinstance(expected, float))


def spec_of(o):
    value = o.get('spec', o.get('key', o.get('FilterKey', o.get('CurrentKey'))))
    if isinstance(value, str) and value.startswith('{'):
        value = json.loads(value)
    if isinstance(value, dict):
        return (enum(value.get('category', 0), ('All', 'Weapon', 'Accessory', 'Arms', 'Armor', 'Container', 'Other')),
                int(value.get('qualityMask', 0)), enum(value.get('status', 0), ('All', 'Main', 'Reserve', 'Worn', 'Board', 'Unused', 'Overflow', 'Warehouse')),
                enum(value.get('sort', 0), SORTS), bool(value.get('favoritesOnly', False)), value.get('text', ''))
    if not isinstance(value, str):
        raise ValueError('sort row missing filter spec/key')
    parts = value.split('|', 5)
    if len(parts) != 6:
        raise ValueError('CurrentKey must have category|qualityMask|status|sort|fav|text')
    return tuple(int(x) for x in parts[:5]) + (parts[5],)


def expected_order(o, raw, assets):
    category, mask, status, sort, fav, text = spec_of(o)
    favorites = decoded(o.get('favoriteIds', raw.get('favoriteIds', [])))
    if fav and not favorites:
        raise ValueError('favoritesOnly requires raw favoriteIds evidence (not count)')
    selected = []
    for i in raw['items']:
        if i is None:
            continue
        t = int(i['type'])
        cat = 5 if t in (9, 10) else 1 if weapon(i) else 2 if t == 8 else 3 if t == 6 else 4 if t in (4, 5, 7) else 6
        st = 3 if i['worn'] else 6 if i['overflow'] else 4 if i['board'] else 1 if i['id'] == raw['main'] else 2 if i['id'] == raw['reserve'] else 5
        if category and category != cat or mask and not mask & (1 << int(i['quality'])) or status and st != status:
            continue
        if fav and i['id'] not in favorites or text and text.lower() not in assets.name(i).lower():
            continue
        selected.append(i)
    if sort:
        def key(i):
            value = -stats(i)[0] if sort == 1 else stats(i)[0] if sort == 2 else -int(i['quality']) if sort == 3 else int(i['quality']) if sort == 4 else int(i['type']) if sort == 5 else ordinal(assets.name(i))
            return value, ordinal(i['id'])
        selected.sort(key=key)
    return [i['id'] for i in selected]


def ids(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str) and value.startswith('['):
        return json.loads(value)
    if not isinstance(value, str):
        raise ValueError('id order must be a list or delimited string')
    return [] if value == '' else value.split('|' if '|' in value else ',')


def audit_observation(a, o, assets):
    if o.get('result') == 'FAIL' or str(o.get('note', '')).startswith('FAIL'):
        a.check('driver-recorded-failure', False, actual=o)
    raw = decoded(o.get('raw'))
    if raw is None and o.get('stage') == 'boot':
        a.rows.append(dict(a.context, check='raw.boot-not-initialized', status='INFO', detail='Boot precedes hero initialization; later per-run raw evidence is still required.'))
        return
    a.check('raw.exists', isinstance(raw, dict), 'object', type(raw).__name__)
    if not isinstance(raw, dict):
        return
    a.check('raw.fields', set(RAW_FIELDS) <= set(raw), RAW_FIELDS, list(raw))
    expected = snapshot(raw)
    compare_tree(a, 'live', {k: expected[k] for k in ('attackPower', 'basicPower')}, raw)
    a.equal('live.bonus', expected['progressionBonus'], raw.get('bonus'), True)
    for slot in ('rig', 'bag'):
        container = raw[slot]
        if container is not None:
            fields = ('definitionId displayName description type quality width height blockedCells moveBonus attackBonus defenseBonus harvestBonus woodCost hideCost oreCost').split()
            a.check(slot + '.fields', set(fields) <= set(container), fields, list(container))
            source = assets.containers.get(container.get('definitionId'))
            a.check(slot + '.asset-source', source is not None, container.get('definitionId'), bool(source))
            if source is not None:
                for field in ('attackBonus', 'defenseBonus'):
                    a.equal(slot + '.asset.' + field, f32(source[field]), container.get(field), True)
    for published, field in (('GearAttack', 'loadoutAttack'), ('GearDefense', 'loadoutDefense'), ('AttackPower', 'attackPower'), ('AttackBonus', 'progressionBonus')):
        if published in o:
            a.equal('published.' + published, expected[field], o[published], True)
    for group in ('items', 'warehouse'):
        for n, i in enumerate(raw[group]):
            prefix = '%s[%d:%s]' % (group, n, i.get('id'))
            a.check(prefix + '.fields', set(ITEM_FIELDS) <= set(i), ITEM_FIELDS, list(i))
            attack, defense = stats(i)
            for field, number in (('derivedAttack', attack), ('derivedDefense', defense)):
                if field in i:
                    a.equal(prefix + '.' + field, number, i[field], True)
            # New frozen stats are checked against asset source, not observation summaries.
            # Upgraded legacy items retain legacy stats and are not "new equipment".
            if i['dataRevision'] > 0 and int(i['legacyTier']) <= 0 and int(i['origin']) != 3 and not str(i['originRunId'] or '').lower().startswith('legacy'):
                definition = assets.items.get(i['definitionId'])
                quality = assets.qualities.get(int(i['quality']))
                a.check(prefix + '.asset-source', definition is not None and quality is not None, i['definitionId'], bool(definition and quality))
                if definition is not None and quality is not None:
                    for field, factor in (('savedAttack', 'attackFactor'), ('savedDefense', 'defenseFactor')):
                        value = 0.0 if int(i['type']) in (9, 10) else mul(quality['power'], definition[factor])
                        a.equal(prefix + '.asset.' + field, value, i[field], True)
    if o.get('stage') == 'sort':
        ordered = expected_order(o, raw, assets)
        if 'publishedIds' in o:
            a.equal('sort.publishedIds', ordered, ids(o['publishedIds']))
        else:
            a.rows.append(dict(a.context, check='sort.no-structured-publishedIds', status='INFO', expected=ordered, actual=dict(FilterKey=o.get('FilterKey'), SortKey=o.get('SortKey')), detail='Real-click observation lacks structured publishedIds; note text is not parsed as published evidence.'))
        if 'renderedIds' in o:
            a.equal('sort.renderedIds', ordered, ids(o['renderedIds']))
    if o.get('stage') == 'preview9':
        before, after = decoded(o['beforeJson']), decoded(o['afterJson'])
        cb = decoded(o.get('canonicalBeforeJson', o.get('beforeCanonicalJson', raw['canonical'])))
        ca = decoded(o.get('canonicalAfterJson', o.get('afterCanonicalJson', raw['canonical'])))
        for name, d in (('beforeJson', before), ('afterJson', after), ('canonicalBefore', cb), ('canonicalAfter', ca), ('raw.canonical', raw['canonical'])):
            a.equal('nine.' + name + '.keys', sorted(NINE), sorted(d))
        for key in NINE:
            a.equal('nine.unchanged.' + key, before.get(key), after.get(key))
            a.equal('nine.canonical.unchanged.' + key, cb.get(key), ca.get(key))
            a.equal('nine.fnv.before.' + key, fnv(cb[key]), before.get(key))
            a.equal('nine.fnv.after.' + key, fnv(ca[key]), after.get(key))
            a.equal('nine.rawCanonical.' + key, ca[key], raw['canonical'].get(key))
    if 'evaluationJson' in o:
        candidate = decoded(o.get('candidateJson'))
        evaluation = decoded(o['evaluationJson'])
        a.equal('preview.candidateId', candidate.get('id') if candidate else None, o.get('candidateId'))
        role = enum(evaluation['role'], ROLES)
        independent = preview(raw, candidate, role, assets)
        if role == 1:
            compare_tree(a, 'preview', independent, evaluation)
        else:
            # C06 asserts read-only state, not container replacement number semantics.
            # Keep every after field in details, but do not turn an out-of-scope risk
            # into a C06 failure. C05 Main after remains fully bitwise verified.
            compare_tree(a, 'preview.before', independent['before'], evaluation.get('before'))
            for key in ('role', 'itemAttack', 'itemDefense', 'feasible', 'reason'):
                compare_tree(a, 'preview.' + key, independent[key], evaluation.get(key))
            a.rows.append(dict(a.context, check='preview.non-Main-after-not-targeted',
                               status='INFO', expected=independent, actual=evaluation,
                               detail='C06 read-only only; container first-worn selection is known non-target numerical risk.'))
    elif o.get('stage') == 'preview9':
        a.check('preview.evaluationJson.exists', False)


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def jsonl(path, audit):
    rows = []
    for n, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError('JSONL row is not an object')
            rows.append((n, row))
        except Exception as ex:
            audit.error(str(path) + ':line:' + str(n), ex)
    return rows


def required_inputs(mode):
    low = mode.lower()
    if any(name in low for name in ('guid', 'golden', 'strength', 'restart')):
        # These modes restore state / inspect APIs rather than click controls.
        return set()
    if 'imgui' in low:
        return {'native-mouse-down', 'native-mouse-up', 'native-window'}
    return {'mouse-down', 'mouse-up', 'ugui-raycast'}


def audit_run(path, audit, assets):
    m = read_json(path)
    root = path.parent
    audit.context = dict(runId=m.get('runId'), mode=m.get('mode'), manifest=str(path))
    audit.check('manifest.runId', isinstance(m.get('runId'), str) and bool(m['runId']), 'nonempty', m.get('runId'))
    audit.check('manifest.pid', isinstance(m.get('pid'), int) and m['pid'] > 0, '>0', m.get('pid'))
    for k, value in (('exitCode', 0), ('completeFlag', 'PASS'), ('timedOut', False), ('forcedTermination', False), ('verdict', 'PLAYER_RUN_COMPLETED')):
        audit.equal('manifest.' + k, value, m.get(k))
    files = m.get('files', {})
    audit.check('manifest.files.nonempty', isinstance(files, dict) and bool(files))
    for rel, info in files.items():
        p = (root / rel).resolve()
        safe = p.is_relative_to(root.resolve())
        audit.check('file.safe:' + rel, safe)
        if not safe:
            continue
        audit.check('file.exists:' + rel, p.is_file())
        if p.is_file():
            audit.equal('file.bytes:' + rel, info.get('bytes'), p.stat().st_size)
            audit.equal('file.sha256:' + rel, str(info.get('sha256', '')).lower(), hashlib.sha256(p.read_bytes()).hexdigest())
    actual_files = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p != path}
    audit.equal('manifest.files.coverage', sorted(actual_files), sorted(files))
    rp = root / 'result.json'
    audit.check('result.exists', rp.is_file())
    if rp.is_file():
        r = read_json(rp)
        audit.equal('result.manifest-copy', m.get('resultJson'), r)
        for key in ('runId', 'mode'):
            if key in r:
                audit.equal('result.' + key, m.get(key), r[key])
        # Support driver result/overall/pass/success schema variants, fail closed if absent.
        verdict = r.get('result', r.get('overall', r.get('status', r.get('pass', r.get('success')))))
        audit.check('result.success', verdict is True or verdict == 'PASS', 'PASS or true', verdict)
        if 'failed' in r:
            audit.equal('result.failed', 0, r['failed'])
        if isinstance(r.get('checks'), int):
            audit.equal('result.check-count', r['checks'], len(r.get('detail', [])))
            audit.equal('result.passed-count', r.get('passed'), sum(c.get('result') == 'PASS' for c in r.get('detail', [])))
        check_rows = r.get('detail', r.get('checks', []))
        if not isinstance(check_rows, list):
            check_rows = []
        for index, c in enumerate(check_rows):
            if isinstance(c, str):
                audit.check('result.check.' + str(index), not c.upper().startswith('FAIL'), actual=c)
            elif isinstance(c, dict):
                audit.check('result.check.' + str(index), c.get('result', c.get('status', c.get('pass'))) in ('PASS', True), actual=c)
    cp = root / 'Player.command.json'
    if cp.is_file():
        command = read_json(cp)
        for key in ('runId', 'mode', 'buildId'):
            audit.equal('command.' + key, m.get(key), command.get(key))
        if 'pid' in command:
            audit.equal('command.pid', m.get('pid'), command['pid'])
    ip = root / 'r1-input-events.jsonl'
    if not ip.is_file():
        candidates = list(root.glob('*input*.jsonl'))
        if len(candidates) == 1:
            ip = candidates[0]
    audit.check('input.raw-file.exists', ip.is_file())
    events = jsonl(ip, audit) if ip.is_file() else []
    kinds = {r.get('kind') for _, r in events}
    required = required_inputs(str(m.get('mode', '')))
    for kind in sorted(required):
        audit.check('input.kind.' + kind, kind in kinds, kind, sorted(str(k) for k in kinds))
    for _, event in events:
        if event.get('kind') == 'native-window':
            values = dict(re.findall(r'(ownPid|windowPid|foregroundPid)=(\d+)', event.get('detail', '')))
            for key in ('ownPid', 'windowPid', 'foregroundPid'):
                audit.equal('input.' + key, m.get('pid'), int(values[key]) if key in values else None)
    op = root / 'r1-observations.jsonl'
    audit.check('observations.exists', op.is_file())
    observations = jsonl(op, audit) if op.is_file() else []
    audit.check('observations.nonempty', bool(observations))
    raw_count = 0
    for n, o in observations:
        audit.context.update(line=n, seq=o.get('seq'), stage=o.get('stage'), flow=o.get('flow'))
        audit.equal('observation.runId', m.get('runId'), o.get('runId'))
        if 'raw' in o:
            raw_count += 1
        try:
            audit_observation(audit, o, assets)
        except Exception as ex:
            audit.error('observation.exception', ex)
    audit.check('run.raw-input.present', raw_count > 0, '>0', raw_count)
    return dict(runId=m.get('runId'), mode=m.get('mode'), manifest=str(path), observations=len(observations),
                rawObservations=raw_count, inputs=len(events), requiredInputKinds=sorted(required), actualInputKinds=sorted(str(k) for k in kinds))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--assets-root', help='Unity workspace root (default: inferred from script location)')
    args = parser.parse_args()
    script = Path(__file__).resolve()
    workspace = Path(args.assets_root).resolve() if args.assets_root else script.parents[4]
    session = Path(args.session)
    if not session.is_absolute() and not session.exists():
        session = script.parent.parent / session
    session = session.resolve()
    output = Path(args.output).resolve()
    if output.exists():
        parser.error('refusing to overwrite existing output directory: ' + str(output))
    if output == session or output.is_relative_to(session):
        parser.error('output must be outside input session to preserve evidence')
    output.mkdir(parents=True, exist_ok=False)
    audit = Audit()
    audit.check('session.exists', session.is_dir(), True, session.is_dir())
    assets = Assets(workspace, audit)
    manifests = sorted(session.rglob('run-manifest.json')) if session.is_dir() else []
    audit.check('session.manifests.nonempty', bool(manifests), '>0', len(manifests))
    runs, seen_runs, seen_pids = [], set(), set()
    for path in manifests:
        try:
            run = audit_run(path, audit, assets)
            audit.context = dict(manifest=str(path), runId=run['runId'])
            audit.check('session.runId.unique', run['runId'] not in seen_runs, actual=run['runId'])
            seen_runs.add(run['runId'])
            pid = read_json(path).get('pid')
            # OS may recycle PIDs; preserve it for review, never assert global uniqueness.
            seen_pids.add(pid)
            runs.append(run)
        except Exception as ex:
            audit.context = dict(manifest=str(path))
            audit.error('run.exception', ex)
    counts = Counter(r['status'] for r in audit.rows)
    summary = dict(schemaVersion=1, oracle='independent-python-float32', session=str(session),
                   assetsRoot=str(workspace), runCount=len(runs), checkCount=len(audit.rows),
                   passed=counts['PASS'], failed=counts['FAIL'], informational=counts['INFO'], verdict='FAIL' if counts['FAIL'] else 'PASS',
                   limitations=['Assets reflect current source, not necessarily built Player; hashes recorded.',
                                'New frozen-stat source check excludes legacyTier>0, LegacyProtected origin, and legacy originRunId.',
                                'Canonical hashes verify supplied UTF16 plaintext independently; Inventory plaintext cannot be regenerated without inventory raw fields.'])
    def dump(name, obj):
        (output / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    dump('summary.json', summary)
    dump('details.json', dict(summary=summary, runs=runs, assetSources=assets.files, checks=audit.rows))
    dump('failures.json', [r for r in audit.rows if r['status'] == 'FAIL'])
    fields = ['runId', 'mode', 'manifest', 'line', 'seq', 'stage', 'flow', 'check', 'status', 'expected', 'actual', 'detail']
    with (output / 'checks.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        for row in audit.rows:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in row.items()})
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if counts['FAIL'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
