#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CP06-C24-B2 | HollowRing contact matrix (deterministic formula MODEL).

This is a formula/geometry model, NOT a Unity Editor or Player run. It mirrors,
line by line, CrystalCavernRingContact.Touches() with float32 rounding. All
parameters and expected outcomes come from the FROZEN contract.json / 
DESIGN_DECISIONS.md, written before any test was run. No expected value is
re-fitted here.

Reads : contract.json (frozen), B1 ring-release.json x4, B1 ring-damage.tsv x4
Writes: Evidence/After/ring-matrix-after.json
"""
import hashlib
import json
import math
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
DELIVERY = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
REPO = os.path.abspath(os.path.join(DELIVERY, "..", "..", ".."))
B1 = os.path.join(REPO, "ProjectDocs", "WanxiangGuitu", "DeliveryCrystalCavernC24B1")
OUT_DIR = os.environ.get("C24B2_EVIDENCE_OUT") or os.path.join(DELIVERY, "Evidence", "After")
FORCE = os.environ.get("C24B2_FORCE") == "1"
SOURCE = os.path.join(REPO, "Assets", "CombatPrototype", "CrystalCavernRingContact.cs")


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def f32(x):
    """Emulate a C# float (single precision) rounding."""
    return struct.unpack("<f", struct.pack("<f", float(x)))[0]


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def touches(radius, height, center_y, distance, origin, frozen):
    r, h = f32(radius), f32(height)
    ri, ro, hh, eps = (f32(frozen["innerRadius"]), f32(frozen["outerRadius"]),
                       f32(frozen["halfHeight"]), f32(frozen["contactEpsilon"]))
    d = f32(math.sqrt(f32(distance) ** 2))  # radial distance is supplied directly
    dr = f32(ri - d) if d < ri else (f32(d - ro) if d > ro else 0.0)
    stem = f32(max(0.0, f32(h * .5) - r))
    low, high = f32(f32(center_y) - stem), f32(f32(center_y) + stem)
    band_low, band_high = f32(f32(origin["y"]) - hh), f32(f32(origin["y"]) + hh)
    vgap = f32(max(0.0, f32(band_low - high), f32(low - band_high)))
    reach = f32(r + eps)
    lhs = f32(f32(dr * dr) + f32(vgap * vgap))
    rhs = f32(reach * reach)
    return lhs <= rhs, {
        "distance": d, "radialGap": dr, "verticalGap": vgap, "reach": reach,
        "lhs": lhs, "rhs": rhs, "closedSetTangency": frozen["closedSetTangency"],
        "capsuleStemY": [low, high], "bandY": [band_low, band_high],
        "radius": r, "height": h, "centerY": f32(center_y),
        "origin": [origin["x"], origin["y"], origin["z"]],
    }


def b1_rows(frozen):
    """Re-read exact B1 world samples; no rounded table values are used."""
    rows = []
    for name in ["inner", "outer", "band", "safe"]:
        p = os.path.join(B1, "Evidence", "Runs", "b1-ring-%s-A1" % name, "ring-release.json")
        d = load(p)
        root, origin = d["root"], d["origin"]
        flat = math.hypot(root["x"] - origin["x"], root["z"] - origin["z"])
        dy = root["y"] - origin["y"]
        old = frozen["innerRadius"] <= flat <= frozen["outerRadius"] and abs(dy) <= frozen["halfHeight"]
        hit, detail = touches(d["radius"], d["height"], d["controllerCenter"]["y"], flat, origin, frozen)
        tsv = os.path.join(B1, "Evidence", "Runs", "b1-ring-%s-A1" % name, "ring-damage.tsv")
        damage = []
        with open(tsv, "r", encoding="utf-8") as f:
            for line in f:
                p2 = line.rstrip("\n").split("\t")
                if len(p2) >= 5 and p2[1] == "Damage":
                    damage.append({"frame": int(p2[0]), "before": float(p2[2]), "after": float(p2[3])})
        rows.append({
            "sample": name,
            "rootRadius": round(flat, 6),
            "rootDeltaY": round(dy, 9),
            "capsuleRadial": [round(d["radialMinimum"], 6), round(d["radialMaximum"], 6)],
            "oldRootPointHitTest": bool(old),
            "newCapsuleContact": hit,
            "b1ObservedDamage": damage,
            "frozenGeometryDetail": detail,
        })
    return rows


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    contract_path = os.path.join(HERE, "contract.json")
    contract = load(contract_path)
    frozen, body = contract["frozen"], contract["body"]
    origin = body["origin"]

    cases = []
    for case in contract["geometryCases"]:
        cy = case.get("centerY", body["centerY"])
        hit, detail = touches(body["radius"], body["height"], cy, case["distance"], origin, frozen)
        expected = case["expected"]
        cases.append({
            "id": case["id"], "layer": "geometry-model",
            "expected": expected, "actual": hit, "pass": hit == expected,
            "note": case["note"], "detail": detail,
        })

    broad = math.sqrt(frozen["outerRadius"] ** 2 + frozen["halfHeight"] ** 2) + frozen["contactEpsilon"]
    result = {
        "scope": "C24-B2 HollowRing narrow-phase deterministic formula model",
        "tier": "MODEL / NOT a Unity Editor or Player run",
        "contractVersion": contract["contractVersion"],
        "contractSHA256": sha256(contract_path),
        "designDecisionsSHA256": sha256(os.path.join(DELIVERY, "DESIGN_DECISIONS.md")),
        "productSourceSHA256": sha256(SOURCE),
        "frozen": frozen,
        "broadPhaseRadius": broad,
        "formula": "dr^2 + vgap^2 <= (radius + epsilon)^2  (closed set, tangency counts)",
        "geometryCases": cases,
        "geometryPass": sum(1 for c in cases if c["pass"]),
        "geometryTotal": len(cases),
        "allGeometryPass": all(c["pass"] for c in cases),
        "b1WorldSamples": b1_rows(frozen),
        "runtimeCases": [
            dict(c, status="NOT_RUN",
                 tier="requires a real Editor/observation Player run; only source control flow is asserted")
            for c in contract["runtimeCases"]
        ],
        "conclusion": "FROZEN_CONTRACT_MODEL_VERIFIED" if all(c["pass"] for c in cases)
                      else "FROZEN_CONTRACT_MODEL_MISMATCH",
    }
    out = os.path.join(OUT_DIR, "ring-matrix-after.json")
    if os.path.exists(out) and not FORCE:
        raise SystemExit("refusing to overwrite existing evidence: " + out +
                         " (use a fresh C24B2_EVIDENCE_OUT or C24B2_FORCE=1)")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({k: result[k] for k in
                      ["geometryPass", "geometryTotal", "allGeometryPass", "conclusion",
                       "broadPhaseRadius", "contractSHA256"]}, indent=2))
    return 0 if result["allGeometryPass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
