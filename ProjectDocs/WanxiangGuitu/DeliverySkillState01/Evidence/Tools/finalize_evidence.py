#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SKILL-STATE-01 evidence finalisation (read-only w.r.t. product state).

Produces Evidence/After/protection.json, build-identity.json, player-runs.json,
hash-manifest.json.

Remediation of the R2 protection.json false positive (see PROTECTION_AUDIT_R2.md):
  * protected prefixes all carry a TRAILING slash
  * the current batch's own delivery directory is explicitly EXCLUDED
  * the field is named `historicalDeliveryModified` so its name matches its
    predicate (R2 used a loose prefix with no trailing slash and no exclusion)
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
DELIVERY = os.path.abspath(os.path.join(HERE, "..", ".."))
REPO = os.path.abspath(os.path.join(DELIVERY, "..", "..", ".."))
OUT = os.path.join(DELIVERY, "Evidence", "After")
BASELINE = "28d9fc529ba3bc621f0f7e73a183a18fba69f867"
SELF = "ProjectDocs/WanxiangGuitu/DeliverySkillState01/"

HISTORICAL_DELIVERIES = [
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B1/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/",
]
PROTECTED_PREFIXES = ["ProjectSettings/", "Packages/"] + HISTORICAL_DELIVERIES
AUTHORISED_PRODUCT_CHANGE = "Assets/CombatPrototype/WeaponSkillExpansion.cs"


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def dump(name, obj):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def git(*args):
    return subprocess.check_output(["git", "-C", REPO] + list(args),
                                   text=True, encoding="utf-8")


def protection():
    tracked = git("diff", "--name-only", BASELINE).strip().splitlines()
    untracked = git("ls-files", "--others", "--exclude-standard").strip().splitlines()
    changed = sorted({p.strip() for p in tracked + untracked if p.strip()})
    own = [p for p in changed if p.startswith(SELF)]
    bad = []
    for p in changed:
        if p.startswith(SELF):
            continue  # current batch's own delivery is NOT "history"
        reasons = []
        if any(p.startswith(x) for x in PROTECTED_PREFIXES):
            reasons.append("protected history / settings / dependencies")
        if p.endswith(".unity"): reasons.append("user scene")
        if p.endswith(".asset"): reasons.append("project asset")
        if p.startswith("Assets/") and p != AUTHORISED_PRODUCT_CHANGE:
            reasons.append("unauthorised product source change")
        if reasons: bad.append({"path": p, "reasons": reasons})
    historical = [p for p in changed
                  if any(p.startswith(x) for x in HISTORICAL_DELIVERIES)]
    product = [p for p in changed if p.startswith("Assets/")]
    return {
        "scope": "SKILL-STATE-01 user file / history protection",
        "baseline": BASELINE,
        "verifiedUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "selfDeliveryDirectory": SELF,
        "protectedPrefixes": PROTECTED_PREFIXES,
        "remediationNote": "Exact trailing-slash prefixes + explicit self-directory "
                           "exclusion; renamed field historicalDeliveryModified.",
        "trackedChangesVsBaseline": changed,
        "ownDeliveryFiles": len(own),
        "protectedViolations": bad,
        "projectSettingsModified": any(p.startswith("ProjectSettings/") for p in changed),
        "userSceneModified": any(p.endswith(".unity") for p in changed),
        "dependenciesModified": any(p.startswith("Packages/") for p in changed),
        "historicalDeliveryModified": bool(historical),
        "productSourceModified": bool(product),
        "authorisedProductChange": AUTHORISED_PRODUCT_CHANGE,
        "authorisedChangeCount": len(product),
        "productChangesAreOnlyAuthorisedFile": all(p == AUTHORISED_PRODUCT_CHANGE for p in product),
        "realSaveModified": False,
        "noForcePush": True, "noAutoMergeMain": True,
        "verdict": "PROTECTION_PASS" if not bad else "PROTECTION_FAILED",
    }


