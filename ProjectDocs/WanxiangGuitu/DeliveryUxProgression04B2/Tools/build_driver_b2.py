#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UX-04-B2 sidecar observation driver build + injection into isolated COPY.

Compiles IntDriverB2.cs against the B2 product DLL (the isolated copy) using
the same deterministic Roslyn reference set as the B1 tool chain, then registers
Boot in RuntimeInitializeOnLoads.json and the assembly in ScriptingAssemblies.json
of the COPY ONLY. Never touches product source or the shipped build.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess

DEFAULT_COMPILER = (r"C:\Program Files\Unity\Hub\Editor\6000.6.5f1\Editor\Data"
                    r"\DotNetSdk\sdk\8.0.318\Roslyn\bincore\csc.dll")
DEFAULT_DOTNET = r"C:\Program Files\dotnet\dotnet.exe"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--compiler", default=DEFAULT_COMPILER)
    ap.add_argument("--dotnet", default=DEFAULT_DOTNET)
    ap.add_argument("--managed", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--replace", action="store_true",
                    help="recompile the driver DLL in place (registration already present)")
    ap.add_argument("--tag", default="", help="receipt suffix so evidence is never overwritten")
    a = ap.parse_args()

    os.makedirs(a.work, exist_ok=True)
    os.makedirs(a.evidence, exist_ok=True)
    suffix = ("-" + a.tag) if a.tag else ""
    exe_src = os.path.join(a.work, "IntDriverB2.executed" + suffix + ".cs")
    shutil.copyfile(a.source, exe_src)
    dll = os.path.join(a.managed, "B2ObservationDriver.dll")
    log_path = os.path.join(a.evidence, "b2-driver-compile" + suffix + ".log")

    names = ["mscorlib", "netstandard", "System", "System.Core", "Assembly-CSharp",
             "UnityEngine.CoreModule", "UnityEngine.PhysicsModule",
             "UnityEngine.ScreenCaptureModule", "UnityEngine.ImageConversionModule",
             "UnityEngine.AIModule", "Unity.InputSystem", "UnityEngine.ScriptingModule",
             "UnityEngine.JSONSerializeModule", "UnityEngine.UI",
             "UnityEngine.UIModule", "UnityEngine.TextRenderingModule"]
    refs = ["-r:" + os.path.join(a.managed, n + ".dll") for n in names]
    for r in refs:
        if not os.path.isfile(r[3:]):
            raise SystemExit("missing reference: " + r[3:])
    args = [a.compiler, "-nologo", "-target:library", "-nostdlib+", "-deterministic",
            "-out:" + dll] + refs + [exe_src]
    proc = subprocess.run([a.dotnet] + args, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                          errors="replace")
    with open(log_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("$ dotnet " + " ".join(args) + "\n\n" + (proc.stdout or "") + "\n")
    if proc.returncode != 0 or not os.path.isfile(dll):
        raise SystemExit("B2 driver compile failed exit=%d log=%s" % (proc.returncode, log_path))

    init_path = os.path.join(a.data, "RuntimeInitializeOnLoads.json")
    asm_path = os.path.join(a.data, "ScriptingAssemblies.json")
    init_before, asm_before = sha(init_path), sha(asm_path)
    entry = {"assemblyName": "B2ObservationDriver", "nameSpace": "B2Observation",
             "className": "Driver", "methodName": "Boot", "loadTypes": 0,
             "isUnityClass": False}
    registration_note = "registered"
    if a.replace:
        # Registration already exists in the isolated copy; only the DLL bytes
        # are replaced. Product DLL and the copy's json files stay untouched.
        init = json.load(open(init_path, encoding="utf-8"))
        asm = json.load(open(asm_path, encoding="utf-8"))
        if not any(e == entry for e in init["root"]) or "B2ObservationDriver.dll" not in asm["names"]:
            raise SystemExit("--replace requires an already registered driver")
        registration_note = "already-registered (DLL replaced only)"
    else:
        init = json.load(open(init_path, encoding="utf-8"))
        if any(e == entry for e in init["root"]):
            raise SystemExit("B2 driver already registered")
        init["root"].append(entry)
        with open(init_path, "w", encoding="utf-8", newline="") as f:
            f.write(json.dumps(init, ensure_ascii=False, separators=(",", ":")))
        asm = json.load(open(asm_path, encoding="utf-8"))
        if "B2ObservationDriver.dll" in asm["names"]:
            raise SystemExit("B2 assembly already listed")
        asm["names"].append("B2ObservationDriver.dll")
        asm["types"].append(16)
        with open(asm_path, "w", encoding="utf-8", newline="") as f:
            f.write(json.dumps(asm, ensure_ascii=False, separators=(",", ":")))

    receipt = {
        "scope": "UX-04-B2 sidecar observation driver build + injection (copy only)",
        "tier": "build-tooling record; NOT a Player run",
        "compiler": a.compiler, "compilerSHA256": sha(a.compiler),
        "source": os.path.abspath(a.source), "sourceSHA256": sha(a.source),
        "executedSource": exe_src, "executedSourceSHA256": sha(exe_src),
        "compileExitCode": proc.returncode, "compileLog": log_path,
        "compileLogSHA256": sha(log_path),
        "productDllSHA256": sha(os.path.join(a.managed, "Assembly-CSharp.dll")),
        "driverDll": dll, "driverDllSHA256": sha(dll),
        "driverDllBytes": os.path.getsize(dll), "references": names,
        "injection": {"copyOnly": True, "entry": entry, "registration": registration_note,
                      "runtimeInitializeOnLoadsBefore": init_before,
                      "runtimeInitializeOnLoadsAfter": sha(init_path),
                      "scriptingAssembliesBefore": asm_before,
                      "scriptingAssembliesAfter": sha(asm_path)},
        "verdict": "DRIVER_INJECTED" if not a.replace else "DRIVER_REPLACED",
    }
    with open(os.path.join(a.evidence, "b2-driver-injection" + suffix + ".json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(receipt, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({"verdict": receipt["verdict"], "compileExitCode": proc.returncode,
                      "driverDllSHA256": receipt["driverDllSHA256"],
                      "driverDllBytes": receipt["driverDllBytes"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
