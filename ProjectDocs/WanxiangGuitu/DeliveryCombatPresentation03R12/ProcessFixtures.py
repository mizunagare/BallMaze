"""Synthetic receipt schemas for tool tests only. Never a Unity process receipt."""
from pathlib import Path
import json

def write_process(root,profile,status,code,timed):
    root=Path(root).resolve();root.mkdir(parents=True,exist_ok=True)
    if profile not in ('Editor','Runtime'):raise ValueError('fixture role required')
    name='CP03Editor.Run' if profile=='Editor' else 'CP03Runtime'
    scope='controlled-editor' if profile=='Editor' else 'nondevelopment-acceptance-player-controlled-combat-API'
    exe='C:/CP03SyntheticFixture/Unity.exe' if profile=='Editor' else 'C:/CP03SyntheticFixture/WanxiangGuitu.exe'
    runner=root/'process-results.json';native=root/(name+'.exit.json')
    row=dict(name=name,scope=scope,status=status,exitCode=code,timedOut=timed,startUtc='2026-10-31T00:00:00Z',endUtc='2026-10-31T00:00:02Z',reason='',log=str(root/name),command=[exe,'-logFile',str(root/'fixture.log')])
    exitdata=dict(exitCode=code,forcedTermination=False,hostPid=1,exitObservedUtc='2026-10-31T00:00:01Z')
    runner.write_bytes(json.dumps(row,indent=2).encode('utf-8'));native.write_bytes(json.dumps(exitdata,indent=2).encode('utf-8'))
    (root/'fixture-provenance.json').write_bytes(json.dumps(dict(kind='SYNTHETIC TOOL SCHEMA; no native process executed',profile=profile)).encode('utf-8'))
    return runner,native
