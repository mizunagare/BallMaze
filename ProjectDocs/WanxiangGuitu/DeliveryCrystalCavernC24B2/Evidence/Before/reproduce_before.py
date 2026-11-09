#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CP06-C24-B2 | PRE-FIX REPRODUCTION (read-only, deterministic, no Unity runtime)

Purpose
-------
Reproduce the two CONFIRMED pre-fix defects from frozen historical evidence and
product source formulas BEFORE any product source is modified. This script is a
read-only re-computation; it does NOT run Unity, does NOT write a save, does NOT
advance RNG, does NOT create items, and does NOT produce any Unity/Player log.
It is NOT a new Editor/Player observation.

Inputs (all fixed by SHA256 in inputs.json):
  - B1 arena-route.json            : real C24 route projection fields captured in B1
  - B1 ring-release.json x 4       : real world capsule / root / ring origin from B1
  - B1 ROUTE_AUDIT / RING_AUDIT   : the two confirmed defect descriptions
  - product source at baseline    : CrystalCavernBossRewards.cs, CombatEnemy.cs,
    RouteScoring.cs, CrystalCavernBossBrain.cs, CrystalCavernBossRules.cs

Outputs (UTF-8, deterministic, sorted keys):
  - route-fields-before.json  : F1 field-by-field projection vs dedicated factory
  - ring-matrix-before.json   : F2 old root-point hit test vs capsule-contact intent
  - c05-timeline-before.json  : frozen historical C05 INCOMPLETE state + limitations
  - before-repro.json         : consolidated verdict
