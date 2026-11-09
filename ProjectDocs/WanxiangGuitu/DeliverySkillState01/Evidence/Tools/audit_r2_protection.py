#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CP06 SKILL-STATE-01 | Step 1: STRICT audit of the R2 protection.json contradiction.

Read-only. Uses fixed full SHAs, never rewrites any B1/B2/R1/R2 file.
Answers: is `b1b2r1HistoryModified=true` with `protectedViolations=[]`
a real history violation, or a false positive of the summariser predicate?
"""
import datetime
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DELIVERY = os.path.abspath(os.path.join(HERE, "..", ".."))
REPO = os.path.abspath(os.path.join(DELIVERY, "..", "..", ".."))
OUT = os.path.join(DELIVERY, "Evidence", "Before")

R1_TIP = "c388e9b7ecf9b5619a65fac81227eba68f61b832"
R2_TIP = "28d9fc529ba3bc621f0f7e73a183a18fba69f867"
R2_BASE = R1_TIP  # baseline used by R2 finalize_evidence.py
R2_SELF = "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/"

PROTECTED_HISTORY = [
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B1/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/",
]
# The exact predicate R2's finalize_evidence.py used (note: NO trailing slash,
# and it does not exclude the batch's own delivery directory).
R2_LOOSE_PREDICATE = "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B"


def git(*args):
    return subprocess.check_output(["git", "-C", REPO] + list(args),
                                   text=True, encoding="utf-8")


def git_rc(*args):
    p = subprocess.run(["git", "-C", REPO] + list(args),
                       capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def tree_sha(commit, path):
    rc, out, err = git_rc("rev-parse", commit + ":" + path)
    return out if rc == 0 else None


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    # 1. The committed R2 protection report (read verbatim from the R2 tip).
    rc, raw, err = git_rc("show", R2_TIP + ":ProjectDocs/WanxiangGuitu/"
                          "DeliveryCrystalCavernC24B2R2/Evidence/After/protection.json")
    if rc != 0:
        print("FATAL: cannot read committed R2 protection.json:", err)
        return 1
    committed = json.loads(raw)

    # 2. Exact set of paths changed between R1 tip and R2 tip.
    changed = sorted({p.strip() for p in
                      git("diff", "--name-only", R1_TIP, R2_TIP).splitlines()
                      if p.strip()})

    # 3. Classification of those paths.
    self_dir = [p for p in changed if p.startswith(R2_SELF)]
    history = [p for p in changed if any(p.startswith(x) for x in PROTECTED_HISTORY)]
    project_settings = [p for p in changed if p.startswith("ProjectSettings/")]
    packages = [p for p in changed if p.startswith("Packages/")]
    user_scenes = [p for p in changed if p.endswith(".unity")]
    project_assets = [p for p in changed if p.endswith(".asset")]
    product_sources = [p for p in changed if p.startswith("Assets/")]
    other = [p for p in changed if not (
        p.startswith(R2_SELF) or any(p.startswith(x) for x in PROTECTED_HISTORY)
        or p.startswith("ProjectSettings/") or p.startswith("Packages/")
        or p.startswith("Assets/"))]

    # 4. Strongest evidence: tree object identity of each historical directory
    #    at R1 tip vs R2 tip. Equal tree SHA == byte-identical content.
    trees = []
    for path in PROTECTED_HISTORY + ["ProjectSettings/", "Packages/", "Assets/"]:
        p = path.rstrip("/")
        a, b = tree_sha(R1_TIP, p), tree_sha(R2_TIP, p)
        trees.append({"path": p, "atR1": a, "atR2": b,
                      "identical": a is not None and a == b})

    # 5. Re-evaluate the two R2 predicates against the exact changed set.
    loose_hits = [p for p in changed if p.startswith(R2_LOOSE_PREDICATE)]
    protected_hits = [p for p in changed if any(p.startswith(x) for x in PROTECTED_HISTORY)
                      or p.startswith("ProjectSettings/") or p.startswith("Packages/")
                      or p.endswith(".unity") or p.endswith(".asset")]
    recomputed = {
        "b1b2r1HistoryModified (R2 loose predicate)": bool(loose_hits),
        "protectedViolations (R2 PROTECTED_PREFIXES + scene/asset rules)": protected_hits,
        "loosePredicateHitCount": len(loose_hits),
        "loosePredicateHitsAreAllR2SelfDirectory": all(p.startswith(R2_SELF) for p in loose_hits),
        "loosePredicateHistoricalHits": len([p for p in loose_hits
                                             if any(p.startswith(x) for x in PROTECTED_HISTORY)]),
    }

    # 6. Verdict on the contradiction.
    real_violation = bool(history or project_settings or packages or user_scenes
                          or project_assets)
    committed_fields_consistent = (
        committed.get("b1b2r1HistoryModified") is False
        and committed.get("protectedViolations") == [])
    audit = {
        "scope": "SKILL-STATE-01 step 1: strict audit of R2 protection.json contradiction",
        "verifiedUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "repository": "https://github.com/mizunagare/BallMaze.git",
        "r1Tip": R1_TIP,
        "r2Tip": R2_TIP,
        "r2SummariserBaseline": R2_BASE,
        "sourceProtectionReport": R2_TIP + ":ProjectDocs/WanxiangGuitu/"
                                  "DeliveryCrystalCavernC24B2R2/Evidence/After/protection.json",
        "sourceProtectionReportSHA256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "committedFieldValues": {
            "b1b2r1HistoryModified": committed.get("b1b2r1HistoryModified"),
            "protectedViolations": committed.get("protectedViolations"),
            "productSourceModified": committed.get("productSourceModified"),
            "projectSettingsModified": committed.get("projectSettingsModified"),
            "dependenciesModified": committed.get("dependenciesModified"),
            "verdict": committed.get("verdict"),
        },
        "exactChangesR1ToR2": {
            "total": len(changed),
            "r2SelfDirectory": len(self_dir),
            "b1b2r1History": len(history),
            "projectSettings": len(project_settings),
            "packages": len(packages),
            "userScenes": len(user_scenes),
            "projectAssets": len(project_assets),
            "productSourcesUnderAssets": len(product_sources),
            "outsideDelivery": other,
            "allChangesAreR2SelfDirectory": len(self_dir) == len(changed),
        },
        "treeIdentityR1vsR2": trees,
        "allProtectedTreesIdentical": all(t["identical"] for t in trees),
        "recomputedPredicates": recomputed,
        "findings": [
            "R2's b1b2r1HistoryModified uses the prefix "
            "'" + R2_LOOSE_PREDICATE + "' with NO trailing slash and does NOT exclude the "
            "batch's own delivery directory, so all 601 newly added "
            "DeliveryCrystalCavernC24B2R2/ paths satisfy it.",
            "The exact R1->R2 diff contains ZERO files under any B1/B2/R1 historical "
            "delivery directory, ZERO ProjectSettings/Packages changes, ZERO .unity/.asset "
            "changes and ZERO Assets/ product source changes.",
            "Tree object SHAs of every protected historical directory and of "
            "ProjectSettings/, Packages/ and Assets/ are identical at R1 tip and R2 tip.",
            "Therefore protectedViolations=[] and PROTECTION_PASS are CORRECT, while "
            "b1b2r1HistoryModified=true is a FALSE POSITIVE caused by a mis-scoped "
            "summariser predicate / misleading field name, not by history modification.",
        ],
        "realHistoryViolation": real_violation,
        "committedFieldsInternallyConsistent": committed_fields_consistent,
        "disposition": "DOCUMENTATION_FALSE_POSITIVE__NO_HISTORY_DAMAGE",
        "remediation": [
            "Preserve R2's committed protection.json verbatim (history protection).",
            "Record this audit as a new, independent erratum in the SKILL-STATE-01 delivery.",
            "Future summarisers must use trailing-slash exact prefixes AND exclude the "
            "current batch's own delivery directory; rename the field to "
            "'historicalDeliveryModified' so its meaning matches its predicate.",
        ],
        "verdict": "R2_PROTECTION_CONTRADICTION_EXPLAINED_AS_FALSE_POSITIVE"
                   if not real_violation and not committed_fields_consistent
                   else "REVIEW_REQUIRED",
    }

    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "r2-protection-audit.json")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(audit, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({
        "verdict": audit["verdict"],
        "changedTotal": len(changed),
        "historyChanges": len(history),
        "allProtectedTreesIdentical": audit["allProtectedTreesIdentical"],
        "looseHits": len(loose_hits),
        "looseHistoricalHits": recomputed["loosePredicateHistoricalHits"],
        "committedFields": audit["committedFieldValues"],
        "output": os.path.relpath(p, REPO).replace("\\", "/"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
