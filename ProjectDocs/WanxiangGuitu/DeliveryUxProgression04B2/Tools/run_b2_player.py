#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UX-04-B2 observation Player launcher (read-only, isolated).

Launches the isolated B2 build copy (product DLL rebuilt from source + sidecar
driver injected into that COPY only), gives each Run a FRESH isolated storage
root, and archives every raw artefact.

Discipline inherited from UX-03 R1C/R2b, UX-04-B0 and B1:
  * never reuses a run root, never overwrites an evidence directory
  * identity (exe / product DLL / driver DLL / buildId / PID) from ACTUAL files
  * exit code, PID, UTC start/end, timeout and forced termination recorded verbatim
  * original user save is never written (-wanxiang-storage-root only)
  * verdict PLAYER_RUN_COMPLETED only when exitCode == 0 and no timeout
  * FAILED runs are preserved as-is; never overwritten
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


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
    ap.add_argument("--data", required=True)
    ap.add_argument("--run-root", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--mode", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--timeout", type=float, default=300)
    ap.add_argument("--mode-file", default="b2-mode.txt")
    ap.add_argument("--driver-dll", default="B2ObservationDriver.dll")
    ap.add_argument("--seed-save", default=None)
    a = ap.parse_args()

    root = os.path.abspath(a.run_root)
    ev = os.path.abspath(a.evidence)
    if os.path.exists(root):
        raise SystemExit("refusing to reuse run root: " + root)
    if os.path.exists(ev):
        raise SystemExit("refusing to overwrite evidence dir: " + ev)
    os.makedirs(root)
    os.makedirs(ev)

    with open(os.path.join(root, a.mode_file), "w", encoding="utf-8") as f:
        f.write(a.mode)
    if a.seed_save:
        if not os.path.isfile(a.seed_save):
            raise SystemExit("seed-save missing: " + a.seed_save)
        save_dir = os.path.join(root, "WanxiangGuitu", "ForestRuins")
        os.makedirs(save_dir, exist_ok=True)
        shutil.copy2(a.seed_save, os.path.join(save_dir, "save.json"))
        with open(os.path.join(root, "seed-save.json"), "w", encoding="utf-8") as f:
            f.write(sha(a.seed_save))

    exe_sha = sha(a.exe)
    product_dll = os.path.join(a.managed, "Assembly-CSharp.dll")
    build_sha = sha(product_dll)
    drv_path = os.path.join(a.managed, a.driver_dll)
    drv_sha = sha(drv_path) if os.path.isfile(drv_path) else None
    init_sha = sha(os.path.join(a.data, "RuntimeInitializeOnLoads.json"))
    asm_sha = sha(os.path.join(a.data, "ScriptingAssemblies.json"))
    build_id = "ux04b2-%s-%s-%s" % (build_sha[:8], exe_sha[:8], (drv_sha or "")[:8])

    player_log = os.path.join(root, "Player.log")
    args = ["-logFile", player_log, "-screen-width", "1280", "-screen-height", "720",
            "-screen-fullscreen", "0", "-force-d3d12",
            "-wanxiang-storage-root", root]
    env = dict(os.environ)
    env["UNITY_TEST_ROOT"] = root

    dump(os.path.join(root, "Player.command.json"), {
        "scope": "UX-04-B2 observation Player launch",
        "mode": a.mode, "runId": a.run_id, "startUtc": utc(),
        "buildId": build_id,
        "exe": os.path.abspath(a.exe), "exeSHA256": exe_sha,
        "productDllSHA256": build_sha, "driverDllSHA256": drv_sha,
        "runtimeInitializeOnLoadsSHA256": init_sha,
        "scriptingAssembliesSHA256": asm_sha,
        "storageRoot": root, "arguments": args,
        "env": {"UNITY_TEST_ROOT": root},
        "originalSaveTouched": False,
        "productSourceModified": False,
    })

    stdout = open(os.path.join(root, "Player.stdout"), "w", encoding="utf-8", errors="replace")
    stderr = open(os.path.join(root, "Player.stderr"), "w", encoding="utf-8", errors="replace")
    start = utc()
    timed_out = False
    forced = False
    proc = subprocess.Popen([a.exe] + args, cwd=os.path.dirname(a.exe),
                            env=env, stdout=stdout, stderr=stderr)
    pid = proc.pid
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

    for name in sorted(os.listdir(root)):
        src = os.path.join(root, name)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(ev, name))
    save_dir = os.path.join(root, "WanxiangGuitu", "ForestRuins")
    if os.path.isdir(save_dir):
        dest = os.path.join(ev, "isolated-save")
        os.makedirs(dest, exist_ok=True)
        for name in sorted(os.listdir(save_dir)):
            src = os.path.join(save_dir, name)
            if os.path.isfile(src):
                shutil.copy2(src, os.path.join(dest, name))

    files = {}
    for dirpath, _, filenames in os.walk(ev):
        for name in sorted(filenames):
            fp = os.path.join(dirpath, name)
            rel = os.path.relpath(fp, ev).replace("\\", "/")
            files[rel] = {"bytes": os.path.getsize(fp), "sha256": sha(fp)}

    manifest = {
        "scope": "UX-04-B2 observation Player run (sidecar driver, isolated copy)",
        "runId": a.run_id, "mode": a.mode, "buildId": build_id,
        "exeSHA256": exe_sha, "dllSHA256": build_sha, "driverDllSHA256": drv_sha,
        "driverInjected": drv_sha is not None, "seedSave": a.seed_save,
        "runtimeInitializeOnLoadsSHA256": init_sha,
        "scriptingAssembliesSHA256": asm_sha,
        "pid": pid, "exitCode": code, "timedOut": timed_out,
        "forcedTermination": forced,
        "verdict": "PLAYER_RUN_COMPLETED" if (code == 0 and not timed_out) else "PLAYER_RUN_FAILED",
        "startUtc": start, "endUtc": end,
        "runRoot": root, "evidenceDir": ev, "arguments": args,
        "unityVersion": "6000.6.5f1", "files": files,
    }
    dump(os.path.join(ev, "run-manifest.json"), manifest)
    print(json.dumps({k: manifest[k] for k in
                      ["runId", "mode", "buildId", "pid", "exitCode", "verdict",
                       "dllSHA256", "driverDllSHA256"]}, indent=2))
    return 0 if manifest["verdict"] == "PLAYER_RUN_COMPLETED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