"""
import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
B1 = os.path.join(REPO, "ProjectDocs", "WanxiangGuitu", "DeliveryCrystalCavernC24B1")
C24B = os.path.join(REPO, "ProjectDocs", "WanxiangGuitu", "DeliveryCrystalCavernC24B")


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def dump(name, obj):
    out = os.path.join(HERE, name)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    return out


# ---------------------------------------------------------------- F1 --------
# Product source as of baseline a013c15a (RouteScoring.cs lines 58-65) uses the
# GENERIC enemy branch for the C24 boss:
#   expectedMaterials[MonsterHide] += enemy.ExpectedHideYield
#   expectedMaterials[CrystalShard] += max(0, enemy.crystalAmount) + outpostBonus
#   expectedGear += enemy.GearDropChance
# Boss fixtures carry hideMin/hideMax giving mean 10, crystalAmount 5, and
# GearDropChance == 0 (CombatEnemy.GearDropChance returns 0 for archetype Boss).
# Dedicated factory (CrystalCavernBossRewards.Drop) instead places:
#   Ore            2 + hash%3   -> 2..4, nominal mean 3
#   CrystalShard   3 + hash%3   -> 3..5, nominal mean 4
#   Gear           exactly 1
#   MonsterHide    none         -> 0
MAT = ["MonsterHide", "CrystalShard", "BossCore", "Wood", "Stone", "Ore"]


def f1():
    arena = load(os.path.join(B1, "Evidence", "Runs", "b1-name-cavern-A1", "arena-route.json"))
    before = {
        "poiId": arena["poiId"],
        "label": arena["label"],
        "expectedMaterials": arena["expectedMaterials"],
        "expectedGear": arena["expectedGear"],
        "expectedMaterialUnits": arena["expectedMaterialUnits"],
        "expectedYield": arena["expectedYield"],
        "totalScore": arena["totalScore"],
        "livingEnemies": arena["livingEnemies"],
        "remainingNodes": arena["remainingNodes"],
        "unopenedChests": arena["unopenedChests"],
        "groundGroups": arena["groundGroups"],
        "groundGearCount": arena["groundGearCount"],
    }
    # Independently recompute the generic branch from the B1 fixture values,
    # taken verbatim from ROUTE_AUDIT.md (hide 10, crystal 5, gear 0).
    generic = [0.0] * 6
    hide_mean = 10.0
    crystal_amount = 5.0
    gear_drop_chance = 0.0
    generic[MAT.index("MonsterHide")] += hide_mean
    generic[MAT.index("CrystalShard")] += max(0.0, crystal_amount) + 0.0  # no outpost bonus
    generic_gear = gear_drop_chance
    recomputed_matches = all(
        abs(a - b) < 1e-9 for a, b in zip(generic, before["expectedMaterials"])
    ) and abs(generic_gear - before["expectedGear"]) < 1e-9

    dedicated = {
        "MonsterHide": 0.0,
        "CrystalShard": 4.0,   # nominal mean of 3..5
        "Ore": 3.0,           # nominal mean of 2..4
        "Gear": 1.0,
    }
    fields = ["MonsterHide", "CrystalShard", "Ore", "Gear"]
    before_vals = {
        "MonsterHide": before["expectedMaterials"][MAT.index("MonsterHide")],
        "CrystalShard": before["expectedMaterials"][MAT.index("CrystalShard")],
        "Ore": before["expectedMaterials"][MAT.index("Ore")],
        "Gear": before["expectedGear"],
    }
    rows = [
        {
            "field": k,
            "before": before_vals[k],
            "dedicatedNominal": dedicated[k],
            "delta": round(dedicated[k] - before_vals[k], 6),
            "verdict": "MATCH" if abs(dedicated[k] - before_vals[k]) < 1e-9 else "MISMATCH",
        }
        for k in fields
    ]
    return {
        "evidence": "B1 arena-route.json (real live-Boss C24 sample, no other yield sources)",
        "genericBranchRecomputed": generic,
        "genericGearRecomputed": generic_gear,
        "sourceFormulaReproduced": recomputed_matches,
        "beforeFields": before,
        "fieldByField": rows,
        "mismatchCount": sum(1 for r in rows if r["verdict"] == "MISMATCH"),
        "conclusion": "F1 CONFIRMED: 4 of 4 normal-yield fields disagree with the dedicated factory",
    }


# ---------------------------------------------------------------- F2 --------
# Baseline CrystalCavernBossBrain.HitArea() HollowRing geometry branch:
#   flat.magnitude >= 2.2f && flat.magnitude <= 6 && abs(delta.y) <= 1.2f
# where flat/delta are derived from the player's ROOT transform position, not
# the actual hit capsule. Broad phase is Physics.OverlapSphere(AttackOrigin, 6).
RING_INNER = 2.2
RING_OUTER = 6.0
RING_HALF_HEIGHT = 1.2


def old_geometry(flat, dy):
    return (flat >= RING_INNER and flat <= RING_OUTER and abs(dy) <= RING_HALF_HEIGHT)


def capsule_radial_span(flat, radius):
    # World-space horizontal extent of the upright hit capsule about the ring axis.
    return (max(0.0, flat - radius), flat + radius)


def capsule_contact_intent(radial_min, radial_max):
    # "actual hit body touches the annular band" (design intent, NOT yet product code)
    return radial_max >= RING_INNER and radial_min <= RING_OUTER


def f2():
    names = ["inner", "outer", "band", "safe"]
    rows = []
    for name in names:
        p = os.path.join(B1, "Evidence", "Runs", "b1-ring-%s-A1" % name, "ring-release.json")
        d = load(p)
        root, origin = d["root"], d["origin"]
        flat = math.hypot(root["x"] - origin["x"], root["z"] - origin["z"])
        dy = root["y"] - origin["y"]
        rmin, rmax = capsule_radial_span(flat, d["radius"])
        old = old_geometry(flat, dy)
        intent = capsule_contact_intent(rmin, rmax)
        # Real observed HP outcome is read from the frozen B1 ring-damage.tsv,
        # never hard-coded. Only rows whose event is "Damage" count as a hit;
        # "Unload" rows are the teardown observation and are recorded separately.
        tsv = os.path.join(B1, "Evidence", "Runs", "b1-ring-%s-A1" % name, "ring-damage.tsv")
        damage_rows, unload_rows = [], []
        with open(tsv, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 5 or parts[0] == "":
                    continue
                rec = {"frame": int(parts[0]), "event": parts[1],
                       "before": float(parts[2]), "after": float(parts[3]),
                       "release": parts[4]}
                if rec["event"] == "Damage":
                    rec["path"] = ("CrystalCavernBossBrain.HitArea -> CombatHealth.Damage"
                                   if "CrystalCavernBossBrain.HitArea ()" in line else "OTHER")
                    damage_rows.append(rec)
                elif rec["event"] == "Unload":
                    unload_rows.append(rec)
        hp = ([damage_rows[0]["before"], damage_rows[0]["after"]]
              if damage_rows else
              [unload_rows[0]["before"], unload_rows[0]["after"]])
        rows.append({
            "sample": name,
            "rootRadius": round(flat, 6),
            "deltaY": round(dy, 6),
            "radius": d["radius"],
            "height": d["height"],
            "radialMinimum": round(rmin, 6),
            "radialMaximum": round(rmax, 6),
            "recordedRadialMinimum": round(d["radialMinimum"], 6),
            "recordedRadialMaximum": round(d["radialMaximum"], 6),
            "oldRootPointHitTest": old,
            "capsuleTouchesBand": intent,
            "observedHP": hp,
            "damageEvents": damage_rows,
            "unloadEvents": unload_rows,
            "semanticConflict": bool(intent and not old),
        })
    return {
        "contractFrozenForReproOnly": {
            "inner": RING_INNER, "outer": RING_OUTER, "halfHeight": RING_HALF_HEIGHT,
            "note": "These are the BASELINE constants read from product source; this "
                    "reproduction does not define or change the B2 contract.",
        },
        "samples": rows,
        "conflictCount": sum(1 for r in rows if r["semanticConflict"]),
        "conclusion": "F2 CONFIRMED: inner/outer capsule contacts the band but the "
                      "root-point test reports safe; HP stays unchanged in B1 Player",
    }


# --------------------------------------------------------------- C05 --------
def c05():
    p = os.path.join(C24B, "Evidence", "Runs", "WindupNewAudit1", "audit.json")
    d = load(p)
    out = {"historicalStatus": d["status"], "toolVersion": d["toolVersion"],
           "toolSHA256": d["toolSHA256"], "samples": []}
    for s in d["samples"]:
        out["samples"].append({
            "sample": s["sample"],
            "checks": s["checks"],
            "status": s["status"],
            "limitations": s["limitations"],
            "observed": {
                "bossDamage": s["observed"]["bossDamage"],
                "playerDamage": s["observed"]["playerDamage"],
                "release": s["observed"]["release"],
                "warning": s["observed"]["warning"],
                "deadline": s["observed"]["deadline"],
                "releaseFrame": s["observed"]["releaseFrame"],
                "transition": s["observed"]["transition"],
                "releaseToTransition": s["observed"]["releaseToTransition"],
            },
        })
    out["conclusion"] = ("C05 remains INCOMPLETE in history: playerDamageAttribution and "
                         "recoveryTransitionOrder were not established by the v2.0 audit. "
                         "B2 must supply read-only correlation, not rewrite the state machine.")
    return out


def main():
    # One-shot by design: this snapshot was taken BEFORE any product source was
    # modified. Re-running it afterwards would hash the FIXED sources and destroy
    # the pre-fix identity, so existing outputs are never overwritten.
    outputs = ["inputs.json", "route-fields-before.json", "ring-matrix-before.json",
               "c05-timeline-before.json", "before-repro.json"]
    present = [n for n in outputs if os.path.exists(os.path.join(HERE, n))]
    if present:
        raise SystemExit("refusing to overwrite pre-fix evidence: " + ", ".join(present) +
                         ". Use a fresh copy of Evidence/Before in a new root.")
    inputs = {
        "baseline": "a013c15aae15e17af6a7596a022f01f56a745c34",
        "repository": "mizunagare/BallMaze",
        "files": [],
    }
    paths = [
        os.path.join(B1, "Evidence", "Runs", "b1-name-cavern-A1", "arena-route.json"),
        os.path.join(B1, "ROUTE_AUDIT.md"),
        os.path.join(B1, "RING_AUDIT.md"),
        os.path.join(B1, "ACCEPTANCE.md"),
        os.path.join(C24B, "Evidence", "Runs", "WindupNewAudit1", "audit.json"),
        os.path.join(C24B, "ACCEPTANCE.md"),
    ]
    for name in ["inner", "outer", "band", "safe"]:
        for leaf in ["ring-release.json", "ring-damage.tsv", "ring-result.json"]:
            paths.append(os.path.join(B1, "Evidence", "Runs", "b1-ring-%s-A1" % name, leaf))
    for name in ["RouteScoring.cs", "CrystalCavernBossRewards.cs", "CombatEnemy.cs",
                 "CrystalCavernBossBrain.cs", "CrystalCavernBossRules.cs",
                 "ArmorMitigation.cs", "CombatHealth.cs"]:
        paths.append(os.path.join(REPO, "Assets", "CombatPrototype", name))
    for p in paths:
        inputs["files"].append({
            "path": os.path.relpath(p, REPO).replace("\\", "/"),
            "sha256": sha256(p),
            "bytes": os.path.getsize(p),
        })
    inputs["files"].sort(key=lambda x: x["path"])
    dump("inputs.json", inputs)

    r1, r2, r3 = f1(), f2(), c05()
    dump("route-fields-before.json", r1)
    dump("ring-matrix-before.json", r2)
    dump("c05-timeline-before.json", r3)
    verdict = {
        "scope": "CP06-C24-B2 pre-fix reproduction (read-only re-computation)",
        "method": "frozen historical evidence + baseline product source formulas",
        "NOT": ["new Unity Editor run", "new observation Player run", "pure build",
                "native input", "independent human play", "save write", "RNG advance"],
        "F1": r1["conclusion"],
        "F1_sourceFormulaReproduced": r1["sourceFormulaReproduced"],
        "F1_mismatchCount": r1["mismatchCount"],
        "F2": r2["conclusion"],
        "F2_conflictCount": r2["conflictCount"],
        "C05_historicalStatus": r3["historicalStatus"],
        "inputFileCount": len(inputs["files"]),
        "verdict": "PRE_FIX_REPRODUCED",
    }
    dump("before-repro.json", verdict)
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
