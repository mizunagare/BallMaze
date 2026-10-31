"""SYNTHETIC schema fixtures only; no process is executed."""
from pathlib import Path
import hashlib,json

def refresh_origin(root):
    root=Path(root).resolve();snapshot=root/'process-results.json';raw=snapshot.read_bytes();(root/'results.json').write_bytes(raw);h=hashlib.sha256(raw).hexdigest()
    (root/'process-origin.json').write_bytes(json.dumps(dict(kind='SYNTHETIC fixture snapshot',source=str(root/'results.json'),snapshot=str(snapshot),sourceSHA256AtSnapshot=h,snapshotSHA256=h,utc='2026-10-31T00:00:02.100000Z'),indent=2).encode())

def write_process(root,profile,status,code,timed):
    root=Path(root).resolve();root.mkdir(parents=True,exist_ok=True)
    if profile not in ('Editor','Runtime'):raise ValueError('fixture role required')
    name='CP03Editor.Run' if profile=='Editor' else 'CP03Runtime';scope='controlled-editor' if profile=='Editor' else 'nondevelopment-acceptance-player-controlled-combat-API'
    exe='C:/CP03SyntheticFixture/Unity.exe' if profile=='Editor' else 'C:/CP03SyntheticFixture/WanxiangGuitu.exe';args=['-logFile',str(root/'fixture.log')]
    runner=root/'process-results.json';native=root/(name+'.exit.json')
    runner.write_bytes(json.dumps(dict(name=name,scope=scope,status=status,exitCode=code,timedOut=timed,startUtc='2026-10-31T00:00:00Z',endUtc='2026-10-31T00:00:02Z',reason='',log=str(root/name),command=[exe]+args),indent=2).encode())
    native.write_bytes(json.dumps(dict(exitCode=code,forcedTermination=False,hostPid=1,exitObservedUtc='2026-10-31T00:00:01Z'),indent=2).encode())
    (root/(name+'.command.json')).write_bytes(json.dumps(dict(hostExe='C:/Synthetic/dotnet.exe',hostPid=1,exe=exe,arguments=args,startUtc='2026-10-31T00:00:00.250000Z'),indent=2).encode())
    (root/(name+'.desktop-process.json')).write_bytes(json.dumps(dict(pid=2,desktop='WGTest_'+'0'*32,exe=exe,utc='2026-10-31T00:00:00.500000Z',inputDesktopActive=False),indent=2).encode())
    refresh_origin(root)
    (root/'fixture-provenance.json').write_bytes(json.dumps(dict(kind='SYNTHETIC TOOL SCHEMA; no native process executed',profile=profile)).encode())
    return runner,native

def association_paths(root,profile):
    root=Path(root).resolve();name='CP03Editor.Run' if profile=='Editor' else 'CP03Runtime'
    return dict(command_receipt=root/(name+'.command.json'),process_origin=root/'process-origin.json',desktop_receipt=root/(name+'.desktop-process.json'))

def cli_association(root,profile):
    p=association_paths(root,profile)
    return ['--command-receipt',str(p['command_receipt']),'--process-origin',str(p['process_origin']),'--desktop-receipt',str(p['desktop_receipt'])]
