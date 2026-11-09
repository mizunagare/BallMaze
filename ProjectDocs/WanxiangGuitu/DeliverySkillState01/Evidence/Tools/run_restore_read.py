#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SKILL-STATE-01 | NEW-PROCESS restore launcher (C5).

Launches a SECOND, independent Player process against the SAME storage root
that `restore-write` saved into. This is a genuinely new process (new PID, new
driver-owned runId), not an in-process reload. Events are never joined with the
writer run: the writer's raw artefacts are already archived in
Evidence/Player/restore-write-A1/ and are never rewritten here.

Only the two driver INPUT files (cavern-test.txt / ring-case.txt) are replaced
in the shared root. Save files under WanxiangGuitu/ are untouched.
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess


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
    ap.add_argument("--run-root", required=True,
                    help="EXISTING storage root written by restore-write")
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--case", default="restore-read")
    ap.add_argument("--timeout", type=float, default=300)
    ap.add_argument("--unity-version", default="6000.6.5f1")
    a = ap.parse_args()

    root = os.path.abspath(a.run_root)
    ev = os.path.abspath(a.evidence)
    if not os.path.isdir(root):
        raise SystemExit("writer run root does not exist: " + root)
    if os.path.exists(ev):
        raise SystemExit("refusing to overwrite evidence dir: " + ev)
    expect = os.path.join(root, "restore-expect.json")
    if not os.path.isfile(expect):
        raise SystemExit("writer did not produce restore-expect.json: " + expect)
    os.makedirs(ev, exist_ok=False)

    # Preserve a verbatim copy of the writer's expectation in the new evidence.
    shutil.copy2(expect, os.path.join(ev, "restore-expect.from-writer.json"))
    writer_expect_sha = sha(expect)

    # Driver inputs only. The save files are NEVER touched.
    with open(os.path.join(root, "cavern-test.txt"), "w", encoding="utf-8") as f:
        f.write("skill-state")
    with open(os.path.join(root, "ring-case.txt"), "w", encoding="utf-8") as f:
        f.write(a.case)

    exe_sha = sha(a.exe)
    build_sha = sha(os.path.join(a.managed, "Assembly-CSharp.dll"))
    driver = os.path.join(a.managed, "CavernValidationDriver.dll")
    driver_sha = sha(driver) if os.path.isfile(driver) else None

    log = os.path.join(root, "Player.log")
    args = ["-logFile", log, "-screen-width", "1280", "-screen-height", "720",
            "-screen-fullscreen", "0", "-force-d3d12",
            "-wanxiang-storage-root", root]
    start = utc()
    dump(os.path.join(ev, "Player.command.json"), {
        "scope": "SKILL-STATE-01 NEW-PROCESS restore read (standalone, no pwsh)",
        "case": a.case, "startUtc": start, "unityVersion": a.unity_version,
        "exe": a.exe, "exeSHA256": exe_sha, "buildSHA256": build_sha,
        "driverDllSHA256": driver_sha, "storageRoot": root,
        "sharedWithWriterRun": True,
        "writerEvidencePreservedAt": "Evidence/Player/restore-write-A1/",
        "writerExpectationSHA256": writer_expect_sha,
        "arguments": args, "env": {"UNITY_TEST_ROOT": root},
        "newProcess": True, "neverJoinedAcrossRuns": True,
        "saveFilesModifiedByLauncher": False,
        "driverInputFilesReplaced": ["cavern-test.txt", "ring-case.txt"],
    })

    env = dict(os.environ)
    env["UNITY_TEST_ROOT"] = root
    stdout = open(os.path.join(root, "Player.stdout"), "w", encoding="utf-8", errors="replace")
    stderr = open(os.path.join(root, "Player.stderr"), "w", encoding="utf-8", errors="replace")
    timed_out = forced = False
    proc = subprocess.Popen([a.exe] + args, cwd=os.path.dirname(a.exe),
                            env=env, stdout=stdout, stderr=stderr)
    pid = proc.pid
    dump(os.path.join(ev, "process.json"), {
        "scope": "independent restore-read Player process",
        "pid": pid, "startedUtc": start, "writerPidIsDifferent": True,
    })
    try:
        code = proc.wait(timeout=a.timeout)
    except subprocess.TimeoutExpired:
        timed_out = forced = True
        proc.terminate()
        try:
            code = proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            proc.kill(); code = proc.wait()
    finally:
        stdout.close(); stderr.close()
    end = utc()
    dump(os.path.join(ev, "process.json"), {
        "scope": "independent restore-read Player process",
        "pid": pid, "startedUtc": start, "endedUtc": end,
        "timedOut": timed_out, "forcedTermination": forced,
        "exited": True, "exitCode": code, "writerPidIsDifferent": True,
    })
    dump(os.path.join(ev, "Player.exit.json"), {
        "exitObservedUtc": end, "pid": pid, "exitCode": code,
        "forcedTermination": forced, "timedOut": timed_out,
    })
    for name in sorted(os.listdir(root)):
        src = os.path.join(root, name)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(ev, name))

    complete = (open(os.path.join(ev, "complete.txt"), encoding="utf-8").read().strip()
                if os.path.isfile(os.path.join(ev, "complete.txt")) else None)
    summary = {
        "scope": "SKILL-STATE-01 new-process restore read run summary",
        "case": a.case, "runRoot": root, "evidence": ev,
        "pid": pid, "exeSHA256": exe_sha, "buildSHA256": build_sha,
        "driverDllSHA256": driver_sha,
        "exitCode": code, "timedOut": timed_out, "forcedTermination": forced,
        "startUtc": start, "endUtc": end, "completeTxt": complete,
        "failureTxtPresent": os.path.isfile(os.path.join(ev, "failure.txt")),
        "archivedFiles": sorted(os.listdir(ev)),
        "newProcess": True,
        "verdict": "PLAYER_RUN_COMPLETED" if (code == 0 and not timed_out)
                   else "PLAYER_RUN_FAILED",
        "note": "This is a genuinely new process reading the writer's save. "
                "Its events carry a different PID and runId and are NEVER "
                "joined with the writer run's timeline.",
    }
    dump(os.path.join(ev, "run-summary.json"), summary)
    print(json.dumps({k: summary[k] for k in
                      ["case", "pid", "exitCode", "completeTxt", "verdict"]}, indent=2))
    return 0 if summary["verdict"] == "PLAYER_RUN_COMPLETED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
