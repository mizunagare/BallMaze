from pathlib import Path
import hashlib
import json
import sys

old, previous_docs, root = map(Path, sys.argv[1:])
base = "d19c461fb9f089fdffa9beab9e42bb1814b629aa"

def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

history = read(previous_docs / "Evidence/manifest.json")
errors = []
for row in history:
    for path, key in ((old / row["sourceRelative"], "sourceSHA256"),
                      (previous_docs / "Evidence" / row["path"], "publishedSHA256")):
        if not path.is_file() or sha(path.read_bytes()) != row[key]:
            errors.append(str(path))

builds = []
baseline_files = read(previous_docs / "Evidence/build-files.json")
for current, baseline in (("TestBuild3", "TestBuild3"), ("TestBuild4", "TestBuild4"), ("PureFrozen", "PureBuild1")):
    prefix = f"{baseline}/Release/"
    entries = [file for file in baseline_files if file["path"].startswith(prefix)]
    if not entries:
        raise ValueError(f"missing frozen input {baseline}")
    files = root / current / "Release"
    actual = {f.relative_to(files).as_posix() for f in files.rglob("*") if f.is_file()}
    expected = {entry["path"][len(prefix):] for entry in entries}
    if actual != expected:
        errors.append(f"{current}: mismatched build inventory")
    for entry in entries:
        relative = entry["path"][len(prefix):]
        if not (files / relative).is_file() or sha((files / relative).read_bytes()) != entry["sha256"]:
            errors.append(f"{current}/{relative}")
    builds.append(dict(build=current, fixedSource=baseline, checked=len(entries)))

snapshots = []
for run in sorted(root.iterdir()):
    if not run.is_dir():
        continue
    for folder in (run / "SeedPackage", run / "WanxiangGuitu/ForestRuins"):
        for name in ("save.json", "save.json.bak"):
            path = folder / name
            if not path.is_file():
                continue
            envelope = read(path)
            if envelope["version"] != 9 or sha(envelope["payload"].encode()) != envelope["checksum"].lower():
                raise ValueError(str(path))
            data = json.loads(envelope["payload"])
            profile = data.get("profile") or {}
            receipts = profile.get("specialRewards") or []
            if len(receipts) != len({r["specialRewardId"] for r in receipts}):
                raise ValueError(f"duplicate receipt: {path}")
            active = data.get("activeRun") or {}
            checkpoint = active.get("checkpoint") or {}
            world = checkpoint.get("forest") or {}
            loot = []
            for reference in checkpoint.get("groundLootPages") or []:
                page = folder / "ground-loot" / (reference["hash"] + ".json")
                raw = page.read_bytes()
                items = json.loads(raw)["items"]
                if sha(raw) != reference["hash"] or len(raw) != reference["bytes"] or len(items) != reference["count"]:
                    raise ValueError(f"page mismatch: {page}")
                loot += items
            if len(loot) != len({item["entityId"] for item in loot}):
                raise ValueError(f"duplicate ground ID: {path}")
            snapshots.append(dict(path=path.relative_to(root).as_posix(), revision=envelope["revision"],
                profileId=profile.get("profileId"), runId=active.get("runId"), rulesR1=active.get("ruinsR1", False),
                mapId=world.get("mapId"), receipts=receipts, pending=[x["pendingId"] for x in profile.get("pending") or []],
                settlement=(data.get("settlement") or {}).get("settlementId"), status=(data.get("settlement") or {}).get("status"),
                loot=[dict(entityId=x["entityId"], gearId=(x.get("gear") or {}).get("id") if x["equipment"] else None,
                    quality=(x.get("gear") or {}).get("quality") if x["equipment"] else None, kind=x["kind"], amount=x["amount"])
                    for x in loot]))

out = root / "Audit"
out.mkdir(exist_ok=True)
for name, result in (("frozen-history", dict(base=base, historicalItems=len(history), builds=builds, differences=errors)),
                     ("v9-snapshots", snapshots)):
    (out / (name + ".json")).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("R1", len(history), "original/published pairs;", sum(x["checked"] for x in builds), "files; R2", len(snapshots), "v9 snapshots")
if errors:
    raise SystemExit("Frozen history/build differences. See Audit/frozen-history.json")

# Verify independent execution boundary and locate actual movement of the selected live actors.
import math
import ntpath

def lines(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines()]

def norm(path):
    return ntpath.normcase(ntpath.normpath(path))

launches = []
for run in sorted(root.iterdir()):
    if not (run / "probe.json").is_file():
        continue
    probe = read(run / "probe.json")
    layer = "Editor" if probe["layer"] == "controlled Editor" else "Player"
    command = read(run / f"{layer}.command.json")
    desktop = read(run / f"{layer}.desktop-process.json")
    launch = read(run / f"{layer}.launch-spec.json")
    process = read(run / "process.json")
    argv = command["arguments"]
    good = (norm(command["exe"]) == norm(desktop["exe"]) == norm(launch["Exe"]) and
            argv == launch["Arguments"] and not desktop["inputDesktopActive"] and
            norm(argv[argv.index("-wanxiang-storage-root") + 1]) == norm(str(run)) and
            norm(argv[argv.index("-logFile") + 1]) == norm(str(run / ("Unity.log" if layer == "Editor" else "Player.log"))) and
            process["exited"] is True and process["timedOut"] is False and process["forcedTermination"] is False)
    if layer == "Editor":
        native_exit = read(run / "Editor.exit.json")
        good = good and native_exit["hostPid"] == command["hostPid"] and native_exit["exitCode"] == process["exitCode"]
    launches.append(dict(run=run.name, layer=layer, command=command["exe"], pid=desktop["pid"],
                         hostPid=command["hostPid"], exitCode=process["exitCode"], bound=good))

def xyz(point):
    return [point[k] for k in ("x", "y", "z")]

geometry = []
for name in ("R2Boss", "Elite"):
    frames = [row for row in lines(root / name / "runtime-trace.jsonl") if row["stage"] == "combat-frame"]
    points = [xyz(row["from"]) for row in frames]
    geometry.append(dict(run=name, frames=len(frames), actor=frames[0]["target"],
                         first=points[0], last=points[-1],
                         maxDisplacement=max(math.dist(points[0], point) for point in points),
                         observedPathLength=sum(math.dist(a, b) for a, b in zip(points, points[1:]))))
for name, result in (("launches", launches), ("enemy-movement", geometry)):
    (out / (name + ".json")).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
if not launches or any(not case["bound"] for case in launches):
    raise SystemExit("Check execution association: Audit/launches.json")
