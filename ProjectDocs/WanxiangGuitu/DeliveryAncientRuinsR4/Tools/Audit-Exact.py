from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import sys
import UnityPy

root = Path(sys.argv[1])
out = root / "Audit"
base = [root / f"Pure{label}/Release/WanxiangGuitu_Data" for label in "AB"]

def read(path):
    return next(iter(UnityPy.load(str(path)).files.values()))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

a, b = [read(path / "resources.assets") for path in base]
left, right = [(path / "resources.assets").read_bytes() for path in base]
reconstructed = bytearray(left)
changed_rows = []
for object_id, before in a.objects.items():
    after = b.objects[object_id]
    row = lambda obj, file: struct.pack(file.header.endian + "qqIi", obj.path_id,
        obj.byte_start - file.header.data_offset, obj.byte_size, obj.type_id)
    rb, ra = row(before, a), row(after, b)
    if rb != ra:
        offset = left.index(rb, 0, a.header.data_offset)
        assert left.find(rb, offset + 1, a.header.data_offset) == -1
        assert right[offset:offset + len(ra)] == ra
        reconstructed[offset:offset + len(ra)] = ra
        changed_rows.append(dict(pathID=object_id, metadataOffset=offset, fromOffset=before.byte_start,
                                 toOffset=after.byte_start, fromSize=before.byte_size, toSize=after.byte_size))
swapped = (248, 249)
assert a.objects[248].get_raw_data() == b.objects[249].get_raw_data()
assert a.objects[249].get_raw_data() == b.objects[248].get_raw_data()
for source_id, dest_id in zip(swapped, swapped[::-1]):
    source, dest = a.objects[source_id], b.objects[dest_id]
    reconstructed[dest.byte_start:dest.byte_start + dest.byte_size] = source.get_raw_data()
# Layout alignment is separate from object payload. All differing gap bytes must be zero padding in B.
low = min(b.objects[i].byte_start for i in swapped)
high = max(file.objects[i].byte_start + file.objects[i].byte_size for file in (a,b) for i in swapped)
padding = []
for offset in range(low, high):
    if any(b.objects[i].byte_start <= offset < b.objects[i].byte_start + b.objects[i].byte_size for i in swapped):
        continue
    if reconstructed[offset] != right[offset]:
        assert not any(obj.path_id not in swapped and obj.byte_start <= offset < obj.byte_start + obj.byte_size for obj in b.objects.values())
        assert right[offset] == 0
        reconstructed[offset] = 0
        padding.append(offset)
remaining = [dict(offset=i, modeled=x, actual=y) for i,(x,y) in enumerate(zip(reconstructed,right)) if x != y]
if remaining:
    (out / "remaining-current-attempt.json").write_text(json.dumps(remaining, indent=2), encoding="utf-8")
    raise ValueError(remaining[:30])

gamemgr = [read(path / "globalgamemanagers") for path in base]
left, right = [(path / "globalgamemanagers").read_bytes() for path in base]
copy = bytearray(left)
manager = next(o for o in gamemgr[0].objects.values() if o.type.name == "ResourceManager")
ptr = lambda path_id: struct.pack("<iq", 5, path_id)
reference_edits = []
for source_id, dest_id in zip(swapped, swapped[::-1]):
    local = manager.get_raw_data().index(ptr(source_id))
    assert manager.get_raw_data().count(ptr(source_id)) == 1
    absolute = manager.byte_start + local
    copy[absolute:absolute + 12] = ptr(dest_id)
    reference_edits.append(dict(offset=absolute, fromPathID=source_id, toPathID=dest_id))
assert copy == right

runtime = {}
for label in "AB":
    run = root / f"RunProbe{label}"
    data = (run / "resource-runtime.tsv").read_text(encoding="utf-8-sig").splitlines()
    index = Counter(line.split("\t", 1)[0] for line in data)
    keylist = (root / "resource-keys.txt").read_text(encoding="utf-8").splitlines()
    assert set(index) == set(keylist)
    rows = [line for line in data if "\tNULL" in line or "\tERROR" in line]
    runtime[label] = dict(keys=len(index), rows=len(data), nullOrError=rows, orderedRows=data)
compare = runtime["A"]["orderedRows"] == runtime["B"]["orderedRows"]
assert compare and all(row["nullOrError"] == ["ancientruins/bakedenvironment\tNULL"] for row in runtime.values())
for label, data in runtime.items():
    # Independently validate the two changed ID payloads from the engine rather than just comparing both runs.
    for path_id in swapped:
        obj = (a if label == "A" else b).objects[path_id].read_typetree()
        expected = hashlib.sha256(obj["m_Script"].encode()).hexdigest()
        line = obj["m_Name"].lower() + "\tUnityEngine.TextAsset\t" + obj["m_Name"] + "\t" + expected
        assert line in data["orderedRows"], line
report = dict(resourcesExactByteReconstruction=True, objectTableEdits=changed_rows,
              changedZeroPaddingOffsets=padding, globalgamemanagersExactByteReconstruction=True,
              resourceManagerPointerEdits=reference_edits, runtimeOrderedMatch=compare, runtime=runtime,
              resourceSidecarHashes=[digest(path / "resources.assets.resS") for path in base])
(out / "exact-reconstruction.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print("Exact offline reconstruction of both changed serialized files, table rows", len(changed_rows))
print("Runtime ordered match", compare, "counts", {k:(v["keys"],v["rows"],len(v["nullOrError"])) for k,v in runtime.items()})
