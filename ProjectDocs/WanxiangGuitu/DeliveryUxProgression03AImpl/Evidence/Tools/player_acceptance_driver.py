#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UX-PROGRESSION-03A Batch D — real-Player acceptance orchestrator.

WHAT THIS DOES
  Drives the >=25 required real-Player acceptance runs. It:
    1. Builds a standalone WanxiangGuitu.exe (Unity batchmode, -nographics).
    2. Runs the built exe N times; each run loads the acceptance scene which uses
       InputSystem.QueueStateEvent to inject Skill input (NEVER Input.GetKey / Editor).
    3. Parses the per-run acceptance_results.json emitted by
       player_acceptance_harness.cs and rolls them up into PLAYER_RUN_MATRIX.csv.

WHY A BUILT EXE (not Editor / not unit test / not the model)
  The implementation task §7 mandates real WanxiangGuitu.exe runs with injected input.
  Editor play-mode, unit tests and the offline balance model are explicitly NOT
  substitutes for the PASS-PLAYER gate.

HOW TO RUN (in the user's environment)
  python player_acceptance_driver.py \
      --unity "C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe" \
      --project "I:/unity/WanxiangGuitu" \
      --out     "ProjectDocs/WanxiangGuitu/DeliveryUxProgression03AImpl/Evidence" \
      --runs 25

NOTE
  This file is documentation + a ready-to-run harness. In the agent session that
  produced this delivery it was NOT executed (building+running 25 standalone builds
  is out of band); PLAYER_RUN_MATRIX.csv therefore ships with status=NOT_RUN and this
  script is the exact procedure to flip those rows to PASS-PLAYER / FAIL.
"""

import argparse, json, os, shutil, subprocess, sys, glob, datetime


def build_exe(unity, project, out):
    build_dir = os.path.join(out, "Build")
    os.makedirs(build_dir, exist_ok=True)
    log = os.path.join(out, "build_exe.log")
    cmd = [unity, "-batchmode", "-nographics", "-projectPath", project,
           "-buildWindowsPlayer", os.path.join(build_dir, "WanxiangGuitu.exe"),
           "-logFile", log, "-quit"]
    print("[driver] building standalone player ->", build_dir)
    rc = subprocess.call(cmd)
    if rc != 0:
        raise SystemExit("[driver] build failed rc=%d (see %s)" % (rc, log))
    return os.path.join(build_dir, "WanxiangGuitu.exe")


def run_once(exe, out, index, seed):
    results_json = os.path.join(os.path.expanduser("~"), "AppData", "LocalLow",
                                "WanxiangGuitu", "acceptance_results.json")
    if os.path.exists(results_json):
        os.remove(results_json)
    # pass a seed + which skill-set to exercise via command-line args the game reads
    subprocess.call([exe, "-acceptance", str(seed), "-batchmode", "-nographics"])
    if not os.path.exists(results_json):
        return [{"skill": "RUN_%d" % index, "pass": False,
                 "detail": "no acceptance_results.json produced"}]
    with open(results_json, encoding="utf-8") as fp:
        data = json.load(fp)
    return [dict(r) for r in data.get("items", [])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--unity", required=True)
    ap.add_argument("--project", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--runs", type=int, default=25)
    a = ap.parse_args()

    exe = build_exe(a.unity, a.project, a.out)
    rows = []
    for i in range(1, a.runs + 1):
        seed = 1000 + i
        items = run_once(exe, a.out, i, seed)
        for it in items:
            rows.append((i, it.get("skill", "?"), "PASS-PLAYER" if it.get("pass") else "FAIL",
                         it.get("detail", ""), seed))
    # write PLAYER_RUN_MATRIX.csv
    matrix = os.path.join(a.out, "PLAYER_RUN_MATRIX.csv")
    with open(matrix, "w", encoding="utf-8", newline="") as fp:
        fp.write("run_id,skill,status,observation,seed\n")
        for r in rows:
            fp.write("%d,%s,%s,%s,%d\n" % r)
    passed = sum(1 for r in rows if r[2] == "PASS-PLAYER")
    print("[driver] wrote %s : %d entries, %d PASS-PLAYER / %d FAIL" %
          (matrix, len(rows), passed, len(rows) - passed))


if __name__ == "__main__":
    main()
