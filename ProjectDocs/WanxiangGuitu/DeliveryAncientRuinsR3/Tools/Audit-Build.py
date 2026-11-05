from pathlib import Path
import difflib
import hashlib
import json
import re
import sys

root, source = map(Path, sys.argv[1:])
out = root / "Audit"
out.mkdir(exist_ok=True)

def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

stages = {}
diff_text = []
inventory = {}
runtime = {}
shader_counts = {}
excluded = set()
guard_fields = ("EnableUnityConnect", "EnableCrashReporting", "EnableInsights",
                "EnableAnalytics", "EnablePerformanceReporting")
for name in ("ProjectA-Import", "ProjectA-Build", "ProjectB-Build"):
    directory = root / name
    process = read(directory / "process.json")
    before = read(directory / "inputs-before.json")
    after = read(directory / "inputs-after.json")
    changes = {}
    for row in after["differences"]:
        rel = row["path"]
        baseline = (source / rel).read_bytes()
        final_path = root / name.split("-")[0] / rel
        snapshot = directory / "Observed" / (rel.replace("/", "_") + "-" + str(row["observed"]) + ".txt")
        actual = snapshot.read_bytes() if snapshot.is_file() else (
            final_path.read_bytes() if final_path.is_file() and sha(final_path) == row["observed"] else None)
        changes[rel] = dict(frozen=row["frozen"], actual=row["observed"], captured=actual is not None)
        if actual is not None:
            try:
                old_text = baseline.decode("utf-8-sig").splitlines()
                new_text = actual.decode("utf-8-sig").splitlines()
            except UnicodeError:
                diff_text.append(f"{name} {rel}: binary delta, SHA256 in stage receipt")
                continue
            text_delta = list(difflib.unified_diff(old_text, new_text, f"frozen/{rel}", f"{name}/{rel}", n=2))
            changes[rel]["textLinesChanged"] = bool(text_delta)
            diff_text.append(f"=== {name} {rel} ===")
            diff_text.extend(text_delta or ["Decoded lines identical; raw encoding or line ends differ"])
    observed = []
    baseline_hashes = {}
    for text in (directory / "writes.jsonl").read_text(encoding="utf-8-sig").splitlines():
        event = json.loads(text)
        rel = event["path"]
        baseline_hashes.setdefault(rel, sha(source / rel))
        file = directory / "Observed" / event["copy"]
        if sha(file) != event["sha256"]:
            raise ValueError(file)
        if event["sha256"] != baseline_hashes[rel]:
            old_lines = (source / rel).read_text(encoding="utf-8-sig").splitlines()
            new_lines = file.read_text(encoding="utf-8-sig").splitlines()
            delta = list(difflib.unified_diff(old_lines, new_lines, f"frozen/{rel}", f"{name}/{event['utc']}", n=2))
            if delta:
                diff_text.append(f"=== observed {name} {rel} {event['utc']} ===")
                diff_text.extend(delta)
            observed.append(event)
    stages[name] = dict(process=process, before=before, after=after, fieldComparisons=changes, observedNonFrozenVersions=observed)
    release = directory / "Release"
    if not release.is_dir():
        continue
    exe = release / "WanxiangGuitu.exe"
    bee = read(exe.with_name(exe.name + ".bee.json"))
    pc = bee["PlayerBuildProgramLibrary.Data.PlayerBuildConfig"]
    receipt = read(exe.with_name(exe.name + ".release.json"))
    if pc["Development"] is not False or any(pc["Services"].get(field) is not False for field in guard_fields):
        raise ValueError(f"release guard mismatch {name}")
    if sha(exe) != receipt["executableSHA256"].lower():
        raise ValueError(f"bad release receipt {name}")
    profile = source / receipt["profile"]
    connect = source / "ProjectSettings/UnityConnectSettings.asset"
    if sha(profile) != receipt["profileSHA256"].lower() or sha(connect) != receipt["unityConnectSHA256"].lower():
        raise ValueError(f"release profile or UnityConnect actual hash differs from checkout {name}")
    stages[name]["release"] = dict(receipt=receipt, services=pc["Services"], development=pc["Development"],
                                  buildReport=exe.with_name(exe.name + ".summary.txt").read_text(encoding="utf-8-sig").splitlines())
    inventory[name] = {file.relative_to(release).as_posix(): sha(file) for file in release.rglob("*") if file.is_file()}
    shader = shader_pass = api = None
    samples = []
    for line in (directory / "Unity.log").read_text(encoding="utf-8-sig", errors="replace").splitlines():
        if match := re.fullmatch(r'Compiling shader "([^"]+)"', line.strip()):
            shader = match[1]
            shader_pass = api = None
        elif match := re.match(r'Pass "(.*)" \(([^)]+)\)$', line.strip()):
            shader_pass = f"{match[1]} ({match[2]})"
            api = None
        elif match := re.search(r'Target graphics API:\s+(\S+)', line):
            api = match[1]
        elif match := re.search(r'After scriptable stripping:\s+(\d+)', line):
            if shader is not None and shader_pass is not None and api is not None:
                samples.append((shader, shader_pass, api, int(match[1])))
    shader_counts[name] = sorted(samples)
    runtime[name] = {}
    for relative, digest in inventory[name].items():
        if relative in {"WanxiangGuitu.exe.bee.json", "WanxiangGuitu.exe.release.json", "WanxiangGuitu.exe.summary.txt"} or "_BackUpThisFolder_ButDontShipItWithYourGame/" in relative:
            excluded.add(relative)
        else:
            runtime[name][relative] = digest

