"""Reproduce final R2 inventory; never alter historical run payloads."""
import csv
import hashlib
import json
from pathlib import Path
from collections import Counter

root = Path.cwd()
delivery = root / 'ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation'
batch = delivery / 'UX05-IMGUI-R2'
ev = batch / 'EVIDENCE'

def load(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest().upper()

def write(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')

base = root / 'Builds/ux05-validation-01'
builds = []
build_exit_lines=(ev/'build-exits.txt').read_text('utf-8-sig').splitlines()
for name, folder in [
    ('Acceptance', base/'Project/Builds/UX05-R2-Acceptance-A02'),
    ('NoDefine', base/'Project/Builds/WanxiangGuitu.AcceptanceNoDefine'),
    ('Release', base/'ReleaseValidationR2A02/Release')]:
    exe = folder/'WanxiangGuitu.exe'
    dll = folder/'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'
    blob = dll.read_bytes()
    markers = [s for s in ['UX_ACCEPTANCE', 'ObjectiveHistoryEntryProbe', 'MigrationValidationHook', 'ObserveMigration', 'ObserveHistoryRepaint'] if s.encode() in blob]
    if name != 'Acceptance':
        assert not markers
        assert not (dll.parent/'CavernValidationDriver.dll').exists()
    row = dict(buildId=f'UX05-R2-{name}-A02', type=name, exe=exe.relative_to(root).as_posix(),
               exeSha256=sha(exe), productDllSha256=sha(dll), markers=markers, buildExitCode=0)
    builds.append(row)
    label={'Acceptance':'acceptance','NoDefine':'nodefine','Release':'release'}[name]
    matches=[line for line in build_exit_lines if line.startswith(label+'-a02 PID=')]
    assert len(matches)==1 and matches[0].endswith('exit=0')
receipt = load(base/'ReleaseValidationR2A02/Release/WanxiangGuitu.exe.release.json')
assert receipt['executableSHA256'].upper() == builds[-1]['exeSha256']
observed = base/'IMGUI-R2-A05/WanxiangGuitu_Data/Managed'
assert sha(observed/'Assembly-CSharp.dll') == builds[0]['productDllSha256']
write(ev/'final-build-identity.json', dict(builds=builds, observerProductDllUnchanged=True,
    driverSha256=sha(observed/'CavernValidationDriver.dll'), driverSourceSha256=sha(batch/'Tools/HistoryObserver.cs'),
    releaseReceipt=receipt, noDefineAndReleaseAcceptanceMarkers=0))

historical = list(csv.DictReader((ev/'historical-runs.csv').open(encoding='utf-8-sig', newline='')))
assert len(historical) == 147
current_path = delivery/'PLAYER_RUN_MATRIX.csv'
with current_path.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    current = list(reader)
assert current[:147] == historical

classifications = {
 'MIXED-A01': ('FAIL', 'MIXED-A02', 'D: inactive uGUI canvas reset IMGUI open; raw product failure retained'),
 'MIXED-A02': ('FAIL', 'MIXED-A05', 'D: IMGUI close leaked click to underlying preparation; raw product failure retained'),
 'MIXED-A03': ('INTERACTION_OBSERVED_AUTOSAVE_ACTIVE', 'MIXED-A05', 'Native controls worked; timed autosave changed SHA; not readonly acceptance'),
 'MIXED-A04': ('PASS_INTERACTION_INCOMPLETE_EXIT', 'MIXED-A05', 'Full interaction; numeric process exit not captured; repeated monitored'),
 'MIXED-A05': ('PASS', 'MIXED-A06', 'Full mixed native input; 15 dual UI states; exit 0; one undelivered intent excluded; final repeat adds scroll screenshot trigger'),
 'MIXED-A06': ('PASS', '', 'Final native mixed matrix; guarded Run/PID binding; archived scroll state and screenshot; exit 0'),
 'EMPTY-A01': ('PASS_INTERACTION_INCOMPLETE_EXIT', 'EMPTY-A03', 'Empty state dual UI interaction verified; numeric exit missing'),
 'EMPTY-A02': ('INCOMPLETE_INPUT_TOOL', 'EMPTY-A03', 'A/B: foreground tool rejection; persistent helper logging association defect; terminated isolated test PID'),
 'EMPTY-A03': ('PASS', '', 'Final native empty-history dual UI matrix; guarded Run/PID binding; monitored exit 0'),
 'UNKNOWN-A01': ('FAIL_DRIVER', 'UNKNOWN-A02', 'B: non-atomic configuration write sharing conflict; original console retained'),
 'UNKNOWN-A02': ('PASS_INTERACTION_INCOMPLETE_EXIT', 'UNKNOWN-A03', 'Unknown state dual UI interaction verified; numeric exit missing'),
 'UNKNOWN-A03': ('PASS', '', 'Final native unknown-history dual UI matrix; guarded Run/PID binding; monitored exit 0'),
}
rows = []
for folder, (status, superseded, scope) in classifications.items():
    run = ev/folder
    m = load(run/'manifest.json')
    verified = run/'verified-result.json'
    raw = run/'result.json'
    raw_path = verified if verified.exists() else raw if raw.exists() else run/'diagnosis.jsonl'
    if not raw_path.exists():
        raw_path = run/'classification.json'
        write(raw_path, dict(runId=m['runId'], status=status, scope=scope, supersededBy=superseded))
    raw_status = load(raw)['status'] if raw.exists() else status
    exit_path = run/'process-exit.json'
    exit_code = str(load(exit_path)['exitCode']) if exit_path.exists() else 'NOT_CAPTURED'
    build_id = 'UX05-R1-Acceptance-A06' if folder=='MIXED-A01' else 'UX05-R2-Acceptance-A01' if folder=='MIXED-A02' else 'UX05-R2-Acceptance-A02'
    driver_receipts = [p for p in ev.glob('DRIVER-*/driver-injection.json')
                       if load(p)['driverDllSHA256'].upper() == m['driverSha256']]
    assert len(driver_receipts)==1
    driver_receipt=driver_receipts[0]
    executed=driver_receipt.parent/'HistoryObserver.executed.cs'
    assert executed.exists() and sha(executed)==load(driver_receipt)['sourceSHA256'].upper()
    if folder in ('MIXED-A06','EMPTY-A03','UNKNOWN-A03'):
        assert m['productDllSha256']==builds[0]['productDllSha256']
        assert sha(Path(m['productDll']))==m['productDllSha256']
        assert sha(Path(m['driver']))==m['driverSha256']
    write(run/'identity-association.json',dict(runId=m['runId'],pid=m['pid'],buildId=build_id,
        productDllSha256=m['productDllSha256'],exeSha256=m.get('exeSha256') or sha(Path(m['exe'])),driverSha256=m['driverSha256'],
        exeShaSource='Original manifest' if 'exeSha256' in m else 'Current preserved copy rescan; absent from original manifest',
        driverCompileReceipt=driver_receipt.relative_to(delivery).as_posix(),
        executedDriverSource=executed.relative_to(delivery).as_posix(),
        nativeActionsSourceSha256=sha(batch/'Tools/NativeActions.js') if folder in ('MIXED-A06','EMPTY-A03','UNKNOWN-A03') else 'SEE_ORIGINAL_ACTION_LOG',
        note='Supplementary identity association; original manifest not rewritten'))
    rows.append(dict(zip(fields, [m['runId'], str(m['pid']),
        build_id,
        status, raw_status, exit_code, scope, 'UX05-IMGUI-R2-'+superseded if superseded else '',
        (run/'manifest.json').relative_to(delivery).as_posix(), raw_path.relative_to(delivery).as_posix()])))
for path, values in [(batch/'PLAYER_RUN_MATRIX.csv', rows), (current_path, historical+rows)]:
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer=csv.DictWriter(f, fieldnames=fields)
        writer.writeheader(); writer.writerows(values)
assert len({r['run_id'] for r in historical+rows}) == 159
write(ev/'run-audit.json', dict(original68=load(ev/'preflight-review.json')['classifications']['original68'],
    r1new79=load(ev/'preflight-review.json')['classifications']['r1new79'],
    r2new12=dict(Counter(r['status'] for r in rows)), total159=dict(Counter(r['status'] for r in historical+rows)),
    original147RowsUnchanged=True, originalFailuresPreserved=True))

identity_path=delivery/'BUILD_IDENTITY.tsv'
with identity_path.open(encoding='utf-8-sig', newline='') as f:
    reader=csv.DictReader(f, delimiter='\t'); headers=reader.fieldnames; identity_rows=list(reader)
for r in identity_rows:
    if r['build_id']=='UX05-R1-NoDefine-A03':
        r['exe_path']='Builds/ux05-validation-01/Project/Builds/UX05-R1-NoDefine-A03-Preserved/WanxiangGuitu.exe'
identity_rows=[r for r in identity_rows if not r['build_id'].startswith('UX05-R2-')]
for b in builds:
    identity_rows.append(dict(zip(headers,[b['buildId'],'Unity-'+b['type'],'BUILT',b['exe'],b['exeSha256'],b['productDllSha256']])))
with identity_path.open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=headers,delimiter='\t');writer.writeheader();writer.writerows(identity_rows)

print(json.dumps(dict(builds=builds, newRunCounts=dict(Counter(r['status'] for r in rows))),ensure_ascii=False,indent=2))
