#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build CHALLENGE_CLOSURE_MATRIX.csv from the archived artefacts of the three
P1C Challenge runs.

Every cell is copied out of assertions.tsv / run-summary.json / int-events.jsonl.
Nothing is inferred: a missing verdict stays MISSING and the row is still written.
"""
import csv
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYER = os.path.join(ROOT, "Player")
OUT = os.path.join(os.path.dirname(ROOT), "CHALLENGE_CLOSURE_MATRIX.csv")

RUNS = [
    ("forest", "p1c-forest-challenge", "forest.challenge"),
    ("ruins", "p1c-ruins-challenge", "ruins.challenge"),
    ("cavern", "p1c-cavern-challenge", "cavern.challenge"),
]

FIELDS = ["region", "card_id", "run_dir", "verdict", "exit_code", "complete_txt",
          "run_id", "target_entity", "target_max_hp", "killed", "hits", "hero_min_hp",
          "hero_end_hp", "max_hp", "dodges", "attack_presses", "heals", "level_choices",
          "max_frame_step", "frame_dt", "speed_mps", "walk_target", "objective_met",
          "achieved_before_extract", "outcome", "settlement_snapshot", "achieved",
          "badge", "next_steps_count", "build_sha", "driver_sha"]


def read_assertions(path):
    rows = {}
    if not os.path.isfile(path):
        return rows
    with io.open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2 or parts[0] == "title":
                continue
            rows[parts[0]] = (parts[1], parts[2] if len(parts) > 2 else "")
    return rows


def grab(pattern, text, default=""):
    m = re.search(pattern, text or "")
    return m.group(1) if m else default


def read_target_event(path):
    """The driver emits one 'target' event per run with entity id and max HP."""
    if not os.path.isfile(path):
        return "", ""
    with io.open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                ev = json.loads(line)
            except Exception:
                continue
            if ev.get("stage") == "target":
                d = ev.get("detail", "")
                return grab(r"entity=([\w:-]+)", d), grab(r"hp=[0-9.]+/([0-9.]+)", d)
    return "", ""


def find(rows, *names):
    """First assertion whose name ends with one of `names` (blocker tags vary)."""
    for name in names:
        for key in rows:
            if key == name or key.endswith("-" + name):
                return key, rows[key]
    return None, ("MISSING", "")


def main():
    out_rows = []
    for region, run_dir, card in RUNS:
        base = os.path.join(PLAYER, run_dir)
        rows = read_assertions(os.path.join(base, "assertions.tsv"))
        summary = {}
        sp = os.path.join(base, "run-summary.json")
        if os.path.isfile(sp):
            with io.open(sp, encoding="utf-8") as f:
                summary = json.load(f)

        k_dead, (v_dead, d_dead) = find(rows, "p1c-fight-enemy-dead")
        # The target may be finished during the approach (blocker loop); that is the
        # same real combat loop, so fall back to the blocker record and say so.
        source = "fight"
        if v_dead == "MISSING" or grab(r"hp=([0-9.]+)", d_dead) not in ("0", "0.0"):
            for key in rows:
                if "-blocker" in key and key.endswith("-enemy-dead") and rows[key][0] == "PASS":
                    v_dead, d_dead, k_dead, source = rows[key][0], rows[key][1], key, "approach"
        k_walk, (v_walk, d_walk) = find(rows, "p1c-walk-target")
        k_met, (v_met, d_met) = find(rows, "p1c-objective-met")
        k_pre, (v_pre, d_pre) = find(rows, "p1c-no-achievement-before-extract")
        k_out, (v_out, d_out) = find(rows, "p1c-outcome")
        k_snap, (v_snap, d_snap) = find(rows, "p1c-settlement-snapshot")
        k_ach, (v_ach, d_ach) = find(rows, "p1c-achieved")
        k_badge, (v_badge, d_badge) = find(rows, "p1c-badge")
        k_next, (v_next, d_next) = find(rows, "p1c-next-steps")
        k_heal, (v_heal, d_heal) = find(rows, "p1c-no-harness-heal")
        k_tp, (v_tp, d_tp) = find(rows, "p1c-no-teleport")
        k_in, (v_in, d_in) = find(rows, "p1c-input-path")
        k_run, (v_run, d_run) = find(rows, "run-id")
        ent, maxhp = read_target_event(os.path.join(base, "int-events.jsonl"))

        out_rows.append({
            "region": region,
            "card_id": card,
            "run_dir": "Evidence/Player/" + run_dir,
            "verdict": summary.get("verdict", "MISSING"),
            "exit_code": summary.get("exitCode", "MISSING"),
            "complete_txt": summary.get("completeTxt", "MISSING"),
            "run_id": d_run if k_run else "MISSING",
            "target_entity": ent or grab(r"entity=([\w:-]+)", d_dead),
            "target_max_hp": maxhp,
            "killed": v_dead + ("(" + source + ")" if source != "fight" else ""),
            "hits": grab(r"hits=(\d+)", d_dead),
            "hero_min_hp": grab(r"minHp=([0-9.]+)", d_heal),
            "hero_end_hp": grab(r"endHp=([0-9.]+)", d_heal),
            "max_hp": grab(r"maxHpEnd=([0-9.]+)", d_heal),
            "dodges": grab(r"dodgePressFrames=(\d+)", d_in),
            "attack_presses": grab(r"attackPressFrames=(\d+)", d_in),
            "heals": grab(r"healEvents=(\d+)", d_heal),
            "level_choices": grab(r"levelChoices=(\d+)", d_heal),
            "max_frame_step": grab(r"maxStep=([0-9.]+)", d_tp),
            "frame_dt": grab(r"dt=([0-9.]+)", d_tp),
            "speed_mps": grab(r"speed=([0-9.]+)", d_tp),
            "walk_target": v_walk + " " + d_walk,
            "objective_met": v_met + " " + d_met,
            "achieved_before_extract": v_pre,
            "outcome": grab(r"outcome=(\w+)", d_out),
            "settlement_snapshot": grab(r"card=([\w.]+)", d_snap),
            "achieved": v_ach + " " + d_ach,
            "badge": d_badge,
            "next_steps_count": len([x for x in d_next.split(" | ") if x.strip()]),
            "build_sha": summary.get("buildSHA256", "MISSING"),
            "driver_sha": summary.get("driverDllSHA256", "MISSING"),
        })

    with io.open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for row in out_rows:
            w.writerow(row)
    print("wrote " + OUT)
    for row in out_rows:
        print("%-7s %-18s %-22s hits=%-3s minHp=%-4s speed=%-6s badge=%s" % (
            row["region"], row["card_id"], row["verdict"], row["hits"],
            row["hero_min_hp"], row["speed_mps"], row["badge"]))


if __name__ == "__main__":
    main()
