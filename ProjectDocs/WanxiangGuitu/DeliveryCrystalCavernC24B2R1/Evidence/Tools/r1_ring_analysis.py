#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CP06-C24-B2-R1 | R1-02 observation Player RingProbe matrix.

Reads the RAW ring-probes.jsonl produced by each REAL observation Player run,
never re-computes geometry from a model, and compares each sample against the
FROZEN C24-B2-RING-1 expectations. Every check records the exact probe row
used, the comparison expression and the status. Missing runs / missing probes
are NOT_RUN or INCOMPLETE, never PASS.

Writes: Evidence/After/ring-player-matrix.json
        Evidence/After/ring-player-checks.tsv
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DELIVERY = os.path.abspath(os.path.join(HERE, "..", ".."))
REPO = os.path.abspath(os.path.join(DELIVERY, "..", "..", ".."))
PLAYER = os.path.join(DELIVERY, "Evidence", "Player")
OUT = os.path.join(DELIVERY, "Evidence", "After")

# Frozen B2 contract values (NOT to be tuned after the fact).
FROZEN = {"inner": 2.2, "outer": 6.0, "halfHeight": 1.2, "epsilon": 1e-4,
          "rawDamage": 22.0, "contractVersion": "C24-B2-RING-1"}

CASES = {
    "band": {"expectGeometry": True, "expectApplied": True, "note": "inside the annulus"},
    "inner-edge": {"expectGeometry": True, "expectApplied": True, "note": "capsule crosses inner radius"},
    "outer-edge": {"expectGeometry": True, "expectApplied": True, "note": "capsule crosses outer radius"},
    "inner-safe": {"expectGeometry": False, "expectApplied": False, "note": "capsule entirely inside the hole"},
    "outer-safe": {"expectGeometry": False, "expectApplied": False, "note": "capsule entirely outside the ring"},
    "wall": {"expectGeometry": True, "expectClear": False, "expectApplied": False,
             "note": "geometry true but line of sight blocked"},
    "dodge": {"expectGeometry": True, "expectEvaded": True, "expectApplied": False,
              "note": "dodge immunity keeps HP unchanged"},
}

NOT_RUN = [
    {"case": "height-in / height-tangent / height-just-out / height-above",
     "reason": "the R1 driver only places the hero on the arena ground plane; "
               "vertical-band samples require a controlled elevated hit body that "
               "this batch did not implement. B2 Editor geometry cases exist but "
               "are NOT Player evidence."},
    {"case": "GameplayPaused clock freeze / Active window deferral",
     "reason": "the driver does not open the UI pause surface; no runtime "
               "pause-state event was captured."},
    {"case": "player death / leave-arena / Boss death / scene unload cancellation",
     "reason": "no dedicated cancellation run was executed; the product "
               "CancelIntent path is only covered by static control flow."},
    {"case": "multiple Colliders on the hero root",
     "reason": "all executed samples observed bodyCount=1 (CharacterController only); "
               "no additional enabled non-trigger capsule was attached."},
    {"case": "native keyboard/mouse input and independent human play",
     "reason": "out of scope for this batch; observations use the same business "
               "entry points but are driven by the sidecar script."},
]


def load_probes(case):
    p = os.path.join(PLAYER, "r1-ring-%s-A1" % case, "ring-probes.jsonl")
    if not os.path.isfile(p):
        return None, p
    with open(p, "r", encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()], p


def identity(rows):
    ids = {(r.get("runId"), r.get("processId"), r.get("buildSha")) for r in rows}
    return len(ids) == 1 and all(all(x not in (None, "", 0) for x in i) for i in ids), ids


def row(name, status, expression, operands, evidence, reason=""):
    return {"check": name, "status": status, "expression": expression,
            "operands": operands, "evidenceRows": evidence, "reason": reason}


