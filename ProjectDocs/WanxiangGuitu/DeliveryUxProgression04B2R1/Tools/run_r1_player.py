#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UX-04-B2-R1 observation Player launcher (read-only, isolated).

Each Run gets a FRESH isolated storage root and its OWN evidence directory;
existing B2/B1 evidence is never touched. Records buildId, product DLL SHA256,
EXE SHA256, driver DLL SHA256, runId, PID, exitCode, result.json, raw input
events and raw state changes verbatim. FAILED runs are preserved as-is.
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
    ap.add_argument("--mode", required=True, choices=["sort-ugui", "sort-imgui", "collection", "restart", "strength0", "strength3", "preview9", "guid", "golden"])
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--timeout", type=float, default=300)
    ap.add_argument("--guid-manifest", default=None)
    ap.add_argument("--restart-from", default=None, help="prior successful collection run-root; copy its isolated save and seed")
    a = ap.parse_args()
    # Popen changes cwd to the Player folder: normalize paths first.
    a.exe, a.managed, a.data = map(os.path.abspath, (a.exe, a.managed, a.data))

    root = os.path.abspath(a.run_root)
    ev = os.path.abspath(a.evidence)
    if os.path.exists(root):
        raise SystemExit("refusing to reuse run root: " + root)
    if os.path.exists(ev):
        raise SystemExit("refusing to overwrite evidence dir: " + ev)
    restart_receipt = None
    if (a.mode == "restart") != bool(a.restart_from):
        raise SystemExit("restart requires --restart-from; other modes must omit it")
    if a.mode == "guid" and not a.guid_manifest:
        raise SystemExit("guid requires --guid-manifest")
    if a.restart_from:
        prior = os.path.abspath(a.restart_from)
        seed_path = os.path.join(prior, "r1-seed.json")
        prior_save = os.path.join(prior, "WanxiangGuitu", "ForestRuins", "save.json")
        prior_result = json.load(open(os.path.join(prior, "result.json"), encoding="utf-8"))
        if prior_result.get("mode") != "collection" or prior_result.get("result") != "PASS":
            raise SystemExit("restart source must be a successful collection")
        seed = json.load(open(seed_path, encoding="utf-8"))
        if seed.get("sourceRunId") != prior_result.get("runId") or seed.get("sourceRunId") == a.run_id:
            raise SystemExit("restart seed run identity mismatch")
        restart_receipt = {"sourceRunRoot": prior, "sourceRunId": seed["sourceRunId"],
                           "seedSHA256": sha(seed_path), "saveSHA256": sha(prior_save), "copied": {}}
    os.makedirs(root)
    os.makedirs(ev)
    if a.restart_from:
        shutil.copytree(os.path.join(prior, "WanxiangGuitu"), os.path.join(root, "WanxiangGuitu"))
        shutil.copy2(seed_path, os.path.join(root, "r1-seed.json"))
        for directory, _, names in os.walk(os.path.join(root, "WanxiangGuitu")):
            for name in names:
                target = os.path.join(directory, name)
                relative = os.path.relpath(target, root)
                if os.path.islink(target) or sha(target) != sha(os.path.join(prior, relative)):
                    raise SystemExit("restart copy verification failed: " + relative)
                restart_receipt["copied"][relative.replace("\\", "/")] = sha(target)
        dump(os.path.join(root, "r1-restart-input.json"), restart_receipt)
    with open(os.path.join(root, "r1-run-id.txt"), "w", encoding="utf-8") as f:
        f.write(a.run_id)

    with open(os.path.join(root, "r1-mode.txt"), "w", encoding="utf-8") as f:
        f.write(a.mode)
    if a.guid_manifest:
        if not os.path.isfile(a.guid_manifest):
            raise SystemExit("guid manifest missing: " + a.guid_manifest)
        shutil.copy2(a.guid_manifest, os.path.join(root, "r1-guid-manifest.json"))

    exe_sha = sha(a.exe)
    product_dll = os.path.join(a.managed, "Assembly-CSharp.dll")
    build_sha = sha(product_dll)
    drv_path = os.path.join(a.managed, "B2R1ObservationDriver.dll")
    drv_sha = sha(drv_path) if os.path.isfile(drv_path) else None
    init_sha = sha(os.path.join(a.data, "RuntimeInitializeOnLoads.json"))
    asm_sha = sha(os.path.join(a.data, "ScriptingAssemblies.json"))
    build_id = "ux04b2r1-%s-%s-%s" % (build_sha[:8], exe_sha[:8], (drv_sha or "")[:8])

    player_log = os.path.join(root, "Player.log")
    args = ["-logFile", player_log, "-screen-width", "1280", "-screen-height", "720",
            "-screen-fullscreen", "0", "-force-d3d12", "-wanxiang-storage-root", root]
    env = dict(os.environ)
    env["UNITY_TEST_ROOT"] = root

    dump(os.path.join(root, "Player.command.json"), {
        "scope": "UX-04-B2-R1 observation Player launch",
        "mode": a.mode, "runId": a.run_id, "startUtc": utc(), "buildId": build_id,
        "exe": os.path.abspath(a.exe), "exeSHA256": exe_sha,
        "assemblyCSharpDllSHA256": build_sha, "driverDllSHA256": drv_sha,
        "runtimeInitializeOnLoadsSHA256": init_sha,
        "scriptingAssembliesSHA256": asm_sha,
        "storageRoot": root, "arguments": args,
        "env": {"UNITY_TEST_ROOT": root},
        "originalSaveTouched": False, "productSourceModified": False,
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

    complete = "MISSING"
    cp = os.path.join(ev, "r1-complete.txt")
    if os.path.isfile(cp):
        complete = open(cp, encoding="utf-8").read().strip()
    result = None
    rp = os.path.join(ev, "result.json")
    if os.path.isfile(rp):
        try:
            result = json.load(open(rp, encoding="utf-8"))
        except Exception:
            result = None
    result_valid = (isinstance(result, dict) and result.get("runId") == a.run_id and result.get("mode") == a.mode
                    and result.get("result") == "PASS" and result.get("checks", 0) > 0
                    and result.get("failed") == 0 and result.get("passed") == result.get("checks"))
    verdict = "PLAYER_RUN_COMPLETED" if (code == 0 and not timed_out and complete == "PASS" and result_valid) else "PLAYER_RUN_FAILED"

    manifest = {
        "scope": "UX-04-B2-R1 observation Player run (sidecar, isolated copy)",
        "runId": a.run_id, "mode": a.mode, "buildId": build_id,
        "exeSHA256": exe_sha, "dllSHA256": build_sha, "driverDllSHA256": drv_sha,
        "driverInjected": drv_sha is not None,
        "runtimeInitializeOnLoadsSHA256": init_sha,
        "scriptingAssembliesSHA256": asm_sha,
        "pid": pid, "exitCode": code, "timedOut": timed_out,
        "forcedTermination": forced, "completeFlag": complete,
        "resultJson": result, "resultIdentityAndChecksValid": result_valid, "restartInput": restart_receipt,
        "verdict": verdict, "startUtc": start, "endUtc": end,
        "runRoot": root, "evidenceDir": ev, "arguments": args,
        "unityVersion": "6000.6.5f1", "files": files,
    }
    dump(os.path.join(ev, "run-manifest.json"), manifest)
    print(json.dumps({k: manifest[k] for k in
                      ["runId", "mode", "buildId", "pid", "exitCode", "completeFlag", "verdict"]}, indent=2))
    return 0 if verdict == "PLAYER_RUN_COMPLETED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
