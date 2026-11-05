import ctypes as c
from ctypes import wintypes as w
import hashlib
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
out = root / "Audit"
out.mkdir(exist_ok=True)
editor = Path("C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor")
dbg = c.WinDLL("dbghelp", use_last_error=True)
kernel = c.WinDLL("kernel32", use_last_error=True)
kernel.GetCurrentProcess.restype = w.HANDLE
process = kernel.GetCurrentProcess()
U64 = c.c_uint64
dbg.SymSetOptions.argtypes = [w.DWORD]
dbg.SymSetOptions(0x00000002 | 0x00000004 | 0x00000400 | 0x00000200)
dbg.SymInitializeW.argtypes = [w.HANDLE,w.LPCWSTR,w.BOOL]
dbg.SymInitializeW.restype = w.BOOL
dbg.SymLoadModuleExW.argtypes = [w.HANDLE,w.HANDLE,w.LPCWSTR,w.LPCWSTR,U64,w.DWORD,c.c_void_p,w.DWORD]
dbg.SymLoadModuleExW.restype = U64
dbg.SymFromAddr.argtypes = [w.HANDLE,U64,c.POINTER(U64),c.c_void_p]
dbg.SymFromAddr.restype = w.BOOL
dbg.SymCleanup.argtypes = [w.HANDLE]
assert dbg.SymInitializeW(process, str(root / "Symbols"), False), c.get_last_error()

class SymbolInfo(c.Structure):
    _fields_ = [("SizeOfStruct",w.ULONG),("TypeIndex",w.ULONG),("Reserved",U64*2),("Index",w.ULONG),
                ("Size",w.ULONG),("ModBase",U64),("Flags",w.ULONG),("Value",U64),("Address",U64),
                ("Register",w.ULONG),("Scope",w.ULONG),("Tag",w.ULONG),("NameLen",w.ULONG),
                ("MaxNameLen",w.ULONG),("Name",c.c_char*1)]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
modules = {}
for index, name in enumerate(("Unity.dll","Unity.exe")):
    target = editor / name
    base = 0x180000000 + index*0x10000000
    pdb = root / "Symbols" / ("Unity_x64.pdb" if name == "Unity.dll" else "Unity_exe_x64.pdb")
    result = dbg.SymLoadModuleExW(process,None,str(pdb),name,base,target.stat().st_size,None,0)
    if result:
        modules[name.lower()] = result
    print(name,hex(result),c.get_last_error())

def resolve(frame):
    base = modules.get((frame["module"] or "").lower())
    if not base or not frame["rva"]:
        return
    buf = c.create_string_buffer(c.sizeof(SymbolInfo)+2048)
    info = SymbolInfo.from_buffer(buf)
    info.SizeOfStruct = c.sizeof(SymbolInfo)
    info.MaxNameLen = 2048
    delta=U64()
    if dbg.SymFromAddr(process,base+int(frame["rva"],16),c.byref(delta),buf):
        frame["symbol"] = c.string_at(c.addressof(buf)+SymbolInfo.Name.offset,info.NameLen).decode(errors="replace")
        frame["symbolDisplacement"] = delta.value
    else:
        frame["symbolError"] = c.get_last_error()

attempts = []
try:
    for stage in ("Import","Build"):
        folder = root / ("NativeProject-"+stage)
        path = folder / "native-stacks.jsonl"
        if not path.exists():
            continue
        records = [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines()]
        for row in records:
            for frame in row.get("stack",[]):
                resolve(frame)
        attempts.append(dict(stage=stage,events=records,sourceSHA256=sha(path)))
    provenance = {p.name:sha(p) for p in (root/"Symbols").glob("*.pdb")}
    (out/"symbolized-writebacks.json").write_text(json.dumps(dict(pdbs=provenance,attempts=attempts),indent=2),encoding="utf-8")
finally:
    dbg.SymCleanup(process)
for attempt in attempts:
    for row in attempt["events"]:
        if not row.get("stack"):
            continue
        print(attempt["stage"],row["event"],row.get("args"),[f.get("symbol") for f in row["stack"] if f.get("symbol")][:6])
