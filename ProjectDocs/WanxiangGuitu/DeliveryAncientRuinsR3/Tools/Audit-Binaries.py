import json
from pathlib import Path
import struct
import sys
import uuid

root = Path(sys.argv[1])
out = root / "Audit"
reports = json.loads((out / "build-audit.json").read_text(encoding="utf-8"))["runtimeDifferences"]
builds = [root / f"Project{name}-Build/Release" for name in ("A", "B")]
guid = [next(line.split("=", 1)[1] for line in (build / "WanxiangGuitu_Data/boot.config").read_text().splitlines()
             if line.startswith("build-guid=")) for build in builds]

def pe_stamp(data):
    if data[:2] != b"MZ":
        return None
    offset = struct.unpack_from("<I", data, 0x3C)[0]
    if data[offset:offset + 4] != b"PE\0\0":
        return None
    return dict(offset=offset + 8, value=struct.unpack_from("<I", data, offset + 8)[0])

def positions(data, needle):
    output = []
    offset = data.find(needle)
    while offset != -1:
        output.append(offset)
        offset = data.find(needle, offset + 1)
    return output

rows = []
for report in reports:
    name = report["path"]
    a, b = [(build / name).read_bytes() for build in builds]
    ranges = []
    start = None
    size = max(len(a), len(b))
    diff_count = 0
    for index, (left, right) in enumerate(zip(a, b)):
        if left != right:
            diff_count += 1
            if start is None:
                start = index
        elif start is not None:
            ranges.append([start, index])
            start = None
    if start is not None or len(a) != len(b):
        ranges.append([min(len(a), len(b)) if start is None else start, size])
        diff_count += abs(len(a) - len(b))
    guid_occurrences = []
    for value, data in zip(guid, (a, b)):
        guid_occurrences.append(dict(ascii=positions(data, value.encode()),
                                     bytes=positions(data, uuid.UUID(value).bytes),
                                     bytesLE=positions(data, uuid.UUID(value).bytes_le)))
    rows.append(dict(path=name, totalDifferentBytes=diff_count, firstRanges=ranges[:24],
                     numberOfRanges=len(ranges), peTimestamps=[pe_stamp(a), pe_stamp(b)],
                     matchingOwnBuildGuidLocations=guid_occurrences))
(out / "runtime-byte-deltas.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
for row in rows:
    print(row["path"], row["totalDifferentBytes"], row["peTimestamps"])
