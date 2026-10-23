"""Read-only checks of explicitly isolated synthetic Player evidence. Never closes a process."""
import argparse, hashlib, json
from pathlib import Path

def payload(path):
    envelope = json.loads(path.read_text(encoding='utf-8-sig'))
    actual = hashlib.sha256(envelope['payload'].encode('utf-8')).hexdigest().upper()
    if actual != envelope['checksum']:
        raise ValueError('Primary save checksum mismatch')
    return envelope, json.loads(envelope['payload'])

def summary(path):
    envelope, data = payload(path)
    run = data.get('activeRun') if data.get('hasActiveRun') else None
    profile = data['profile']
    state = dict(revision=envelope['revision'], profileId=profile['profileId'],
                 warehouseMaterials=profile['materials'], committedRuns=profile['committedRuns'],
                 warehouseIds=sorted(i['id'] for i in profile['warehouse']),
                 warehouseGearDigest=digest(sorted(profile['warehouse'], key=lambda i: i['id'])),
                 recipes=profile['unlockedRecipes'], pendingDigest=digest(profile['pending']))
    if run:
        checkpoint = run['checkpoint']
        forest = checkpoint.get('forest') or {}
        state.update(runId=run['runId'], regionInstanceId=run['regionInstanceId'], seed=run['seed'],
                     layoutSeed=forest.get('seed'), phase=run['phase'],
                     brought=run['broughtRemaining'], earned=run['earnedRemaining'],
                     materials=checkpoint['materials'], broughtPotions=run['broughtPotions'],
                     earnedPotions=run['earnedPotions'], gearIds=sorted(i['id'] for i in checkpoint['gear']),
                     gearDigest=digest(sorted(checkpoint['gear'], key=lambda i: i['id'])),
                     mainWeapon=checkpoint['mainWeapon'], reserveWeapon=checkpoint['reserveWeapon'],
                     entryGearDigest=digest(run['entryGear']), worldLayoutDigest=digest(forest),
                     exits=[dict(id=e['id'], repaired=e.get('repaired', False),
                                 receipt=e.get('repairReceipt')) for e in forest.get('exits', [])])
    record = data.get('settlement') if data.get('hasSettlement') else None
    if record:
        state['settlement'] = dict(id=record['settlementId'], status=record['status'])
    return state

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def compare(previous, current):
    # Save revisions advance normally; comparison does not edit either file.
    a, b = summary(previous), summary(current)
    a.pop('revision'); b.pop('revision')
    return dict(passed=a == b, before=a, resumed=b)

def analyze(root, process_name, log_name, audit_start=None, save_override=None, before_save=None):
    process = json.loads((root / process_name).read_text(encoding='utf-8-sig'))
    lines = (root / log_name).read_text(encoding='utf-8-sig', errors='replace').splitlines()
    markers = [(i + 1, s) for i, s in enumerate(lines)
               if any(term in s for term in ('Native Crash Reporting', 'Got a UNKNOWN', 'Crash!!!', 'Unhandled Exception:'))]
    audit = [json.loads(s) for s in (root / 'storage-audit.jsonl').read_text(encoding='utf-8-sig').splitlines() if s.strip()]
    if audit_start:
        audit = [r for r in audit if r['utc'] >= audit_start]
    end_utc = process.get('utc') or process.get('endUtc')
    if end_utc:
        audit = [r for r in audit if r['utc'] <= end_utc]
    quit_index = next((i for i, r in enumerate(audit) if r['operation'] == 'quit'), None)
    exit_audit = [] if quit_index is None else audit[quit_index:]
    ordered = [r['operation'] for r in exit_audit]
    audit_ok = 'quit' in ordered and 'before-exit' in ordered and 'save' in ordered and ordered.index('before-exit') < ordered.index('save')
    save = save_override or root / 'WanxiangGuitu/ForestRuins/save.json'
    state = summary(save)
    previous_revision = summary(before_save)['revision'] if before_save else None
    advanced = previous_revision is not None and state['revision'] > previous_revision
    return dict(cleanExitPassed=process.get('exitCode') == 0 and not process.get('timedOut', True)
                and audit_ok and not markers and advanced, process=process, nativeErrorLines=markers,
                quitAudit=exit_audit, exitAuditPassed=audit_ok, finalSave=state,
                previousRevision=previous_revision, saveRevisionAdvanced=advanced,
                limitation='A save audit records an attempted save; final primary checksum/revision is separately read. Root cause is not inferred from exit code.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--process', required=True)
    parser.add_argument('--log', required=True)
    parser.add_argument('--since')
    parser.add_argument('--save', type=Path)
    parser.add_argument('--before', required=True, type=Path)
    parser.add_argument('--previous', type=Path)
    parser.add_argument('--current', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if not args.root.is_absolute() or 'locallow' in (p.lower() for p in args.root.parts):
        raise ValueError('Explicit isolated root outside LocalLow required')
    result = analyze(args.root, args.process, args.log, args.since, args.save, args.before)
    if args.previous:
        if not args.current: raise ValueError('Resume comparison requires both snapshots')
        result['resume'] = compare(args.previous, args.current)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(dict(cleanExitPassed=result['cleanExitPassed'], resumePassed=result.get('resume', {}).get('passed'))))
    raise SystemExit(0 if result['cleanExitPassed'] and result.get('resume', {}).get('passed', True) else 1)
