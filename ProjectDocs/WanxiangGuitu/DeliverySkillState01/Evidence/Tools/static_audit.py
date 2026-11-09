#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SKILL-STATE-01 | frozen STATIC source audit (read-only, no Unity runtime).

Hashes the exact product sources at the delivery baseline and records the
control-flow facts that DESIGN_DECISIONS.md freezes. This tier is PASS-STATIC
only: it never claims a Player result and never triggers a product fix.
"""
import datetime
import hashlib
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
DELIVERY = os.path.abspath(os.path.join(HERE, "..", ".."))
REPO = os.path.abspath(os.path.join(DELIVERY, "..", "..", ".."))
OUT = os.path.join(DELIVERY, "Evidence", "Before")
BASELINE = "28d9fc529ba3bc621f0f7e73a183a18fba69f867"

SOURCES = [
    "Assets/CombatPrototype/WeaponSkillExpansion.cs",
    "Assets/CombatPrototype/AdventureCombat.cs",
    "Assets/CombatPrototype/SkillPhysicalEffects.cs",
    "Assets/CombatPrototype/ThirdPersonHero.cs",
    "Assets/CombatPrototype/PlayerHudPresenter.cs",
    "Assets/CombatPrototype/CombatAim.cs",
    "Assets/CombatPrototype/CombatSaveData.cs",
    "Assets/CombatPrototype/CombatSaveSystem.cs",
    "Assets/CombatPrototype/AdventureLoadout.cs",
    "Assets/CombatPrototype/HeroDodge.cs",
    "Assets/CombatPrototype/GameEntry.cs",
]

# (id, file, needle, meaning)
FACTS = [
    ("P-1", "WeaponSkillExpansion.cs", "expires=Time.time+3",
     "impact-field registers a pending entry with a 3s wall-clock (scaled) TTL"),
    ("P-2", "WeaponSkillExpansion.cs", "if(Time.time>=pair.Value.expires)expired.Add(pair.Key)",
     "LateUpdate expires pending entries unconditionally before any gate"),
    ("P-3", "AdventureCombat.cs", "if(hero.GameplayPaused||Time.timeScale<=0)return;",
     "projectile Update freezes completely when gameplay is paused"),
    ("P-4", "AdventureCombat.cs", "shot.life=2.5f",
     "projectile nominal life 2.5s; natural Dispose emits no resolved event"),
    ("P-5", "WeaponSkillExpansion.cs", "if(!fields.TryGetValue(e.projectile.AttackId,out var field))return;",
     "field creation requires the pending entry to still exist at resolve time"),
    ("P-6", "ThirdPersonHero.cs", "public bool GameplayPaused =>",
     "GameplayPaused is a computed property, not a single stored flag"),
    ("P-7", "PlayerHudPresenter.cs", "hero.HudPanelOpen=true;Time.timeScale=0",
     "the real UI entry ALWAYS also freezes timeScale (R2 measured this)"),
    ("P-8", "AdventureCombat.cs", "!hero.GameplayPaused&&Time.timeScale>0&&!hero.Dodge.IsRolling",
     "Ready gate includes paused / timescale / rolling / dead"),
    ("P-9", "WeaponSkillExpansion.cs", "CancelSequence();return;",
     "context loss cancels the active cast but does not clear fields"),
    ("P-10", "WeaponSkillExpansion.cs", "fields.Clear();SkillPiercingProjectile.Clear(hero);SkillImpactField.Clear(hero)",
     "OnDisable clears pending registry and spawned effects"),
    ("P-12", "CombatSaveData.cs", "public float weaponSkillCooldown",
     "save schema persists only skill cooldown, not Selected / pending / projectiles"),
    ("P-13", "AdventureCombat.cs", "public void RestoreCooldown(float remaining",
     "read restores cooldowns only; no transient skill state is rehydrated"),
    ("P-14", "WeaponSkillExpansion.cs", "ChargeFraction=>",
     "charge fraction derives from Time.time - started"),
    ("P-15", "SkillPhysicalEffects.cs", "f.next=Time.time+.25f",
     "impact-field pulses also use scaled Time.time"),
    ("P-16", "SkillPhysicalEffects.cs", "life=2.5f",
     "piercing projectile uses the same paused-return pattern"),
]


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    files = []
    for rel in SOURCES:
        p = os.path.join(REPO, rel)
        files.append({"path": rel, "sha256": sha(p), "bytes": os.path.getsize(p)})

    facts = []
    for ident, name, needle, meaning in FACTS:
        rel = "Assets/CombatPrototype/" + name
        text = open(os.path.join(REPO, rel), encoding="utf-8", errors="replace").read()
        lines = [i + 1 for i, l in enumerate(text.splitlines()) if needle in l]
        facts.append({"id": ident, "file": rel, "needle": needle,
                      "lines": lines, "found": bool(lines), "meaning": meaning})

    checks = {
        "allFrozenFactsFound": all(f["found"] for f in facts),
        "factCount": len(facts),
        "sourceFileCount": len(files),
        "conclusion": [
            "Global pause (timeScale=0) freezes Time.time as well as projectile life: "
            "pending TTL and projectile stay consistent (static inference only).",
            "UI-only pause (GameplayPaused=true, timeScale=1) advances Time.time while "
            "the projectile is frozen: after >3s the pending entry expires but the "
            "projectile is still alive. On resume its resolve cannot create the field.",
            "The UI-only state is a product-supported state contract, but the real UI "
            "entry always sets timeScale=0, so it is NOT reachable from a normal menu; "
            "it must be tested as a controlled state injection and labelled as such.",
            "Save schema v9 stores only weaponSkillCooldown; Selected resets to slot 0 "
            "by explicit CP06-A design limitation. No transient skill objects persist.",
        ],
        "requiresPlayerReproduction": True,
        "productVerdict": "NOT_DECIDED_BY_STATIC_AUDIT",
        "tier": "PASS-STATIC",
    }
    audit = {
        "scope": "SKILL-STATE-01 frozen static source audit (pre-reproduction)",
        "verifiedUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "baseline": BASELINE,
        "branch": "fix/skill-state-01",
        "sources": files,
        "facts": facts,
        "fiveContracts": {
            "C1_staffFieldProjectileAndDelayedSpawn": "P-1/P-2/P-4/P-5",
            "C2_bowChargeStartHoldReleaseCancel": "P-8/P-9/P-14",
            "C3_lifecyclePauseDeathDodgeSwitchUnload": "P-3/P-6/P-7/P-8/P-9/P-10",
            "C4_timeConsistencyProjectilePendingFollowup": "P-1/P-2/P-3/P-5/P-15/P-16",
            "C5_newProcessRestoreAndSaveContract": "P-12/P-13",
        },
        "checks": checks,
        "note": "This tier only reads frozen sources. It does NOT decide product FAIL "
                "and does NOT authorise a code change; see DESIGN_DECISIONS.md section 4.",
        "verdict": "STATIC_AUDIT_FROZEN",
    }
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "static-audit.json")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(audit, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({"verdict": audit["verdict"],
                      "allFrozenFactsFound": checks["allFrozenFactsFound"],
                      "facts": len(facts), "sources": len(files),
                      "missing": [f["id"] for f in facts if not f["found"]]}, indent=2))
    return 0 if checks["allFrozenFactsFound"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
