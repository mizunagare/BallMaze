from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import sys
import UnityPy
from UnityPy.helpers import TypeTreeHelper

root, project = map(Path, sys.argv[1:])
out = root / "Audit"
out.mkdir(exist_ok=True)
# Prefer the audited Python decoder for reproducibility and explicit parser errors.
TypeTreeHelper.read_typetree_boost = None

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save(name, result):
    (out / (name + ".json")).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

def read(path):
    return next(iter(UnityPy.load(str(path)).files.values()))

def external(file):
    return [dict(path=e.path, guid=e.guid.hex(), type=e.type) for e in file.externals]

def pointers(value, where="$"):
    if isinstance(value, dict):
        if "m_FileID" in value and "m_PathID" in value:
            yield dict(field=where, fileID=value["m_FileID"], pathID=value["m_PathID"])
        for key, child in value.items():
            yield from pointers(child, where + "." + key)
    elif isinstance(value, (list, tuple)):
        for i, child in enumerate(value):
            yield from pointers(child, f"{where}[{i}]")

def names(file):
    results = []
    for entry in file.objects.values():
        try:
            name = entry.peek_name()
            error = None
        except Exception as exc:
            name = None
            error = type(exc).__name__
        results.append(dict(pathID=entry.path_id, type=entry.type.name, name=name, nameReadError=error,
                            index=len(results), offset=entry.byte_start, size=entry.byte_size, sha256=sha(entry.get_raw_data())))
    return results

def target(key, pointer, manager, file):
    file_id, path_id = pointer["m_FileID"], pointer["m_PathID"]
    dep = external(manager)[file_id - 1] if file_id else dict(path="globalgamemanagers", guid=None, type=None)
    obj = file.objects[path_id] if dep["path"].lower() == "resources.assets" else None
    return dict(key=key, fileID=file_id, pathID=path_id, external=dep, type=obj.type.name if obj else None,
                name=obj.peek_name() if obj else None, rawSHA256=sha(obj.get_raw_data()) if obj else None)

source = {}
for meta in (project / "Assets").rglob("*.meta"):
    segments = meta.relative_to(project).parts
    if "Resources" not in segments or not meta.with_suffix("").is_file():
        continue
    pos = len(segments) - 1 - tuple(reversed(segments)).index("Resources")
    key = Path(*segments[pos + 1:]).with_suffix("").with_suffix("").as_posix().lower()
    line = next((s[6:] for s in meta.read_text(encoding="utf-8-sig").splitlines() if s.startswith("guid: ")), None)
    source.setdefault(key, []).append(dict(source=meta.with_suffix("").relative_to(project).as_posix(), guid=line))

items, records, file_list, candidate_refs = {}, {}, {}, {}
for label in "AB":
    data = root / f"Pure{label}/Release/WanxiangGuitu_Data"
    resources = read(data / "resources.assets")
    manager = read(data / "globalgamemanagers")
    rm = next(o for o in manager.objects.values() if o.type.name == "ResourceManager")
    container = rm.read_typetree()["m_Container"]
    rows = [target(key, pointer, manager, resources) for key, pointer in container]
    for row in rows:
        row["projectGuidCandidates"] = source.get(row["key"].lower(), [])
    records[label] = rows
    objects = names(resources)
    items[label] = dict(version=resources.unity_version, serializedFormat=resources.header.version,
                        hasEmbeddedTypeTree=resources._enable_type_tree, count=len(objects),
                        types=dict(Counter(o["type"] for o in objects)), externals=external(resources), objects=objects,
                        streamSHA256=sha((data / "resources.assets.resS").read_bytes()))
    file_list[label] = {}
    candidate_refs[label] = []
    files = [p for p in data.iterdir() if p.name in ("resources.assets", "globalgamemanagers", "globalgamemanagers.assets")
             or p.name.startswith("sharedassets") and p.suffix == ".assets" or p.name.startswith("level") and p.name[5:].isdigit()]
    for p in files:
        file = read(p)
        file_list[label][p.name] = dict(count=len(file.objects), externals=external(file), sha256=sha(p.read_bytes()))
        file_ids = [i for i, ext in enumerate(external(file), 1) if ext["path"].lower() == "resources.assets"]
        if p.name == "resources.assets":
            file_ids.append(0)
        if not file_ids:
            continue
        candidates = [struct.pack(file.header.endian + "iq", i, path) for i in file_ids for path in (248, 249)]
        for obj in file.objects.values():
            raw = obj.get_raw_data()
            if not any(needle in raw for needle in candidates):
                continue
            try:
                refs = [ref for ref in pointers(obj.read_typetree()) if ref["fileID"] in file_ids and ref["pathID"] in (248, 249)]
                error = None
            except Exception as exc:
                refs = []
                error = type(exc).__name__
            candidate_refs[label].append(dict(file=p.name, objectID=obj.path_id, type=obj.type.name, refs=refs, parseError=error))
    save("inventory-" + label, items[label])
    save("resource-index-" + label, rows)

a, b = ([o["pathID"] for o in items[label]["objects"]] for label in "AB")
assert a == b
changed = [x["pathID"] for x, y in zip(items["A"]["objects"], items["B"]["objects"]) if x["sha256"] != y["sha256"]]
changed_content = []
for label in "AB":
    path = root / f"Pure{label}/Release/WanxiangGuitu_Data/resources.assets"
    resources = read(path)
    for oid in changed:
        obj = resources.objects[oid]
        payload = obj.read_typetree()
        changed_content.append(dict(build=label, pathID=oid, type=obj.type.name, name=payload["m_Name"],
                                    text=payload["m_Script"], textSHA256=sha(payload["m_Script"].encode()), dependencies=list(pointers(payload))))
logical = lambda row: (row["key"], row["external"], row["type"], row["name"], row["rawSHA256"])
order_equal = all(logical(x) == logical(y) for x, y in zip(records["A"], records["B"])) and len(records["A"]) == len(records["B"])
ids = [dict(key=x["key"], A=x["pathID"], B=y["pathID"]) for x, y in zip(records["A"], records["B"]) if x["pathID"] != y["pathID"]]
save("resources-comparison", dict(pathOrderIdentical=a==b, changedPayloadIDs=changed, changedContent=changed_content,
     resourceKeyCount=len(records["A"]), logicalResourceIndexIdentical=order_equal, changedResourcePathIDs=ids,
     serializedFiles=file_list, referenceCandidates=candidate_refs))
keys = [r["key"] for r in records["A"] if r["key"]]
keys = list(dict.fromkeys(keys))
(root / "resource-keys.txt").write_text("\n".join(keys) + "\n", encoding="utf-8")
print("objects", len(a), "changed", changed, "logical key equality", order_equal, "keys", len(keys))
print({label: len(refs) for label, refs in candidate_refs.items()})
