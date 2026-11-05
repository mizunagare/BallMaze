from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
out = root / "Audit"
out.mkdir(exist_ok=True)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

types = {11: "TwinBlades", 12: "Greatsword", 13: "Scythe"}
cases = []
problems = []
gear_ids = set()
run_ids = set()
counts = Counter()
for case in (root / f"White{i}" for i in range(1, 9)):
    process = read(case / "process.json")
    probe = read(case / "probe.json")
    rows = (case / "ordinary-drops.txt").read_text(encoding="utf-8-sig").splitlines()
    pages = {}
    for page in (case / "WanxiangGuitu/ForestRuins/ground-loot").glob("*.json"):
        raw = page.read_bytes()
        if sha(raw) != page.stem:
            raise ValueError(f"invalid saved page {page}")
        for item in json.loads(raw)["items"]:
            identity = item["entityId"]
            if identity in pages and pages[identity][0] != item:
                raise ValueError(f"conflicting identity {identity}")
            pages[identity] = item, page.stem
    attempted = []
    if not process["exited"] or process["timedOut"] or process["exitCode"] not in (0, 1):
        problems.append(f"{case.name}: process evidence invalid")
    failures = [row["name"] for row in probe["rows"] if row["status"] != "PASS"]
    if (process["exitCode"] == 0) != (not failures) or any(name != "two-new-runs-white-equipment" for name in failures):
        problems.append(f"{case.name}: unexpected runtime assertion {failures}")
    for line in rows:
        run, seed, signature, quality = line.split()
        if run in run_ids or not re.fullmatch(r"[a-f0-9]{32}", run):
            problems.append(f"duplicate or invalid run {run}")
        run_ids.add(run)
        site = f"C1-RUINS-1/{run}/{run}:AncientRuins:1/{seed}/c1:plaza-chest"
        roll = int(sha(site.encode())[:4], 16)
        expected_materials = {
            "c1:" + sha((site + "/Ore").encode())[:32] + f":{1 + roll % 3}:Ore:",
            "c1:" + sha((site + "/CrystalShard").encode())[:32] + ":1:CrystalShard:",
        }
        expected_gear = roll % 100 < 25
        observed = quality == "gear-quality=White"
        if quality not in {"gear-quality=none", "gear-quality=White"} or observed != expected_gear:
            problems.append(f"{case.name}/{run}: formula/actual disagreement")
        record = dict(run=run, seed=int(seed), roll=roll, dropped=observed)
        actual_items = set(signature.split("|"))
        if observed:
            source = site + "/gear"
            expected_type = 11 + int(sha(source.encode())[:4], 16) % 3
            expected_entity = "c1:" + sha(source.encode())[:32]
            expected_id = sha(("NW1/id/" + source).encode())[:32]
            item, page = pages.get(expected_entity, ({}, None))
            gear = item.get("gear", {})
            expected_materials.add(f"{expected_entity}:1:CrystalShard:{expected_id}")
            if (not item.get("equipment") or gear.get("quality") != 0 or gear.get("id") != expected_id or
                    gear.get("type") != expected_type or gear.get("affixes") != [] or expected_id in gear_ids):
                problems.append(f"{case.name}/{run}: persisted object mismatch or repeat")
            else:
                gear_ids.add(expected_id)
                counts[types[expected_type]] += 1
            record.update(type=types[expected_type], entityId=expected_entity, gearId=expected_id, groundPage=page)
        if actual_items != expected_materials:
            problems.append(f"{case.name}/{run}: emitted item quantities or identities changed")
        attempted.append(record)
    if not 1 <= len(attempted) <= 18 or sum(x["dropped"] for x in attempted) > 2:
        problems.append(f"{case.name}: campaign exceeded bound or lacks actual attempts")
    cases.append(dict(case=case.name, processExit=process["exitCode"], failures=failures, runs=attempted))

buckets = sum(n % 100 < 25 for n in range(65536))
type_buckets = Counter(types[11 + n % 3] for n in range(65536))
passed = not problems and all(counts[label] >= 2 for label in types.values())
report = dict(status="PASS" if passed else "FAIL", campaigns=cases, actualFreshRuns=len(run_ids),
              actualQualityWhitePerType=dict(counts), discrepancies=problems,
              staticPrefixModel=dict(domain=65536, chestEligibility=buckets, gearTypeBuckets=dict(type_buckets),
                                     note="Separate hash inputs; no measured drop probability or distribution guarantee"))
(out / "white-audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(report["status"], len(run_ids), dict(counts), "campaign exits", [x["processExit"] for x in cases], problems)