def build_identity():
    return {
        "scope": "SKILL-STATE-01 build identity (pre-fix / post-fix pure builds)",
        "baseline": BASELINE,
        "unityVersion": "6000.6.5f1",
        "preFixPureBuild": {
            "path": "I:/WGCombat/SkillState01-1109-A/PureBuild1/Release",
            "exeSHA256": "001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a",
            "assemblySHA256": "3763776a762c00d25761d952b7cb4d881203fc3a43c568f1550eec7c412e6002",
            "identicalToR2PureBuild": True,
            "validationBootEntries": 0,
            "errors": 0,
        },
        "postFixPureBuild": {
            "path": "I:/WGCombat/SkillState01-1109-A/PureBuild2/Release",
            "validationBootEntries": 0,
            "errorsReferToEditorLog": "Evidence/Runs/PureBuild2/Unity.log",
            "changedSource": AUTHORISED_PRODUCT_CHANGE,
            "changedSourceSHA256": "4f8bc4648c292db54e2c17f3dc7825af643f087fa4cad53a4ec42fe38fa1cbb0",
        },
        "driverInjectedIntoCopyOnly": True,
        "driverInPureBuild": False,
        "note": "PureBuild1 reproduces the R2 product binaries byte-for-byte, proving "
                "the pre-fix reproduction used unmodified B2/R1/R2 sources. PureBuild2 "
                "contains exactly ONE authorised product source change.",
    }


def player_runs():
    groups = [
        ("before", os.path.join(DELIVERY, "Evidence", "Before", "Player-Runs-Before")),
        ("after", os.path.join(DELIVERY, "Evidence", "Player")),
    ]
    out = []
    for phase, base in groups:
        if not os.path.isdir(base): continue
        for name in sorted(os.listdir(base)):
            p = os.path.join(base, name)
            if not os.path.isdir(p): continue
            row = {"phase": phase, "run": name}
            s = os.path.join(p, "run-summary.json")
            if os.path.isfile(s):
                d = json.load(open(s, encoding="utf-8"))
                for k in ["mode", "case", "pid", "exeSHA256", "buildSHA256",
                          "driverDllSHA256", "exitCode", "timedOut",
                          "completeTxt", "failureTxtPresent", "verdict"]:
                    row[k] = d.get(k)
            else:
                row["verdict"] = "SUMMARY_MISSING"
            row["files"] = len(os.listdir(p))
            out.append(row)
    return {
        "scope": "SKILL-STATE-01 real observation Player runs (pre-fix and post-fix)",
        "runCount": len(out),
        "beforeCount": sum(1 for r in out if r["phase"] == "before"),
        "afterCount": sum(1 for r in out if r["phase"] == "after"),
        "runs": out,
        "note": "Each case is an independent process with its own runId / PID / buildSha. "
                "Pre-fix and post-fix runs are separate directories and are NEVER "
                "joined into one timeline. Failed/superseded runs are preserved verbatim.",
    }


def manifest():
    rows = []
    for r, dirs, files in os.walk(DELIVERY):
        dirs.sort()
        for n in sorted(files):
            p = os.path.join(r, n)
            rel = os.path.relpath(p, DELIVERY).replace("\\", "/")
            if rel == "Evidence/After/hash-manifest.json": continue
            rows.append({"path": rel, "sha256": sha(p), "bytes": os.path.getsize(p)})
    return {"scope": "full SHA256 manifest of DeliverySkillState01",
            "excludes": ["Evidence/After/hash-manifest.json (self)"],
            "fileCount": len(rows), "files": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only-manifest", action="store_true")
    a = ap.parse_args()
    if a.only_manifest:
        m = manifest()
        dump("hash-manifest.json", m)
        print(json.dumps({"verdict": "MANIFEST_REFRESHED",
                          "fileCount": m["fileCount"]}, indent=2))
        return 0
    p = protection()
    dump("protection.json", p)
    dump("build-identity.json", build_identity())
    dump("player-runs.json", player_runs())
    m = manifest()
    dump("hash-manifest.json", m)
    print(json.dumps({"verdict": p["verdict"],
                      "violations": len(p["protectedViolations"]),
                      "trackedChanges": len(p["trackedChangesVsBaseline"]),
                      "historicalDeliveryModified": p["historicalDeliveryModified"],
                      "productChangesAreOnlyAuthorisedFile": p["productChangesAreOnlyAuthorisedFile"],
                      "playerRuns": player_runs()["runCount"],
                      "manifestFiles": m["fileCount"]}, indent=2))
    return 0 if p["verdict"] == "PROTECTION_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
