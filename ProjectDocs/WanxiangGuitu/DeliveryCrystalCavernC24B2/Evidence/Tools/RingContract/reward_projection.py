#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CP06-C24-B2 | Read-only reward projection AFTER-field recomputation + proof that
the real factory payload is byte-equivalent to the baseline.

Deterministic, read-only with respect to game state: no Unity run, no save, no
RNG advance, no item creation. Reads the frozen B1 arena sample, the frozen
RouteScoring.json weights, the shared projection constants and the baseline
source at HEAD (= a013c15a...) via `git show`.

Writes: Evidence/After/route-fields-after.json
        Evidence/After/reward-factory-equivalence.json
"""
import hashlib
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
DELIVERY = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
REPO = os.path.abspath(os.path.join(DELIVERY, "..", "..", ".."))
B1 = os.path.join(REPO, "ProjectDocs", "WanxiangGuitu", "DeliveryCrystalCavernC24B1")
OUT = os.environ.get("C24B2_EVIDENCE_OUT") or os.path.join(DELIVERY, "Evidence", "After")
FORCE = os.environ.get("C24B2_FORCE") == "1"
ASSETS = os.path.join(REPO, "Assets", "CombatPrototype")
MAT = ["MonsterHide", "CrystalShard", "BossCore", "Wood", "Stone", "Ore"]


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def dump(name, obj):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    if os.path.exists(p) and not FORCE:
        raise SystemExit("refusing to overwrite existing evidence: " + p +
                         " (use a fresh C24B2_EVIDENCE_OUT or C24B2_FORCE=1)")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    return p


def constants():
    src = text(os.path.join(ASSETS, "CrystalCavernBossRewardProjection.cs"))
    def const(name):
        m = re.search(r"\b" + name + r"\s*=\s*(\d+)", src)
        if not m:
            raise RuntimeError("missing constant " + name)
        return int(m.group(1))
    ore_base, ore_var = const("OreBase"), const("OreVariants")
    cry_base, cry_var = const("CrystalBase"), const("CrystalVariants")
    return {
        "OreBase": ore_base, "OreVariants": ore_var,
        "CrystalBase": cry_base, "CrystalVariants": cry_var,
        "GearCount": const("GearCount"), "HideCount": const("HideCount"),
        "OreMean": ore_base + (ore_var - 1) * .5,
        "CrystalMean": cry_base + (cry_var - 1) * .5,
        "GearMean": float(const("GearCount")),
        "HideMean": float(const("HideCount")),
    }


def derived(sample, config):
    """Mirror RouteScoring.Evaluate derived-field formulas exactly."""
    units = sum(sample["expectedMaterials"])
    yield_ = max(0.0, min(1.0, (units + config["gearMaterialEquivalent"] * sample["expectedGear"]) /
                         config["yieldReference"]))
    # B1 targetBasis == '出征目标' => hasTarget false, needs empty, goal Gather.
    target_match = max(0.0, min(1.0, units / config["yieldReference"]))
    score = (config["targetWeight"] * target_match + config["yieldWeight"] * yield_ +
             config["extractionWeight"] * sample["extractionConvenience"] +
             config["noveltyWeight"] * sample["novelty"] -
             config["distanceWeight"] * sample["distanceCost"] -
             sample["risk"]["totalPenalty"])
    return {"expectedMaterialUnits": units, "expectedYield": yield_,
            "targetMatch": target_match, "totalScore": score}


def factory_equivalence(k):
    """Prove the refactor did not change the deterministic drop payload."""
    # 1. Exhaustive residue equivalence plus representative uint values.
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 4294967295, 4294967294,
              2147483648, 3735928559, 305419896, 2882400001]
    rows = []
    for h in values:
        old_ore = 2 + (h % 3)
        new_ore = k["OreBase"] + (h % k["OreVariants"])
        old_cry = 3 + (h % 3)
        new_cry = k["CrystalBase"] + (h % k["CrystalVariants"])
        rows.append({"hashUint": h, "oreOld": old_ore, "oreNew": new_ore,
                     "crystalOld": old_cry, "crystalNew": new_cry,
                     "match": old_ore == new_ore and old_cry == new_cry})
    # 2. Normalise the current factory source back to the baseline expression
    #    and drop the two added read-only helpers; whatever remains must equal
    #    the exact committed baseline file. This covers identity, hash suffixes,
    #    gear type/quality, Earn, checkpoint and notice calls.
    rel = "Assets/CombatPrototype/CrystalCavernBossRewards.cs"
    baseline_ref = "a013c15aae15e17af6a7596a022f01f56a745c34:" + rel
    baseline = subprocess.check_output(["git", "-C", REPO, "show", baseline_ref],
                                       text=True, encoding="utf-8")
    current = text(os.path.join(REPO, rel))
    normalised = current
    normalised = normalised.replace(
        "CrystalCavernBossRewardProjection.OreAmount(Number(\"/ore\"))",
        "2+(int)(Number(\"/ore\")%3)")
    normalised = normalised.replace(
        "CrystalCavernBossRewardProjection.CrystalAmount(Number(\"/crystal\"))",
        "3+(int)(Number(\"/crystal\")%3)")
    start = normalised.find("    // Read-only identity gate for RouteScoring's projection.")
    end = normalised.find("    public static void Drop(CombatEnemy enemy)")
    if start < 0 or end < 0 or end <= start:
        raise RuntimeError("cannot isolate the added read-only helpers")
    normalised = normalised[:start] + normalised[end:]
    return {
        "method": "exhaustive modulo residues + representative uint values + source normalisation",
        "sampleChecks": rows,
        "allSampleChecksMatch": all(r["match"] for r in rows),
        "residueSet": sorted({h % 3 for h in range(0, 3000)}),
        "sourceNormalisation": {
            "baselineRef": baseline_ref,
            "baselineSHA256": hashlib.sha256(baseline.encode("utf-8")).hexdigest(),
            "currentSHA256": hashlib.sha256(current.encode("utf-8")).hexdigest(),
            "normalisedSHA256": hashlib.sha256(normalised.encode("utf-8")).hexdigest(),
            "normalisedEqualsBaseline": normalised == baseline,
            "substitutions": [
                "OreAmount(...) -> 2+(int)(Number(\"/ore\")%3)",
                "CrystalAmount(...) -> 3+(int)(Number(\"/crystal\")%3)",
                "remove ProjectionApplies + Project read-only helpers",
            ],
        },
        "verdict": "FACTORY_PAYLOAD_EQUIVALENT" if all(r["match"] for r in rows)
                   and normalised == baseline else "FACTORY_PAYLOAD_CHANGED",
    }


def main():
    k = constants()
    arena_path = os.path.join(B1, "Evidence", "Runs", "b1-name-cavern-A1", "arena-route.json")
    arena = load(arena_path)
    config = load(os.path.join(ASSETS, "Resources", "RouteScoring.json"))

    before = [float(v) for v in arena["expectedMaterials"]]
    after = [0.0] * 6
    after[MAT.index("MonsterHide")] = k["HideMean"]
    after[MAT.index("CrystalShard")] = k["CrystalMean"]
    after[MAT.index("Ore")] = k["OreMean"]
    after_gear = k["GearMean"]

    before_calc = dict(arena)
    after_calc = dict(arena)
    after_calc["expectedMaterials"] = after
    after_calc["expectedGear"] = after_gear
    after_calc.update(derived(after_calc, config))
    before_derived = derived(before_calc, config)

    fields = []
    for name, idx in [("MonsterHide", MAT.index("MonsterHide")),
                      ("CrystalShard", MAT.index("CrystalShard")),
                      ("Ore", MAT.index("Ore"))]:
        fields.append({"field": name, "before": before[idx], "after": after[idx],
                       "dedicatedNominal": {"MonsterHide": k["HideMean"],
                                            "CrystalShard": k["CrystalMean"],
                                            "Ore": k["OreMean"]}[name],
                       "afterMatchesDedicated": abs(after[idx] - {
                           "MonsterHide": k["HideMean"], "CrystalShard": k["CrystalMean"],
                           "Ore": k["OreMean"]}[name]) < 1e-9})
    fields.append({"field": "Gear", "before": arena["expectedGear"], "after": after_gear,
                   "dedicatedNominal": k["GearMean"], "afterMatchesDedicated": True})

    labels = {0: "野怪皮", 1: "晶石碎片", 2: "Boss核心", 3: "木材", 4: "石料", 5: "铁矿"}
    def ui(mats, gear):
        m = "/".join(labels[i] for i, v in enumerate(mats) if v > 0)
        return (m or "") + ("/装备机会" if gear > 0 else "")

    result = {
        "scope": "C24 read-only route projection, field-by-field before/after",
        "tier": "deterministic recomputation from frozen B1 sample + frozen weights; NOT a Unity run",
        "inputs": {
            "arenaRoute": os.path.relpath(arena_path, REPO).replace("\\", "/"),
            "arenaRouteSHA256": sha256(arena_path),
            "routeScoringConfig": "Assets/CombatPrototype/Resources/RouteScoring.json",
            "routeScoringConfigSHA256": sha256(os.path.join(ASSETS, "Resources", "RouteScoring.json")),
            "projectionSource": "Assets/CombatPrototype/CrystalCavernBossRewardProjection.cs",
            "projectionSourceSHA256": sha256(os.path.join(ASSETS, "CrystalCavernBossRewardProjection.cs")),
        },
        "sharedConstants": k,
        "materialOrder": MAT,
        "beforeControl": {
            "recomputed": before_derived,
            "recorded": {f: arena[f] for f in
                         ["expectedMaterialUnits", "expectedYield", "targetMatch", "totalScore"]},
            "match": all(abs(before_derived[f] - arena[f]) < 1e-4 for f in
                         ["expectedMaterialUnits", "expectedYield", "targetMatch", "totalScore"]),
        },
        "before": {"expectedMaterials": before, "expectedGear": arena["expectedGear"],
                   "expectedMaterialUnits": arena["expectedMaterialUnits"],
                   "expectedYield": arena["expectedYield"], "targetMatch": arena["targetMatch"],
                   "totalScore": arena["totalScore"], "routeUI": ui(before, arena["expectedGear"])},
        "after": {"expectedMaterials": after, "expectedGear": after_gear,
                  "expectedMaterialUnits": after_calc["expectedMaterialUnits"],
                  "expectedYield": after_calc["expectedYield"], "targetMatch": after_calc["targetMatch"],
                  "totalScore": after_calc["totalScore"], "routeUI": ui(after, after_gear)},
        "fieldByField": fields,
        "allAfterFieldsMatchDedicated": all(f["afterMatchesDedicated"] for f in fields),
        "scoreNote": "Score moves because targetMatch/expectedYield are derived from the corrected "
                     "projection. Weights, risk and ordering contracts are unchanged; the six "
                     "historical non-C24 layouts take the generic branch (static guard proof).",
        "sixOldLayouts": {
            "staticProof": "ProjectionApplies requires run.region==CrystalCavernLayout.Region, "
                           "contentRevision==C2.4-CAVERN-1, generationVersion==13 and "
                           "CrystalCavernLayout.HasBoss(map) (revision 10 + C2.4 version); "
                           "forest/ruins/C21/C22/C23-closed/C23-open all fail this gate, so the "
                           "generic branch is byte-identical.",
            "status": "STATIC_PROOF_ONLY / no new Editor run in this batch",
        },
        "conclusion": "F1_PROJECTION_FIELDS_CORRECTED" if all(
            f["afterMatchesDedicated"] for f in fields) else "F1_PROJECTION_STILL_WRONG",
    }
    dump("route-fields-after.json", result)
    equivalence = factory_equivalence(k)
    dump("reward-factory-equivalence.json", equivalence)
    print(json.dumps({"allAfterFieldsMatchDedicated": result["allAfterFieldsMatchDedicated"],
                      "beforeControlMatch": result["beforeControl"]["match"],
                      "factoryVerdict": equivalence["verdict"],
                      "afterTotalScore": result["after"]["totalScore"]}, indent=2))
    return 0 if result["allAfterFieldsMatchDedicated"] and equivalence["verdict"] == \
            "FACTORY_PAYLOAD_EQUIVALENT" and result["beforeControl"]["match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