a, b = runtime["ProjectA-Build"], runtime["ProjectB-Build"]
differing = [dict(path=key, A=a.get(key), B=b.get(key)) for key in sorted(a.keys() | b.keys()) if a.get(key) != b.get(key)]
for change in differing:
    path = change["path"]
    if change["A"] is None or change["B"] is None:
        continue
    left = (root / "ProjectA-Build" / "Release" / path).read_bytes()
    right = (root / "ProjectB-Build" / "Release" / path).read_bytes()
    prefix = next((i for i, (a_byte, b_byte) in enumerate(zip(left, right)) if a_byte != b_byte), min(len(left), len(right)))
    change.update(bytesA=len(left), bytesB=len(right), commonPrefixBytes=prefix)
    if path.endswith((".config", ".json")):
        try:
            change["decodedDiff"] = list(difflib.unified_diff(left.decode("utf-8-sig").splitlines(),
                right.decode("utf-8-sig").splitlines(), f"A/{path}", f"B/{path}", n=1))
        except UnicodeError:
            pass
if any(not stage["process"]["exited"] or stage["process"]["timedOut"] or stage["process"]["exitCode"] != 0 for stage in stages.values()):
    state = "FAIL"
elif any(stage["after"]["differences"] or stage["before"]["differences"] or stage["observedNonFrozenVersions"] for stage in stages.values()):
    state = "UNRESOLVED"
else:
    state = "PASS"
byte_status = "PASS" if state == "PASS" else "FAIL" if state == "UNRESOLVED" else "NOT_RUN"
report = dict(checkoutByteIdentity=byte_status, effectiveBuildInputEquivalence=state, stages=stages, runtimeFilesCompared=len(a.keys() | b.keys()),
              runtimeDifferences=differing, metadataAndNonShippingExcluded=sorted(excluded),
              outputScope="A/B binary comparison only, separate from checkout equivalence")
(out / "build-audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
(out / "serialized-fields.txt").write_text("\n".join(diff_text) + "\n", encoding="utf-8")
(out / "shader-variant-counts.json").write_text(json.dumps(dict(
    samples=shader_counts,
    matching=bool(shader_counts.get("ProjectA-Build")) and shader_counts.get("ProjectA-Build") == shader_counts.get("ProjectB-Build"),
    scope="Editor log sample per named shader pass and API. Counts do not prove shader binary identity."),
    indent=2), encoding="utf-8")
(out / "build-file-hashes.json").write_text(json.dumps(inventory, indent=2), encoding="utf-8")
print(state, "runtime differences", len(differing), "/", report["runtimeFilesCompared"])
for name, stage in stages.items():
    print(name, "before", len(stage["before"]["differences"]), "after", len(stage["after"]["differences"]))