def analyse_case(case, spec):
    probes, path = load_probes(case)
    rel = os.path.relpath(path, REPO).replace("\\", "/")
    if probes is None or len(probes) == 0:
        return {"case": case, "path": rel, "status": "NOT_RUN",
                "checks": [row("probeRecorded", "NOT_RUN", "len(probes) > 0",
                               {"probes": 0}, [], "no raw RingProbe record")],
                "note": spec["note"]}, ["NOT_RUN"]
    first = probes[0]
    applied = [p for p in probes if p.get("applied")]
    ident_ok, ids = identity(probes)
    checks = []

    def add(name, ok, expr, operands, ev, missing=False, reason=""):
        status = "PASS-PLAYER" if ok else ("NOT_RUN" if missing else "FAIL")
        checks.append(row(name, status, expr, operands, ev, reason))

    add("probeRecorded", True, "len(probes) > 0", {"probes": len(probes)},
        [rel + ":1"])
    g = first.get("geometry")
    add("geometryMatchesFrozenContract", g == spec["expectGeometry"],
        "first.geometry == %s" % spec["expectGeometry"],
        {"geometry": g, "expected": spec["expectGeometry"],
         "heroRootRadius": first.get("heroRootRadius"),
         "bodyRadius": first.get("bodyRadius")}, [rel + ":1"])
    if "expectClear" in spec:
        add("lineOfSightBlocked", first.get("clear") == spec["expectClear"],
            "first.clear == %s" % spec["expectClear"],
            {"clear": first.get("clear"), "expected": spec["expectClear"]}, [rel + ":1"])
    if "expectEvaded" in spec:
        add("dodgeImmunityObserved", first.get("evaded") == spec["expectEvaded"],
            "first.evaded == %s" % spec["expectEvaded"],
            {"evaded": first.get("evaded"), "expected": spec["expectEvaded"]}, [rel + ":1"])
    add("singleDamagePerRelease", len(applied) <= 1,
        "count(applied==true) <= 1 for one release",
        {"appliedCount": len(applied), "release": first.get("release"),
         "probeFrames": len(probes)}, [rel + ":1..%d" % len(probes)])
    # Product semantics (CrystalCavernBossBrain.HitArea): alreadySpent is TRUE
    # only AFTER the one Damage opportunity has been consumed (hit == true).
    # A no-hit window (safe zone / occlusion / dodge) keeps hit == false and
    # re-evaluates every Active frame, so alreadySpent stays FALSE by design.
    # The R1.0 analysis tool incorrectly demanded alreadySpent on those
    # windows; that was a TEST ASSERTION error, never a product defect. The
    # initial verdict is preserved in ring-player-matrix-initial.json.
    if spec.get("expectApplied"):
        add("laterFramesAreAlreadySpent",
            all(p.get("alreadySpent") for p in probes[1:]) if len(probes) > 1 else False,
            "all(probes[1:].alreadySpent == true) after the damage opportunity was spent",
            {"laterFrames": len(probes) - 1,
             "alreadySpentCount": sum(1 for p in probes[1:] if p.get("alreadySpent"))},
            [rel + ":2..%d" % len(probes)], missing=(len(probes) <= 1))
    else:
        add("noDamageAcrossAllFrames",
            all(not p.get("applied") for p in probes),
            "all(probes.applied == false) for a no-hit window; "
            "alreadySpent remains false because hit was never set",
            {"probeFrames": len(probes), "appliedCount": len(applied),
             "alreadySpentCount": sum(1 for p in probes if p.get("alreadySpent"))},
            [rel + ":1..%d" % len(probes)])
    hp_b, hp_a = first.get("hpBefore"), probes[-1].get("hpAfter")
    if "expectApplied" in spec and not spec["expectApplied"]:
        add("hpUnchangedWhenNoDamage", hp_b == hp_a,
            "first.hpBefore == last.hpAfter", {"hpBefore": hp_b, "hpAfter": hp_a},
            [rel + ":1", rel + ":%d" % len(probes)])
    add("frozenParametersUnchanged",
        all(abs(first.get(k, -1) - FROZEN[k]) < 1e-3
            for k in ["inner", "outer", "halfHeight", "epsilon"]) and
        abs(first.get("rawDamage", -1) - FROZEN["rawDamage"]) < 1e-6,
        "inner/outer/halfHeight/epsilon/rawDamage == frozen C24-B2-RING-1",
        {k: first.get(k) for k in ["inner", "outer", "halfHeight", "epsilon", "rawDamage"]},
        [rel + ":1"])
    add("sameRunIdentity", ident_ok,
        "len(distinct(runId,processId,buildSha)) == 1 AND no empty component",
        {"probeRows": len(probes), "distinctIdentities": len(ids)},
        [rel + ":1..%d" % len(probes)])
    if spec["expectGeometry"]:
        add("narrowPhaseUsesRealBodies", (first.get("bodyCount") or 0) >= 1,
            "first.bodyCount >= 1 when geometry is true",
            {"bodyCount": first.get("bodyCount"),
             "bodyHeight": first.get("bodyHeight")}, [rel + ":1"])

    statuses = [c["status"] for c in checks]
    if "FAIL" in statuses:
        overall = "FAIL"
    elif "NOT_RUN" in statuses or "INCOMPLETE" in statuses:
        overall = "INCOMPLETE"
    else:
        overall = "PASS-PLAYER"
    return {"case": case, "path": rel, "status": overall,
            "probeCount": len(probes), "release": first.get("release"),
            "hpBefore": hp_b, "hpAfter": hp_a,
            "appliedCount": len(applied),
            "firstProbe": {k: first.get(k) for k in
                           ["frame", "release", "bodyCount", "contact", "geometry",
                            "clear", "evaded", "applied", "alreadySpent",
                            "heroRootRadius", "deltaY", "bodyRadius", "bodyHeight"]},
            "checks": checks, "note": spec["note"]}, statuses


