#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CP06-INTEGRATION-02-R1 / R1-01: single-source RUN_LEDGER.csv generator.

Reads ONLY the archived raw evidence under Evidence/Player/<run>/ and emits one
row per independent Player run. No number in the delivery documents may be
typed by hand: REPORT / ACCEPTANCE / Evidence INDEX / CURRENT_STATUS all quote
the totals printed by this script.

Classification is mechanical and mutually exclusive:
  PASS  -> complete.txt == "PASS" and exitCode == 0 and zero FAIL assertions
  FAIL  -> one or more FAIL assertions (complete.txt == "FAIL")
  SKIP  -> assertions exist but every step is SKIP (none in this batch)
  NOT_RUN / INCOMPLETE -> no complete.txt / process exited before the driver
                         wrote a verdict (none in this batch)

Exit code 0 alone is never treated as PASS: the assertion ledger, complete.txt
and absence of failure.txt are all required.

The per-run `classificationReason` / `category` annotations come from the
frozen REVIEW_NOTES table below. They are prose reasons for a verdict that was
already derived mechanically; they never change a verdict.
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLAYER = os.path.abspath(os.path.join(HERE, "..", "Player"))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "RUN_LEDGER.csv"))

# runName -> (category, reason, supersededBy)
# category: PRODUCT_FAILURE | DRIVER_ERROR | PRECONDITION_ERROR | PRODUCT_LEGAL_REFUSAL |
#           ACCEPTED | ACCEPTED_SCENARIO_ONLY
REVIEW = {
    "forest-loop": ("PRECONDITION_ERROR",
                    "hero not pinned adjacent before striking (dist=2.43m > 1.8m melee volume), so Strike() began but Melee() never reached the enemy",
                    "forest-loop-7"),
    "forest-loop-2": ("PRECONDITION_ERROR",
                      "same distance precondition (dist=2.43m); added diagnostics only",
                      "forest-loop-7"),
    "forest-loop-3": ("PRECONDITION_ERROR",
                      "one-time RestorePosition removed, so stale depart-time combat state blocked Ready (began=0, dist=1.10m)",
                      "forest-loop-7"),
    "forest-loop-4": ("DRIVER_ERROR",
                      "driver called PlayerInput.Focus(true) on the SAME frame as Strike(); Focus() runs Barrier() -> UIBlocked=true -> Ready=false",
                      "forest-loop-7"),
    "forest-loop-5": ("DRIVER_ERROR",
                      "same-frame Focus/Strike conflict confirmed by ReadyDiag (uiBlocked=True was the only blocking sub-condition)",
                      "forest-loop-7"),
    "forest-loop-6": ("ACCEPTED",
                      "complete sortie passed; superseded by forest-loop-7 which additionally defeats the engaged enemy",
                      "forest-loop-7"),
    "forest-loop-7": ("ACCEPTED",
                      "forest sortie: real kill, real gather+pickup, extract/commit/ack, re-depart with a new run id", ""),
    "ruins-loop": ("PRECONDITION_ERROR",
                   "driver demanded a vein although ForestRegionRuntime.BuildRuins hides every in-scene AdventureResource and builds none (ruins has no gatherable node by design)",
                   "ruins-loop-3"),
    "ruins-loop-2": ("PRECONDITION_ERROR",
                     "same: zero active veins after the hides, driver had no SKIP path yet (available empty)",
                     "ruins-loop-3"),
    "ruins-loop-3": ("ACCEPTED",
                     "ruins sortie: real guard kill 60->0, gather step recorded SKIP with the product-side reason, real extract/settle, new run id", ""),
    "cavern-loop-1": ("ACCEPTED",
                      "cavern sortie: real watcher kill, Ore gather + real pickup (duplicate refused), extract/settle, new run id", ""),
    "cavern-boss-1": ("ACCEPTED",
                      "real challenge interaction then real boss damage (33) and legitimate extraction", ""),
    "cross-region-chain-1": ("ACCEPTED",
                             "forest -> ruins -> cavern in one process, distinct run ids and region identities, no contamination", ""),
    "xproc-1": ("ACCEPTED",
                "process 1 saves mid-run and writes xproc-expect.txt (runId/region/instance/seed/wave)", ""),
    "xproc-2": ("ACCEPTED",
                "process 2 restores the SAME run through the real Continue() entry; run id read from the product save API matches xproc-expect.txt", ""),
    "weapon-smoke-1": ("DRIVER_ERROR",
                       "first Strike() of the first weapon was swallowed by the depart transition, driver had no bounded retry yet",
                       "weapon-smoke-2"),
    "weapon-smoke-2": ("ACCEPTED",
                       "seven weapons: select + real Strike + release frame confirmed for each", ""),
    "skill-smoke-1": ("PRODUCT_LEGAL_REFUSAL",
                      "slot 2 was cast before slot 1's cooldown finished; PrepareExpanded shares one skillAt, so the product legitimately refused (phase=Cancelled)",
                      "skill-smoke-3"),
    "skill-smoke-2": ("DRIVER_ERROR",
                      "driver projectile counter locked onto the first AttackId, so the cross-region staff projectile was filtered out (cavern passed, forest falsely failed)",
                      "skill-smoke-3"),
    "skill-smoke-3": ("ACCEPTED",
                      "eight expanded skills over two regions incl. cooldown waits, bow charging and staff field projectile", ""),
    "reward-loop-1": ("ACCEPTED_SCENARIO_ONLY",
                      "single-region reward loop passed as a scenario; crafted=False because one cavern sortie cannot pay the White recipe (Wood2+Stone1+Ore2). NOT evidence of successful crafting",
                      "reward-loop-2"),
    "reward-loop-2": ("ACCEPTED",
                      "two-region gather -> atomic warehouse commit -> real craft of a White sword (items 8->9) -> re-depart", ""),
    "fail-paths-1": ("PRODUCT_LEGAL_REFUSAL",
                     "death settlement committed but never acknowledged, so HasResult stayed set and Depart was legitimately refused",
                     "fail-paths-2"),
    "fail-paths-2": ("ACCEPTED",
                     "extraction blocked away from exit, real death -> Death outcome -> region unload -> ack -> recovery depart, isolated save path", ""),
    # ---- R1-02 additions: real-input natural release of bow.pierce ----
    "bow-pierce-natural-1": ("DRIVER_ERROR",
                             "driver picked the firing spot from the enemy's own Y, so the hero was placed under the terrain (pierce-spawn y=-3.44); the projectile hit ground and blocked. Cooldown assertion was also placed after the 5 s flight wait, so an 11 s cooldown was read as 0",
                             "bow-pierce-natural-8"),
    "bow-pierce-natural-2": ("DRIVER_ERROR",
                             "driver asserted the bow muzzle sits at chest height (+0.6 m) but the product's bow string source is ~0.30 m above the hero origin; ground-relative check replaced it",
                             "bow-pierce-natural-8"),
    "bow-pierce-natural-3": ("DRIVER_ERROR",
                             "no PlayerInput.Focus(true) before the second cast, so after the 11 s cooldown the skill key produced no Down edge and charging never started",
                             "bow-pierce-natural-8"),
    "bow-pierce-natural-4": ("ACCEPTED",
                             "first clean natural release: hold -> key-up -> unique release + unique pierce spawn -> contact + HP drop; multi-target step SKIPped because no collinear pair was available on that trajectory",
                             "bow-pierce-natural-8"),
    "bow-pierce-natural-5": ("DRIVER_ERROR",
                             "lifecycle wait did not allow for the product freezing the game clock (level-up choice / death Freeze); the projectile is intentionally not advanced while paused, so the wait timed out. Repeats were also counted globally across both casts instead of per projectile",
                             "bow-pierce-natural-8"),
    "bow-pierce-natural-6": ("ACCEPTED",
                             "two natural releases, both piercing two targets, per-projectile repeats 0, real cooldown 10.17 s with a refused cast; the cast-2 target list was closed before the contacts arrived, so its detail read cast2DistinctTargets=0[]",
                             "bow-pierce-natural-8"),
    "bow-pierce-natural-7": ("ACCEPTED",
                             "same chain with the cast-2 window kept open (cast2DistinctTargets=1); the level-up pause still cut the cast-2 flight short, so the lifecycle step ended on a product freeze",
                             "bow-pierce-natural-8"),
    "bow-pierce-natural-8": ("ACCEPTED",
                             "primary R1-02 evidence: partial charge (key-up 0.504) and full charge (1.0) both released by real key-up, one release + one pierce spawn each, each projectile pierced 2 targets (HP 60->5.43->0), per-projectile repeats 0, cooldown 10.17 s with a refused second cast, both projectiles expired; the level-up pause was resolved through HeroProgression.SelectChoice so the cast-2 flight could finish", ""),
}

