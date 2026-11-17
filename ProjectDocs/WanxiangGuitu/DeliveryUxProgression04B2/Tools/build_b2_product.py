#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UX-04-B2 deterministic PRODUCT rebuild (isolated COPY only).

Compiles the FULL product source set from Unity's own Bee response file with
Roslyn, adding the four B2 source files and the UX_ACCEPTANCE define (matching
the Acceptance build's 149 defines / 336 references). The resulting
Assembly-CSharp.dll is written into an isolated COPY of the Acceptance Player.

Why this route: the Unity batchmode build chain toggles Standalone scripting
define symbols, which writes ProjectSettings.asset. B2 explicitly protects
ProjectSettings, scenes and prefabs. This compile touches NONE of them --
only the isolated copy under Builds/ux04b2/player (gitignored).

NEVER modifies product source, the shipped Acceptance build, user saves,
drop rates, crafting costs, quality values or the random stream.
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
DEFAULT_RSP = "Library/Bee/artifacts/1900b0aE.dag/Assembly-CSharp.rsp"

B2_SOURCES = [
    "Assets/CombatPrototype/B2AttackModel.cs",
    "Assets/CombatPrototype/B2InventoryQuery.cs",
    "Assets/CombatPrototype/B2Collection.cs",
]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=r"I:\unity\WanxiangGuitu")
    ap.add_argument("--rsp", default=DEFAULT_RSP)
    ap.add_argument("--compiler", default=DEFAULT_COMPILER)
    ap.add_argument("--dotnet", default=DEFAULT_DOTNET)
    ap.add_argument("--source-build", default="Builds/WanxiangGuitu.Acceptance")
    ap.add_argument("--copy", default="Builds/ux04b2/player")
    ap.add_argument("--work", default="Evidence/Runs04B2/_build")
    ap.add_argument("--evidence", default="Evidence/Runs04B2/_build/receipt")
    a = ap.parse_args()

    os.chdir(a.project)
    os.makedirs(a.work, exist_ok=True)
    os.makedirs(a.evidence, exist_ok=True)
    os.makedirs(a.copy, exist_ok=True)

    lines = open(a.rsp, encoding="utf-8").read().splitlines()
    out_dll = os.path.abspath(os.path.join(a.work, "Assembly-CSharp.dll"))
    out_ref = os.path.abspath(os.path.join(a.work, "Assembly-CSharp.ref.dll"))

    new_lines = []
    defines = 0
    for ln in lines:
        s = ln.strip()
        if s.startswith("-out:") or s.startswith("-refout:"):
            continue
        new_lines.append(ln)
        if s.startswith("-define:"):
            defines += 1
    new_lines.insert(0, "-target:library")
    new_lines.insert(1, '-out:"%s"' % out_dll)
    new_lines.insert(2, '-refout:"%s"' % out_ref.replace("\\", "/"))
    # The Acceptance Player was built with this define; the persisted rsp has
    # it removed by AcceptanceBuild.ResetDefine(). Restore it for parity.
    new_lines.insert(3 + defines, "-define:UX_ACCEPTANCE")

    # Append B2 sources just after the last source entry, before trailing flags.
    last_src = max(i for i, l in enumerate(new_lines) if l.strip().endswith('.cs"'))
    for i, src in enumerate(B2_SOURCES):
        if not os.path.isfile(src):
            raise SystemExit("missing B2 source: " + src)
        new_lines.insert(last_src + 1 + i, '"%s"' % src)

    exe_rsp = os.path.join(a.work, "b2-product.rsp")
    with open(exe_rsp, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(new_lines) + "\n")

    # -nostdlib+ because every framework reference is supplied explicitly.
    args = [a.compiler, "@" + os.path.abspath(exe_rsp), "-nostdlib+", "-nologo"]
    proc = subprocess.run([a.dotnet] + args, cwd=a.project, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                          errors="replace")
    log = os.path.join(a.evidence, "b2-product-compile.log")
    with open(log, "w", encoding="utf-8", newline="\n") as f:
        f.write("$ dotnet " + " ".join(args) + "\n\n" + (proc.stdout or "") + "\n")
    if proc.returncode != 0 or not os.path.isfile(out_dll):
        raise SystemExit("B2 product compile FAILED exit=%d log=%s" % (proc.returncode, log))

    # Copy the shipped build to an isolated location, then replace ONLY the DLL.
    if os.path.isdir(a.copy) and os.listdir(a.copy):
        raise SystemExit("refusing to reuse existing copy: " + a.copy)
    shutil.copytree(a.source_build, a.copy, dirs_exist_ok=True)
    managed = os.path.join(a.copy, "WanxiangGuitu_Data", "Managed")
    original_dll = os.path.join(managed, "Assembly-CSharp.dll")
    original_sha = sha(original_dll)
    shutil.copy2(out_dll, original_dll)
    pdb_src = os.path.join(a.work, "Assembly-CSharp.pdb")
    if os.path.isfile(pdb_src):
        shutil.copy2(pdb_src, os.path.join(managed, "Assembly-CSharp.pdb"))

    receipt = {
        "scope": "UX-04-B2 deterministic full-source product rebuild (isolated copy)",
        "tier": "build-tooling record; NOT a Player run",
        "baselineCommit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=a.project,
                                         capture_output=True, text=True).stdout.strip(),
        "compiler": a.compiler, "compilerSHA256": sha(a.compiler),
        "responseFile": os.path.abspath(exe_rsp), "responseSHA256": sha(exe_rsp),
        "definesInSourceRsp": defines, "definesAfterAddingAcceptance": defines + 1,
        "b2SourcesAdded": B2_SOURCES,
        "b2SourceSHA256": {s: sha(s) for s in B2_SOURCES},
        "productDllSHA256": sha(out_dll), "productDllBytes": os.path.getsize(out_dll),
        "preB2AcceptanceDllSHA256": original_sha,
        "compileExitCode": proc.returncode, "compileLog": log,
        "compileLogSHA256": sha(log),
        "isolatedCopy": a.copy,
        "modified": ["%s/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll" % a.copy],
        "unmodified": ["ProjectSettings", "Packages", "Assets scenes/prefabs",
                       "B1 product sources other than the approved D-02 files"],
        "verdict": "PRODUCT_REBUILT",
    }
    with open(os.path.join(a.evidence, "b2-product-build.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(receipt, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({"verdict": receipt["verdict"],
                      "productDllSHA256": receipt["productDllSHA256"],
                      "productDllBytes": receipt["productDllBytes"],
                      "preB2AcceptanceDllSHA256": original_sha}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
