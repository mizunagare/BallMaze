import hashlib
import json
from pathlib import Path
import re
import sys

root, prior, source = map(Path, sys.argv[1:])
old = Path("I:/WGCombat/C1R3-1105-A")
out = root / "Audit"
out.mkdir(exist_ok=True)
def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name, value):
    (out / (name + ".json")).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")

history = read(prior / "Evidence/manifest.json")
for row in history:
    assert sha(old / row["sourceRelative"]) == row["sourceSHA256"], row
    assert sha(prior / "Evidence" / row["path"]) == row["publishedSHA256"], row
protected = read(Path("I:/WGCombat/C1-1105-A/protected-before.json"))
for row in protected:
    assert sha(Path(row["path"])) == row["sha256"], row["path"]

expected = read(old / "Audit/build-file-hashes.json")
altered = {"WanxiangGuitu_Data/RuntimeInitializeOnLoads.json", "WanxiangGuitu_Data/ScriptingAssemblies.json",
           "WanxiangGuitu_Data/Managed/C1R4ResourceProbe.dll"}
builds = {}
bee_values = []
stages = {}
for stage in ("ProjectA-Import", "ProjectA-Build", "ProjectB-Build"):
    directory = old / stage
    events = [json.loads(line) for line in (directory / "writes.jsonl").read_text(encoding="utf-8-sig").splitlines()]
    watched = []
    for event in events:
        observed = directory / "Observed" / event["copy"]
        assert sha(observed) == event["sha256"]
        watched.append(dict(event, observedAbsolutePath=str(observed), sourceAbsolutePath=str(source / event["path"])))
    stages[stage] = dict(before=read(directory / "inputs-before.json"), after=read(directory / "inputs-after.json"),
                         command=read(directory / "Editor.command.json"), events=watched)
for label in "AB":
    stage = f"Project{label}-Build"
    original = old / stage / "Release"
    pure, probe = (root / f"{kind}{label}/Release" for kind in ("Pure", "Probe"))
    releases = [{p.relative_to(path).as_posix(): sha(p) for p in path.rglob("*") if p.is_file()}
                for path in (original, pure, probe)]
    assert releases[0] == expected[stage] == releases[1]
    changes = {p for p in releases[1].keys() | releases[2].keys() if releases[1].get(p) != releases[2].get(p)}
    assert changes == altered
    assert "C1R4ResourceProbe.dll" not in (pure / "WanxiangGuitu_Data/ScriptingAssemblies.json").read_text(encoding="utf-8-sig")
    for kind in ("Pure", "Probe"):
        receipt = read(root / f"Run{kind}{label}/pure-runtime.json")
        assert receipt["titleOnly"] and receipt["titleReady"] and receipt["actualProcessExited"]
        assert receipt["exitCode"] == 0 and receipt["unchangedSyntheticFiles"] and not receipt["forcedTermination"]
    bee = read(pure / "WanxiangGuitu.exe.bee.json")
    cfg = bee["PlayerBuildProgramLibrary.Data.PlayerBuildConfig"]
    assert cfg["Development"] is False
    for key in ("EnableUnityConnect","EnablePerformanceReporting","EnableAnalytics","EnableCrashReporting","EnableInsights"):
        assert cfg["Services"][key] is False
    bee_values.append(bee)
    log = (old / stage / "Unity.log").read_text(encoding="utf-8-sig", errors="replace")
    meta = [dict(guid=match[1], resource=match[2]) for match in re.finditer(
        r"Importing 'GUID: ([0-9a-f]+) - Path: Assets/Resources/(PerformanceTestRun(?:Info|Settings)\.json)'", log)]
    builds[label] = dict(originalAbsolutePath=str(original), engineVersion=re.search(
        r"Initialize engine version: ([^\r\n]+)", log)[1], buildStatus=read(old / stage / "process.json"),
        resourceMetadataImportGuids=meta, pureFileCount=len(releases[1]), pureSHA256=releases[1],
        probeChangedFiles={p: releases[2].get(p) for p in sorted(changes)}, beeGuard=cfg["Services"],
        releaseProfile=read(pure / "WanxiangGuitu.exe.release.json"))
    assert len(meta) == 2

def changed(a, b, path="$"):
    if a == b:
        return []
    if isinstance(a, dict) and isinstance(b, dict):
        return [row for key in sorted(a.keys() | b.keys()) for row in changed(a.get(key), b.get(key), path + "." + key)]
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return [row for i, (x, y) in enumerate(zip(a, b)) for row in changed(x, y, f"{path}[{i}]")]
    return [dict(field=path, A=a, B=b)]
def normalized(value, label):
    if isinstance(value, str):
        # Normalize only the known twin directories, not settings or any other variable.
        return re.sub(r"Project" + label + r"(?=$|[-/\\])", "Project{arm}", value)
    if isinstance(value, dict):
        return {key:normalized(item,label) for key,item in value.items()}
    if isinstance(value, list):
        return [normalized(item,label) for item in value]
    return value
diff = changed(*bee_values)
normalized_diff = changed(*(normalized(data, label) for data, label in zip(bee_values,"AB")))
write("build-inputs", stages)
write("release-manifest", dict(historyPairsVerified=len(history), protectedFiles=len(protected), builds=builds,
      rawBeeDifferences=diff, differencesAfterExplicitRootMapping=normalized_diff))
print("Original and copied release files", [b["pureFileCount"] for b in builds.values()],
      "Bee differences raw/after twin path normalization", len(diff), len(normalized_diff))
