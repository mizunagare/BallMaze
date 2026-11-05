"""Read-only extraction of the shipping GraphicsSettings object and its PSO block."""
import hashlib
import json
from pathlib import Path
import struct
import sys

import UnityPy

root, original = map(Path, sys.argv[1:])
result = {}
for arm in 'AB':
    package = original / f'Project{arm}-Build/Release/WanxiangGuitu_Data'
    path = package / 'globalgamemanagers'
    asset = next(iter(UnityPy.load(str(path)).files.values()))
    obj, = (o for o in asset.objects.values() if o.type.name == 'GraphicsSettings')
    raw = obj.get_raw_data()
    (root / f'graphics-object-{arm}.hex.txt').write_text(raw.hex(' ') + '\n', encoding='utf-8')
    # The unversioned fallback tree predates this PSO block. Preserve that failure.
    try:
        obj.read_typetree()
        type_tree = 'strict decode succeeded'
    except (ValueError, EOFError) as exc:
        type_tree = f'{type(exc).__name__}: {exc}'
    assert asset.header.endian == '<' if hasattr(asset.header, 'endian') else asset.reader.endian == '<'
    anchor = raw.index(b'TracedCollection')
    assert raw.count(b'TracedCollection') == 1
    start = anchor - 20
    assert start >= 0 and start % 4 == 0
    pos = start
    def take(fmt):
        global pos
        values = struct.unpack_from('<' + fmt, raw, pos)
        pos += struct.calcsize('<' + fmt)
        return values[0] if len(values) == 1 else list(values)
    def string():
        global pos
        n = take('I')
        assert n < 128
        value = raw[pos:pos+n].decode('ascii')
        pos = (pos+n+3) & ~3
        return value
    pso = {}
    pso['collectionPPtr'] = take('iq')
    pso['startupAction'] = take('i')
    pso['traceSavePath'] = string()
    pso['traceSendToEditor'] = take('B')
    pos = (pos+3) & ~3
    pso['additionalWarmupCount'] = take('i')
    assert pso['additionalWarmupCount'] == 0
    pso['warmupAsync'] = take('B')
    pso['enableCacheMissTracing'] = take('B')
    pos = (pos+3) & ~3
    pso['warmupProgressivelyLimit'] = take('i')
    pso['cacheMissCollectionPath'] = string()
    assert pso['traceSavePath'] == 'TracedCollection' and pso['cacheMissCollectionPath'] == 'CacheMissCollection'
    result[arm] = dict(path=str(path), unityVersion=asset.unity_version, pathID=obj.path_id,
                       objectBytes=len(raw), objectSHA256=hashlib.sha256(raw).hexdigest(),
                       typeTreePresent=obj.serialized_type.node is not None, strictUnityPyDecode=type_tree,
                       psoOffset=[start,pos], psoRaw=raw[start:pos].hex(' '), psoDecoded=pso)
assert result['A']['objectSHA256'] == result['B']['objectSHA256']
(root/'graphics-payload.json').write_text(json.dumps(result,indent=2), encoding='utf-8')
