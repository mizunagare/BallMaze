import ctypes as c
from ctypes import wintypes as w
import hashlib
import json
from pathlib import Path
import struct
import sys
import uuid

root, dll = map(Path, sys.argv[1:])
identity = json.loads((root/'unitydll-pdb-id.json').read_text('utf-8-sig'))[0]
path = root/'Symbols'/identity['file']
raw = path.read_bytes()
block, _, _, count, _, block_map = struct.unpack_from('<6I', raw, 32)
n = (count+block-1)//block
pages = struct.unpack_from(f'<{n}I', raw, block_map*block)
directory = b''.join(raw[p*block:(p+1)*block] for p in pages)[:count]
streams, first_size = struct.unpack_from('<II', directory)
first_pages = 0 if first_size==0xffffffff else (first_size+block-1)//block
info_page, = struct.unpack_from('<I', directory, 4+4*streams+4*first_pages)
age, = struct.unpack_from('<I', raw, info_page*block+8)
guid = uuid.UUID(bytes_le=raw[info_page*block+12:info_page*block+28]).hex.upper()
assert (guid,age)==(identity['guid'],identity['age'])

api = c.WinDLL('dbghelp', use_last_error=True)
kernel = c.WinDLL('kernel32', use_last_error=True)
kernel.GetCurrentProcess.restype = w.HANDLE
handle = kernel.GetCurrentProcess()
U64=c.c_uint64
api.SymSetOptions.argtypes=[w.DWORD]
api.SymSetOptions(0x00000002|0x00000400|0x00000200)
api.SymInitializeW.argtypes=[w.HANDLE,w.LPCWSTR,w.BOOL]
api.SymLoadModuleExW.argtypes=[w.HANDLE,w.HANDLE,w.LPCWSTR,w.LPCWSTR,U64,w.DWORD,c.c_void_p,w.DWORD]
api.SymLoadModuleExW.restype=U64
api.SymCleanup.argtypes=[w.HANDLE]

class Info(c.Structure):
    _fields_=[('SizeOfStruct',w.ULONG),('TypeIndex',w.ULONG),('Reserved',U64*2),('Index',w.ULONG),
              ('Size',w.ULONG),('ModBase',U64),('Flags',w.ULONG),('Value',U64),('Address',U64),
              ('Register',w.ULONG),('Scope',w.ULONG),('Tag',w.ULONG),('NameLen',w.ULONG),
              ('MaxNameLen',w.ULONG),('Name',c.c_char*1)]

callback=c.WINFUNCTYPE(w.BOOL,c.POINTER(Info),w.ULONG,c.c_void_p)
api.SymEnumSymbols.argtypes=[w.HANDLE,U64,c.c_char_p,callback,c.c_void_p]
assert api.SymInitializeW(handle,str(path.parent),False)
base=api.SymLoadModuleExW(handle,None,str(path),dll.name,0x180000000,dll.stat().st_size,None,0)
assert base
patterns=('*GraphicsStateCollection*','*GraphicsSettings*','*LightBaker*','*ShaderBuildSettings*','*CacheMissTracing*','*DefaultLightBaker*')
matches={}
for pattern in patterns:
    rows=[]
    @callback
    def collect(info,size,context):
        sym=info.contents
        name=c.string_at(c.addressof(sym)+Info.Name.offset,sym.NameLen).decode(errors='replace')
        rows.append(dict(name=name,rva=hex(sym.Address-base),size=size,tag=sym.Tag))
        return True
    ok=api.SymEnumSymbols(handle,base,pattern.encode(),collect,None)
    matches[pattern]=dict(ok=bool(ok),rows=rows)
api.SymCleanup(handle)
(root/'editor-symbols.json').write_text(json.dumps(dict(guid=guid,age=age,
    pdbSHA256=hashlib.sha256(raw).hexdigest(),matches=matches),indent=2),encoding='utf-8')
