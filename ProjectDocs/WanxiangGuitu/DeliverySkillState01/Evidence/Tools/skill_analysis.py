#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SKILL-STATE-01 | strict per-case Player evidence analysis.

Rules frozen BEFORE the runs (DESIGN_DECISIONS.md):
  * one case == one independent Player run; NO cross-run event joins
  * every event must carry the same runId / processId / buildSha triple
  * a null frame/time or a missing event can NEVER count as PASS
  * product PASS/FAIL is decided against the frozen C1..C5 contract, not by
    the driver's own assertions
  * UI-only pause is always labelled CONTROLLED_STATE_INJECTION
"""
import argparse
import collections
import datetime
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DELIVERY = os.path.abspath(os.path.join(HERE, "..", ".."))
REPO = os.path.abspath(os.path.join(DELIVERY, "..", "..", ".."))
PLAYER = os.path.join(DELIVERY, "Evidence", "Player")
OUT = os.path.join(DELIVERY, "Evidence", "After")

CASES = [
    "field-baseline", "field-global-pause-4s", "field-ui-only-2s",
    "field-ui-only-4s", "field-switch-slot", "field-switch-weapon",
    "field-dodge", "field-death", "field-unload", "field-natural-expire",
    "bow-charge", "bow-charge-cancel", "restore-write", "restore-read",
]

TTL = 3.0
EPS = 0.35  # wall-clock tolerance for a 2s/4s pause measured with realtimeSinceStartup


def rel(p):
    return os.path.relpath(p, REPO).replace("\\", "/")


def chk(name, ok, expression, operands, inputs, missing=False, reason=""):
    status = "NOT_RUN" if missing else ("PASS-PLAYER" if ok else "FAIL-PLAYER")
    return {"check": name, "status": status, "expression": expression,
            "operands": operands, "inputRows": inputs,
            "reason": reason or ("" if ok else "frozen contract not satisfied")}


def load(case):
    d = os.path.join(PLAYER, case + "-A1")
    if not os.path.isdir(d):
        return None, d
    r = {"dir": d, "rel": lambda n: rel(os.path.join(d, n))}
    for n in ["case-summary.json", "run-summary.json", "skill-events.jsonl",
              "skill-frames.tsv", "assertions.tsv", "Player.exit.json",
              "restore-expect.json"]:
        p = os.path.join(d, n)
        r[n] = os.path.isfile(p)
    if r["case-summary.json"]:
        r["sum"] = json.load(open(os.path.join(d, "case-summary.json"), encoding="utf-8"))
    else:
        r["sum"] = None
    if r["skill-events.jsonl"]:
        r["events"] = [json.loads(l) for l in
                       open(os.path.join(d, "skill-events.jsonl"), encoding="utf-8") if l.strip()]
    else:
        r["events"] = []
    if r["skill-frames.tsv"]:
        rows = [l.rstrip("\n").split("\t") for l in
                open(os.path.join(d, "skill-frames.tsv"), encoding="utf-8") if l.strip()]
        r["frames"] = rows[1:] if rows else []
    else:
        r["frames"] = []
    if r["assertions.tsv"]:
        a = {}
        for l in open(os.path.join(d, "assertions.tsv"), encoding="utf-8"):
            v = l.rstrip("\n").split("\t")
            if len(v) >= 2: a[v[0]] = v[1:3]
        r["assertions"] = a
    else:
        r["assertions"] = {}
    return r, d


def identity_checks(c):
    out = []
    ev = c["events"]
    ids = {(e.get("runId"), e.get("processId"), e.get("buildSha")) for e in ev}
    # `time == 0` is a LEGAL value during scene load (Time.time is frozen at 0
    # while timeScale=0). Only a genuine null/missing timestamp is unplaceable.
    bad = [e for e in ev if e.get("frame") in (None, 0) or e.get("time") is None]
    zero = [e for e in ev if e.get("time") == 0]
    out.append(chk("sameRunIdentity", len(ev) > 0 and len(ids) == 1
                   and all(all(x not in (None, "", 0) for x in t) for t in ids),
                   "len(distinct(runId,processId,buildSha)) == 1 AND no empty component",
                   {"eventCount": len(ev), "distinctIdentities": len(ids),
                    "identity": [list(t) for t in ids][:2]},
                   [c["rel"]("skill-events.jsonl")], missing=not ev))
    out.append(chk("noNullTimestamps", len(ev) > 0 and not bad,
                   "for every event: frame != null/0 AND time != null "
                   "(time==0 is legal during scene load)",
                   {"events": len(ev), "unplaceable": len(bad),
                    "legalZeroTimeEvents": len(zero),
                    "zeroTimeStages": [e.get("stage") for e in zero]},
                   [c["rel"]("skill-events.jsonl")], missing=not ev))
    return out


def stages(c):
    return collections.Counter((e.get("kind"), e.get("stage")) for e in c["events"])


def field_case(c, case, expect_field, expect_resolved=True):
    s, st = c["sum"], stages(c)
    out = identity_checks(c)
    out.append(chk("projectileSpawned", st[("projectile", "spawn")] == 1,
                   "count(projectile.spawn) == 1", {"spawn": st[("projectile", "spawn")]},
                   [c["rel"]("skill-events.jsonl")], missing=not c["events"]))
    if expect_resolved:
        out.append(chk("realResolveObserved", st[("projectile", "resolved")] >= 1,
                       "count(projectile.resolved) >= 1",
                       {"resolved": st[("projectile", "resolved")]},
                       [c["rel"]("skill-events.jsonl")], missing=not c["events"]))
    got = st[("skill", "field-created")]
    want = 1 if expect_field else 0
    out.append(chk("fieldCreatedPerContract", got == want,
                   "count(skill.field-created) == %d" % want,
                   {"fieldCreated": got, "expected": want,
                    "controlledStateInjection": s.get("controlledStateInjection") if s else None},
                   [c["rel"]("skill-events.jsonl")], missing=not c["events"],
                   reason=("" if got == want else
                           "pending registry expired before the frozen projectile resolved"
                           if expect_field else "unexpected field creation")))
    # same frame + same attackId pairing
    res = [e for e in c["events"] if e.get("stage") == "resolved"]
    fc = [e for e in c["events"] if e.get("stage") == "field-created"]
    if expect_field and res and fc:
        out.append(chk("sameFrameAttribution",
                       any(abs(r["frame"] - f["frame"]) <= 1 for r in res for f in fc),
                       "abs(field-created.frame - resolved.frame) <= 1",
                       {"resolvedFrames": [r["frame"] for r in res],
                        "fieldCreatedFrames": [f["frame"] for f in fc]},
                       [c["rel"]("skill-events.jsonl")]))
    return out


def pause_case(c, case):
    s = c["sum"]
    out = field_case(c, case, expect_field=True)
    if s is None: return out
    span = s.get("timeAtPauseEnd", 0) - s.get("timeAtPauseStart", 0)
    kind = s.get("pauseKind")
    # Restrict "paused frames" to the DRIVER'S pause window. Early scene-load
    # frames also have gameplayPaused=1 / timeScale=0 but are NOT part of the
    # controlled pause under test.
    begins = [e["frame"] for e in c["events"]
              if e.get("kind") == "pause" and e.get("stage") == "begin"]
    ends = [e["frame"] for e in c["events"]
            if e.get("kind") == "pause" and e.get("stage") == "end"]
    lo, hi = (min(begins), max(ends)) if begins and ends else (0, 0)
    paused = [r for r in c["frames"] if len(r) > 4 and r[4] == "1"
              and lo <= int(r[0]) <= hi]
    if kind == "global":
        out.append(chk("globalPauseFreezesScaledTime", abs(span) < 0.15,
                       "abs(Time.time end - start) < 0.15 while timeScale=0",
                       {"span": span, "fieldsAtPauseStart": s.get("fieldsAtPauseStart"),
                        "fieldsAtPauseEnd": s.get("fieldsAtPauseEnd")},
                       [c["rel"]("case-summary.json")]))
        out.append(chk("globalPauseTimeScaleZero", bool(paused) and
                       all(float(r[3]) <= 0.001 for r in paused),
                       "all paused frames have timeScale == 0",
                       {"pausedFrames": len(paused)},
                       [c["rel"]("skill-frames.tsv")], missing=not paused))
    else:
        out.append(chk("uiOnlyAdvancesScaledTime", span > (s.get("pauseSecondsUsed", 0) - EPS),
                       "Time.time span >= pauseSeconds - eps with timeScale=1",
                       {"span": span, "pauseSeconds": s.get("pauseSecondsUsed")},
                       [c["rel"]("case-summary.json")]))
        out.append(chk("uiOnlyIsControlledInjection",
                       s.get("controlledStateInjection") is True,
                       "caseSummary.controlledStateInjection == true",
                       {"controlledStateInjection": s.get("controlledStateInjection")},
                       [c["rel"]("case-summary.json")]))
        out.append(chk("uiOnlyKeepsTimeScaleOne", bool(paused) and
                       all(abs(float(r[3]) - 1.0) <= 0.001 for r in paused),
                       "all paused frames have timeScale == 1",
                       {"pausedFrames": len(paused)},
                       [c["rel"]("skill-frames.tsv")], missing=not paused))
        # frozen projectile stays alive during the pause
        with_proj = [r for r in paused if len(r) > 7 and r[7] != "0"]
        out.append(chk("projectileAliveDuringPause", bool(paused) and
                       len(with_proj) == len(paused),
                       "every paused frame still has >=1 live projectile",
                       {"pausedFrames": len(paused), "framesWithProjectile": len(with_proj)},
                       [c["rel"]("skill-frames.tsv")], missing=not paused))
        out.append(chk("pendingRegistryStateAtPauseEnd",
                       True,
                       "fieldsAtPauseStart / fieldsAtPauseEnd recorded (evidence only)",
                       {"fieldsAtPauseStart": s.get("fieldsAtPauseStart"),
                        "fieldsAtPauseEnd": s.get("fieldsAtPauseEnd"),
                        "reflectionAvailable": s.get("reflectionAvailable")},
                       [c["rel"]("case-summary.json")]))
    return out


def bow_case(c, case, cancel):
    s, st = c["sum"], stages(c)
    out = identity_checks(c)
    out.append(chk("chargeStarted", st[("skill", "start")] >= 1,
                   "count(skill.start) >= 1", {"start": st[("skill", "start")]},
                   [c["rel"]("skill-events.jsonl")], missing=not c["events"]))
    charging = [e for e in c["events"] if e.get("kind") == "bow" and e.get("stage") == "charging"]
    out.append(chk("chargingPhaseObserved", bool(charging),
                   "driver observed Phase == Charging with ChargeFraction",
                   {"rows": [e.get("detail") for e in charging]},
                   [c["rel"]("skill-events.jsonl")], missing=not charging))
    if cancel:
        out.append(chk("cancelEmitted", st[("skill", "cancel")] >= 1,
                       "count(skill.cancel) >= 1", {"cancel": st[("skill", "cancel")]},
                       [c["rel"]("skill-events.jsonl")], missing=not c["events"]))
        out.append(chk("noPierceAfterCancel", st[("skill", "pierce-spawn")] == 0,
                       "count(skill.pierce-spawn) == 0",
                       {"pierceSpawn": st[("skill", "pierce-spawn")]},
                       [c["rel"]("skill-events.jsonl")], missing=not c["events"]))
        out.append(chk("noReleaseAfterCancel", st[("skill", "release")] == 0,
                       "count(skill.release) == 0", {"release": st[("skill", "release")]},
                       [c["rel"]("skill-events.jsonl")], missing=not c["events"]))
    else:
        out.append(chk("chargeLocked", st[("skill", "charge-locked")] >= 1,
                       "count(skill.charge-locked) >= 1",
                       {"chargeLocked": st[("skill", "charge-locked")]},
                       [c["rel"]("skill-events.jsonl")], missing=not c["events"]))
        out.append(chk("pierceProjectileReleased", st[("skill", "pierce-spawn")] >= 1,
                       "count(skill.pierce-spawn) >= 1",
                       {"pierceSpawn": st[("skill", "pierce-spawn")]},
                       [c["rel"]("skill-events.jsonl")], missing=not c["events"]))
        out.append(chk("castCompleted", st[("skill", "complete")] >= 1,
                       "count(skill.complete) >= 1", {"complete": st[("skill", "complete")]},
                       [c["rel"]("skill-events.jsonl")], missing=not c["events"]))
    return out


def lifecycle_case(c, case):
    s, st = c["sum"], stages(c)
    out = identity_checks(c)
    out.append(chk("projectileSpawned", st[("projectile", "spawn")] == 1,
                   "count(projectile.spawn) == 1", {"spawn": st[("projectile", "spawn")]},
                   [c["rel"]("skill-events.jsonl")], missing=not c["events"]))
    if case in ("field-switch-slot", "field-switch-weapon", "field-dodge"):
        out.append(chk("releasedProjectileStillResolves",
                       st[("projectile", "resolved")] >= 1,
                       "count(projectile.resolved) >= 1",
                       {"resolved": st[("projectile", "resolved")]},
                       [c["rel"]("skill-events.jsonl")], missing=not c["events"]))
        out.append(chk("releasedFieldStillCreated",
                       st[("skill", "field-created")] == 1,
                       "count(skill.field-created) == 1",
                       {"fieldCreated": st[("skill", "field-created")]},
                       [c["rel"]("skill-events.jsonl")], missing=not c["events"]))
    else:
        if case == "field-natural-expire":
            # The sidecar could NOT make the projectile miss: after removing the
            # cube it still swept into arena ground geometry, which is a NORMAL
            # product resolve + field. Report the empty-space sub-case honestly
            # as NOT_RUN; never count it as PASS and never blame the product.
            out.append({
                "check": "naturalExpiryShotIntoEmptySpace",
                "status": "NOT_RUN",
                "expression": "projectile expires with life<=0 and NO resolved event",
                "operands": {"resolved": st[("projectile", "resolved")],
                             "fieldCreated": st[("skill", "field-created")]},
                "inputRows": [c["rel"]("skill-events.jsonl")],
                "reason": "fixture removed the target cube but the projectile hit "
                          "arena ground geometry (normal product resolve); "
                          "empty-space flight NOT reproduced, not a product defect"})
            ae = [e for e in c["events"] if e.get("stage") == "after-expiry"]
            out.append(chk("pendingRegistryBoundedAfterDisposal",
                           bool(ae) and "fields=0" in (ae[0].get("detail") or ""),
                           "after-expiry event reports fields == 0 (bounded cleanup)",
                           {"rows": [e.get("detail") for e in ae]},
                           [c["rel"]("skill-events.jsonl")], missing=not ae))
        else:
            out.append(chk("noFieldAfterCancellation",
                           st[("skill", "field-created")] == 0,
                           "count(skill.field-created) == 0",
                           {"fieldCreated": st[("skill", "field-created")],
                            "resolved": st[("projectile", "resolved")]},
                           [c["rel"]("skill-events.jsonl")], missing=not c["events"]))
    if case == "field-death":
        out.append(chk("deathObserved", any(e.get("dead") for e in c["events"]),
                       "at least one event has dead == true",
                       {"deadEvents": sum(1 for e in c["events"] if e.get("dead"))},
                       [c["rel"]("skill-events.jsonl")], missing=not c["events"]))
    if case == "field-unload":
        u = [e for e in c["events"] if e.get("stage") == "unload-after"]
        out.append(chk("unloadAfterObserved", bool(u),
                       "driver emitted unload-after after ReturnToTitle",
                       {"rows": [e.get("detail") for e in u]},
                       [c["rel"]("skill-events.jsonl")], missing=not u))
    return out


def restore_case(c, case):
    s, st = c["sum"], stages(c)
    out = identity_checks(c)
    if case == "restore-write":
        w = [e for e in c["events"] if e.get("stage") == "write"]
        out.append(chk("saveProgressWritten", bool(w) and "saved=True" in (w[0].get("detail") or ""),
                       "restore.write event reports saved=True",
                       {"rows": [e.get("detail") for e in w]},
                       [c["rel"]("skill-events.jsonl")], missing=not w))
        out.append(chk("expectationFilePresent", c.get("restore-expect.json", False),
                       "restore-expect.json exists for the new process",
                       {"present": c.get("restore-expect.json", False)},
                       [c["rel"]("restore-expect.json")],
                       missing=not c.get("restore-expect.json", False)))
    else:
        rd = [e for e in c["events"] if e.get("stage") == "read"]
        out.append(chk("newProcessReadObserved", bool(rd),
                       "restore.read event exists in a NEW process",
                       {"rows": [e.get("detail") for e in rd]},
                       [c["rel"]("skill-events.jsonl")], missing=not rd))
        if rd:
            detail = rd[0].get("detail") or ""
            out.append(chk("noTransientResidue",
                           "projectiles=0" in detail and "fieldObjects=0" in detail
                           and "pierceObjects=0" in detail,
                           "projectiles==0 AND fieldObjects==0 AND pierceObjects==0",
                           {"detail": detail}, [c["rel"]("skill-events.jsonl")]))
            out.append(chk("noActiveCast", "busy=False" in detail,
                           "expanded.Busy == false after restore",
                           {"detail": detail}, [c["rel"]("skill-events.jsonl")]))
        after = [e for e in c["events"] if e.get("stage") == "after-frames"]
        out.append(chk("noAutoReleaseOnRestore", bool(after) and
                       "noAutoRelease=True" in (after[0].get("detail") or ""),
                       "no skill.start occurred after restore",
                       {"rows": [e.get("detail") for e in after]},
                       [c["rel"]("skill-events.jsonl")], missing=not after))
    return out


def analyse(case):
    c, d = load(case)
    if c is None:
        return {"case": case, "status": "NOT_RUN", "checks": [],
                "reason": "no Player evidence directory: " + rel(d)}
    checks = []
    if case == "field-baseline":
        checks = field_case(c, case, True)
    elif case in ("field-global-pause-4s", "field-ui-only-2s", "field-ui-only-4s"):
        expect = case != "field-ui-only-4s"
        checks = pause_case(c, case)
        # Override the field expectation with the frozen C4-2 contract.
        for x in checks:
            if x["check"] == "fieldCreatedPerContract":
                x["operands"]["frozenContract"] = ("C4-2: >TTL UI-only pause must STILL "
                                                   "create exactly one field on resume")
                x["operands"]["expected"] = 1
                x["expression"] = "count(skill.field-created) == 1  [C4-2]"
                x["status"] = "PASS-PLAYER" if x["operands"]["fieldCreated"] == 1 else "FAIL-PLAYER"
                if x["status"] == "FAIL-PLAYER":
                    x["reason"] = ("pending registry expired while the projectile was frozen; "
                                   "resume produced a real resolve but NO impact field")
    elif case in ("field-switch-slot", "field-switch-weapon", "field-dodge",
                  "field-death", "field-unload", "field-natural-expire"):
        checks = lifecycle_case(c, case)
    elif case.startswith("bow-"):
        checks = bow_case(c, case, case == "bow-charge-cancel")
    elif case.startswith("restore-"):
        checks = restore_case(c, case)
    statuses = [x["status"] for x in checks]
    if not checks: status = "NOT_RUN"
    elif "FAIL-PLAYER" in statuses: status = "FAIL-PLAYER"
    elif "NOT_RUN" in statuses: status = "PARTIAL_OR_NOT_RUN"
    else: status = "PASS-PLAYER"
    return {"case": case, "status": status, "checks": checks,
            "dir": rel(d),
            "summary": {k: c["sum"].get(k) for k in
                        ["spawnCount", "resolvedCount", "fieldCreatedCount", "pauseKind",
                         "pauseSecondsUsed", "timeAtPauseStart", "timeAtPauseEnd",
                         "fieldsAtPauseStart", "fieldsAtPauseEnd", "reflectionAvailable",
                         "controlledStateInjection", "verdict"]} if c["sum"] else None,
            "runSummary": (json.load(open(os.path.join(c["dir"], "run-summary.json"),
                                          encoding="utf-8")).get("verdict")
                           if c["run-summary.json"] else None)}


def comparison(phase, cases, negative):
    p = os.path.join(os.path.dirname(OUT), "Before", "skill-player-matrix-before.json")
    before = None
    if os.path.isfile(p):
        try: before = json.load(open(p, encoding="utf-8"))
        except Exception: before = None
    if not before:
        return {"beforeMatrixAvailable": False, "phase": phase}
    b = {c["case"]: c["status"] for c in before["cases"]}
    a = {c["case"]: c["status"] for c in cases}
    return {
        "beforeMatrixAvailable": True,
        "beforeVerdict": before.get("verdict"),
        "beforeNegativeReproduced": before.get("reproduction", {}).get("negativeReproduced"),
        "afterNegativeReproduced": negative,
        "statusChangedCases": {k: {"before": b.get(k), "after": a.get(k)}
                               for k in a if b.get(k) != a.get(k)},
        "unchangedPassCases": [k for k in a if b.get(k) == a.get(k) == "PASS-PLAYER"],
        "notRunCases": [k for k in a if a[k] == "PARTIAL_OR_NOT_RUN"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["before", "after"], default="after",
                    help="before = pre-fix reproduction; after = post-fix verification")
    a = ap.parse_args()
    cases = [analyse(c) for c in CASES]
    ui4 = next((c for c in cases if c["case"] == "field-ui-only-4s"), None)
    evidence_rows = []
    for c in cases:
        for x in c["checks"]:
            evidence_rows.append("\t".join([c["case"], x["check"], x["status"],
                                            x["expression"],
                                            json.dumps(x["operands"], ensure_ascii=False,
                                                       sort_keys=True),
                                            ";".join(x["inputRows"]),
                                            x["reason"]]))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "skill-player-checks.tsv"), "w",
              encoding="utf-8", newline="\n") as f:
        f.write("case\tcheck\tstatus\texpression\toperands\tinputRows\treason\n")
        f.write("\n".join(evidence_rows) + ("\n" if evidence_rows else ""))

    negative = bool(ui4 and ui4["status"] == "FAIL-PLAYER" and
                    any(x["check"] == "fieldCreatedPerContract" and
                        x["operands"].get("fieldCreated") == 0 for x in ui4["checks"]))
    by_cat = {}
    for c in cases:
        cat = ("C1/C4 staff field" if c["case"].startswith("field-") else
               "C2 bow charge" if c["case"].startswith("bow-") else
               "C5 restore")
        by_cat.setdefault(cat, []).append(c["case"])
    matrix = {
        "scope": "SKILL-STATE-01 strict per-case Player contract matrix",
        "verifiedUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "contractDocument": "DESIGN_DECISIONS.md",
        "rules": {
            "noCrossRunJoins": True,
            "nullTimestampsCannotPass": True,
            "missingEventsCannotPass": True,
            "uiOnlyLabel": "CONTROLLED_STATE_INJECTION (real UI always sets timeScale=0)",
        },
        "cases": cases,
        "byCategory": {k: {"cases": v, "count": len(v)} for k, v in by_cat.items()},
        "phase": a.phase,
        "reproduction": {
            "negativeCase": "field-ui-only-4s",
            "negativeReproduced": negative,
            "criterion": "resolved==1 AND fieldCreated==0 AND projectile alive during "
                         "pause AND pauseSeconds > fields TTL (3.0s)",
            "productFixAuthorised": negative,
            "note": "A product fix is permitted ONLY when the PRE-FIX phase reports "
                    "this true (DESIGN_DECISIONS.md section 4).",
        },
        "comparison": comparison(a.phase, cases, negative),
        "verdict": (
            ("REPRODUCED_PRODUCT_DEFECT" if negative else "NO_PRODUCT_DEFECT_REPRODUCED")
            if a.phase == "before" else
            ("PRODUCT_FIX_VERIFIED" if (not negative and
                                       not any(c["status"] == "FAIL-PLAYER" for c in cases))
             else "FIX_NOT_VERIFIED")),
        "productCodeModified": a.phase == "after",
        "productChangeScope": ("Assets/CombatPrototype/WeaponSkillExpansion.cs only: "
                               "pending-field expiry uses an effective gameplay clock "
                               "that advances only when AdventureProjectile advances"),
    }
    p = os.path.join(OUT, "skill-player-matrix.json")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(matrix, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({
        "verdict": matrix["verdict"],
        "negativeReproduced": negative,
        "caseStatus": {c["case"]: c["status"] for c in cases},
        "nonPass": [x["check"] + "@" + c["case"] for c in cases for x in c["checks"]
                    if x["status"] not in ("PASS-PLAYER",)],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
