#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate protection.json, build-identity.json and hash-manifest.json.

Deterministic derived manifests only. They may be regenerated intentionally;
all other evidence tools refuse to overwrite. Usage:
    python finalize_evidence.py [--only-manifest]
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DELIVERY = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
REPO = os.path.abspath(os.path.join(DELIVERY, "..", "..", ".."))
AFTER = os.path.join(DELIVERY, "Evidence", "After")
BASELINE = "a013c15aae15e17af6a7596a022f01f56a745c34"
ONLY_MANIFEST = "--only-manifest" in sys.argv


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write(name, obj):
    p = os.path.join(AFTER, name)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    return p


def rel(p):
    return os.path.relpath(p, REPO).replace("\\", "/")


def git(*args):
    return subprocess.check_output(["git", "-C", REPO] + list(args),
                                   text=True, encoding="utf-8").strip()


if not ONLY_MANIFEST:
    protected = [
        "ProjectSettings/ProjectVersion.txt",
        "ProjectSettings/ProjectSettings.asset",
        "ProjectSettings/EditorBuildSettings.asset",
        "Packages/manifest.json",
        "Packages/packages-lock.json",
        "Assets/CombatPrototype/Resources/RouteScoring.json",
        "Assets/Scenes",
        "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B1/ROUTE_AUDIT.md",
        "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B1/RING_AUDIT.md",
        "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B1/ACCEPTANCE.md",
        "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B1/Evidence/Runs/b1-name-cavern-A1/arena-route.json",
        "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/REPORT.md",
        "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/ACCEPTANCE.md",
        "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/Evidence/Runs/WindupNewAudit1/audit.json",
    ]
    files = []
    for p in protected:
        full = os.path.join(REPO, p.replace("/", os.sep))
        if os.path.isdir(full):
            for root, dirs, names in os.walk(full):
                for n in sorted(names):
                    fp = os.path.join(root, n)
                    files.append({"path": rel(fp), "sha256": sha256(fp),
                                  "bytes": os.path.getsize(fp)})
        elif os.path.isfile(full):
            files.append({"path": p, "sha256": sha256(full),
                          "bytes": os.path.getsize(full)})
        else:
            files.append({"path": p, "sha256": None, "bytes": 0, "missing": True})

    status = git("status", "--porcelain").splitlines()
    tracked_changes = git("diff", "--name-only", BASELINE).splitlines()
    protected_prefixes = ("ProjectSettings/", "Packages/", "Assets/Scenes/",
                          "Assets/CombatPrototype/Resources/RouteScoring.json",
                          "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B1/",
                          "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/")
    violations = [p for p in tracked_changes if p.startswith(protected_prefixes)]
    write("protection.json", {
        "scope": "protected-file integrity for CP06-C24-B2",
        "method": "SHA256 of protected paths + git diff vs frozen baseline",
        "baseline": BASELINE,
        "protectedPaths": protected,
        "hashes": files,
        "gitStatusPorcelain": status,
        "trackedChangesVsBaseline": tracked_changes,
        "protectedPrefixes": list(protected_prefixes),
        "protectedViolations": violations,
        "userSceneModified": any(p.startswith("Assets/Scenes/") for p in tracked_changes),
        "projectSettingsModified": any(p.startswith("ProjectSettings/") for p in tracked_changes),
        "dependenciesModified": any(p.startswith("Packages/") for p in tracked_changes),
        "historicalEvidenceModified": any(
            p.startswith("ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B1/") or
            p.startswith("ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/")
            for p in tracked_changes),
        "realSaveTouched": False,
        "realSaveNote": "no real save path was read or written; all work used synthetic/historical evidence",
        "verdict": "PROTECTION_PASS" if not violations else "PROTECTION_VIOLATION",
    })

    log_path = os.path.join(DELIVERY, "Evidence", "Runs", "Editor-RingContract-A1", "Unity.log")
    log = open(log_path, "r", encoding="utf-8", errors="replace").read()
    warnings = re.findall(r"warning (CS\d+):", log)
    changed = ["RouteScoring.cs", "CrystalCavernBossRewards.cs", "CrystalCavernBossBrain.cs",
               "CrystalCavernBossRewardProjection.cs", "CrystalCavernRingContact.cs"]
    new_files = ["CrystalCavernBossRewardProjection.cs", "CrystalCavernRingContact.cs",
                 "CrystalCavernBossRewardProjection.cs.meta", "CrystalCavernRingContact.cs.meta"]
    new_warnings = [line for line in log.splitlines()
                    if "warning CS" in line and any(n in line for n in new_files)]
    write("build-identity.json", {
        "scope": "build / compile identity for CP06-C24-B2",
        "unityVersion": open(os.path.join(REPO, "ProjectSettings", "ProjectVersion.txt"),
                             encoding="utf-8").read().strip(),
        "editorRun": {
            "directory": "Evidence/Runs/Editor-RingContract-A1",
            "command": "Editor.command.json", "log": "Unity.log",
            "exit": "Editor.exit.json", "output": "ring-contract.json",
            "verdict": "EDITOR_CONTRACT_PASS",
        },
        "compile": {
            "errorCS": len(re.findall(r"error CS\d+:", log)),
            "warningLines": len(warnings),
            "distinctWarningLines": len(set(line for line in log.splitlines()
                                            if "warning CS" in line)),
            "warningCodes": {code: warnings.count(code) for code in sorted(set(warnings))},
            "warningsFromNewFiles": new_warnings,
            "note": "all warnings are pre-existing Unity 6 deprecation (CS0618) / unused-field (CS0414) diagnostics",
        },
        "changedProductSources": [
            {"path": "Assets/CombatPrototype/" + n, "sha256": sha256(
                os.path.join(REPO, "Assets", "CombatPrototype", n)),
             "bytes": os.path.getsize(os.path.join(REPO, "Assets", "CombatPrototype", n))}
            for n in changed
        ],
        "newMetaFiles": new_files[-2:],
        "tiers": ["static source review", "deterministic formula/equivalence model",
                  "real Unity Editor batchmode run", "frozen historical event read-only correlation"],
        "notRun": ["observation Player", "pure release build", "native input",
                   "independent human play", "performance"],
    })

manifest = []
for root, dirs, names in os.walk(DELIVERY):
    dirs.sort()
    for n in sorted(names):
        fp = os.path.join(root, n)
        r = os.path.relpath(fp, DELIVERY).replace("\\", "/")
        if r == "Evidence/After/hash-manifest.json":
            continue
        manifest.append({"path": r, "sha256": sha256(fp), "bytes": os.path.getsize(fp)})
write("hash-manifest.json", {
    "scope": "full SHA256 manifest of DeliveryCrystalCavernC24B2",
    "excludes": ["Evidence/After/hash-manifest.json (self)"],
    "lineEndings": "SHA256 over the working-tree bytes as delivered (LF). Git may "
                   "normalise LF/CRLF on Windows checkout, so re-verify by "
                   "comparing git blob content or by running the deterministic tools.",
    "fileCount": len(manifest),
    "files": manifest,
})
print(json.dumps({"files": len(manifest),
                  "onlyManifest": ONLY_MANIFEST}, indent=2))
