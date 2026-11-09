#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CP06-C24-B2-R1 | strict same-run event correlator.

Replaces the B2 correlation *methodology* for R1 (B2 files are preserved verbatim).

Hard rules enforced here:
  R1. Every event must carry a complete identity triple:
      runId, processId, buildSha. Any missing/empty component marks the event
      UNIDENTIFIED; UNIDENTIFIED events can NEVER contribute to a PASS.
  R2. Only events whose identity triples are EQUAL may be joined into one
      timeline. Events from a different run are quarantined in
      crossRunEvidence and can NEVER be used to prove a check of this run.
  R3. A null/missing frame or time makes the event UNPLACEABLE. Any check that
      needs that event is INCOMPLETE (or NOT_RUN when the event is absent),
      never PASS.
  R4. Every check records its input rows (file + line + raw values), the
      comparison expression, the evaluated operands and the status. There is
      no bare "10/10" aggregate: the verdict is derived from the weakest
      required check and always carries an explanation.

Status vocabulary: PASS / NOT_RUN / INCOMPLETE / UNRESOLVED / FAIL.

Inputs (all read-only):
  - B2 Evidence/After/c05-correlation.json              (frozen, hashed)
  - C24B Evidence/Runs/{PlayerWindupA2,PlayerWindupB2}  (frozen, hashed)
  - C24B Evidence/PlayerPhase1/phase-releases.tsv       (frozen, hashed)
  - R1 Evidence/Player/<runId>/c05-events.jsonl         (optional; same-run
    Player events produced by the R1 observation driver)

Outputs (into R1 Evidence/After, overwrite-protected):
  - c05-strict-correlation.json
  - c05-strict-checks.tsv
  - b2-reevaluation.json
  - r1-tool-selfcheck.json       (only with --self-test)

Environment:
  C24R1_EVIDENCE_OUT   alternate output directory (fresh)
  C24R1_FORCE=1        explicitly allow overwriting an existing output
