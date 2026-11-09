#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CP06-C24-B2-R1 sidecar driver build + injection.

Equivalent to the historical DeliveryCrystalCavernC24B1/Tools/Prepare-Player.ps1
step, but driven by a self-contained Python tool so it does not depend on the
missing PowerShell 7 launcher. It:

  1. Copies the R1 driver source into the isolated observation copy.
  2. Compiles it with the SAME Roslyn compiler and SAME reference list that the
     historical launcher used, against the NEWLY BUILT pure release package.
  3. Registers its Boot method in RuntimeInitializeOnLoads.json and the assembly
     in ScriptingAssemblies.json of the COPY only.
  4. Records compiler identity, arguments, exit code, DLL hash and log hash.

The pure build itself is never modified; the driver is a sidecar in a copy.
All external paths are passed as arguments (absolute Windows paths).
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# Same compiler + host as historical DeliveryCrystalCavernC24B1/Tools/
# Prepare-Player.ps1. Kept as tool defaults so the launcher does not need to
# spell out a compiler binary on its command line.
DEFAULT_COMPILER = (r"C:\Program Files\Unity\Hub\Editor\6000.6.5f1\Editor\Data"
                    r"\DotNetSdk\sdk\8.0.318\Roslyn\bincore\csc.dll")
DEFAULT_DOTNET = r"C:\Program Files\dotnet\dotnet.exe"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--compiler", default=DEFAULT_COMPILER)
    ap.add_argument("--dotnet", default=DEFAULT_DOTNET)
    ap.add_argument("--managed", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--evidence", required=True)
    a = ap.parse_args()

    os.makedirs(a.evidence, exist_ok=True)
    os.makedirs(a.work, exist_ok=True)
    exe_src = os.path.join(a.work, "R1Driver.executed.cs")
    shutil.copyfile(a.source, exe_src)
    dll = os.path.join(a.managed, "CavernValidationDriver.dll")
    log_path = os.path.join(a.evidence, "driver-compile.log")

    names = ["mscorlib", "netstandard", "System", "System.Core", "Assembly-CSharp",
             "UnityEngine.CoreModule", "UnityEngine.PhysicsModule",
             "UnityEngine.ScreenCaptureModule", "UnityEngine.ImageConversionModule",
             "UnityEngine.AIModule", "Unity.InputSystem", "UnityEngine.ScriptingModule",
             "UnityEngine.JSONSerializeModule",
             # R1-02: the bow natural-release mode presses the product's own skill
             # slot Button (WeaponSkillPanel) and feeds KeyboardState events.
             "UnityEngine.UI", "UnityEngine.UIModule", "UnityEngine.TextRenderingModule"]
    refs = ["-r:" + os.path.join(a.managed, n + ".dll") for n in names]
    for r in refs:
        p = r[3:]
        if not os.path.isfile(p):
            raise SystemExit("missing reference: " + p)
    # -deterministic: 同一份源码 + 同一套引用必须产出逐字节相同的 DLL，
    # 否则"三条 Run 用同一版驱动"就只剩口头承诺（PE 时间戳与 MVID 会随机变）。
    args = [a.compiler, "-nologo", "-target:library", "-nostdlib+", "-deterministic",
            "-out:" + dll] + refs + [exe_src]
    proc = subprocess.run([a.dotnet] + args, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                          errors="replace")
    with open(log_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("$ dotnet " + " ".join(args) + "\n\n" + (proc.stdout or "") + "\n")
    if proc.returncode != 0 or not os.path.isfile(dll):
        raise SystemExit("driver compile failed, exit=%d, log=%s" % (proc.returncode, log_path))

    # --- inject into the COPY only ---
    init_path = os.path.join(a.data, "RuntimeInitializeOnLoads.json")
    asm_path = os.path.join(a.data, "ScriptingAssemblies.json")
    init_before, asm_before = sha(init_path), sha(asm_path)
    init = json.load(open(init_path, encoding="utf-8"))
    entry = {"assemblyName": "CavernValidationDriver", "nameSpace": "CavernValidation",
             "className": "Driver", "methodName": "Boot", "loadTypes": 0,
             "isUnityClass": False}
    if any(e == entry for e in init["root"]):
        raise SystemExit("driver already registered; refusing double injection")
    init["root"].append(entry)
    with open(init_path, "w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(init, ensure_ascii=False, separators=(",", ":")))

    asm = json.load(open(asm_path, encoding="utf-8"))
    if "CavernValidationDriver.dll" in asm["names"]:
        raise SystemExit("driver assembly already listed; refusing double injection")
    asm["names"].append("CavernValidationDriver.dll")
    asm["types"].append(16)
    with open(asm_path, "w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(asm, ensure_ascii=False, separators=(",", ":")))

    receipt = {
        "scope": "CP06-C24-B2-R1 sidecar observation driver build + injection",
        "tier": "build-tooling record; NOT a Player run",
        "compiler": a.compiler,
        "compilerSHA256": sha(a.compiler),
        "dotnet": a.dotnet,
        "source": os.path.relpath(a.source, a.evidence).replace("\\", "/"),
        "sourceSHA256": sha(a.source),
        "executedSource": exe_src,
        "executedSourceSHA256": sha(exe_src),
        "arguments": args,
        "compileExitCode": proc.returncode,
        "compileLog": os.path.relpath(log_path, a.evidence).replace("\\", "/"),
        "compileLogSHA256": sha(log_path),
        "driverDll": dll,
        "driverDllSHA256": sha(dll),
        "driverDllBytes": os.path.getsize(dll),
        "references": names,
        "injection": {
            "copyOnly": True,
            "runtimeInitializeOnLoadsBefore": init_before,
            "runtimeInitializeOnLoadsAfter": sha(init_path),
            "scriptingAssembliesBefore": asm_before,
            "scriptingAssembliesAfter": sha(asm_path),
            "entry": entry,
            "rootEntriesAfter": len(init["root"]),
            "assembliesAfter": len(asm["names"]),
        },
        "note": "The pure release build (PureBuild2) contains ZERO validation Boot "
                "entries; this driver is added only to the isolated observation copy.",
        "verdict": "DRIVER_INJECTED",
    }
    p = os.path.join(a.evidence, "driver-injection.json")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(receipt, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({"verdict": receipt["verdict"],
                      "compileExitCode": proc.returncode,
                      "driverDllSHA256": receipt["driverDllSHA256"],
                      "rootEntriesAfter": len(init["root"]),
                      "validationBootEntries": sum(
                          1 for e in init["root"] if "Validation" in str(e) or "B1Route" in str(e))},
                     indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