# The 24 runs that existed before CP06-INTEGRATION-02-R1 (the R1-01 baseline).
# Everything else in Evidence/Player was produced by this round (phase R1-02).
BASE_RUNS = {
    "forest-loop", "forest-loop-2", "forest-loop-3", "forest-loop-4", "forest-loop-5",
    "forest-loop-6", "forest-loop-7", "ruins-loop", "ruins-loop-2", "ruins-loop-3",
    "cavern-loop-1", "cavern-boss-1", "cross-region-chain-1", "xproc-1", "xproc-2",
    "weapon-smoke-1", "weapon-smoke-2", "skill-smoke-1", "skill-smoke-2", "skill-smoke-3",
    "reward-loop-1", "reward-loop-2", "fail-paths-1", "fail-paths-2",
}


def read_summary(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def driver_run_id(path):
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                j = json.loads(line)
            except ValueError:
                continue
            if j.get("kind") == "identity":
                return j.get("runId", "")
    return ""


def audit_asserts(path):
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    first_fail = ""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 2 or parts[1] not in counts:
                    continue
                counts[parts[1]] += 1
                if parts[1] == "FAIL" and not first_fail:
                    first_fail = parts[0]
    return counts, first_fail


def read_text(path):
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read().strip()


def launcher_record(run_dir):
    """Player.exit.json as written by the launcher (pid / exit code / timeout)."""
    p = os.path.join(run_dir, "Player.exit.json")
    if os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as f:
                return json.load(f)
        except ValueError:
            return {}
    return {}


def exit_code_of(run_dir, summary):
    """Exit code of the Player process.

    Newer runs record it in run-summary.json; the six earliest R1-02 runs were
    produced by an older driver schema that omitted it, so the archived
    Player.exit.json (written by the launcher, not by the driver) is the
    authoritative fallback. Both are raw evidence files.
    """
    if summary.get("exitCode") is not None:
        return summary.get("exitCode")
    return launcher_record(run_dir).get("exitCode")


def classify(run_dir):
    name = os.path.basename(run_dir)
    summary_path = os.path.join(run_dir, "run-summary.json")
    if not os.path.exists(summary_path):
        return dict(runName=name, mode="", pid="", exitCode="", finalVerdict="INCOMPLETE",
                    firstFailure="", detail="run-summary.json missing")
    s = read_summary(summary_path)
    exit_code = exit_code_of(run_dir, s)
    pid = s.get("pid") or launcher_record(run_dir).get("pid") or ""
    counts, first_fail = audit_asserts(os.path.join(run_dir, "assertions.tsv"))
    complete = read_text(os.path.join(run_dir, "complete.txt"))
    has_failure = os.path.exists(os.path.join(run_dir, "failure.txt"))
    if has_failure or counts["FAIL"] > 0 or complete == "FAIL":
        verdict = "FAIL"
    elif complete == "PASS" and exit_code == 0:
        verdict = "PASS" if counts["PASS"] > 0 else "NOT_RUN"
    elif not complete:
        verdict = "INCOMPLETE"
    else:
        verdict = "INCOMPLETE"
    return dict(
        runName=name, mode=s.get("mode", ""), pid=pid,
        exitCode=exit_code, finalVerdict=verdict,
        firstFailure=first_fail, complete=complete, passes=counts["PASS"],
        fails=counts["FAIL"], skips=counts["SKIP"],
        driverRunId=driver_run_id(os.path.join(run_dir, "int-events.jsonl")),
        driverSha=s.get("driverDllSHA256", ""), exeSha=s.get("exeSHA256", ""),
        startUtc=s.get("startUtc", ""), failureTxt=has_failure)


def main():
    if not os.path.isdir(PLAYER):
        raise SystemExit("missing Player evidence dir: " + PLAYER)
    runs = [classify(os.path.join(PLAYER, d)) for d in sorted(os.listdir(PLAYER))
            if os.path.isdir(os.path.join(PLAYER, d))]
    rows = []
    for r in runs:
        cat, reason, superseded = REVIEW.get(r["runName"], ("UNREVIEWED", "", ""))
        historical = "yes" if r["finalVerdict"] == "FAIL" or superseded else "no"
        if r["finalVerdict"] == "PASS" and cat == "UNREVIEWED":
            raise SystemExit("PASS run without a review note: " + r["runName"])
        rows.append({
            "runId": r["driverRunId"],
            "runName": r["runName"],
            "phase": "R0" if r["runName"] in BASE_RUNS else "R1-02",
            "mode": r["mode"],
            "pid": r["pid"],
            "exitCode": r["exitCode"],
            "finalVerdict": r["finalVerdict"],
            "isHistorical": historical,
            "category": cat,
            "firstFailure": r["firstFailure"] or "-",
            "supersededBy": superseded or "-",
            "passAssertions": r["passes"],
            "failAssertions": r["fails"],
            "skipAssertions": r["skips"],
            "classificationReason": reason,
            "evidencePath": "Evidence/Player/" + r["runName"],
        })
    cols = ["runId", "runName", "phase", "mode", "pid", "exitCode", "finalVerdict",
            "isHistorical", "category", "firstFailure", "supersededBy",
            "passAssertions", "failAssertions", "skipAssertions",
            "classificationReason", "evidencePath"]
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow(row)

    total = len(rows)
    verdicts = {}
    for row in rows:
        verdicts[row["finalVerdict"]] = verdicts.get(row["finalVerdict"], 0) + 1
    ids = [row["runId"] for row in rows]
    summary = {
        "ledger": os.path.relpath(OUT, os.path.dirname(OUT)).replace("\\", "/"),
        "rows": total,
        "uniqueRunIds": len(set(ids)),
        "verdicts": verdicts,
        "historical": sum(1 for row in rows if row["isHistorical"] == "yes"),
        "byPhase": {},
        "categories": {},
    }
    for row in rows:
        p = summary["byPhase"].setdefault(row["phase"], {"rows": 0, "PASS": 0, "FAIL": 0})
        p["rows"] += 1
        p[row["finalVerdict"]] = p.get(row["finalVerdict"], 0) + 1
    for row in rows:
        summary["categories"][row["category"]] = summary["categories"].get(row["category"], 0) + 1
    with open(os.path.join(HERE, "r1-ledger-summary.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    if len(set(ids)) != total:
        raise SystemExit("duplicate runId in ledger")
    if sum(verdicts.values()) != total:
        raise SystemExit("classification does not close")
    return 0


if __name__ == "__main__":
    sys.exit(main())
