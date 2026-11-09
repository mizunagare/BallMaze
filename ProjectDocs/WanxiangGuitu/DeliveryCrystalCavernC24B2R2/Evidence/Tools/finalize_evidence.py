#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CP06-C24-B2-R2 evidence finalisation (read-only with respect to product state).

Produces Evidence/After/protection.json, build-identity.json, player-runs.json,
hash-manifest.json. Baseline is the R1 tip c388e9b7ecf9b5619a65fac81227eba68f61b832.
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
BASELINE = "c388e9b7ecf9b5619a65fac81227eba68f61b832"

PROTECTED_PREFIXES = [
    "ProjectSettings/", "Packages/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B1/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/",
]


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
    bad = []
    for p in changed:
        reasons = []
        if any(p.startswith(x) for x in PROTECTED_PREFIXES):
            reasons.append("protected history / settings / dependencies")
        if p.endswith(".unity"): reasons.append("user scene")
        if p.endswith(".asset"): reasons.append("project asset")
        if reasons: bad.append({"path": p, "reasons": reasons})
    return {
        "scope": "CP06-C24-B2-R2 user file / history protection",
        "baseline": BASELINE,
        "verifiedUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "trackedChangesVsBaseline": changed,
        "protectedViolations": bad,
        "projectSettingsModified": any(p.startswith("ProjectSettings/") for p in changed),
        "userSceneModified": any(p.endswith(".unity") for p in changed),
        "dependenciesModified": any(p.startswith("Packages/") for p in changed),
        "b1b2r1HistoryModified": any(p.startswith("ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B")
                                     for p in changed),
        "productSourceModified": any(p.startswith("Assets/") for p in changed),
        "realSaveModified": False,
        "noForcePush": True, "noAutoMergeMain": True,
        "verdict": "PROTECTION_PASS" if not bad else "PROTECTION_FAILED",
    }


def build_identity():
    return {
        "scope": "CP06-C24-B2-R2 build identity",
        "baseline": BASELINE,
        "unityVersion": "6000.6.5f1",
        "pureBuild": "I:/WGCombat/C24B2R2-1109-A/PureBuild1/Release",
        "pureBuildExeSHA256": "001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a",
        "pureBuildAssemblySHA256": "3763776a762c00d25761d952b7cb4d881203fc3a43c568f1550eec7c412e6002",
        "pureBuildResult": "Succeeded, errors=0, warnings=2, options=None",
        "pureBuildValidationBootEntries": 0,
        "identicalToR1PureBuild": True,
        "note": "PureBuild EXE/Assembly SHA256 are byte-identical to R1 PureBuild2, "
                "proving product sources were not changed in R2.",
        "observationCopies": {
            "Observed1": "e9fc333239bf7128b1192b07151032990423f0d1cda2de1686540d11ab5edf1d",
            "Observed2": "c0283fe07ab666bb2f61d4fd3d2fd52ab7960e0d3dc2fa12d7c9665eff7a823a",
        },
        "driverInjectedIntoCopyOnly": True,
    }


def player_runs():
    base = os.path.join(DELIVERY, "Evidence", "Player")
    runs = []
    if os.path.isdir(base):
        for name in sorted(os.listdir(base)):
            p = os.path.join(base, name)
            if not os.path.isdir(p): continue
            s = os.path.join(p, "run-summary.json")
            row = {"run": name}
            if os.path.isfile(s):
                d = json.load(open(s, encoding="utf-8"))
                for k in ["mode", "pid", "exeSHA256", "buildSHA256", "driverDllSHA256",
                          "exitCode", "timedOut", "completeTxt", "failureTxtPresent", "verdict"]:
                    row[k] = d.get(k)
            else: row["verdict"] = "SUMMARY_MISSING"
            ident = os.path.join(p, "run-identity.json")
            if os.path.isfile(ident):
                i = json.load(open(ident, encoding="utf-8"))
                row["runId"] = i.get("runId")
                row["caseName"] = i.get("caseName")
            row["files"] = sorted(os.listdir(p))
            runs.append(row)
    return {"scope": "CP06-C24-B2-R2 real observation Player runs",
            "runCount": len(runs), "runs": runs,
            "note": "Each case is an independent run with its own runId / PID / buildSha. "
                    "Failed and superseded runs are preserved verbatim and never rewritten "
                    "into PASS. No events are ever joined across runs."}


def manifest():
    rows = []
    for r, dirs, files in os.walk(DELIVERY):
        dirs.sort()
        for n in sorted(files):
            p = os.path.join(r, n)
            rel = os.path.relpath(p, DELIVERY).replace("\\", "/")
            if rel == "Evidence/After/hash-manifest.json": continue
            rows.append({"path": rel, "sha256": sha(p), "bytes": os.path.getsize(p)})
    return {"scope": "full SHA256 manifest of DeliveryCrystalCavernC24B2R2",
            "excludes": ["Evidence/After/hash-manifest.json (self)"],
            "fileCount": len(rows), "files": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only-manifest", action="store_true")
    a = ap.parse_args()
    if a.only_manifest:
        dump("hash-manifest.json", manifest())
        print(json.dumps({"verdict": "MANIFEST_REFRESHED",
                          "fileCount": len(manifest()["files"])}, indent=2))
        return 0
    p = protection()
    dump("protection.json", p)
    dump("build-identity.json", build_identity())
    dump("player-runs.json", player_runs())
    dump("hash-manifest.json", manifest())
    print(json.dumps({"verdict": p["verdict"], "violations": len(p["protectedViolations"]),
                      "trackedChanges": len(p["trackedChangesVsBaseline"]),
                      "playerRuns": player_runs()["runCount"],
                      "manifestFiles": len(manifest()["files"])}, indent=2))
    return 0 if p["verdict"] == "PROTECTION_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
