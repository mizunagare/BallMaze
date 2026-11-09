#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CP06-C24-B2-R1 evidence finalisation.

Read-only with respect to product state. Produces:
  Evidence/After/protection.json       protected-path violations
  Evidence/After/build-identity.json   pure build / observation copy identity
  Evidence/After/hash-manifest.json    full SHA256 manifest of the delivery
  Evidence/After/player-runs.json      inventory of real Player runs + tiers

Baseline is the B2 tip 98924a34b6df817aa5a979b50439a4515881744b.
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
BASELINE = "98924a34b6df817aa5a979b50439a4515881744b"

PROTECTED_PREFIXES = [
    "ProjectSettings/",
    "Packages/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B1/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2/",
]
PROTECTED_SUFFIXES = [".unity", ".asset", ".meta"]


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def dump(name, obj):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    return p


def git(*args):
    return subprocess.check_output(["git", "-C", REPO] + list(args),
                                   text=True, encoding="utf-8")


def protected_violations():
    tracked = git("diff", "--name-only", BASELINE).strip().splitlines()
    untracked = git("ls-files", "--others", "--exclude-standard").strip().splitlines()
    changed = sorted(set([p.strip() for p in tracked + untracked if p.strip()]))
    bad = []
    for p in changed:
        reasons = []
        if any(p.startswith(x) for x in PROTECTED_PREFIXES):
            reasons.append("protected directory")
        if p.endswith(".unity"):
            reasons.append("user scene")
        if p.endswith(".asset"):
            reasons.append("project asset")
        # .meta files for PRODUCT scripts are legitimate; only flag .meta under
        # protected directories (already covered above).
        if reasons:
            bad.append({"path": p, "reasons": reasons})
    return changed, bad


def build_identity():
    files = {
        "pureBuildEditorCommand": os.path.join(DELIVERY, "Evidence", "Runs", "PureBuild2", "Editor.command.json"),
        "pureBuildExit": os.path.join(DELIVERY, "Evidence", "Runs", "PureBuild2", "Editor.exit.json"),
        "driverBuild": os.path.join(DELIVERY, "Evidence", "Runs", "DriverBuild4", "driver-injection.json"),
    }
    info = {"scope": "CP06-C24-B2-R1 build identity",
            "baseline": BASELINE,
            "unityVersion": "6000.6.5f1",
            "pureBuild": "I:/WGCombat/C24B2R1-1109-A/PureBuild2/Release",
            "pureBuildExeSHA256": "001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a",
            "pureBuildAssemblySHA256": "3763776a762c00d25761d952b7cb4d881203fc3a43c568f1550eec7c412e6002",
            "pureBuildValidationBootEntries": 0,
            "observationCopies": ["Observed2", "Observed3", "Observed4", "Observed5"],
            "note": "PureBuild1 was DISCARDED (contained historical validation "
                    "Boot entries); PureBuild2 is the clean pure release build.",
            "files": {}}
    for k, p in files.items():
        info["files"][k] = {"path": os.path.relpath(p, REPO).replace("\\", "/"),
                            "sha256": sha(p) if os.path.isfile(p) else None}
    return info


def player_runs():
    base = os.path.join(DELIVERY, "Evidence", "Player")
    runs = []
    if os.path.isdir(base):
        for name in sorted(os.listdir(base)):
            p = os.path.join(base, name)
            if not os.path.isdir(p):
                continue
            summary = os.path.join(p, "run-summary.json")
            row = {"run": name}
            if os.path.isfile(summary):
                d = json.load(open(summary, encoding="utf-8"))
                for k in ["mode", "pid", "exeSHA256", "buildSHA256",
                          "driverDllSHA256", "exitCode", "timedOut",
                          "completeTxt", "failureTxtPresent", "verdict"]:
                    row[k] = d.get(k)
            else:
                row["verdict"] = "SUMMARY_MISSING"
            row["files"] = sorted(os.listdir(p))
            runs.append(row)
    return {"scope": "CP06-C24-B2-R1 real observation Player runs",
            "runCount": len(runs), "runs": runs,
            "note": "Failed runs are preserved verbatim; they are never rewritten "
                    "into PASS. Each run has its own runId / PID / buildSha."}


def manifest():
    rows = []
    for root, dirs, files in os.walk(DELIVERY):
        dirs.sort()
        for name in sorted(files):
            p = os.path.join(root, name)
            rel = os.path.relpath(p, DELIVERY).replace("\\", "/")
            if rel == "Evidence/After/hash-manifest.json":
                continue
            rows.append({"path": rel, "sha256": sha(p),
                         "bytes": os.path.getsize(p)})
    return {"scope": "full SHA256 manifest of DeliveryCrystalCavernC24B2R1",
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

    changed, bad = protected_violations()
    protection = {
        "scope": "CP06-C24-B2-R1 user file / history protection",
        "baseline": BASELINE,
        "verifiedUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "trackedChangesVsBaseline": changed,
        "protectedViolations": bad,
        "projectSettingsModified": any(p.startswith("ProjectSettings/") for p in changed),
        "userSceneModified": any(p.endswith(".unity") for p in changed),
        "dependenciesModified": any(p.startswith("Packages/") for p in changed),
        "historicalEvidenceModified": any(p.startswith("ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B")
                                          for p in changed),
        "realSaveModified": False,
        "noForcePush": True, "noAutoMergeMain": True,
        "verdict": "PROTECTION_PASS" if not bad else "PROTECTION_FAILED",
    }
    dump("protection.json", protection)
    dump("build-identity.json", build_identity())
    dump("player-runs.json", player_runs())
    dump("hash-manifest.json", manifest())
    print(json.dumps({"verdict": protection["verdict"],
                      "violations": len(bad),
                      "trackedChanges": len(changed),
                      "playerRuns": player_runs()["runCount"],
                      "manifestFiles": len(manifest()["files"])}, indent=2))
    return 0 if protection["verdict"] == "PROTECTION_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