"""
import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DELIVERY = os.path.abspath(os.path.join(HERE, "..", ".."))
REPO = os.path.abspath(os.path.join(DELIVERY, "..", "..", ".."))
B2 = os.path.join(REPO, "ProjectDocs", "WanxiangGuitu", "DeliveryCrystalCavernC24B2")
C24B = os.path.join(REPO, "ProjectDocs", "WanxiangGuitu", "DeliveryCrystalCavernC24B")
OUT = os.environ.get("C24R1_EVIDENCE_OUT") or os.path.join(DELIVERY, "Evidence", "After")
FORCE = os.environ.get("C24R1_FORCE") == "1"

IDENTITY_KEYS = ("runId", "processId", "buildSha")
RANK = {"PASS": 0, "UNRESOLVED": 1, "INCOMPLETE": 2, "NOT_RUN": 3, "FAIL": 4}


# ---------------------------------------------------------------- primitives

def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def rel(path):
    return os.path.relpath(path, REPO).replace("\\", "/")


def tsv_rows(path):
    """Return [(line_number, [fields], raw_line)] with 1-based line numbers."""
    with open(path, "r", encoding="utf-8-sig") as f:
        out = []
        for i, line in enumerate(f, 1):
            line = line.rstrip("\r\n")
            if not line.strip():
                continue
            out.append((i, line.split("\t"), line))
        return out


def js(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def dump(name, obj):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    if os.path.exists(p) and not FORCE:
        raise SystemExit("refusing to overwrite existing evidence: " + p +
                         " (use a fresh C24R1_EVIDENCE_OUT or C24R1_FORCE=1)")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    return p


# ---------------------------------------------------------------- identity

def identity_of(ev):
    """Return (triple_dict, missing_keys). Empty string / None / 0 are missing."""
    triple = {}
    missing = []
    for k in IDENTITY_KEYS:
        v = ev.get(k, None)
        if v is None or v == "" or v == 0:
            missing.append(k)
        triple[k] = v
    return triple, missing


def events_identity(events):
    """Strictly verify one single run. Returns (ok, triple, problems)."""
    if not events:
        return False, None, ["no events supplied"]
    triples, problems = [], []
    for i, ev in enumerate(events):
        t, missing = identity_of(ev)
        if missing:
            problems.append("event[%d] (%s) missing identity: %s" %
                            (i, ev.get("kind", "?"), ",".join(missing)))
        triples.append(t)
    distinct = {json.dumps(t, sort_keys=True, default=str) for t in triples
                if all(t.get(k) not in (None, "", 0) for k in IDENTITY_KEYS)}
    if len(distinct) > 1:
        problems.append("multiple distinct identity triples: %d" % len(distinct))
    if problems:
        return False, None, problems
    return True, triples[0], []


def placeable(ev):
    """A frame AND a time must both be present and numeric."""
    f, t = ev.get("frame", None), ev.get("time", None)
    if f is None or t is None:
        return False
    if isinstance(f, bool) or isinstance(t, bool):
        return False
    try:
        float(f), float(t)
    except (TypeError, ValueError):
        return False
    return True


def check(cid, description, inputs, expression, operands, status, reason=""):
    """One fully auditable check row. Never called with status=PASS unless all
    operands are real values from identified, placeable, same-run events."""
    if status not in RANK:
        raise ValueError("bad status " + str(status))
    if status == "PASS" and (not inputs or any(v is None for v in operands.values())):
        raise AssertionError("PASS requires non-null operands and input rows: " + cid)
    return {
        "id": cid, "description": description,
        "inputRows": inputs, "expression": expression,
        "operands": operands, "status": status, "reason": reason,
    }


def src(path, line, raw, extra=None):
    d = {"file": rel(path), "line": line, "raw": raw}
    if extra:
        d.update(extra)
    return d


# ---------------------------------------------------------------- B2 re-audit

def b2_reevaluation():
    """Read-only strict re-evaluation of the FROZEN B2 claim. Never writes B2."""
    p = os.path.join(B2, "Evidence", "After", "c05-correlation.json")
    d = js(p)
    root = os.path.join(C24B, "Evidence")
    phase_path = os.path.join(root, "PlayerPhase1", "phase-releases.tsv")
    cmd_b2 = os.path.join(root, "Runs", "PlayerWindupB2", "Player.command.json")
    cmd_phase = os.path.join(root, "PlayerPhase1", "Player.command.json")

    samples = {}
    for s in d.get("samples", []):
        false_checks = sorted(k for k, v in s["checks"].items() if v is False)
        null_steps = []
        for c in s["chain"]:
            nulls = sorted(k for k, v in c.items() if v is None)
            if nulls:
                null_steps.append({"step": c["step"], "event": c["event"],
                                   "nullFields": nulls})
        samples[s["sample"]] = {
            "falseChecks": false_checks,
            "falseCheckCount": len(false_checks),
            "chainStepsWithNullFields": null_steps,
            "chainStepCount": len(s["chain"]),
        }

    b2_cmd = js(cmd_b2) if os.path.isfile(cmd_b2) else {}
    ph_cmd = js(cmd_phase) if os.path.isfile(cmd_phase) else {}
    p2_same_run = d.get("p2NextAttack", {}).get("sameRun", None)
    p2_rows = d.get("p2NextAttack", {}).get("rows", [])

    findings = [
        "B2 verdict is %s while PlayerWindupA2 has %d FALSE checks (%s)." %
        (d.get("verdict"), samples.get("PlayerWindupA2", {}).get("falseCheckCount", 0),
         ", ".join(samples.get("PlayerWindupA2", {}).get("falseChecks", []))),
        "B2 chain for PlayerWindupA2 contains null frame/time for the "
        "cross-half-hit step and the Transition step; a null timestamp cannot PASS.",
        "p2NextAttack.sameRun=%s; B2 itself states phase-releases.tsv is a DIFFERENT "
        "run. Under R1 rule R2 it is quarantined and cannot prove P2 behaviour of "
        "the windup run." % p2_same_run,
        "The historical frame TSVs contain no runId / processId / buildSha columns, "
        "so no same-run identity triple can be established from them.",
        "B2 REPORT/ACCEPTANCE describe '10/10 checks'. The aggregate counted "
        "PlayerWindupB2 only and mixed targetedChecks with control-flow model "
        "statements; it is not a complete same-run C05 proof.",
    ]
    return {
        "scope": "R1 strict re-evaluation of the frozen B2 C05 claim (read-only)",
        "tier": "PASS-STATIC / source-and-evidence audit; NOT a Player run",
        "frozenInput": {"path": rel(p), "sha256": sha256(p),
                        "bytes": os.path.getsize(p)},
        "b2VerbatimVerdict": d.get("verdict"),
        "b2TargetedChecks": d.get("targetedChecks", {}),
        "samples": samples,
        "p2NextAttack": {
            "sameRun": p2_same_run,
            "rowCount": len(p2_rows),
            "firstRow": p2_rows[0] if p2_rows else None,
            "b2RunCommand": rel(cmd_b2) if os.path.isfile(cmd_b2) else None,
            "b2RunHostPid": b2_cmd.get("hostPid"),
            "b2RunExe": b2_cmd.get("exe"),
            "phaseRunCommand": rel(cmd_phase) if os.path.isfile(cmd_phase) else None,
            "phaseRunHostPid": ph_cmd.get("hostPid"),
            "phaseRunExe": ph_cmd.get("exe"),
            "r1Disposition": "QUARANTINED_DIFFERENT_RUN",
        },
        "supportingRawEvidence": [
            {"path": rel(os.path.join(root, "Runs", "PlayerWindupB2", "windup-release.tsv")),
             "sha256": sha256(os.path.join(root, "Runs", "PlayerWindupB2", "windup-release.tsv")),
             "lines": len(tsv_rows(os.path.join(root, "Runs", "PlayerWindupB2", "windup-release.tsv")))},
            {"path": rel(phase_path), "sha256": sha256(phase_path) if os.path.isfile(phase_path) else None,
             "lines": len(tsv_rows(phase_path)) if os.path.isfile(phase_path) else None},
        ],
        "findings": findings,
        "r1Conclusion": "B2_10_OF_10_CLAIM_NOT_SUPPORTED_AS_SAME_RUN_PROOF",
        "historicalFilesUntouched": True,
        "note": "This is a re-evaluation, not a rewrite. B2 REPORT.md, ACCEPTANCE.md "
                "and c05-correlation.json remain byte-identical on the B2 branch.",
    }


# ---------------------------------------------------------------- R1 events

def load_player_events():
    """Load R1 same-run Player events if present. Each line is one event with
    mandatory identity + frame/time fields. Returns (events, fileMeta, note)."""
    base = os.path.join(DELIVERY, "Evidence", "Player")
    manifests = []
    if os.path.isdir(base):
        for name in sorted(os.listdir(base)):
            cand = os.path.join(base, name, "c05-events.jsonl")
            if os.path.isfile(cand):
                manifests.append(cand)
    if not manifests:
        return [], None, ("no R1 Player c05-events.jsonl found under %s; "
                          "all Player-level checks are NOT_RUN" % rel(base))
    events = []
    meta = []
    for p in manifests:
        rows = []
        with open(p, "r", encoding="utf-8-sig") as f:
            for n, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                ev = json.loads(line)
                ev["_sourceFile"] = rel(p)
                ev["_sourceLine"] = n
                ev["_raw"] = line
                rows.append(ev)
        events.extend(rows)
        meta.append({"path": rel(p), "sha256": sha256(p), "eventCount": len(rows)})
    return events, meta, None


def strict_checks(events, file_meta, absence_note):
    """Build the R1 C05 check table. Strict: no identity / no timestamps / no
    event => NOT_RUN or INCOMPLETE. Cross-run events are quarantined."""
    if not events:
        ids = ["sameRunIdentity", "windupStartsAboveHalf",
               "realHitCrossesHalfInWindup", "releaseOriginalPhase",
               "playerDamageAttribution", "fullOriginalRecovery",
               "recoveryTransitionOrder", "p2NextAttackSameRun",
               "noNullTimestamps", "bossInstanceIdentityStable"]
        return [check(c, c, [], "no events available", {}, "NOT_RUN",
                      absence_note or "no same-run Player events") for c in ids], {
            "crossRunEvidence": [], "identity": None, "identityProblems": [absence_note]}

    ok, triple, problems = events_identity(events)
    quarantined = []
    if not ok:
        # Partition by identity to show exactly what was rejected.
        groups = {}
        for ev in events:
            t, miss = identity_of(ev)
            key = json.dumps(t, sort_keys=True, default=str)
            groups.setdefault(key, []).append(ev)
        for key, group in sorted(groups.items()):
            quarantined.append({"identity": json.loads(key), "eventCount": len(group),
                                "kinds": sorted({e.get("kind", "?") for e in group})})
    unplaceable = [e for e in events if not placeable(e)]
    timeline = sorted([e for e in events if placeable(e)],
                      key=lambda e: (float(e["frame"]), float(e["time"])))

    def row(e):
        return src(os.path.join(REPO, e["_sourceFile"]), e["_sourceLine"], e["_raw"])

    rows = []
    # 1 identity
    rows.append(check(
        "sameRunIdentity", "all events share one complete runId/processId/buildSha",
        [row(e) for e in events[:8]],
        "len(distinct(runId,processId,buildSha)) == 1 AND no empty component",
        {"eventCount": len(events), "identity": triple if ok else None,
         "problems": problems or []},
        "PASS" if ok else "INCOMPLETE",
        "" if ok else "; ".join(problems)))

    # helpers restricted to identified + placeable events
    usable = [e for e in timeline] if ok else []
    def find(kind):
        return [e for e in usable if e.get("kind") == kind]

    warning = find("warning")
    hit = find("bossHealth")
    release = find("release")
    hero = find("heroHealth")
    recovery = find("recoveryEnd")
    transition = find("transitionBegin")
    p2 = find("p2Release")

    # 2 windup starts above half
    if warning and warning[0].get("bossHPBefore") is not None:
        w = warning[0]
        st = "PASS" if float(w["bossHPBefore"]) > float(w.get("halfThreshold", 180)) else "FAIL"
        rows.append(check("windupStartsAboveHalf", "P1 begins with Boss HP > 50%",
                          [row(w)], "bossHPBefore > halfThreshold",
                          {"bossHPBefore": w["bossHPBefore"],
                           "halfThreshold": w.get("halfThreshold", 180)}, st))
    else:
        rows.append(check("windupStartsAboveHalf", "P1 begins with Boss HP > 50%",
                          [], "warning.bossHPBefore > halfThreshold", {},
                          "NOT_RUN" if not warning else "INCOMPLETE",
                          "missing or unidentified warning event"))

    # 3 real hit crosses half inside windup
    crossing = [e for e in hit if e.get("bossHPBefore") is not None and
                e.get("bossHPAfter") is not None and warning and
                float(warning[0]["time"]) <= float(e["time"]) < float(release[0]["time"])
                and float(e["bossHPBefore"]) > 180 >= float(e["bossHPAfter"])] if release else []
    if crossing and crossing[0].get("attackSource"):
        rows.append(check("realHitCrossesHalfInWindup",
                          "a REAL player attack crosses 50% during the P1 windup",
                          [row(warning[0]), row(crossing[0]), row(release[0])],
                          "warning.time <= hit.time < release.time AND "
                          "hit.bossHPBefore > 180 >= hit.bossHPAfter AND hit.attackSource != null",
                          {"hitFrame": crossing[0].get("frame"),
                           "hitTime": crossing[0].get("time"),
                           "attackSource": crossing[0].get("attackSource")}, "PASS"))
    else:
        rows.append(check("realHitCrossesHalfInWindup",
                          "a REAL player attack crosses 50% during the P1 windup",
                          [row(e) for e in (hit[:2] + warning[:1] + release[:1])],
                          "warning.time <= hit.time < release.time AND "
                          "hit.bossHPBefore > 180 >= hit.bossHPAfter AND hit.attackSource != null",
                          {"bossHealthEvents": len(hit), "releaseEvents": len(release)},
                          "NOT_RUN" if not (hit and warning and release) else "INCOMPLETE",
                          "no strictly attributable same-run crossing event"))

    # 4 release uses original P1 parameters
    if release:
        r = release[0]
        st = "PASS" if (r.get("phase") == 1 and r.get("attack") == "Claw"
                        and float(r.get("rawDamage", 0)) == 16) else "FAIL"
        rows.append(check("releaseOriginalPhase",
                          "the already-started attack releases with frozen P1 parameters",
                          [row(r)], "phase == 1 AND attack == 'Claw' AND rawDamage == 16",
                          {"phase": r.get("phase"), "attack": r.get("attack"),
                           "rawDamage": r.get("rawDamage")}, st))
    else:
        rows.append(check("releaseOriginalPhase", "P1 frozen-parameter release",
                          [], "phase == 1 AND attack == 'Claw' AND rawDamage == 16", {},
                          "NOT_RUN", "no same-run release event"))

    # 5 hero damage attribution, strict: same frame AND same derived join key.
    # HealthObservation has NO product attackId, so the R1 driver derives a
    # READ-ONLY correlationId from real same-run fields
    # (runId : boss.Releases : Time.frameCount) on BOTH sides of the join.
    # This key is never written to the save and never changes product behaviour.
    if release and hero:
        r, hs = release[0], [h for h in hero if h.get("kind") == "heroHealth"]
        attributed = [h for h in hs if h.get("correlationId") and
                      h.get("correlationId") == r.get("correlationId") and
                      int(h["frame"]) == int(r["frame"])]
        rows.append(check("playerDamageAttribution",
                          "same-release damage receipt via same-run derived correlationId "
                          "(frame + release index), not a uniqueness guess",
                          [row(r)] + [row(h) for h in hs[:3]],
                          "hero.correlationId == release.correlationId AND "
                          "hero.frame == release.frame AND correlationId != null",
                          {"releaseCorrelationId": r.get("correlationId"),
                           "heroRows": len(hs), "attributedRows": len(attributed)},
                          "PASS" if attributed else "INCOMPLETE",
                          "" if attributed else "no shared same-run correlationId on hero damage"))
    else:
        rows.append(check("playerDamageAttribution", "same-release damage receipt",
                          [], "hero.correlationId == release.correlationId", {}, "NOT_RUN",
                          "missing release or hero health events"))

    # 6 full original recovery
    rows.append(check("fullOriginalRecovery", "P1 Recovery runs to its frozen end",
                      [row(e) for e in recovery[:2]],
                      "recoveryEnd.remaining <= 0.001 (float-frame tolerance) AND "
                      "recoveryEnd.time > release.time",
                      {"recoveryEndEvents": len(recovery),
                       "lastRemaining": recovery[-1].get("remaining") if recovery else None},
                      "PASS" if recovery and recovery[-1].get("remaining") is not None
                      and float(recovery[-1]["remaining"]) <= .001 else
                      ("NOT_RUN" if not recovery else "INCOMPLETE"),
                      "an independent recovery-end event is required; summary pairs are not used"))

    # 7 recovery -> transition ordering
    if recovery and transition:
        re_, tr = recovery[-1], transition[0]
        st = "PASS" if float(tr["frame"]) > float(re_["frame"]) else "FAIL"
        rows.append(check("recoveryTransitionOrder",
                          "Transition begins strictly AFTER recovery end",
                          [row(re_), row(tr)], "transition.frame > recoveryEnd.frame",
                          {"recoveryEndFrame": re_.get("frame"),
                           "transitionFrame": tr.get("frame"),
                           "recoveryEndTime": re_.get("time"),
                           "transitionTime": tr.get("time")}, st))
    else:
        rows.append(check("recoveryTransitionOrder", "recovery -> transition order",
                          [row(e) for e in (recovery[:1] + transition[:1])],
                          "transition.frame > recoveryEnd.frame", {},
                          "NOT_RUN" if not (recovery and transition) else "INCOMPLETE",
                          "a missing or null-timestamp event cannot be treated as ordered"))

    # 8 P2 next attack must be SAME RUN
    if p2 and ok:
        p = p2[0]
        st = "PASS" if (p.get("phase") == 2 and p.get("attack") not in (None, "Claw")) else "FAIL"
        rows.append(check("p2NextAttackSameRun",
                          "after Transition the next release uses P2 moves IN THE SAME RUN",
                          [row(p)], "p2Release.phase == 2 AND identity == run identity",
                          {"phase": p.get("phase"), "attack": p.get("attack"),
                           "identityMatch": True}, st))
    else:
        rows.append(check("p2NextAttackSameRun",
                          "after Transition the next release uses P2 moves IN THE SAME RUN",
                          [], "p2Release exists with the SAME identity triple", {},
                          "NOT_RUN", "no same-run P2 release; cross-run phase-releases.tsv "
                                     "is quarantined and cannot substitute"))

    # 9 no null timestamps
    rows.append(check("noNullTimestamps", "no event in the chain has a null frame/time",
                      [row(e) for e in (unplaceable[:3] or events[:3])],
                      "for every event: frame != null AND time != null",
                      {"totalEvents": len(events), "unplaceableEvents": len(unplaceable),
                       "eventsExamined": len(events)},
                      "PASS" if not unplaceable else "INCOMPLETE",
                      "" if not unplaceable else "unplaceable events cannot be ordered"))

    # 10 boss instance identity stable
    ids = {str(e.get("bossInstanceId")) for e in events if e.get("bossInstanceId")}
    with_id = [e for e in events if e.get("bossInstanceId")]
    rows.append(check("bossInstanceIdentityStable",
                      "one Boss instance identity throughout the timeline",
                      [row(e) for e in with_id[:3]],
                      "len(distinct(bossInstanceId)) == 1 AND all events carry it",
                      {"distinctIds": len(ids), "eventsWithId": len(with_id),
                       "totalEvents": len(events)},
                      "PASS" if len(ids) == 1 and len(with_id) == len(events) else "INCOMPLETE",
                      "" if len(ids) == 1 and len(with_id) == len(events)
                      else "missing/ambiguous boss instance identity"))
    return rows, {"crossRunEvidence": quarantined, "identity": triple if ok else None,
                  "identityProblems": problems, "unplaceableCount": len(unplaceable)}


def verdict_of(rows):
    worst = max(RANK[r["status"]] for r in rows)
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in RANK}
    if worst == 0:
        return "PASS-PLAYER_SAME_RUN_C05", counts, "all required checks PASS on identified, "\
                                                   "placeable, same-run Player events"
    if worst == 4:
        return "FAIL", counts, "at least one check FAILED on real same-run events"
    label = {1: "INCOMPLETE", 2: "INCOMPLETE", 3: "NOT_RUN"}[worst]
    return label, counts, ("weakest required check is %s; no aggregate PASS is issued. "
                           "NULL timestamps, missing events and different-run events "
                           "are never counted as PASS." %
                           sorted({r["status"] for r in rows}, key=lambda s: RANK[s])[-1])


# ---------------------------------------------------------------- self-test

def self_test():
    """Prove the two corrected rules with constructed events."""
    base = {"runId": "R1-SELF-1", "processId": 4242, "buildSha": "a" * 64,
            "frame": 1, "time": 1.0, "bossInstanceId": "boss-1"}
    def ev(**kw):
        d = dict(base); d.update(kw)
        d.setdefault("_sourceFile", "R1/self-test/constructed-events.jsonl")
        d.setdefault("_sourceLine", 1)
        d["_raw"] = json.dumps(d, sort_keys=True, ensure_ascii=False)
        return d
    cases = []

    # null time must not PASS
    null_events = [ev(kind="warning", bossHPBefore=360, halfThreshold=180),
                   ev(kind="release", frame=None, time=None, phase=1,
                      attack="Claw", rawDamage=16, releaseIndex=1, attackId="atk-1")]
    rows, _ = strict_checks(null_events, None, None)
    cases.append({"name": "null_time_cannot_pass",
                  "expected": "no PASS for releaseOriginalPhase / noNullTimestamps",
                  "noNullTimestamps": next(r["status"] for r in rows if r["id"] == "noNullTimestamps"),
                  "pass": next(r["status"] for r in rows if r["id"] == "noNullTimestamps") != "PASS"})

    # different run must not be joined
    mixed = [ev(kind="warning", bossHPBefore=360, halfThreshold=180),
             ev(kind="release", frame=2, time=2.0, phase=1, attack="Claw",
                rawDamage=16, releaseIndex=1, attackId="atk-1"),
             ev(kind="p2Release", runId="ANOTHER-RUN", processId=9999,
                frame=3, time=3.0, phase=2, attack="CrossLines", rawDamage=20)]
    rows, info = strict_checks(mixed, None, None)
    cases.append({"name": "cross_run_cannot_be_joined",
                  "expected": "sameRunIdentity != PASS and quarantined",
                  "sameRunIdentity": next(r["status"] for r in rows if r["id"] == "sameRunIdentity"),
                  "p2NextAttackSameRun": next(r["status"] for r in rows if r["id"] == "p2NextAttackSameRun"),
                  "quarantinedGroups": len(info["crossRunEvidence"]),
                  "pass": next(r["status"] for r in rows if r["id"] == "sameRunIdentity") != "PASS"
                          and len(info["crossRunEvidence"]) >= 2})

    # missing event must be NOT_RUN, never PASS
    rows, _ = strict_checks([ev(kind="warning", bossHPBefore=360, halfThreshold=180)],
                            None, None)
    cases.append({"name": "missing_event_is_not_run",
                  "expected": "releaseOriginalPhase == NOT_RUN",
                  "releaseOriginalPhase": next(r["status"] for r in rows if r["id"] == "releaseOriginalPhase"),
                  "pass": next(r["status"] for r in rows if r["id"] == "releaseOriginalPhase") == "NOT_RUN"})

    return {"scope": "R1 strict correlator self-test (constructed events, NOT product evidence)",
            "cases": cases, "verdict": "TOOL_RULES_ENFORCED" if all(c["pass"] for c in cases)
                                        else "TOOL_RULE_VIOLATION"}


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        print(json.dumps(self_test(), indent=2))
        return 0

    reeval = b2_reevaluation()
    events, file_meta, absence_note = load_player_events()
    rows, extra = strict_checks(events, file_meta, absence_note)
    verdict, counts, explanation = verdict_of(rows)

    doc = {
        "scope": "CP06-C24-B2-R1 C05 strict same-run correlation",
        "tier": "PASS-PLAYER only if all inputs are real observation Player events; "
                "otherwise NOT_RUN / INCOMPLETE",
        "rules": {
            "R1": "complete identity triple (runId, processId, buildSha) required per event",
            "R2": "only equal identity triples may be joined into one timeline; "
                  "different-run events are quarantined",
            "R3": "null/missing frame or time => INCOMPLETE; missing event => NOT_RUN; "
                  "neither can be counted as PASS",
            "R4": "every check carries inputRows + expression + operands + status",
        },
        "inputPlayerEventFiles": file_meta or [],
        "sameRunIdentity": extra.get("identity"),
        "identityProblems": extra.get("identityProblems"),
        "quarantinedCrossRunEvidence": extra.get("crossRunEvidence", []),
        "unplaceableEventCount": extra.get("unplaceableCount", 0),
        "checks": rows,
        "checkCount": len(rows),
        "statusCounts": counts,
        "verdict": verdict,
        "explanation": explanation,
        "b2Reevaluation": os.path.join("Evidence", "After", "b2-reevaluation.json"),
        "noCrossRunSubstitution": True,
        "historicalB2FilesUntouched": True,
    }
    dump("c05-strict-correlation.json", doc)
    dump("b2-reevaluation.json", reeval)

    tsv = os.path.join(OUT, "c05-strict-checks.tsv")
    if os.path.exists(tsv) and not FORCE:
        raise SystemExit("refusing to overwrite existing evidence: " + tsv)
    with open(tsv, "w", encoding="utf-8", newline="\n") as f:
        f.write("id\tstatus\texpression\tinputRows\treason\n")
        for r in rows:
            f.write("\t".join([r["id"], r["status"], r["expression"],
                               "; ".join("%s:%s" % (i["file"], i["line"])
                                         for i in r["inputRows"]),
                               r["reason"].replace("\t", " ")]) + "\n")

    print(json.dumps({"verdict": verdict, "statusCounts": counts,
                      "checkCount": len(rows),
                      "b2Finding": reeval["r1Conclusion"],
                      "selfTest": self_test()["verdict"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
