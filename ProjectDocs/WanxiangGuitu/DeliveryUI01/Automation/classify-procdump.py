"""Version-pinned empirical exit-count interpretation; never blanket-accept exit 1."""
import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path

spec = importlib.util.spec_from_file_location('md', Path(__file__).with_name('inspect-minidump.py'))
md = importlib.util.module_from_spec(spec); spec.loader.exec_module(md)


def load(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def write(path, value): path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
def decode(path):
    data = path.read_bytes()
    return data.decode('utf-16' if data.startswith((b'\xff\xfe', b'\xfe\xff')) else ('utf-16-le' if data[1:100:2].count(0) > 20 else 'utf-8-sig'), errors='replace')


def calibrate(root):
    owner = load(root/'owner.json')
    if owner['kind'] != 'ProcDump synthetic target controls': raise ValueError('Owned synthetic controls required')
    tool = load(root/'tool.json'); rows = {r['name']: r for r in load(root/'results.json')}
    checks = {}
    for name, expected in [('single', 1), ('double', 2), ('termination', 1)]:
        paths = list((root/name).glob('*.dmp')) if name != 'termination' else [root/'termination.dmp']
        dumps = [md.inspect(p) for p in paths]
        if rows[name]['timedOut'] or rows[name]['exitCode'] != expected or len(dumps) != expected:
            raise ValueError('Exit-count control failed: '+name)
        checks[name] = dict(exitCode=rows[name]['exitCode'], dumpCount=len(dumps), dumps=dumps)
    if rows['invalid-pid']['exitCode'] >= 0 or (root/'invalid.dmp').exists() or rows['synthetic-target']['exitCode'] != 0:
        raise ValueError('Negative PID or target lifecycle control failed')
    if tool['signature'] != 'Valid' or 'Microsoft Corporation' not in tool['signer']: raise ValueError('Unsigned/unexpected tool')
    return dict(status='PASS', tool=tool, controls=checks, negativeExit=rows['invalid-pid']['exitCode'],
                interpretation='Observed positive exit equals completed dump count for this exact signed binary; not a universal documented API',
                limitation='Does not establish any game crash cause; memory dumps remain local')


def classify(args):
    calibration = load(args.calibration)
    proof_path = args.calibration.parent / calibration['proof']
    if hashlib.sha256(proof_path.read_bytes()).hexdigest() != calibration['proofSha256']: raise ValueError('Calibration proof hash mismatch')
    proof = load(proof_path); tool = load(args.tool_info)
    if proof['status'] != 'PASS' or tool['signature'] != 'Valid' or tool['sha256'] != proof['tool']['sha256'] or tool['version'] != proof['tool']['version']:
        raise ValueError('Uncalibrated or unsigned monitor binary; nonzero not accepted')
    paths = list(args.dump_dir.glob('*.dmp')); dumps = [md.inspect(p) for p in paths]
    text = decode(args.stdout)
    completed = re.findall(r'Dump\s+(\d+)\s+complete:', text)
    if not 0 < args.exit_code == len(dumps) == len(completed) <= args.max_dumps:
        raise ValueError('Raw exit/count/completion/structural checks disagree')
    if re.search(r'(?im)^.*\bError (?:opening|writing|creating|dumping)\b', text+decode(args.stderr)):
        raise ValueError('Monitor reports an error')
    return dict(status='PASS', rawExitCode=args.exit_code, interpretation='Pinned empirical dump-count exit; validated artifacts, not ignored nonzero',
                tool=tool, calibrationProofSha256=calibration['proofSha256'], dumps=dumps,
                gameCloseStatus='SEPARATE', gameRootCause='UNRESOLVED', symbolizedStack='NOT_RUN')


if __name__ == '__main__':
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest='mode', required=True)
    c = sub.add_parser('calibrate'); c.add_argument('root', type=Path); c.add_argument('--output', required=True, type=Path)
    c = sub.add_parser('classify')
    for name in ['calibration', 'tool-info', 'dump-dir', 'stdout', 'stderr', 'output']: c.add_argument('--'+name, required=True, type=Path)
    c.add_argument('--exit-code', type=int, required=True); c.add_argument('--max-dumps', type=int, default=1)
    args = p.parse_args()
    try: result = calibrate(args.root) if args.mode == 'calibrate' else classify(args); code = 0
    except Exception as e: result = dict(status='FAIL', reason=str(e), rawExitCode=getattr(args, 'exit_code', None)); code = 1
    write(args.output, result); raise SystemExit(code)
