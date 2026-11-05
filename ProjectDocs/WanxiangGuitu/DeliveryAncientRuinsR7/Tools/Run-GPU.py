"""Launch the observed Player from the runner's owned, inactive desktop."""
import ctypes as c
from ctypes import wintypes as w
import hashlib
import json
import os
from pathlib import Path
import sys
import time

import frida

exe, run = (Path(p).resolve() for p in sys.argv[1:3])
assert 'C1R7-1106-A' in exe.parts and 'C1R7-1106-A' in run.parts
assert Path(os.environ['UNITY_TEST_ROOT']).resolve()==run
user=c.WinDLL('user32',use_last_error=True)
kernel=c.WinDLL('kernel32',use_last_error=True)
user.GetThreadDesktop.argtypes=[w.DWORD]
user.GetThreadDesktop.restype=w.HANDLE
user.GetUserObjectInformationW.argtypes=[w.HANDLE,c.c_int,c.c_void_p,w.DWORD,c.POINTER(w.DWORD)]
user.OpenInputDesktop.argtypes=[w.DWORD,w.BOOL,w.DWORD]
user.OpenInputDesktop.restype=w.HANDLE
user.CloseDesktop.argtypes=[w.HANDLE]
kernel.GetCurrentThreadId.restype=w.DWORD

def name(handle):
    buf=c.create_unicode_buffer(260)
    needed=w.DWORD()
    if not handle or not user.GetUserObjectInformationW(handle,2,buf,c.sizeof(buf),c.byref(needed)):
        return None
    return buf.value

desktop=name(user.GetThreadDesktop(kernel.GetCurrentThreadId()))
active=user.OpenInputDesktop(0,False,1)
input_desktop=name(active)
if active:
    user.CloseDesktop(active)
assert desktop and desktop.startswith('WGTest_') and desktop!=input_desktop,(desktop,input_desktop)
assert hashlib.sha256(exe.with_name('UnityPlayer.dll').read_bytes()).hexdigest() == '3bdc6e4cd1b5eb85e1562b1c6018949145cdedf50cf7aceab0d1518143f9aa7c'
trace=run/'gpu.jsonl'

def event(payload):
    with trace.open('a',encoding='utf-8') as out:
        out.write(json.dumps(payload)+'\n')

device=frida.get_local_device()
args=[str(exe),'-logFile',str(run/'Player.log'),'-screen-width','1280','-screen-height','720',
      '-screen-fullscreen','0','-force-d3d12','-wanxiang-storage-root',str(run)]
pid=device.spawn(args,cwd=str(run),env=dict(os.environ))
kernel.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD]
kernel.OpenProcess.restype=w.HANDLE
kernel.WaitForSingleObject.argtypes=[w.HANDLE,w.DWORD]
kernel.GetExitCodeProcess.argtypes=[w.HANDLE,c.POINTER(w.DWORD)]
kernel.CloseHandle.argtypes=[w.HANDLE]
handle=kernel.OpenProcess(0x00101000,False,pid)
assert handle
event(dict(kind='launch',pid=pid,desktop=desktop,inputDesktop=input_desktop,args=args))
session=None
try:
    session=device.attach(pid)
    script=session.create_script(Path(__file__).with_name('Trace-D3D12.js').read_text('utf-8'))
    script.on('message',lambda message,_: event(message.get('payload',message)))
    script.load()
finally:
    device.resume(pid)

deadline=time.monotonic()+95
summary=None
while kernel.WaitForSingleObject(handle,100)==258 and time.monotonic()<deadline:
    if (run/'gpu-flush.txt').is_file() and summary is None and session and not session.is_detached:
        summary=script.exports_sync.report()
        event(summary)
code=w.DWORD()
assert kernel.GetExitCodeProcess(handle,c.byref(code))
kernel.CloseHandle(handle)
receipt=dict(pid=pid,exited=code.value!=259,exitCode=None if code.value==259 else code.value,
             gpuCatalog=summary is not None,forcedTermination=False)
(run/'player-process.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
assert receipt['exitCode']==0 and (run/'render-complete.txt').is_file(),receipt
