"""Find validated Direct3D shader containers in packaged Unity shader segments."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import struct
import sys

import lz4.block
import UnityPy

run, originals = map(Path, sys.argv[1:])
def sha(value):
    return hashlib.sha256(value).hexdigest()

def containers(data):
    for match in re.finditer(b'DXBC',data):
        pos = match.start()
        if len(data)-pos < 32:
            continue
        version,length,count = struct.unpack_from('<III',data,pos+20)
        if version!=1 or not 0<count<128 or not 32+4*count <= length <= len(data)-pos:
            continue
        offsets = struct.unpack_from(f'<{count}I',data,pos+32)
        if any(i<32+4*count or i+8>length for i in offsets):
            continue
        chunks = []
        for offset in offsets:
            size, = struct.unpack_from('<I',data,pos+offset+4)
            chunk = data[pos+offset:pos+offset+4]
            if not re.fullmatch(b'[A-Z0-9_]{4}',chunk) or offset+8+size>length:
                break
            chunks.append(chunk.decode('ascii'))
        else:
            if {'SHDR','SHEX','DXIL'} & set(chunks):
                yield dict(sha256=sha(data[pos:pos+length]),length=length,offset=pos,chunks=chunks)

def segments(raw):
    def ints(pos,n):
        return struct.unpack_from(f'<{n}I',raw,pos)
    def table(pos,n):
        count, = ints(pos,1)
        if count!=n:
            raise ValueError
        result=[]
        pos+=4
        for _ in range(n):
            size,=ints(pos,1)
            pos+=4
            if not 0<size<4096:
                raise ValueError
            result.append(ints(pos,size))
            pos+=4*size
        return pos,result
    for pos in range(0,len(raw)-48,4):
        n,=ints(pos,1)
        if not 1<=n<=5:
            continue
        platforms=ints(pos+4,n)
        if not set(platforms)&{4,28} or any(p>40 for p in platforms):
            continue
        try:
            off,offsets=table(pos+4+4*n,n)
            off,compressed=table(off,n)
            off,expanded=table(off,n)
            length,=ints(off,1)
            start=off+4
            if not 0<length<=len(raw)-start:
                continue
            bounds=[]
            for i in range(n):
                if not len(offsets[i])==len(compressed[i])==len(expanded[i]):
                    raise ValueError
                for k,(offset,comp,unc) in enumerate(zip(offsets[i],compressed[i],expanded[i])):
                    if not 0<comp<=length-offset or not 0<unc<=64*1024*1024:
                        raise ValueError
                    bounds.append((offset,offset+comp,platforms[i],k,unc))
            distinct=sorted({(a,b) for a,b,_,_,_ in bounds})
            if distinct[0][0]!=0 or distinct[-1][1]!=length or any(b!=c for (_,b),(c,_) in zip(distinct,distinct[1:])):
                continue
            decoded=[]
            for a,b,platform,k,unc in bounds:
                if platform not in (4,28):
                    continue
                payload=lz4.block.decompress(raw[start+a:start+b],uncompressed_size=unc)
                if len(payload)!=unc:
                    raise ValueError
                decoded.append(dict(platform=platform,segment=k,compressed=b-a,decompressed=unc,
                                    bytecodes=list(containers(payload))))
            if decoded:
                yield pos,decoded
        except (struct.error,ValueError,lz4.block.LZ4BlockError):
            continue

result={}
for arm in 'AB':
    data=originals/f'Project{arm}-Build/Release/WanxiangGuitu_Data'
    rows=[]
    for path in sorted(data.iterdir()):
        if not path.is_file() or not (path.name in ('globalgamemanagers','unity default resources','unity_builtin_extra')
                                      or path.suffix=='.assets' or re.fullmatch(r'level\d+',path.name)):
            continue
        for obj in UnityPy.load(str(path)).objects:
            if obj.type.name!='Shader':
                continue
            raw=obj.get_raw_data()
            candidates=list(segments(raw))
            try:
                name=obj.parse_as_object().m_ParsedForm.m_Name
            except (ValueError,AttributeError,EOFError,struct.error):
                name=None
            rows.append(dict(file=path.name,pathID=obj.path_id,name=name,objectSHA256=sha(raw),
                             candidateCount=len(candidates),segments=candidates[0][1] if len(candidates)==1 else []))
    result[arm]=rows
assert result['A']==result['B']
(run/'packaged-shaders.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('objects',len(result['A']), 'segments',Counter(x['candidateCount'] for x in result['A']))
print('DXBC fingerprints',len({h['sha256'] for row in result['A'] for s in row['segments'] for h in s['bytecodes']}))
