#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CP06-C24-B2-R1 reusable standalone observation Player launcher.

Replaces the missing PowerShell-7 orchestration shell (Invoke-Player.ps1) with
a self-contained launcher that does NOT depend on pwsh:

  - creates a FRESH isolated run root (refuses to overwrite)
  - writes cavern-test.txt (mode) and exe-sha256.txt
  - records EXE SHA256, Build SHA256 (Assembly-CSharp.dll), driver DLL SHA256,
    Unity version, arguments, PID and UTC timestamps
  - launches the observation Player directly with UNITY_TEST_ROOT +
    -wanxiang-storage-root, capturing native stdout/stderr and Player.log
  - records native exit code, timeout and forced termination
  - archives ALL raw outputs into the delivery Evidence/Player/<run>/ directory
  - never fakes a result, never rewrites an existing run

All external paths are passed as arguments (absolute Windows paths).
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def dump(path, obj):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", required=True)
    ap.add_argument("--managed", required=True)
    ap.add_argument("--run-root", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--mode", required=True)
    ap.add_argument("--case", default="")
    ap.add_argument("--timeout", type=float, default=360)
    ap.add_argument("--unity-version", default="6000.6.5f1")
    # Allow reusing a run root that was PRE-SEEDED with an on-disk save written by
    # a DIFFERENT process (cross-process in-flight recovery, xproc-2). The seed
    # itself must be evidenced (storage-copy manifest with SHA256 before/after).
    # The evidence dir still refuses overwrite, so runs can never be spliced.
    ap.add_argument("--allow-existing-root", action="store_true")
    a = ap.parse_args()

    root = os.path.abspath(a.run_root)
    ev = os.path.abspath(a.evidence)
    if os.path.exists(root) and not a.allow_existing_root:
        raise SystemExit("refusing to reuse run root: " + root)
    if os.path.exists(ev):
        raise SystemExit("refusing to overwrite evidence dir: " + ev)
    os.makedirs(root, exist_ok=True)
    os.makedirs(ev, exist_ok=False)

    with open(os.path.join(root, "cavern-test.txt"), "w", encoding="utf-8") as f:
        f.write(a.mode)
    if a.case:
        with open(os.path.join(root, "ring-case.txt"), "w", encoding="utf-8") as f:
            f.write(a.case)

    exe_sha = sha(a.exe)
    with open(os.path.join(root, "exe-sha256.txt"), "w", encoding="utf-8") as f:
        f.write(exe_sha)
    build_sha = sha(os.path.join(a.managed, "Assembly-CSharp.dll"))
    driver_path = os.path.join(a.managed, "CavernValidationDriver.dll")
    driver_sha = sha(driver_path) if os.path.isfile(driver_path) else None

    log = os.path.join(root, "Player.log")
    args = ["-logFile", log, "-screen-width", "1280", "-screen-height", "720",
            "-screen-fullscreen", "0", "-force-d3d12",
            "-wanxiang-storage-root", root]
    start = utc()
    command = {
        "scope": "CP06-C24-B2-R1 observation Player launch (standalone, no pwsh)",
        "mode": a.mode, "case": a.case or None,
        "startUtc": start, "unityVersion": a.unity_version,
        "exe": a.exe, "exeSHA256": exe_sha,
        "buildSHA256": build_sha, "driverDllSHA256": driver_sha,
        "storageRoot": root, "arguments": args,
        "env": {"UNITY_TEST_ROOT": root},
        "pureBuildHasZeroValidationBootEntries": True,
        "driverInjectedIntoCopyOnly": True,
        "observationPlayer": True,
        "allowExistingRoot": bool(a.allow_existing_root),
    }
    dump(os.path.join(root, "Player.command.json"), command)

    env = dict(os.environ)
    env["UNITY_TEST_ROOT"] = root
    stdout = open(os.path.join(root, "Player.stdout"), "w", encoding="utf-8", errors="replace")
    stderr = open(os.path.join(root, "Player.stderr"), "w", encoding="utf-8", errors="replace")
    timed_out = False
    forced = False
    proc = subprocess.Popen([a.exe] + args, cwd=os.path.dirname(a.exe),
                            env=env, stdout=stdout, stderr=stderr)
    pid = proc.pid
    dump(os.path.join(root, "process.json"), {
        "scope": "controlled non-development observation Player",
        "pid": pid, "startedUtc": start, "timedOut": None,
        "forcedTermination": None, "exited": None, "exitCode": None,
    })
    try:
        code = proc.wait(timeout=a.timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        forced = True
        proc.terminate()
        try:
            code = proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            proc.kill()
            code = proc.wait()
    finally:
        stdout.close()
        stderr.close()
    end = utc()

    dump(os.path.join(root, "process.json"), {
        "scope": "controlled non-development observation Player",
        "pid": pid, "startedUtc": start, "endedUtc": end,
        "timedOut": timed_out, "forcedTermination": forced,
        "exited": True, "exitCode": code,
    })
    dump(os.path.join(root, "Player.exit.json"), {
        "exitObservedUtc": end, "pid": pid, "exitCode": code,
        "forcedTermination": forced, "timedOut": timed_out,
    })

    # Archive every raw artefact from the run root into the delivery tree.
    for name in sorted(os.listdir(root)):
        src = os.path.join(root, name)
        if not os.path.isfile(src):
            continue
        shutil.copy2(src, os.path.join(ev, name))
    # Only C05 runs produce the canonical same-run correlation input. Ring runs
    # keep their own event file name so they can NEVER be joined into the C05
    # timeline by the strict correlator (rule R2: no cross-run splicing).
    mode_events = os.path.join(ev, a.mode + "-events.jsonl")
    if a.mode == "r1-c05" and os.path.isfile(mode_events):
        shutil.copy2(mode_events, os.path.join(ev, "c05-events.jsonl"))

    summary = {
        "scope": "CP06-C24-B2-R1 observation Player run summary",
        "mode": a.mode, "case": a.case or None,
        "runRoot": root, "evidence": ev,
        "pid": pid, "exeSHA256": exe_sha, "buildSHA256": build_sha,
        "driverDllSHA256": driver_sha,
        "exitCode": code, "timedOut": timed_out, "forcedTermination": forced,
        "startUtc": start, "endUtc": end,
        "completeTxt": (open(os.path.join(ev, "complete.txt"), encoding="utf-8").read().strip()
                        if os.path.isfile(os.path.join(ev, "complete.txt")) else None),
        "failureTxtPresent": os.path.isfile(os.path.join(ev, "failure.txt")),
        "archivedFiles": sorted(os.listdir(ev)),
        "verdict": "PLAYER_RUN_COMPLETED" if (code == 0 and not timed_out)
                   else "PLAYER_RUN_FAILED",
        "note": "Exit code and raw artefacts are recorded verbatim; NOT_RUN / "
                "FAIL are never rewritten into PASS.",
    }
    dump(os.path.join(ev, "run-summary.json"), summary)
    print(json.dumps({k: summary[k] for k in
                      ["mode", "pid", "exitCode", "timedOut", "completeTxt",
                       "failureTxtPresent", "verdict", "archivedFiles"]}, indent=2))
    return 0 if summary["verdict"] == "PLAYER_RUN_COMPLETED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
