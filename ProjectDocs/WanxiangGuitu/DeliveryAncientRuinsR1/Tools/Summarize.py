from collections import Counter
from pathlib import Path
import json
import statistics
import sys

root = Path(sys.argv[1])
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


cases = []
boss = []
builds = []
for run in sorted(p for p in root.iterdir() if p.is_dir()):
    process = read(run / "process.json") if (run / "process.json").is_file() else None
    receipt = next((run / name for name in ("probe.json", "rules.json") if (run / name).is_file()), None)
    if receipt:
        data = read(receipt)
        counts = dict(Counter(row["status"] for row in data["rows"]))
        accepted = bool(data["rows"]) and set(counts) == {"PASS"} and process is not None and (
            process.get("exited") is True and process.get("exitCode") == 0 and process.get("timedOut") is False
        )
        cases.append(dict(run=run.name, layer=data.get("layer", "controlled Editor rules"),
                          mode=data.get("mode"), process=process, counts=counts, accepted=accepted,
                          failures=[row for row in data["rows"] if row["status"] != "PASS"]))
    trace = run / "boss-trace.jsonl"
    if trace.is_file():
        releases = {}
        begins = {}
        hit = Counter()
        evade = Counter()
        transition = Counter()
        previous = None
        for line in trace.read_text(encoding="utf-8-sig").splitlines():
            row = json.loads(line)
            key = (row["phase"], row["attack"])
            if row["stage"].startswith("phase-transition"):
                transition[row["stage"]] += 1
                continue
            if row["stage"] == "begin":
                begins[key] = row
            if row["stage"] == "release":
                summary = releases.setdefault(key, dict(phase=key[0], attack=key[1], releases=0,
                    windupSeconds=[], samePhaseReleaseIntervals=[], nominal={k:row[k] for k in
                    ("damage","windup","recovery","gap","reach","width","innerRadius")}))
                summary["releases"] += 1
                if key in begins:
                    summary["windupSeconds"].append(round(row["time"] - begins[key]["time"], 4))
                if previous and previous["phase"] == row["phase"]:
                    summary["samePhaseReleaseIntervals"].append(round(row["time"] - previous["time"], 4))
                previous = row
            if row["stage"] == "collision-damage" and row["after"] < row["before"]:
                hit[key] += 1
            if row["stage"] == "physical-miss" or row["stage"] == "collision-damage" and row["after"] == row["before"]:
                evade[key] += 1
        boss.append(dict(run=run.name, transition=dict(transition), attacks=[
            dict(summary, hpLossContacts=hit[key], avoidedContacts=evade[key]) for key, summary in releases.items()
        ]))
    release = run / "Release"
    if (release / "WanxiangGuitu.exe.summary.txt").is_file():
        files = sorted(release.glob("WanxiangGuitu.exe.*"))
        for path in files:
            (out / (run.name + "-" + path.name)).write_bytes(path.read_bytes())
        warning_log = (run / "Unity.log").read_text(encoding="utf-8-sig", errors="replace")
        warnings = [line for line in warning_log.splitlines() if "warning" in line.lower()]
        (out / (run.name + "-warning-log.txt")).write_text("\n".join(warnings), encoding="utf-8")
        builds.append(dict(run=run.name, process=process, warningLogLines=len(warnings)))
for name, rows in [("case-summary", cases), ("boss-timing", boss), ("build-summary", builds)]:
    (out / (name + ".json")).write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
for case in cases:
    print(case["run"], case["accepted"], case["counts"], [row["name"] for row in case["failures"]])
