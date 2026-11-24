"""Read-only Win32 measurement for a recorded Player PID; performs no UI actions."""
import ctypes as c,ctypes.wintypes as w,json,sys,pathlib,datetime
pid=int(sys.argv[1]);target=pathlib.Path(sys.argv[2]);assert not target.exists()
u=c.WinDLL('user32',use_last_error=True)
u.GetForegroundWindow.restype=w.HWND
u.GetWindowThreadProcessId.argtypes=[w.HWND,c.POINTER(w.DWORD)]
u.GetClientRect.argtypes=[w.HWND,c.POINTER(w.RECT)]
u.GetWindowRect.argtypes=[w.HWND,c.POINTER(w.RECT)]
u.GetDpiForWindow.argtypes=[w.HWND];u.GetDpiForWindow.restype=w.UINT
u.ClientToScreen.argtypes=[w.HWND,c.POINTER(w.POINT)]
windows=[]
callback=c.WINFUNCTYPE(w.BOOL,w.HWND,w.LPARAM)
def owner(hwnd):
    value=w.DWORD();u.GetWindowThreadProcessId(hwnd,c.byref(value));return value.value
@callback
def visit(hwnd,_):
    if owner(hwnd)==pid and u.IsWindowVisible(hwnd):windows.append(hwnd)
    return True
u.EnumWindows(visit,0)
assert len(windows)==1,windows
hwnd=windows[0];client=w.RECT();window=w.RECT();origin=w.POINT()
assert u.GetClientRect(hwnd,c.byref(client)) and u.GetWindowRect(hwnd,c.byref(window)) and u.ClientToScreen(hwnd,c.byref(origin))
foreground=u.GetForegroundWindow()
data={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':pid,'hwnd':hwnd,'hwndPid':owner(hwnd),
      'foregroundHwnd':foreground,'foregroundPid':owner(foreground),'dpi':u.GetDpiForWindow(hwnd),
      'clientRect':[client.left,client.top,client.right,client.bottom],
      'windowRect':[window.left,window.top,window.right,window.bottom],'clientScreenOrigin':[origin.x,origin.y],
      'readOnly':True}
target.write_text(json.dumps(data,indent=2),encoding='utf-8');print(json.dumps(data))