def main():
    os.makedirs(OUT, exist_ok=True)
    results, all_status = [], []
    for case, spec in CASES.items():
        r, st = analyse_case(case, spec)
        results.append(r)
        all_status.extend(st)
    covered = len([r for r in results if r["status"] == "PASS-PLAYER"])
    doc = {
        "scope": "CP06-C24-B2-R1 R1-02 real observation Player RingProbe matrix",
        "tier": "PASS-PLAYER only where raw Player probe rows exist; "
                "NOT_RUN / INCOMPLETE / FAIL are never promoted",
        "frozenContract": FROZEN,
        "input": "Evidence/Player/r1-ring-<case>-A1/ring-probes.jsonl (raw)",
        "cases": results,
        "coveredCaseCount": covered,
        "declaredCaseCount": len(CASES),
        "notRunOrUnimplemented": NOT_RUN,
        "productCodeModified": False,
        "noToleranceTuning": True,
        "assertionCorrection": {
            "initialVerdictFile": "Evidence/After/ring-player-matrix-initial.json",
            "initialVerdict": "RING_PLAYER_MATRIX_PARTIAL (4/7, 3 FAIL)",
            "rootCause": "The first analysis demanded alreadySpent=true on no-hit "
                         "windows. Product semantics: alreadySpent only becomes true "
                         "AFTER the single Damage opportunity is consumed; safe-zone / "
                         "occlusion / dodge windows keep hit=false and re-evaluate "
                         "each Active frame. This was a TEST assertion error, not a "
                         "product defect, and no frozen geometry parameter was changed.",
            "changed": "analysis tool only; product source untouched",
        },
        "verdict": ("RING_PLAYER_MATRIX_PASS" if covered == len(CASES) else
                    "RING_PLAYER_MATRIX_PARTIAL"),
        "note": "Partial coverage is explicitly reported. B2 Editor geometry "
                "cases are a DIFFERENT tier and are not merged into this verdict.",
    }
    with open(os.path.join(OUT, "ring-player-matrix.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    with open(os.path.join(OUT, "ring-player-checks.tsv"), "w",
              encoding="utf-8", newline="\n") as f:
        f.write("case\tcheck\tstatus\texpression\tevidenceRows\treason\n")
        for r in results:
            for c in r["checks"]:
                f.write("\t".join([r["case"], c["check"], c["status"],
                                   c["expression"], ";".join(c["evidenceRows"]),
                                   c["reason"].replace("\t", " ")]) + "\n")
    print(json.dumps({"verdict": doc["verdict"],
                      "covered": covered, "declared": len(CASES),
                      "perCase": {r["case"]: r["status"] for r in results}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
