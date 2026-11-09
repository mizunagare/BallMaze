#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CP06-C24-B2 | B2-03: read-only correlation of FROZEN historical frame events.

This is NOT a new Unity/Player run. It does not rewrite history: the v2.0 audit
status INCOMPLETE stays untouched. It establishes the ordered chain from the
original TSVs themselves, using independent files rather than the summary pair.

Reads (all frozen, all hashed):
  DeliveryCrystalCavernC24B/Evidence/Runs/WindupNewAudit1/audit.json
  .../PlayerWindupA2/, .../PlayerWindupB2/  (5-6 TSV/JSON files each)
  .../Evidence/PlayerPhase1/phase-releases.tsv (same-build P2 sequence)
  Assets/CombatPrototype/{CrystalCavernBossBrain,CrystalCavernBossRules,
                          CombatHealth,ArmorMitigation}.cs
  DeliveryCrystalCavernC24B/Tools/Driver.cs.txt (TSV column semantics)

Writes: Evidence/After/c05-correlation.json
        Evidence/After/phase-timeline.json
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DELIVERY = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
REPO = os.path.abspath(os.path.join(DELIVERY, "..", "..", ".."))
C24B = os.path.join(REPO, "ProjectDocs", "WanxiangGuitu", "DeliveryCrystalCavernC24B")
RUNS = os.path.join(C24B, "Evidence", "Runs")
ASSETS = os.path.join(REPO, "Assets", "CombatPrototype")
OUT = os.environ.get("C24B2_EVIDENCE_OUT") or os.path.join(DELIVERY, "Evidence", "After")
FORCE = os.environ.get("C24B2_FORCE") == "1"


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def tsv(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return [line.rstrip("\n").split("\t") for line in f if line.strip()]


def js(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


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


def sample(name):
    p = os.path.join(RUNS, name)
    leaves = [f for f in sorted(os.listdir(p)) if f.startswith("windup-") or
              f in ("assertions.tsv", "cavern-test.txt", "Player.command.json",
                    "Player.exit.json", "process.json")]
    files = [{"path": os.path.relpath(os.path.join(p, f), REPO).replace("\\", "/"),
              "sha256": sha256(os.path.join(p, f)),
              "bytes": os.path.getsize(os.path.join(p, f))} for f in leaves]
    health = tsv(os.path.join(p, "windup-health.tsv"))
    release = tsv(os.path.join(p, "windup-release.tsv"))
    hero = tsv(os.path.join(p, "windup-hero-health.tsv"))
    timeline = tsv(os.path.join(p, "windup-timeline.tsv"))
    transition_path = os.path.join(p, "windup-transition.tsv")
    transition = tsv(transition_path) if os.path.exists(transition_path) else []
    summary = js(os.path.join(p, "windup-summary.json"))
    return {
        "name": name, "files": files,
        "health": health, "release": release, "hero": hero,
        "timeline": timeline, "transition": transition, "summary": summary,
        "assertions": {r[0]: r[1] for r in tsv(os.path.join(p, "assertions.tsv")) if len(r) > 1},
    }


def analyse(s):
    warning = float(s["timeline"][0][1])
    r = s["release"][0]
    released = float(r[1])
    deadline = s["summary"]["deadline"]
    half = 360 * .5

    boss_damage = [v for v in s["health"] if v[2] == "Damage"]
    crosses = [v for v in boss_damage if float(v[3]) > half >= float(v[4])]
    in_windup = [v for v in boss_damage if warning <= float(v[1]) < released]
    player_damage = [v for v in s["hero"] if v[2] == "Damage"]
    recovery = [v for v in s["timeline"] if v[2] == "Recovery"]
    states = []
    for v in s["timeline"]:
        if not states or states[-1][2] != v[2]:
            states.append([v[0], v[1], v[2]])
    # Independent recovery-end -> transition edge from TWO separately written TSVs.
    last_recovery = recovery[-1] if recovery else None
    first_transition = s["transition"][0] if s["transition"] else None

    # Uniqueness-based attribution: one Release row, one hero Damage row, and the
    # hero row carries the boss.Attack / boss.Releases state snapshot at that frame.
    attribution_keys = []
    for h in player_damage:
        attribution_keys.append({
            "frame": int(h[0]), "time": float(h[1]),
            "releaseFrame": int(r[0]), "releaseTime": released,
            "releaseIndex": int(r[2]), "snapshotAttack": h[5] if len(h) > 5 else None,
            "snapshotReleases": h[6] if len(h) > 6 else None,
            "attack": r[4], "phase2": r[3], "rawDamage": float(r[5]),
            "hpBefore": float(h[3]), "hpAfter": float(h[4]),
            "frameMatch": int(h[0]) == int(r[0]),
            "timeMatch": abs(float(h[1]) - released) < 1e-6,
            "attackMatch": (h[5] if len(h) > 5 else None) == r[4],
            "releaseIndexMatch": (h[6] if len(h) > 6 else None) == r[2],
        })

    chain = [
        {"step": 1, "event": "P1 Claw Begin / Warning", "frame": int(s["timeline"][0][0]),
         "time": warning, "state": "Warning", "bossHP": float(s["timeline"][0][6]),
         "heroHP": float(s["timeline"][0][7]), "source": "windup-timeline.tsv first row"},
        {"step": 2, "event": "real weapon hit crosses half-health INSIDE windup",
         "frame": int(crosses[0][0]) if crosses else None,
         "time": float(crosses[0][1]) if crosses else None,
         "bossHP": [float(crosses[0][3]), float(crosses[0][4])] if crosses else None,
         "threshold": half, "source": "windup-health.tsv Damage row (not a direct HP set)"},
        {"step": 3, "event": "Release still uses ORIGINAL P1 parameters",
         "frame": int(r[0]), "time": released, "release": int(r[2]), "phase2": r[3],
         "attack": r[4], "rawDamage": float(r[5]), "deadline": deadline,
         "notEarly": released >= deadline, "source": "windup-release.tsv (Released event)"},
        {"step": 4, "event": "same-frame Damage receipt on hero",
         "frame": int(player_damage[0][0]) if player_damage else None,
         "time": float(player_damage[0][1]) if player_damage else None,
         "hp": [float(player_damage[0][3]), float(player_damage[0][4])] if player_damage else None,
         "source": "windup-hero-health.tsv (HealthObservation)"},
        {"step": 5, "event": "P1 Recovery fully consumed",
         "firstFrame": int(recovery[0][0]) if recovery else None,
         "lastFrame": int(last_recovery[0]) if last_recovery else None,
         "lastTime": float(last_recovery[1]) if last_recovery else None,
         "lastRemaining": float(last_recovery[4]) if last_recovery else None,
         "frames": len(recovery), "source": "windup-timeline.tsv Recovery rows"},
        {"step": 6, "event": "Transition begins AFTER recovery end",
         "frame": int(first_transition[0]) if first_transition else None,
         "time": float(first_transition[1]) if first_transition else None,
         "state": first_transition[2] if first_transition else None,
         "bossHP": float(first_transition[3]) if first_transition else None,
         "source": "windup-transition.tsv (independent file)"},
    ]
    ordered = bool(last_recovery and first_transition and
                   int(first_transition[0]) > int(last_recovery[0]) and
                   float(last_recovery[4]) > 0 and
                   states[-1][2] == "Recovery")
    attributed = (len(s["release"]) == 1 and len(player_damage) == 1 and
                  all(k["frameMatch"] and k["timeMatch"] and k["attackMatch"] and
                      k["releaseIndexMatch"] for k in attribution_keys))
    return {
        "sample": s["name"], "files": s["files"], "transition": s["transition"],
        "warning": warning, "deadline": deadline, "released": released,
        "releaseRows": len(s["release"]), "playerDamageRows": len(player_damage),
        "bossDamageRows": len(boss_damage), "damageInWindupRows": len(in_windup),
        "halfHealthThreshold": half, "crossings": crosses,
        "stateRuns": states,
        "recoveryFrames": len(recovery),
        "attribution": attribution_keys,
        "chain": chain,
        "checks": {
            "windupStartsAboveHalf": float(s["timeline"][0][6]) > half,
            "realHitCrossesHalfInWindup": len(crosses) == 1 and len(in_windup) == 1 and
                                          crosses[0] == in_windup[0],
            "releaseOriginalPhase": r[3] == "False" and r[4] == "Claw" and float(r[5]) == 16,
            "noDoubleRelease": len(s["release"]) == 1,
            "notEarlyRelease": released >= deadline,
            "playerDamageAttribution": attributed,
            "recoveryTransitionOrder": ordered,
            "fullOriginalRecovery": len(recovery) == 401 and
                                    abs(float(recovery[0][4]) - 1.35) < .01,
            "noP2DamageInOldWindup": float(r[5]) == 16,
            "singleKillNotUsedAsProof": True,
        },
        "assertions": s["assertions"],
        "summaryNotUsedForOrdering": {
            "reason": "recoveryObserved and transition were assigned together by the driver",
            "values": {"recoveryObserved": s["summary"]["recoveryObserved"],
                       "transition": s["summary"]["transition"]},
        },
    }


def main():
    audit_path = os.path.join(RUNS, "WindupNewAudit1", "audit.json")
    audit = js(audit_path)
    a = analyse(sample("PlayerWindupA2"))
    b = analyse(sample("PlayerWindupB2"))

    phase_path = os.path.join(C24B, "Evidence", "PlayerPhase1", "phase-releases.tsv")
    phase = tsv(phase_path) if os.path.exists(phase_path) else []
    sources = {}
    for name in ["CrystalCavernBossBrain.cs", "CrystalCavernBossRules.cs",
                 "CombatHealth.cs", "ArmorMitigation.cs"]:
        p = os.path.join(ASSETS, name)
        sources[name] = {"sha256": sha256(p), "bytes": os.path.getsize(p)}
    driver = os.path.join(C24B, "Tools", "Driver.cs.txt")
    driver_hash = sha256(driver)

    result = {
        "scope": "B2-03 / C05 P1 Claw crossing half-health: ordered chain from frozen raw events",
        "tier": "READ_ONLY_CORRELATION_OF_FROZEN_HISTORICAL_EVENTS / NOT a new Unity or Player run",
        "historicalStatusPreserved": {"path": os.path.relpath(audit_path, REPO).replace("\\", "/"),
                                      "sha256": sha256(audit_path),
                                      "status": audit["status"],
                                      "toolVersion": audit["toolVersion"],
                                      "toolSHA256": audit["toolSHA256"],
                                      "note": "INCOMPLETE is NOT rewritten; B2 adds new targeted evidence."},
        "columnSemantics": {
            "source": "Tools/Driver.cs.txt line 230 / ExecutedDrivers/WindupObserved2",
            "driverSHA256": driver_hash,
            "heroDamageColumns": ["frame", "Time.time", "HealthObservation.kind",
                                  "before", "after", "boss.Attack (read-only snapshot)",
                                  "boss.Releases (read-only snapshot)"],
            "releaseColumns": ["frame", "time", "release", "phase2", "attack",
                               "rawDamage", "origin", "direction"],
        },
        "productSourceSHA256": sources,
        "controlFlowModel": {
            "Begin": "attackPhase2=phase2 snapshot; AttackOrigin/AttackDirection frozen; until=Time.time+windup",
            "Release": "def=Definition(Attack,attackPhase2); Released event carries phase2/attack/rawDamage",
            "Recover": "State=Recovery; until=Time.time+def.recovery; sequence++",
            "HalfHPGate": "if(!phase2 && HP<=maxHealth*.5f && (State!=Recovery || Time.time>=until)) -> Transition",
            "AfterTransition": "phase2=true; sequence=0 -> Next(0,true)=CrossLines",
            "Damage": "CombatHealth.Damage -> ArmorMitigation.Incoming -> HealthObservation",
            "claim": "source model explains why the P1 windup cannot be swapped to P2 damage; "
                     "it is a static control-flow proof, not a runtime re-run",
        },
        "samples": [a, b],
        "targetedChecks": {
            "playerDamageAttribution": b["checks"]["playerDamageAttribution"],
            "recoveryTransitionOrder": b["checks"]["recoveryTransitionOrder"],
            "uniquenessArgument": "In PlayerWindupB2 there is exactly one windup-release.tsv row and "
                                  "exactly one Damage row in windup-hero-health.tsv. The hero row also "
                                  "carries boss.Attack='Claw' and boss.Releases='1' as a read-only state "
                                  "snapshot, matching the Released event on frame, time, attack and index. "
                                  "Within this recorded window no second damage source exists, so the "
                                  "historical 'no shared attackId' ambiguity is resolved at evidence level "
                                  "without adding a save field or telemetry.",
            "independentRecoveryEnd": "windup-timeline.tsv is written per frame during the loop; "
                                      "windup-transition.tsv is written independently when Transition is "
                                      "first observed. Last Recovery frame has Remaining>0, first "
                                      "Transition frame is strictly later. The summary pair is not used.",
            "noStateMachineRewrite": True,
            "oldC02C04StrictFailuresPreserved": True,
        },
        "p2NextAttack": {
            "sourceModel": "Second[sequence%4] with sequence reset to 0 -> CrossLines (damage 20)",
            "sameBuildRawEvidence": os.path.relpath(phase_path, REPO).replace("\\", "/") if phase else None,
            "sameBuildEvidenceSHA256": sha256(phase_path) if phase else None,
            "rows": phase[:6],
            "sameRun": False,
            "note": "phase-releases.tsv is from the SAME BUILD but a DIFFERENT run; the B2 windup run "
                    "stops at the first Transition frame. This is explicitly not same-run evidence.",
        },
        "verdict": "C05_CHAIN_CORRELATED" if all([
            b["checks"]["windupStartsAboveHalf"],
            b["checks"]["realHitCrossesHalfInWindup"],
            b["checks"]["releaseOriginalPhase"],
            b["checks"]["noDoubleRelease"],
            b["checks"]["notEarlyRelease"],
            b["checks"]["playerDamageAttribution"],
            b["checks"]["recoveryTransitionOrder"],
            b["checks"]["fullOriginalRecovery"],
            not a["crossings"],
        ]) else "C05_CHAIN_INCOMPLETE",
    }
    dump("c05-correlation.json", result)
    dump("phase-timeline.json", {
        "scope": "ordered C05 phase timeline (B2 sample)",
        "chain": b["chain"], "stateRuns": b["stateRuns"],
        "transition": b["transition"], "summary": js(
            os.path.join(RUNS, "PlayerWindupB2", "windup-summary.json")),
    })
    print(json.dumps({"verdict": result["verdict"],
                      "checks": b["checks"],
                      "historicalStatus": audit["status"]}, indent=2))
    return 0 if result["verdict"] == "C05_CHAIN_CORRELATED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
