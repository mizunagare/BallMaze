import hashlib
import json
from pathlib import Path
import struct
import sys
import uuid

root = Path(sys.argv[1])
out = root / "Audit"
mvid = {row["label"]: row["mvid"] for row in json.loads((out / "managed-mvid.json").read_text(encoding="utf-8-sig"))}
files = {}
for label in "AB":
    data = (root / f"Pure{label}/Release/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll").read_bytes()
    u16 = lambda pos: struct.unpack_from("<H", data, pos)[0]
    u32 = lambda pos: struct.unpack_from("<I", data, pos)[0]
    pe = u32(0x3C)
    optional = pe + 24
    directory = optional + (96 if u16(optional) == 0x10B else 112)
    sections = optional + u16(pe + 20)
    def raw_offset(rva):
        for i in range(u16(pe + 6)):
            pos = sections + i * 40
            vsize, va, size, raw = struct.unpack_from("<IIII", data, pos + 8)
            if va <= rva < va + max(vsize, size):
                return raw + rva - va
        raise ValueError(rva)
    debug_rva, length = struct.unpack_from("<II", data, directory + 6 * 8)
    debug_offset = raw_offset(debug_rva)
    marked = [dict(kind="PE COFF timestamp", start=pe + 8, end=pe + 12)]
    gid = uuid.UUID(mvid[label]).bytes_le
    offset = data.index(gid)
    assert data.count(gid) == 1
    marked.append(dict(kind="CLI Module MVID", start=offset, end=offset + 16, value=mvid[label]))
    for i in range(0, length, 28):
        pos = debug_offset + i
        type_id, size, _, pointer = struct.unpack_from("<IIII", data, pos + 12)
        marked.append(dict(kind="debug directory timestamp", type=type_id, start=pos + 4, end=pos + 8))
        if type_id == 2 and data[pointer:pointer + 4] == b"RSDS":
            value = data[pointer + 24:pointer + size].split(b"\0", 1)[0].decode()
            marked.append(dict(kind="CodeView PDB GUID/age/path", start=pointer + 4, end=pointer + size, path=value))
        if type_id == 19:
            algo, digest = data[pointer:pointer + size].split(b"\0", 1)
            marked.append(dict(kind="PDB checksum", start=pointer + len(algo) + 1, end=pointer + size,
                               algorithm=algo.decode(), digest=digest.hex()))
    files[label] = (data, marked)
a,b = (files[label][0] for label in "AB")
assert len(a) == len(b)
diff = [i for i,(x,y) in enumerate(zip(a,b)) if x != y]
uncovered = [i for i in diff if any(not any(row["start"] <= i < row["end"] for row in files[label][1]) for label in "AB")]
report = dict(differingBytes=len(diff), uncoveredOffsets=uncovered,
              knownSections={label: files[label][1] for label in "AB"})
(out / "managed-byte-attribution.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print("Managed differences", len(diff), "outside known metadata", uncovered)
