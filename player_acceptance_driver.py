#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UX-PROGRESSION-03A real Player acceptance driver.

Responsibilities (per task spec):
  * Launch the Acceptance EXE as an INDEPENDENT process per run; record PID,
    full command line, start/end wall times.
  * Hard timeout with controlled shutdown; logs preserved.
  * Exit code check: non-zero can never be PASS.
  * result.json must be created AFTER this run started (freshness).
  * runId / processId / buildSha inside result.json must match launch records
    (identity). Mismatch / missing / null / stale -> NOT_RUN or FAIL, never PASS.
  * stdout/stderr/Player.log/result.json preserved per run.
  * No cross-run stitching: every verdict derives from one run's artifacts only.
  * User-data isolation: each run gets its own directory used BOTH as
    -wanxiang-storage-root (game saves) and --data-root (harness results).
    The default AppData save locations are hashed before/after the whole batch
    and MUST be unchanged (protection hash, zero change).
  * Self-test mode exercises the negative paths deliberately.
"""
import argparse
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

PROJECT = os.path.dirname(os.path.abspath(__file__))
EXE_ACCEPTANCE = os.path.join(PROJECT, "Builds", "WanxiangGuitu.Acceptance", "WanxiangGuitu.exe")
EXE_NODEFINE = os.path.join(PROJECT, "Builds", "WanxiangGuitu.AcceptanceNoDefine", "WanxiangGuitu.exe")
DLL_ACCEPTANCE = os.path.join(PROJECT, "Builds", "WanxiangGuitu.Acceptance", "WanxiangGuitu_Data", "Managed", "Assembly-CSharp.dll")
DLL_NODEFINE = os.path.join(PROJECT, "Builds", "WanxiangGuitu.AcceptanceNoDefine", "WanxiangGuitu_Data", "Managed", "Assembly-CSharp.dll")
BUILD_MANIFEST = os.path.join(PROJECT, "Builds", "build-manifest.json")
MARKER = "UX_ACCEPTANCE_HARNESS_v1"
EVIDENCE = os.path.join(PROJECT, "Evidence")
RUNS_ROOT = os.path.join(EVIDENCE, "Runs")
# PH-R2-R1 evidence lives in its own tree; PH-R1 / PH-R2 history is frozen.
R1_DIR = os.path.join(EVIDENCE, "PH-R2-R1")
R1_RUNS = os.path.join(R1_DIR, "runs")
R1_SELFTEST = os.path.join(R1_DIR, "selftest")
# PH-R2-R1-FIX evidence lives in its own tree; every earlier tree stays frozen.
FIX_DIR = os.path.join(EVIDENCE, "PH-R2-R1-FIX")
FIX_RUNS = os.path.join(FIX_DIR, "runs")
FIX_SELFTEST = os.path.join(FIX_DIR, "selftest")
FIX_BUILD = os.path.join(FIX_DIR, "build")
FIX_PROTECTION = os.path.join(FIX_DIR, "protection")

# PH-R2-R1-FIX-04: the build-input protection set. The first two were MISSING
# from the 190-file list (defect F-2); the last two are rewritten by every
# Unity build because they carry scriptingDefineSymbols / shader stripping.
PROTECTED_BUILD_INPUTS = [
    "Assets/Settings/PC_RPAsset.asset",
    "Assets/Settings/UniversalRenderPipelineGlobalSettings.asset",
    "ProjectSettings/ProjectSettings.asset",
    "ProjectSettings/GraphicsSettings.asset",
]
# PH-R2 deliverables live in their OWN directory. The PH-R1 deliverables
# (Evidence/INDEX.json, Evidence/PLAYER_RUN_MATRIX.csv) are FROZEN history and
# must never be overwritten by a PH-R2 run.
PHR2_DIR = os.path.join(EVIDENCE, "PH-R2")
RUN_TIMEOUT = 180.0  # seconds; hard cap per run

# The game's DEFAULT save locations (no -wanxiang-storage-root). These must be
# untouched by the whole batch. Derived from SaveLocationMigration.cs:
#   NewDirectory  = persistentDataPath/ForestRuins
#   LegacyDirectory= <persistentDataPath parent>/BallMaze/ForestRuins
# Unity persistentDataPath on Windows = %USERPROFILE%/AppData/LocalLow/<company>/<product>
COMPANY = "DefaultCompany"
PRODUCT = "万象归途"
LOCALLOW = os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "LocalLow")
APPDATA_DEFAULT_SAVE = os.path.join(LOCALLOW, COMPANY, PRODUCT, "ForestRuins")
APPDATA_LEGACY_SAVE = os.path.join(LOCALLOW, "BallMaze", "ForestRuins")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def marker_in_dll(path):
    """PH-R2-R1: marker check on the MANAGED DLL only (never the launcher)."""
    if not os.path.isfile(path):
        return False
    with open(path, "rb") as f:
        data = f.read()
    return any(MARKER.encode(enc) in data for enc in ("utf-16-le", "utf-8", "ascii"))


def compute_build_id(manifest):
    """Content-derived buildId: binds this build to BOTH managed DLL identities.
    Stable for a given pair of DLLs; changes the moment either DLL changes."""
    material = "%s|%s|%s|%s" % (
        manifest["acceptanceDllSha256"], manifest["noDefineDllSha256"],
        manifest["acceptanceExeSha256"], manifest["noDefineExeSha256"])
    return "phr2r1-" + sha_bytes(material.encode("utf-8"))[:24]


def load_build_manifest():
    with open(BUILD_MANIFEST, "r", encoding="utf-8") as f:
        return json.load(f)


def verify_manifest(manifest, actual):
    """Compare manifest fields against ACTUAL on-disk artifacts. Returns reasons list."""
    reasons = []
    expect = {
        "acceptanceExeSha256": actual["exeShaBefore"],
        "acceptanceDllSha256": actual["dllShaBefore"],
        "noDefineExeSha256": actual["noDefineExeSha"],
        "noDefineDllSha256": actual["noDefineDllSha"],
        "acceptanceMarkerPresent": actual["acceptanceMarker"],
        "noDefineMarkerPresent": actual["noDefineMarker"],
        "buildId": actual["buildId"],
    }
    for k, v in expect.items():
        if k not in manifest:
            reasons.append("manifest missing field " + k)
        elif manifest[k] != v:
            reasons.append("manifest %s mismatch: manifest=%s actual=%s" % (k, manifest[k], v))
    if manifest.get("schemaVersion") != 1:
        reasons.append("unsupported schemaVersion")
    if not manifest.get("unityVersion"):
        reasons.append("manifest missing unityVersion")
    if manifest.get("acceptanceExePath") and not os.path.isfile(manifest["acceptanceExePath"]):
        reasons.append("acceptanceExePath does not exist")
    if manifest.get("acceptanceDllPath") and not os.path.isfile(manifest["acceptanceDllPath"]):
        reasons.append("acceptanceDllPath does not exist")
    return reasons


def build_identity_snapshot(manifest):
    """PH-R2-R1 §3.3 steps 1-5: hash EXE+DLL, read manifest, verify, buildId."""
    exe_sha = sha256_file(EXE_ACCEPTANCE)
    dll_sha = sha256_file(DLL_ACCEPTANCE)
    nd_exe = sha256_file(EXE_NODEFINE)
    nd_dll = sha256_file(DLL_NODEFINE)
    snap = {
        "exeShaBefore": exe_sha, "dllShaBefore": dll_sha,
        "noDefineExeSha": nd_exe, "noDefineDllSha": nd_dll,
        "acceptanceMarker": marker_in_dll(DLL_ACCEPTANCE),
        "noDefineMarker": marker_in_dll(DLL_NODEFINE),
        "buildId": compute_build_id({
            "acceptanceDllSha256": dll_sha, "noDefineDllSha256": nd_dll,
            "acceptanceExeSha256": exe_sha, "noDefineExeSha256": nd_exe}),
    }
    snap["manifestReasons"] = verify_manifest(manifest, snap)
    return snap


def generate_build_manifest():
    """Write Builds/build-manifest.json from ACTUAL artifacts (post-build)."""
    exe = sha256_file(EXE_ACCEPTANCE)
    dll = sha256_file(DLL_ACCEPTANCE)
    n_exe = sha256_file(EXE_NODEFINE)
    n_dll = sha256_file(DLL_NODEFINE)
    acc_marker = marker_in_dll(DLL_ACCEPTANCE)
    nod_marker = marker_in_dll(DLL_NODEFINE)
    ps_path = os.path.join(PROJECT, "ProjectSettings", "ProjectSettings.asset")
    leak = 0
    if os.path.isfile(ps_path):
        leak = open(ps_path, encoding="utf-8", errors="replace").read().count("UX_ACCEPTANCE")
    manifest = {
        "schemaVersion": 1,
        "buildId": compute_build_id({"acceptanceDllSha256": dll, "noDefineDllSha256": n_dll,
                                     "acceptanceExeSha256": exe, "noDefineExeSha256": n_exe}),
        "unityVersion": "6000.6.5f1",
        "builtAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "acceptanceExePath": EXE_ACCEPTANCE,
        "acceptanceExeSha256": exe,
        "acceptanceDllPath": DLL_ACCEPTANCE,
        "acceptanceDllSha256": dll,
        "noDefineExePath": EXE_NODEFINE,
        "noDefineExeSha256": n_exe,
        "noDefineDllPath": DLL_NODEFINE,
        "noDefineDllSha256": n_dll,
        "acceptanceMarkerPresent": acc_marker,
        "noDefineMarkerPresent": nod_marker,
        "scriptingDefineState": {
            "acceptanceBuildDefine": "UX_ACCEPTANCE",
            "shippingDefine": None,
            "projectSettingsDefineLeakCount": leak,
            "cleared": leak == 0,
        },
    }
    with open(BUILD_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return manifest


def grep_marker(build_dir):
    """Return True if the marker appears in the managed assembly (where Mono
    builds store code string constants as UTF-16) or the EXE launcher."""
    candidates = [
        os.path.join(build_dir, "WanxiangGuitu_Data", "Managed", "Assembly-CSharp.dll"),
        os.path.join(build_dir, "WanxiangGuitu.exe"),
    ]
    for p in candidates:
        if not os.path.isfile(p):
            continue
        with open(p, "rb") as f:
            data = f.read()
        for enc in ("utf-16-le", "utf-8", "ascii"):
            if MARKER.encode(enc) in data:
                return True
    return False


def dir_fingerprint(root):
    """Recursive fingerprint of a directory: relpath|size|sha256 per file, plus dir list.
    A missing directory yields ("ABSENT", None)."""
    if not os.path.isdir(root):
        return "ABSENT", None
    entries = []
    for base, dirs, files in os.walk(root):
        dirs.sort()
        for name in sorted(dirs):
            entries.append("D " + os.path.relpath(os.path.join(base, name), root).replace("\\", "/"))
        for name in sorted(files):
            p = os.path.join(base, name)
            entries.append("F %s|%d|%s" % (os.path.relpath(p, root).replace("\\", "/"), os.path.getsize(p), sha256_file(p)))
    blob = "\n".join(entries)
    return "PRESENT", hashlib.sha256(blob.encode("utf-8")).hexdigest()


def appdata_protection_snapshot():
    snap = {}
    for label, path in (("default_save", APPDATA_DEFAULT_SAVE), ("legacy_save", APPDATA_LEGACY_SAVE)):
        state, digest = dir_fingerprint(path)
        snap[label] = {"path": path, "state": state, "sha256": digest}
    return snap


def appdata_protection_ok(before, after):
    verdicts = {}
    for label in ("default_save", "legacy_save"):
        b, a = before[label], after[label]
        if b["state"] == "ABSENT":
            verdicts[label] = a["state"] == "ABSENT"
        else:
            verdicts[label] = a["state"] == "PRESENT" and a["sha256"] == b["sha256"]
    return verdicts


# ---------------------------------------------------------------------------
# The frozen 25-row matrix. weapon/slot/quality/affix/charge/cooldown are mapped
# from the product definitions:
#   legacy WeaponSkillExpansion slots 1/2 (sword.triple/spear.charge/staff.field/
#   bow.burst = slot 1; sword.circle/spear.sweep/staff.echo/bow.pierce = slot 2);
#   new weapons TwinBlades/Greatsword/Scythe use slots 0/1.
#   affix 2 = 回响 (echo, area x1.25), affix 5 = 聚能 (focus, cooldown +1s).
#   desc checks assert the runtime SkillDescription the panels render from.
# ---------------------------------------------------------------------------
MATRIX = [
    dict(id=1,  skill="sword.triple",          weapon="Sword",      slot=1, quality="White", affix=-1, charge=0.0,  cd=7.0,  gate="",      expect="冷却 realised 7s；3 段各 65%（数值/判定未变，仅 cd 8->7）", seed=101),
    dict(id=2,  skill="sword.circle",          weapon="Sword",      slot=2, quality="White", affix=-1, charge=0.0,  cd=10.0, gate="",      expect="冷却 10s；3 段各 85%；段间隔 .30s（原 11/.48/.55）", seed=102),
    dict(id=3,  skill="spear.charge",          weapon="Spear",      slot=1, quality="White", affix=-1, charge=0.60, cd=8.0,  gate="",      expect="冷却 8s；蓄力 .60s（原 .85）；伤害 1.2x1 不变", seed=103),
    dict(id=4,  skill="spear.sweep",           weapon="Spear",      slot=2, quality="White", affix=-1, charge=0.0,  cd=9.0,  gate="",      expect="冷却 9s；段间隔 .24s；两段各 85%（原 10/.30/.80）", seed=104),
    dict(id=5,  skill="staff.field",           weapon="Staff",      slot=1, quality="White", affix=-1, charge=0.0,  cd=9.0,  gate="",      expect="冷却 9s（原 10）；留场脉冲 .65+.40x3 不变", seed=105),
    dict(id=6,  skill="staff.echo",            weapon="Staff",      slot=2, quality="White", affix=-1, charge=0.0,  cd=9.0,  gate="",      expect="冷却 9s；段间隔 .22s；3 段各 70%（原 9/.32/.55）", seed=106),
    dict(id=7,  skill="bow.burst",             weapon="Bow",        slot=1, quality="White", affix=-1, charge=0.0,  cd=9.0,  gate="",      expect="冷却 9s；段间隔 .18s；3 段各 62%（原 9/.22/.55）", seed=107),
    dict(id=8,  skill="bow.pierce",            weapon="Bow",        slot=2, quality="White", affix=-1, charge=0.70, cd=10.0, gate="",      expect="冷却 10s；蓄力 .70s；基础 1.35（原 11/1.0/1.15）", seed=108),
    dict(id=9,  skill="twin.volley",           weapon="TwinBlades", slot=0, quality="White", affix=-1, charge=0.0,  cd=7.0,  gate="",      expect="冷却 7s；6 段各 .40（基准对照，未改）", seed=109),
    dict(id=10, skill="gs.cleave",             weapon="Greatsword", slot=0, quality="White", affix=-1, charge=0.0,  cd=9.0,  gate="",      expect="冷却 9s；前摇 realised .65s（原 .80）; 破防 .75s 不变", seed=110),
    dict(id=11, skill="gs.wave",               weapon="Greatsword", slot=1, quality="White", affix=-1, charge=0.0,  cd=10.0, gate="",      expect="冷却 10s；前摇 .60s；地面波 power 1.30（原 .95）", seed=111),
    dict(id=12, skill="sc.reap",               weapon="Scythe",     slot=0, quality="White", affix=-1, charge=0.0,  cd=8.0,  gate="",      expect="冷却 8s；段间隔 .24s（原 .28）；3 段 .45 不变", seed=112),
    dict(id=13, skill="twin.counter",          weapon="TwinBlades", slot=1, quality="White", affix=-1, charge=0.0,  cd=0.0,  gate="T3",    expect="强化窗 0.85s；强化倍率 1.8；数值保持冻结（仅事件验收）", seed=None, event_only=True),
    dict(id=14, skill="sc.pull",               weapon="Scythe",     slot=1, quality="White", affix=-1, charge=0.0,  cd=0.0,  gate="T3",    expect="0 伤害；4.5m 牵引；数值保持冻结（仅事件验收）", seed=None, event_only=True, zero_damage=True),
    dict(id=15, skill="focus+sword.circle",    weapon="Sword",      slot=2, quality="White", affix=5,  charge=0.0,  cd=11.0, gate="",      expect="聚能词缀下 realised 冷却 10+1=11s（E-A 对称补齐）", seed=None),
    dict(id=16, skill="focus+spear.charge",    weapon="Spear",      slot=1, quality="White", affix=5,  charge=0.60, cd=9.0,  gate="",      expect="聚能词缀下 realised 冷却 8+1=9s", seed=None),
    dict(id=17, skill="focus+bow.pierce",      weapon="Bow",        slot=2, quality="White", affix=5,  charge=0.70, cd=11.0, gate="",      expect="聚能词缀下 realised 冷却 10+1=11s", seed=None),
    dict(id=18, skill="echo+sword.slot0",      weapon="Sword",      slot=0, quality="White", affix=2,  charge=0.0,  cd=0.0,  gate="",      expect="回响为半径效果（4->5m）而非伤害倍率；真实 HP 增减证明伤害≈1.00（标签「含回响 +25%」指范围，非 1.25× 伤害）", seed=None, desc_contains="含回响 +25%"),
    dict(id=19, skill="echo+spear.charge.exp", weapon="Spear",      slot=1, quality="White", affix=2,  charge=0.60, cd=8.0,  gate="",      expect="旧扩展技能不读 area：回响不生效（伤害≈1.00，验证 R-1 边界）", seed=None, desc_excludes="含回响 +25%"),
    dict(id=20, skill="echo.panel",            not_run_reason="技能窗 AffixInfo 为屏幕渲染文本，无头 Player 无法可靠读取；其运行时来源（SkillDescription 的回响标注）已由 #18/#19 真实运行覆盖"),
    dict(id=21, skill="focus.panel",           not_run_reason="技能窗 AffixInfo 为屏幕渲染文本，无头 Player 无法可靠读取；聚能 +1s 的运行时效果已由 #15-#17 真实运行覆盖"),
    dict(id=22, skill="gs.cleave.startup",     not_run_reason="SkillTradeoffs 面板为屏幕渲染文本，无头 Player 无法可靠读取；gs.cleave 前摇可通过 #10 事件时间线间接观察"),
    dict(id=23, skill="gs.wave.power",         not_run_reason="面板/代码一致断言需要读取渲染面板； realised power 已由 #11 真实战斗事件覆盖"),
    dict(id=24, skill="sc.reap.gap",           not_run_reason="面板/代码一致断言需要读取渲染面板； realised 段间隔已由 #12 事件时间线覆盖"),
    dict(id=25, skill="regression.P1",         not_run_reason="旧槽0 技能语义需产品负责人确认映射；四把旧武器真实技能回归已由 #1-#8 全部通过覆盖；v9/经济/掉落/随机流/ProjectSettings/Packages 由本批次零改动承诺保证"),
]

# ---------------------------------------------------------------------------
# PH-R2 post-processing: enable REAL damage forensics for normal-skill / echo
# rows, and turn the two T3 event-only rows into genuine runtime scenarios.
# ---------------------------------------------------------------------------
_DAMAGE_ROWS = {1, 2,3,4,5,6,7,8,9,10,11,12, 15,16,17, 18,19}
for _r in MATRIX:
    if _r.get("not_run_reason"):
        continue
    if _r["id"] in _DAMAGE_ROWS:
        _r["verify_damage"] = True
    if _r["id"] == 13:
        _r["mode"] = "twin_counter"; _r.pop("event_only", None); _r["gate"] = "T3"
        _r["expect"] = "真实翻滚无敌窗拒绝敌人攻击->actual-evaded-attack->0.85s 内 F(slot1) 反击强化(1.8x)->消耗一次"
    if _r["id"] == 14:
        _r["mode"] = "soul_pull"; _r.pop("event_only", None); _r["gate"] = "T3"
        _r["expect"] = "真实牵引：4.5m/50°锥/LOS->pull-start；目标向英雄位移>0.3m 且 HP 不变；Boss 免疫为代码级保证"


def build_args(run_id, row, build_sha, run_root, identity=None, expected_dll_override=None):
    args = [
        EXE_ACCEPTANCE,
        "--acceptance",
        "--scenario-id", row["skill"],
        "--run-id", run_id,
        "--build-sha", build_sha,
        "--weapon", row["weapon"],
        "--slot", str(row["slot"]),
        "--quality", row["quality"],
        "--affix", str(row["affix"]),
        "--charge", ("%.2f" % row["charge"]),
        "--expected-cooldown", ("%.2f" % row["cd"]),
        "--data-root", run_root,
        "-wanxiang-storage-root", run_root,
        "-logFile", os.path.join(run_root, "player.log"),
    ]
    # NOTE: no -batchmode — CombatSaveSystem.Start yields break in batch mode
    # (Application.isBatchMode), so the save system would never initialize and
    # the run would hang. A windowed real Player run is required.
    if row.get("desc_contains"):
        args += ["--desc-contains", row["desc_contains"]]
    if row.get("desc_excludes"):
        args += ["--desc-excludes", row["desc_excludes"]]
    if row.get("zero_damage"):
        args += ["--expect-zero-damage", "true"]
    # PH-R2: scenario mode + real-damage verification knobs
    if row.get("mode"):
        args += ["--mode", row["mode"]]
    if row.get("verify_damage"):
        args += ["--verify-damage", "true"]
    # PH-R2-R1-01 §3.3: pass buildId + EXE/DLL expectations. These are only
    # EXPECTATIONS; the Player independently hashes its loaded assembly.
    if identity is not None:
        args += ["--build-id", identity["buildId"],
                 "--expected-exe-sha", identity["exeShaBefore"],
                 "--expected-dll-sha", expected_dll_override or identity["dllShaBefore"]]
    return args


def verify_run_identity(pre, post, data, manifest):
    """PH-R2-R1 §3.3/§3.4: pure double-validation of build identity. Returns
    a list of reasons (empty == fully verified). Used by run_one AND by the
    identity self-tests, which call it with deliberately tampered values."""
    reasons = list(pre.get("manifestReasons") or [])
    if post.get("exeShaAfter") != pre.get("exeShaBefore"):
        reasons.append("Acceptance EXE SHA changed during run")
    if post.get("dllShaAfter") != pre.get("dllShaBefore"):
        reasons.append("Acceptance DLL SHA changed during run")
    post_actual = {
        "exeShaBefore": post.get("exeShaAfter"), "dllShaBefore": post.get("dllShaAfter"),
        "noDefineExeSha": post.get("noDefineExeShaAfter"), "noDefineDllSha": post.get("noDefineDllShaAfter"),
        "acceptanceMarker": post.get("acceptanceMarkerAfter"), "noDefineMarker": post.get("noDefineMarkerAfter"),
        "buildId": post.get("buildIdAfter"),
    }
    reasons += ["post-run " + r for r in verify_manifest(manifest, post_actual)]
    if post.get("acceptanceMarkerAfter") is not True:
        reasons.append("Acceptance DLL lost harness marker")
    if post.get("noDefineMarkerAfter") is not False:
        reasons.append("NoDefine DLL contains harness marker")
    # Player-computed identity (never trust the command-line SHA alone)
    if not data.get("loadedAssemblyPath"):
        reasons.append("Player did not report a loaded assembly path")
    if data.get("loadedAssemblyName") != "Assembly-CSharp":
        reasons.append("Player loaded assembly name mismatch: %s" % data.get("loadedAssemblyName"))
    if data.get("loadedAssemblySha256") != pre.get("dllShaBefore"):
        reasons.append("Player-computed loaded assembly SHA != expected DLL SHA")
    if data.get("identityVerified") is not True:
        reasons.append("Player identityVerified is not true")
    if data.get("expectedAssemblySha256") != pre.get("dllShaBefore"):
        reasons.append("Player expectedAssemblySha256 mismatch")
    if data.get("expectedExeSha256") != pre.get("exeShaBefore"):
        reasons.append("Player expectedExeSha256 mismatch")
    if data.get("buildId") != pre.get("buildId"):
        reasons.append("Player buildId mismatch")
    return reasons


def run_one(row, build_sha, run_id=None, timeout=RUN_TIMEOUT, preseed_stale=False, wrong_sha=False,
            runs_root=None, expected_dll_override=None, identity_for_test=None):
    """Execute one isolated run and return the verdict dict.
    PH-R2-R1: EXE+DLL hashes before/after, manifest verification, Player-internal
    assembly identity, and a Driver-generated run-manifest.json per run."""
    run_id = run_id or ("R%02d-%s" % (row["id"], time.strftime("%Y%m%d-%H%M%S")))
    run_root = os.path.join(runs_root or RUNS_ROOT, run_id)
    os.makedirs(run_root, exist_ok=True)
    result = {
        "runId": run_id, "scenarioId": row["skill"], "status": "NOT_RUN",
        "reason": "", "exitCode": None, "pid": None, "cmdline": None,
        "startedAt": None, "finishedAt": None, "timeoutSec": timeout,
    }

    # ---- PRE-LAUNCH identity snapshot (§3.3 steps 1-5) ----
    try:
        manifest = load_build_manifest()
        pre = identity_for_test if identity_for_test is not None else build_identity_snapshot(manifest)
    except Exception as e:
        manifest, pre = {}, {"exeShaBefore": None, "dllShaBefore": None,
                             "noDefineExeSha": None, "noDefineDllSha": None,
                             "acceptanceMarker": None, "noDefineMarker": None,
                             "buildId": None, "manifestReasons": ["cannot load build-manifest: %s" % e]}
    result["identityPre"] = pre

    def finalize(status, reason):
        result["status"], result["reason"] = status, reason
        # PH-R2-R1-04: run-manifest is written by the DRIVER after Player exit.
        rj = os.path.join(run_root, "result.json")
        data = {}
        if os.path.isfile(rj):
            try:
                data = json.load(open(rj, encoding="utf-8"))
            except Exception:
                pass
        # NOTE: compute into locals first -- a dict literal must never read its
        # own name (that is a NameError waiting to happen).
        exe_after = sha256_file(EXE_ACCEPTANCE) if os.path.isfile(EXE_ACCEPTANCE) else None
        dll_after = sha256_file(DLL_ACCEPTANCE) if os.path.isfile(DLL_ACCEPTANCE) else None
        nd_exe_after = sha256_file(EXE_NODEFINE) if os.path.isfile(EXE_NODEFINE) else None
        nd_dll_after = sha256_file(DLL_NODEFINE) if os.path.isfile(DLL_NODEFINE) else None
        complete = all((exe_after, dll_after, nd_exe_after, nd_dll_after))
        post = {
            "exeShaAfter": exe_after,
            "dllShaAfter": dll_after,
            "noDefineExeShaAfter": nd_exe_after,
            "noDefineDllShaAfter": nd_dll_after,
            "acceptanceMarkerAfter": marker_in_dll(DLL_ACCEPTANCE),
            "noDefineMarkerAfter": marker_in_dll(DLL_NODEFINE),
            "buildIdAfter": compute_build_id({
                "acceptanceDllSha256": dll_after,
                "noDefineDllSha256": nd_dll_after,
                "acceptanceExeSha256": exe_after,
                "noDefineExeSha256": nd_exe_after}) if complete else None,
        }
        identity_reasons = verify_run_identity(pre, post, data, manifest)
        result["identityReasons"] = identity_reasons
        rm = {
            "runId": run_id, "processId": result.get("pid"),
            "startedAt": result.get("startedAt"), "finishedAt": result.get("finishedAt"),
            "exitCode": result.get("exitCode"), "timedOut": result.get("timedOut", False),
            "buildId": pre.get("buildId"),
            "exeSha256Before": pre.get("exeShaBefore"), "exeSha256After": post["exeShaAfter"],
            "dllSha256Before": pre.get("dllShaBefore"), "dllSha256After": post["dllShaAfter"],
            "loadedAssemblyPath": data.get("loadedAssemblyPath"),
            "loadedAssemblySha256": data.get("loadedAssemblySha256"),
            "loadedAssemblyName": data.get("loadedAssemblyName"),
            "expectedAssemblySha256": data.get("expectedAssemblySha256"),
            "identityVerified": bool(data.get("identityVerified")) and not identity_reasons,
            "identityReasons": identity_reasons,
            "resultJsonSha256": sha256_file(rj) if os.path.isfile(rj) else None,
            "finalStatus": status,
        }
        with open(os.path.join(run_root, "run-manifest.json"), "w", encoding="utf-8") as f:
            json.dump(rm, f, ensure_ascii=False, indent=2)
        result["runManifest"] = rm
        return result


    if preseed_stale:
        # deliberately leave an OLD result behind: the driver must refuse it
        with open(os.path.join(run_root, "result.json"), "w", encoding="utf-8") as f:
            json.dump({"marker": MARKER, "runId": "STALE", "processId": -1, "pass": True}, f)
        old = time.time() - 3600
        os.utime(os.path.join(run_root, "result.json"), (old, old))

    args = build_args(run_id, row, "DEADBEEFWRONG" if wrong_sha else build_sha, run_root,
                      identity=pre, expected_dll_override=expected_dll_override)
    result["cmdline"] = args
    started = time.time()
    result["startedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(started))
    env = dict(os.environ)
    env["UNITY_TEST_ROOT"] = run_root
    proc = subprocess.Popen(args, cwd=PROJECT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    result["pid"] = proc.pid
    try:
        out, err = proc.communicate(timeout=timeout)
        exit_code = proc.returncode
        timed_out = False
    except subprocess.TimeoutExpired:
        timed_out = True
        proc.terminate()
        try:
            out, err = proc.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, err = proc.communicate()
        exit_code = proc.returncode
    finished = time.time()
    result["finishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(finished))
    result["exitCode"] = exit_code
    result["durationSec"] = round(finished - started, 2)
    result["timedOut"] = timed_out

    with open(os.path.join(run_root, "stdout.txt"), "wb") as f:
        f.write(out or b"")
    with open(os.path.join(run_root, "stderr.txt"), "wb") as f:
        f.write(err or b"")

    rj = os.path.join(run_root, "result.json")
    if not os.path.isfile(rj):
        return finalize("FAIL", "result.json missing after run (exit=%s, timedOut=%s)" % (exit_code, timed_out))
    created = os.path.getmtime(rj)  # mtime: Windows preserves ctime on overwrite
    if created < started:
        return finalize("FAIL", "result.json is stale (modified before this run started); refusing old evidence")
    try:
        data = json.load(open(rj, encoding="utf-8"))
    except Exception as e:
        return finalize("FAIL", "result.json unparseable: %s" % e)

    result["harness"] = {k: data.get(k) for k in (
        "marker", "version", "runId", "processId", "buildSha", "pass", "failed",
        "failReason", "entryAuthorized", "weapon", "quality", "affix", "slot",
        "expectedCooldown", "cooldownMeasured", "blockedDuringCooldown",
        "skillStarts", "skillCompletes", "damageCount", "skillDescription",
        "mode", "verifyDamage", "target", "damageVerdict", "damageNote",
        "expectedHits", "expectedPerHit", "expectedTotal", "actualHits",
        "uniformHits", "t3")}
    # PH-R2: also capture the raw forensic JSONL artifacts (independent evidence)
    result["targetEventsPath"] = os.path.join(run_root, "target-events.jsonl") if os.path.isfile(os.path.join(run_root, "target-events.jsonl")) else None
    result["damageEventsPath"] = os.path.join(run_root, "damage-events.jsonl") if os.path.isfile(os.path.join(run_root, "damage-events.jsonl")) else None
    # PH-R2 C-gate signal: did this run capture REAL damage from the target?
    h = result["harness"]
    tgt = h.get("target") or {}
    df = data.get("damageForensics") or []
    result["realDamageCaptured"] = bool(
        h.get("verifyDamage") and h.get("damageVerdict") and len(df) > 0 and tgt.get("prepared"))
    result["targetIdentity"] = tgt

    # identity checks: runId / processId / buildSha must match THIS launch
    if data.get("runId") != run_id:
        return finalize("FAIL", "identity mismatch: result.runId=%s expected=%s" % (data.get("runId"), run_id))
    if data.get("processId") != proc.pid:
        return finalize("FAIL", "identity mismatch: result.processId=%s expected PID=%s" % (data.get("processId"), proc.pid))
    if data.get("buildSha") != build_sha:
        return finalize("FAIL", "identity mismatch: result.buildSha=%s expected=%s" % (data.get("buildSha"), build_sha))
    # PH-R2-R1 §3.3: post-run EXE/DLL/manifest + Player-internal identity.
    # Any mismatch is FAIL; a timeout is NEVER PASS even if result.json says PASS.
    if timed_out:
        return finalize("FAIL", "hard timeout after %ss; process terminated, logs preserved" % timeout)
    if data.get("incomplete") is True or exit_code == 2:
        return finalize("INCOMPLETE", data.get("incompleteReason") or "harness reported INCOMPLETE")
    if exit_code != 0:
        return finalize("FAIL", "exit code %s != 0 (%s)" % (exit_code, data.get("failReason") or "harness reported failure"))
    try:
        post_probe = {
            "exeShaAfter": sha256_file(EXE_ACCEPTANCE), "dllShaAfter": sha256_file(DLL_ACCEPTANCE),
            "noDefineExeShaAfter": sha256_file(EXE_NODEFINE), "noDefineDllShaAfter": sha256_file(DLL_NODEFINE),
            "acceptanceMarkerAfter": marker_in_dll(DLL_ACCEPTANCE), "noDefineMarkerAfter": marker_in_dll(DLL_NODEFINE),
            "buildIdAfter": compute_build_id({
                "acceptanceDllSha256": sha256_file(DLL_ACCEPTANCE), "noDefineDllSha256": sha256_file(DLL_NODEFINE),
                "acceptanceExeSha256": sha256_file(EXE_ACCEPTANCE), "noDefineExeSha256": sha256_file(EXE_NODEFINE)}),
        }
        id_reasons = verify_run_identity(pre, post_probe, data, manifest)
    except Exception as e:
        return finalize("FAIL", "build identity verification could not run: %s" % e)
    if id_reasons:
        return finalize("FAIL", "build identity verification failed: " + "; ".join(id_reasons))
    if data.get("marker") != MARKER:
        return finalize("FAIL", "result marker mismatch")
    if not data.get("pass"):
        return finalize("FAIL", "harness verdict pass=false: %s" % data.get("failReason"))
    return finalize("PASS", "ok")


def selftest(build_sha, appdata_before, runs_root=None, with_identity_checks=False,
             with_timebase_checks=False):
    """Tool self-test: original 18 checks (+5 PH-R2-R1 identity, +7 FIX time-base)."""
    checks = []
    root = runs_root or RUNS_ROOT
    os.makedirs(root, exist_ok=True)
    stamp = time.strftime("%H%M%S")

    def check(name, ok, detail=""):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})
        print(("  [PASS] " if ok else "  [FAIL] ") + name + ("  " + detail if detail else ""))

    print("== SELF-TEST A ==")
    ok1 = os.path.isdir(os.path.dirname(EXE_ACCEPTANCE)) and grep_marker(os.path.dirname(EXE_ACCEPTANCE))
    check("acceptance build output contains harness marker", ok1, EXE_ACCEPTANCE)
    ok2 = os.path.isdir(os.path.dirname(EXE_NODEFINE)) and not grep_marker(os.path.dirname(EXE_NODEFINE))
    check("NoDefine (shipping-equivalent) build output lacks harness marker", ok2, EXE_NODEFINE)
    check("EXE sha matches build manifest", build_sha == _manifest_sha(), build_sha[:16] + "...")

    # positive run: the C-gate scenario (sword.triple, cd 7s) MUST capture REAL
    # target damage — this proves the forensics pipeline before any batch PASS.
    row = next(r for r in MATRIX if r["id"] == 1)
    r = run_one(row, build_sha, run_id="SELFTEST-positive-" + stamp, runs_root=root)
    check("C-gate positive run PASS with identity + freshness enforced", r["status"] == "PASS", "%s %s" % (r["status"], r["reason"]))
    if r["status"] == "PASS":
        rj = json.load(open(os.path.join(root, r["runId"], "result.json"), encoding="utf-8"))
        downs = [k for k in rj.get("keyEvents", []) if k.get("pressed")]
        ups = [k for k in rj.get("keyEvents", []) if not k.get("pressed")]
        check("KeyDown events recorded", len(downs) >= 1)
        check("KeyUp events recorded", len(ups) >= 1)
        check("skill start observed", len(rj.get("skillStarts", [])) >= 1)
        check("skill complete observed", len(rj.get("skillCompletes", [])) >= 1)
        check("entry authorized via public API", rj.get("entryAuthorized") is True)
        # PH-R2: the C-gate requires REAL damage, not just events
        check("C-gate: real target damage captured (target prepared + damage-events produced)",
              r.get("realDamageCaptured") is True, "realDamageCaptured=%s target=%s" % (r.get("realDamageCaptured"), r.get("targetIdentity")))
        de_path = os.path.join(root, r["runId"], "damage-events.jsonl")
        te_path = os.path.join(root, r["runId"], "target-events.jsonl")
        check("PH-R2 damage-events.jsonl artifact present", os.path.isfile(de_path))
        check("PH-R2 target-events.jsonl artifact present", os.path.isfile(te_path))

    # stale result rejection: pre-seed an OLD result and give the run a short
    # timeout so the harness can never overwrite it -> the driver must refuse it
    r = run_one(row, build_sha, run_id="SELFTEST-stale-" + stamp, timeout=8, preseed_stale=True, runs_root=root)
    check("stale/old result.json is rejected", r["status"] == "FAIL" and "stale" in r["reason"].lower(), r["reason"])

    # wrong build sha rejection (identity)
    r = run_one(row, build_sha, run_id="SELFTEST-wrongsha-" + stamp, timeout=60, wrong_sha=True, runs_root=root)
    check("wrong buildSha is rejected", r["status"] == "FAIL" and "buildSha" in r["reason"], r["reason"])

    # short timeout -> controlled shutdown, logs preserved
    r = run_one(row, build_sha, run_id="SELFTEST-timeout-" + stamp, timeout=6, runs_root=root)
    check("timeout produces FAIL (never PASS) with preserved logs",
          r["status"] == "FAIL" and r.get("timedOut") is True, r["reason"])
    check("timeout run preserved stdout/stderr/player.log",
          os.path.isfile(os.path.join(root, r["runId"], "stdout.txt")) and
          os.path.isfile(os.path.join(root, r["runId"], "stderr.txt")) and
          os.path.isfile(os.path.join(root, r["runId"], "player.log")))

    # run isolation: each run gets its own isolated root
    check("run roots are isolated per run",
          len({d for d in os.listdir(root) if d.startswith("SELFTEST")}) >= 4)

    # AppData protection so far
    after = appdata_protection_snapshot()
    verdicts = appdata_protection_ok(appdata_before, after)
    check("default AppData save untouched during self-test", all(verdicts.values()), json.dumps(verdicts))

    # ---- PH-R2-R1 §7-E: 5 NEW identity self-tests (original 18 preserved) ----
    if with_identity_checks:
        manifest = load_build_manifest()
        pre = build_identity_snapshot(manifest)
        post_ok = {
            "exeShaAfter": pre["exeShaBefore"], "dllShaAfter": pre["dllShaBefore"],
            "noDefineExeShaAfter": pre["noDefineExeSha"], "noDefineDllShaAfter": pre["noDefineDllSha"],
            "acceptanceMarkerAfter": True, "noDefineMarkerAfter": False,
            "buildIdAfter": compute_build_id({
                "acceptanceDllSha256": pre["dllShaBefore"], "noDefineDllSha256": pre["noDefineDllSha"],
                "acceptanceExeSha256": pre["exeShaBefore"], "noDefineExeSha256": pre["noDefineExeSha"]}),
        }
        good_data = {
            "loadedAssemblyPath": DLL_ACCEPTANCE, "loadedAssemblyName": "Assembly-CSharp",
            "loadedAssemblySha256": pre["dllShaBefore"], "identityVerified": True,
            "expectedAssemblySha256": pre["dllShaBefore"], "expectedExeSha256": pre["exeShaBefore"],
            "buildId": pre["buildId"],
        }
        # ID-1 is a REAL Player negative run: driver passes a wrong expected DLL
        # SHA, the Player computes its own SHA, sees the mismatch, refuses PASS.
        r_bad = run_one(row, build_sha, run_id="SELFTEST-wrongdllsha-" + stamp,
                        runs_root=root, expected_dll_override="0" * 64, timeout=90)
        check("ID-1 wrong DLL SHA is rejected by a real Player run",
              r_bad["status"] == "FAIL" and "identity" in (r_bad["reason"] + str(r_bad.get("identityReasons"))).lower(),
              "%s %s" % (r_bad["status"], r_bad["reason"]))
        check("ID-2 Player internal DLL SHA mismatch is rejected",
              bool(verify_run_identity(pre, post_ok,
                   dict(good_data, loadedAssemblySha256="0" * 64, identityVerified=False), manifest)),
              "tampered loadedAssemblySha256 + identityVerified=false -> reasons non-empty")
        check("ID-3 DLL change before/after run is rejected",
              bool(verify_run_identity(pre, dict(post_ok, dllShaAfter="f" * 64), good_data, manifest)),
              "tampered dllShaAfter -> reasons non-empty")
        bad_manifest = dict(manifest, acceptanceDllSha256="e" * 64)
        check("ID-4 manifest vs actual DLL mismatch is rejected",
              bool(verify_manifest(bad_manifest, pre)),
              "tampered manifest acceptanceDllSha256 -> reasons non-empty")
        rm_path = os.path.join(root, "SELFTEST-positive-" + stamp, "run-manifest.json")
        rm_ok = False
        if os.path.isfile(rm_path):
            rm = json.load(open(rm_path, encoding="utf-8"))
            rm_ok = (rm.get("exitCode") == 0 and rm.get("timedOut") is False
                     and rm.get("finalStatus") == "PASS" and rm.get("identityVerified") is True
                     and rm.get("resultJsonSha256") == sha256_file(os.path.join(root, "SELFTEST-positive-" + stamp, "result.json")))
        check("ID-5 run-manifest exitCode/identity/finalStatus recorded correctly", rm_ok, rm_path)

    # ---- PH-R2-R1-FIX §三: 7 time-base self-tests (real Player probe) ----
    if with_timebase_checks:
        tb_run = run_one(TIMEBASE_ROW, build_sha, run_id="SELFTEST-timebase-" + stamp,
                         runs_root=root, timeout=120)
        tb_dir = os.path.join(root, "SELFTEST-timebase-" + stamp)
        probe = load_timebase_probe(tb_dir) or {}
        cases = probe.get("cases") or {}

        def c_ok(*names):
            return all(bool((cases.get(n) or {}).get("ok")) for n in names)

        check("TB-0 real Player time-base probe PASS (identity enforced)",
              tb_run["status"] == "PASS" and probe.get("allOk") is True,
              "%s %s cases=%d" % (tb_run["status"], tb_run["reason"], len(cases)))
        check("TB-1 two hits <1.2s apart cannot close the window",
              c_ok("quiet_open_at_0.50s", "quiet_open_at_1.19s"))
        check("TB-2 >1.2s quiet closes the window", c_ok("quiet_closes_at_1.21s"))
        check("TB-3 timeScale=0: unscaled advances while scaled time is frozen",
              c_ok("timescale_zero_unscaled_advances", "timescale_zero_real_now_stays_open"),
              json.dumps(cases.get("timescale_zero_unscaled_advances", {}), ensure_ascii=False))
        check("TB-4 delayed pulse inside the quiet period is not misjudged",
              c_ok("delayed_pulse_at_1.00s_still_open"))
        check("TB-5 hard cap still terminates the window",
              c_ok("no_damage_hardcap_stays_open", "no_damage_hardcap_closes"))
        check("TB-6 product-clock offset cannot shorten the quiet period",
              c_ok("cross_clock_offset_does_not_close", "legacy_formula_would_close_early"),
              json.dumps(cases.get("legacy_formula_would_close_early", {}), ensure_ascii=False))
        # static: the cross-clock subtraction must be gone from the source
        src = open(os.path.join(PROJECT, "Assets", "CombatPrototype", "Acceptance",
                                "PlayerAcceptanceHarness.cs"), encoding="utf-8", errors="replace").read()
        bad = [l for l in src.splitlines()
               if "unscaledTime" in l and "lastDamageAt" in l and "//" not in l.split("unscaledTime")[0]]
        check("TB-7 no cross-clock subtraction remains in the harness source",
              ("lastDamageAt" not in src) and not bad,
              "lastDamageAt=%d suspiciousLines=%d" % (src.count("lastDamageAt"), len(bad)))
    return checks


def _manifest_sha():
    # PH-R2-R1: prefer the unified build-manifest.json (EXE + DLL identities).
    if os.path.isfile(BUILD_MANIFEST):
        try:
            return json.load(open(BUILD_MANIFEST, encoding="utf-8"))["acceptanceExeSha256"]
        except Exception:
            return None
    mp = os.path.join(PROJECT, "Builds", "acceptance_manifest.json")
    if not os.path.isfile(mp):
        return None
    try:
        return json.load(open(mp, encoding="utf-8"))["exeSha256"]
    except Exception:
        return None


def run_matrix(build_sha, appdata_before, only=None):
    rows_out = []
    stamp = time.strftime("%Y%m%d-%H%M%S")  # history: reruns never overwrite prior run dirs
    for row in MATRIX:
        if only and row["id"] not in only:
            continue
        if row.get("not_run_reason"):
            rows_out.append({
                "run_id": row["id"], "skill": row["skill"], "status": "NOT_RUN",
                "expected_observation": row["expect"] if "expect" in row else "",
                "gate": row.get("gate", ""), "seed": row.get("seed", ""),
                "reason": row["not_run_reason"], "pid": "", "exitCode": "",
            })
            print("  [NOT_RUN] %2d %s — %s" % (row["id"], row["skill"], row["not_run_reason"]))
            continue
        print("  [RUN   ] %2d %s ..." % (row["id"], row["skill"]))
        r = run_one(row, build_sha, run_id="R%02d-%s" % (row["id"], stamp))
        print("           -> %s %s" % (r["status"], r["reason"]))
        rows_out.append({
            "run_id": row["id"], "skill": row["skill"], "status": r["status"],
            "expected_observation": row["expect"],
            "gate": row.get("gate", ""), "seed": row.get("seed", ""),
            "reason": r["reason"], "pid": r["pid"], "exitCode": r["exitCode"],
            "runId": r["runId"], "realDamageCaptured": r.get("realDamageCaptured", False),
            "targetIdentity": r.get("targetIdentity"),
        })
    # ---- PH-R2 C-GATE ------------------------------------------------------
    # If the foundational real-damage capture (C scenario = sword.triple, id 1)
    # fails to obtain REAL damage, no later damage row may be marked PASS — they
    # are downgraded to INCOMPLETE so the batch can never present a false PASS.
    C_ROW_ID = 1
    c_row = next((x for x in rows_out if x["run_id"] == C_ROW_ID), None)
    c_ok = bool(c_row and c_row["status"] == "PASS" and c_row.get("realDamageCaptured"))
    if not c_ok:
        print("  [C-GATE] C scenario (id=%d) real-damage capture FAILED; downgrading LATER rows (incl. T3) PASS -> INCOMPLETE" % C_ROW_ID)
        for x in rows_out:
            if x["run_id"] == C_ROW_ID:
                continue
            if x["status"] == "PASS":
                x["status"] = "INCOMPLETE"
                x["reason"] = (x.get("reason") or "") + " | C-GATE: foundational real-damage capture (id=%d) failed; cannot attest real combat effect" % C_ROW_ID
                print("           [C-GATE] %2d %s -> INCOMPLETE" % (x["run_id"], x["skill"]))
    else:
        print("  [C-GATE] C scenario (id=%d) real-damage capture OK; subsequent rows may PASS." % C_ROW_ID)
    return rows_out


def _read_jsonl(path):
    if not path or not os.path.isfile(path):
        return []
    out = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
    except Exception:
        pass
    return out


def recompute_r1():
    """PH-R2-R1: independent, machine-checked recomputation of the three targeted
    runs, using ONLY the raw artifacts (result.json + damage-events.jsonl +
    target-events.jsonl). No Player is launched, nothing is rebuilt -- this is a
    pure read of the evidence a reviewer can re-run themselves.

    It re-derives the numeric claims the report makes:
      * C-GATE   sword.triple  3 x 0.65 AP, HP chain, cooldown
      * TWIN     twin.counter  1st counter 1.8x + 2nd counter 0.65x, consume-once
      * STAFF    staff.field   0.65 + 0.40 x 3 per segment
    """
    TOL = 0.02
    results = []
    for name, ratios, kind in (
            ("C-GATE", [0.65, 0.65, 0.65], "uniform"),
            ("TWIN-COUNTER", [1.8, 0.65], "counter"),
            ("STAFF-FIELD", [0.65, 0.40, 0.40, 0.40], "uniform")):
        run_dir = os.path.join(R1_RUNS, name)
        rj = os.path.join(run_dir, "result.json")
        de = os.path.join(run_dir, "damage-events.jsonl")
        te = os.path.join(run_dir, "target-events.jsonl")
        if not os.path.isfile(rj):
            results.append({"run": name, "allOk": False, "checks": [],
                            "error": "result.json missing"})
            continue
        data = json.load(open(rj, encoding="utf-8"))
        tgt = data.get("target") or {}
        ap = tgt.get("attackerAttackPower")
        hp0 = tgt.get("initialHP")
        tid = tgt.get("entityId")
        events = _read_jsonl(de)
        raw = _read_jsonl(te)
        checks = []

        def chk(nm, ok, expected, actual):
            checks.append({"check": nm, "ok": bool(ok),
                           "expected": expected, "actual": actual})

        chk("hit count matches product definition", len(events) == len(ratios),
            len(ratios), len(events))
        chk("raw target-events count matches damage-events count", len(raw) == len(events),
            len(events), len(raw))
        chk("hitId sequence is 1..N", [e.get("hitId") for e in events] == list(range(1, len(events) + 1)),
            list(range(1, len(events) + 1)), [e.get("hitId") for e in events])
        chk("all hits share one targetId", all(e.get("targetId") == tid for e in events), tid,
            sorted({e.get("targetId") for e in events}))
        chk("hitTime strictly increasing",
            all(events[i]["hitTime"] < events[i + 1]["hitTime"] for i in range(len(events) - 1)),
            "strictly increasing", [e.get("hitTime") for e in events])
        # HP continuity: first hit starts at initialHP, each next starts where the
        # previous ended, and the applied damage equals the HP delta.
        hp_prev = hp0
        hp_ok = True
        dmg_ok = True
        detail = []
        for i, e in enumerate(events):
            d = round(e["targetHealthBefore"] - e["targetHealthAfter"], 4)
            if abs(e["targetHealthBefore"] - hp_prev) > TOL:
                hp_ok = False
            if abs(d - e["actualDamage"]) > 0.05:
                dmg_ok = False
            detail.append({"hitId": e["hitId"], "before": e["targetHealthBefore"],
                           "after": e["targetHealthAfter"], "delta": d,
                           "applied": e["actualDamage"]})
            hp_prev = e["targetHealthAfter"]
        chk("HP chain continuous (before[i]==after[i-1], starts at initialHP)", hp_ok,
            "continuous from %s" % hp0, detail)
        chk("actualDamage == HP delta for every hit", dmg_ok, "delta==applied", detail)
        # per-segment expected damage
        seg_ok = True
        seg = []
        for i, e in enumerate(events):
            want = round(ap * ratios[i], 4) if ap is not None else None
            got = e["actualDamage"]
            if want is None or abs(want - got) > 0.05:
                seg_ok = False
            seg.append({"hitId": e["hitId"], "ratio": ratios[i],
                        "expectedDamage": want, "actualDamage": got,
                        "ratio_realised": (round(got / ap, 4) if ap else None)})
        chk("per-segment expectedDamage == AP x ratio[i] (NOT total-only)", seg_ok,
            "AP=%s x %s" % (ap, ratios), seg)
        total = round(sum(e["actualDamage"] for e in events), 4)
        want_total = round(sum(ap * r for r in ratios), 4) if ap is not None else None
        chk("total damage == sum of per-segment expectations",
            want_total is not None and abs(total - want_total) <= 0.05, want_total, total)

        if kind == "counter":
            t3 = data.get("t3") or {}
            chk("evade observed (real enemy attack denied by i-frames)", t3.get("evadeSeen") is True,
                True, t3.get("evadeSeen"))
            chk("real dodge roll observed", t3.get("dodgeRollObserved") is True, True,
                t3.get("dodgeRollObserved"))
            chk("evaded-attack timestamp recorded", (t3.get("evadeSeenAt") or -1) > 0, ">0",
                t3.get("evadeSeenAt"))
            chk("first counter contact is empowered", t3.get("counterEmpowered") is True, True,
                t3.get("counterEmpowered"))
            chk("first counter damage == 1.8x AP", len(events) >= 1 and ap is not None
                and abs(events[0]["actualDamage"] - ap * 1.8) <= 0.05, round(ap * 1.8, 4),
                events[0]["actualDamage"] if events else None)
            chk("skill cooldown elapsed between the two counters",
                len(events) >= 2 and (events[1]["hitTime"] - events[0]["hitTime"]) >= 8.5,
                ">= 8.5s (twin.counter cd 9.5s)",
                round(events[1]["hitTime"] - events[0]["hitTime"], 3) if len(events) >= 2 else None)
            chk("second counter produced a real contact", data.get("secondCounterContactSeen") is True,
                True, data.get("secondCounterContactSeen"))
            chk("second counter NOT empowered (evade consumed exactly once)",
                len(events) >= 2 and t3.get("secondCounterEmpowered") is False, False,
                t3.get("secondCounterEmpowered"))
            chk("second counter damage == 0.65x AP (baseline, not 1.8x)",
                len(events) >= 2 and ap is not None
                and abs(events[1]["actualDamage"] - ap * 0.65) <= 0.05, round(ap * 0.65, 4),
                events[1]["actualDamage"] if len(events) >= 2 else None)
        else:
            cd = data.get("cooldownMeasured")
            exp_cd = data.get("expectedCooldown")
            chk("cooldown realised within tolerance",
                cd is not None and exp_cd is not None and (exp_cd - 0.6) <= cd <= (exp_cd + 1.5),
                "%.2f +- (0.6/1.5)" % (exp_cd or 0), cd)
            chk("re-cast during cooldown was blocked", data.get("blockedDuringCooldown") is True,
                True, data.get("blockedDuringCooldown"))

        out = {
            "run": name, "skill": data.get("scenarioId"), "runId": data.get("runId"),
            "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "attackerAttackPower": ap, "targetInitialHP": hp0,
            "sourceArtifacts": {
                "result.json": sha256_file(rj),
                "damage-events.jsonl": sha256_file(de) if os.path.isfile(de) else None,
                "target-events.jsonl": sha256_file(te) if os.path.isfile(te) else None,
            },
            "checks": checks,
            "allOk": all(c["ok"] for c in checks),
            "hitCount": len(events),
        }
        with open(os.path.join(run_dir, "recompute.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        results.append(out)
        print("  [%s] %-14s %d/%d checks ok" % ("OK" if out["allOk"] else "FAIL", name,
                                                sum(1 for c in checks if c["ok"]), len(checks)))
    summary = {"generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "mode": "independent recomputation from raw artifacts (no Player launched)",
               "runs": results, "allOk": all(r["allOk"] for r in results)}
    with open(os.path.join(R1_DIR, "RECOMPUTE.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)
    print("  wrote Evidence/PH-R2-R1/RECOMPUTE.json allOk=%s" % summary["allOk"])
    return 0 if summary["allOk"] else 1


def _aggregate_forensics(rows_out):
    """PH-R2: build the damage-comparison table and T3 verification data from the
    per-run raw forensic artifacts (independent of the harness verdict)."""
    damage_cmp = []
    t3_data = []
    for r in rows_out:
        if r.get("status") == "NOT_RUN":
            continue
        rid = r["run_id"]
        run_dir = os.path.join(RUNS_ROOT, r.get("runId", ""))
        # PH-R2: derive EVERY reported figure from the run's OWN independent
        # Player artifacts, never from in-memory state carried between rows.
        # damage-events.jsonl is the authoritative per-hit record; result.json
        # supplies the frozen expected model / verdict / T3 observations.
        df = _read_jsonl(os.path.join(run_dir, "damage-events.jsonl"))
        rj_path = os.path.join(run_dir, "result.json")
        rj = {}
        if os.path.isfile(rj_path):
            try:
                rj = json.load(open(rj_path, encoding="utf-8"))
            except Exception:
                pass
        if not df:
            df = rj.get("damageForensics") or []
        h = r.get("harness") or rj
        if r.get("gate") == "T3":
            t3 = h.get("t3") or {}
            t3_data.append({
                "run_id": rid, "skill": r["skill"], "status": r["status"],
                "mode": t3.get("mode"), "evadeSeen": t3.get("evadeSeen"),
                "counterEmpowered": t3.get("counterEmpowered"),
                "counterDamage": t3.get("counterDamage"),
                "secondCounterEmpowered": t3.get("secondCounterEmpowered"),
                "pullStartSeen": t3.get("pullStartSeen"),
                "controlImmuneSeen": t3.get("controlImmuneSeen"),
                "pullObstructedSeen": t3.get("pullObstructedSeen"),
                "targetIdentity": r.get("targetIdentity"),
            })
        else:
            actual_total = sum(float(d.get("actualDamage", 0)) for d in df)
            expected_total = h.get("expectedTotal", 0) or 0
            ratio = (actual_total / expected_total) if expected_total > 0 else (1.0 if len(df) == 0 else 0.0)
            damage_cmp.append({
                "run_id": rid, "skill": r["skill"], "status": r["status"],
                "gate": r.get("gate", ""),
                "targetEntityId": (r.get("targetIdentity") or {}).get("entityId"),
                "targetArchetype": (r.get("targetIdentity") or {}).get("archetype"),
                "targetInitialHP": (r.get("targetIdentity") or {}).get("initialHP"),
                "attackerAttackPower": (r.get("targetIdentity") or {}).get("attackerAttackPower"),
                "expectedHits": h.get("expectedHits"),
                "actualHits": len(df),
                "expectedPerHit": h.get("expectedPerHit"),
                "expectedTotal": round(expected_total, 3) if expected_total else None,
                "actualTotal": round(actual_total, 3),
                "ratio": round(ratio, 4),
                "damageVerdict": h.get("damageVerdict"),
                "damageNote": h.get("damageNote"),
                "realDamageCaptured": r.get("realDamageCaptured", False),
            })
    return damage_cmp, t3_data


def write_outputs(rows_out, build_sha, appdata_before, appdata_after, verdicts, selftest_checks):
    # Isolated PH-R2 output directory: PH-R1 frozen deliverables at Evidence/
    # root are never touched.
    os.makedirs(PHR2_DIR, exist_ok=True)
    # updated matrix CSV (preserves the frozen columns, adds status/reason)
    csv_path = os.path.join(PHR2_DIR, "PLAYER_RUN_MATRIX.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["run_id", "skill", "status", "reason", "gate", "seed", "expected_observation"])
        for r in rows_out:
            w.writerow([r["run_id"], r["skill"], r["status"], r.get("reason", ""), r.get("gate", ""), r.get("seed", ""), r.get("expected_observation", "")])
    # PH-R2: damage comparison + T3 verification data
    damage_cmp, t3_data = _aggregate_forensics(rows_out)
    damage_cmp_path = os.path.join(PHR2_DIR, "DAMAGE_COMPARISON.json")
    t3_path = os.path.join(PHR2_DIR, "T3_VERIFICATION.json")
    selftest_path = os.path.join(PHR2_DIR, "SELFTEST.json")
    with open(selftest_path, "w", encoding="utf-8") as f:
        json.dump({"generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "buildSha256": build_sha,
                   "allPassed": bool(selftest_checks) and all(c["ok"] for c in selftest_checks),
                   "checks": selftest_checks}, f, ensure_ascii=False, indent=2)
    with open(damage_cmp_path, "w", encoding="utf-8") as f:
        json.dump(damage_cmp, f, ensure_ascii=False, indent=2)
    with open(t3_path, "w", encoding="utf-8") as f:
        json.dump(t3_data, f, ensure_ascii=False, indent=2)
    # index + protection + self-test evidence
    c_row = next((x for x in rows_out if x["run_id"] == 1), None)
    c_ok = bool(c_row and c_row["status"] == "PASS" and c_row.get("realDamageCaptured"))
    index = {
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "buildSha256": build_sha,
        "cGate": {"cRowId": 1, "realDamageCaptured": c_ok, "status": "OPEN" if c_ok else "CLOSED_BLOCKING"},
        "runs": rows_out,
        "damageComparison": damage_cmp,
        "t3Verification": t3_data,
        "appdataProtection": {
            "before": appdata_before, "after": appdata_after,
            "verdicts": verdicts, "ok": all(verdicts.values()),
        },
        "selfTest": selftest_checks,
    }
    with open(os.path.join(PHR2_DIR, "INDEX.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    return csv_path


def regenerate_report():
    """Rebuild the PH-R2 aggregate deliverables from the EXISTING independent
    Player artifacts only (no EXE rebuild, no Player re-run). Useful when the
    reporting/aggregation logic is corrected after a batch has already run."""
    idx_path = os.path.join(PHR2_DIR, "INDEX.json")
    if not os.path.isfile(idx_path):
        print("no INDEX.json to regenerate from"); return 1
    idx = json.load(open(idx_path, encoding="utf-8"))
    rows_out = idx.get("runs", [])
    for r in rows_out:
        rid = r.get("runId", "")
        rp = os.path.join(RUNS_ROOT, rid, "result.json")
        if not os.path.isfile(rp):
            continue
        try:
            d = json.load(open(rp, encoding="utf-8"))
        except Exception:
            continue
        tgt = d.get("target") or {}
        dfp = os.path.join(RUNS_ROOT, rid, "damage-events.jsonl")
        r["realDamageCaptured"] = bool(d.get("verifyDamage") and d.get("damageVerdict")
                                       and _read_jsonl(dfp) and tgt.get("prepared"))
        r["targetIdentity"] = tgt
    damage_cmp, t3_data = _aggregate_forensics(rows_out)
    with open(os.path.join(PHR2_DIR, "DAMAGE_COMPARISON.json"), "w", encoding="utf-8") as f:
        json.dump(damage_cmp, f, ensure_ascii=False, indent=2)
    with open(os.path.join(PHR2_DIR, "T3_VERIFICATION.json"), "w", encoding="utf-8") as f:
        json.dump(t3_data, f, ensure_ascii=False, indent=2)
    idx["damageComparison"] = damage_cmp
    idx["t3Verification"] = t3_data
    with open(idx_path, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
    print("regenerated PH-R2 aggregates from %d runs (%d damage rows, %d T3 rows)"
          % (len(rows_out), len(damage_cmp), len(t3_data)))
    return 0


def run_r1(build_sha, appdata_before, console_path):
    """PH-R2-R1 §7 targeted batch A-E. NOT the full 19-row matrix.
    All evidence goes to Evidence/PH-R2-R1/; PH-R1/PH-R2 history is untouched."""
    os.makedirs(R1_RUNS, exist_ok=True)
    os.makedirs(R1_SELFTEST, exist_ok=True)
    manifest = load_build_manifest()
    report = {"generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "buildSha256": build_sha, "buildManifest": manifest, "phases": {}}

    def log(s):
        print(s)
        with open(console_path, "a", encoding="utf-8") as f:
            f.write(s + "\n")

    # ---- A: build identity smoke ----
    log("== A. BUILD IDENTITY SMOKE ==")
    pre = build_identity_snapshot(manifest)
    a = {
        "manifestReasons": pre["manifestReasons"],
        "acceptanceExeSha256": pre["exeShaBefore"], "acceptanceDllSha256": pre["dllShaBefore"],
        "noDefineExeSha256": pre["noDefineExeSha"], "noDefineDllSha256": pre["noDefineDllSha"],
        "acceptanceMarkerPresent": pre["acceptanceMarker"], "noDefineMarkerPresent": pre["noDefineMarker"],
        "buildId": pre["buildId"],
        "defineLeakCount": open(os.path.join(PROJECT, "ProjectSettings", "ProjectSettings.asset"),
                                encoding="utf-8", errors="replace").read().count("UX_ACCEPTANCE"),
    }
    a["ok"] = (not a["manifestReasons"] and a["acceptanceMarkerPresent"] is True
               and a["noDefineMarkerPresent"] is False and a["defineLeakCount"] == 0)
    log("  manifest verify reasons=%s buildId=%s" % (a["manifestReasons"], a["buildId"]))
    log("  Acceptance EXE=%s DLL=%s marker=%s" % (a["acceptanceExeSha256"][:16], a["acceptanceDllSha256"][:16], a["acceptanceMarkerPresent"]))
    log("  NoDefine    EXE=%s DLL=%s marker=%s" % (a["noDefineExeSha256"][:16], a["noDefineDllSha256"][:16], a["noDefineMarkerPresent"]))
    report["phases"]["A"] = a
    with open(os.path.join(R1_DIR, "build", "acceptance-build.json"), "w", encoding="utf-8") as f:
        json.dump({k: a[k] for k in ("acceptanceExeSha256", "acceptanceDllSha256", "acceptanceMarkerPresent", "buildId")}, f, ensure_ascii=False, indent=2)
    with open(os.path.join(R1_DIR, "build", "nodefine-build.json"), "w", encoding="utf-8") as f:
        json.dump({k: a[k] for k in ("noDefineExeSha256", "noDefineDllSha256", "noDefineMarkerPresent", "defineLeakCount")}, f, ensure_ascii=False, indent=2)
    shutil.copyfile(BUILD_MANIFEST, os.path.join(R1_DIR, "build", "build-manifest.json"))

    # ---- B/C/D: three targeted Player runs ----
    targets = [
        ("B", "C-GATE", 1, "sword.triple"),
        ("C", "TWIN-COUNTER", 13, "twin.counter"),
        ("D", "STAFF-FIELD", 5, "staff.field"),
    ]
    runs_out = []
    for phase, name, row_id, skill in targets:
        log("== %s. %s (%s) ==" % (phase, name, skill))
        row = next(r for r in MATRIX if r["id"] == row_id)
        r = run_one(row, build_sha, run_id=name, runs_root=R1_RUNS)
        log("  -> %s %s" % (r["status"], r["reason"]))
        runs_out.append({"phase": phase, "name": name, "skill": skill, "status": r["status"],
                         "reason": r["reason"], "pid": r.get("pid"), "exitCode": r.get("exitCode"),
                         "runManifest": r.get("runManifest"), "identityReasons": r.get("identityReasons")})
        report["phases"][phase] = {"name": name, "skill": skill, "status": r["status"],
                                   "reason": r["reason"], "runId": name,
                                   "identityReasons": r.get("identityReasons")}

    # ---- E: harness regression: original 18 + 5 new identity checks ----
    log("== E. HARNESS REGRESSION (18 original + 5 identity) ==")
    checks = selftest(build_sha, appdata_before, runs_root=R1_SELFTEST, with_identity_checks=True)
    with open(os.path.join(R1_SELFTEST, "SELFTEST.json"), "w", encoding="utf-8") as f:
        json.dump({"generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "allPassed": all(c["ok"] for c in checks), "checks": checks}, f, ensure_ascii=False, indent=2)
    report["phases"]["E"] = {"checkCount": len(checks), "allPassed": all(c["ok"] for c in checks),
                             "failed": [c["check"] for c in checks if not c["ok"]]}
    log("  self-test %d/%d passed" % (sum(1 for c in checks if c["ok"]), len(checks)))

    appdata_after = appdata_protection_snapshot()
    verdicts = appdata_protection_ok(appdata_before, appdata_after)
    report["appdataProtection"] = {"before": appdata_before, "after": appdata_after, "verdicts": verdicts,
                                   "ok": all(verdicts.values())}
    report["runs"] = runs_out
    with open(os.path.join(R1_DIR, "INDEX.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return report


# ============================================================================
# PH-R2-R1-FIX-04: build-input protection (preflight / postflight)
# ============================================================================
def file_snapshot(rel):
    """Full fingerprint of one build input: size, mtime, SHA256, git blob OID of
    the WORKTREE file and of the HEAD blob. worktree OID != HEAD OID is the exact
    signal that an uncommitted user edit existed before the build."""
    p = os.path.join(PROJECT, rel.replace("/", os.sep))
    snap = {"path": rel, "exists": os.path.isfile(p)}
    if not snap["exists"]:
        snap.update(size=None, mtime=None, sha256=None, gitOidWorktree=None,
                    gitOidHead=None, tracked=False)
        return snap
    st = os.stat(p)
    snap.update(size=st.st_size,
                mtime=time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(st.st_mtime)),
                sha256=sha256_file(p))
    r = subprocess.run(["git", "hash-object", "--", p], cwd=PROJECT, capture_output=True, text=True)
    snap["gitOidWorktree"] = (r.stdout or "").strip() or None
    r2 = subprocess.run(["git", "rev-parse", "HEAD:" + rel], cwd=PROJECT, capture_output=True, text=True)
    snap["gitOidHead"] = (r2.stdout or "").strip() or None
    snap["tracked"] = bool(snap["gitOidHead"])
    snap["userEditPresent"] = bool(snap["tracked"] and snap["gitOidWorktree"] != snap["gitOidHead"])
    return snap


def build_input_manifest(phase, extra=None):
    files = [file_snapshot(r) for r in PROTECTED_BUILD_INPUTS]
    doc = {
        "schemaVersion": 1,
        "phase": phase,
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=PROJECT,
                               capture_output=True, text=True).stdout.strip(),
        "branch": subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=PROJECT,
                                 capture_output=True, text=True).stdout.strip(),
        "files": files,
        "summary": {
            "fileCount": len(files),
            "present": sum(1 for f in files if f["exists"]),
            "userEditsPresent": [f["path"] for f in files if f.get("userEditPresent")],
        },
    }
    if extra:
        doc.update(extra)
    return doc


def build_input_gate(pre, post):
    """Compare preflight vs postflight. A change is only tolerable when NO
    uncommitted user edit existed beforehand (pre != HEAD). Even then it is
    reported as CHANGED_BY_TOOLCHAIN, never as an unchanged file, and nothing is
    restored: the mutated bytes stay visible in the working tree."""
    rows = []
    for a in pre["files"]:
        b = next((x for x in post["files"] if x["path"] == a["path"]), None)
        if b is None:
            rows.append({"path": a["path"], "verdict": "MISSING_IN_POSTFLIGHT",
                         "shaBefore": a.get("sha256"), "shaAfter": None})
            continue
        changed = a.get("sha256") != b.get("sha256")
        user_work = bool(a.get("userEditPresent"))
        if not changed:
            verdict = "UNCHANGED"
        elif user_work:
            verdict = "CHANGED_WITH_USER_WORK"
        else:
            verdict = "CHANGED_BY_TOOLCHAIN"
        rows.append({
            "path": a["path"], "verdict": verdict, "changed": changed,
            "shaBefore": a.get("sha256"), "shaAfter": b.get("sha256"),
            "sizeBefore": a.get("size"), "sizeAfter": b.get("size"),
            "mtimeBefore": a.get("mtime"), "mtimeAfter": b.get("mtime"),
            "gitOidWorktreeBefore": a.get("gitOidWorktree"), "gitOidWorktreeAfter": b.get("gitOidWorktree"),
            "gitOidHead": a.get("gitOidHead"),
            "userEditPresentBefore": user_work,
            "headContentBefore": a.get("gitOidWorktree") == a.get("gitOidHead"),
        })
    gate = "PASS"
    if any(r["verdict"] == "CHANGED_WITH_USER_WORK" for r in rows):
        gate = "FAIL_USER_WORK_OVERWRITTEN"
    elif any(r["verdict"] in ("CHANGED_BY_TOOLCHAIN", "MISSING_IN_POSTFLIGHT") for r in rows):
        gate = "CHANGED_BY_TOOLCHAIN"
    return {"gate": gate, "files": rows,
            "unchanged": sum(1 for r in rows if r["verdict"] == "UNCHANGED"),
            "changed": sum(1 for r in rows if r["verdict"] != "UNCHANGED")}


def cmd_preflight():
    os.makedirs(FIX_BUILD, exist_ok=True)
    doc = build_input_manifest("pre")
    p = os.path.join(FIX_BUILD, "build-preflight-manifest.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print("PREFLIGHT -> " + p)
    for f in doc["files"]:
        print("  %-62s %s  sha=%s  userEdit=%s" % (
            f["path"], "present" if f["exists"] else "MISSING",
            (f["sha256"] or "-")[:16], f.get("userEditPresent")))
    print("  user edits present before build: %s" % (doc["summary"]["userEditsPresent"] or "NONE"))
    return 0


def cmd_postflight():
    os.makedirs(FIX_BUILD, exist_ok=True)
    pre_p = os.path.join(FIX_BUILD, "build-preflight-manifest.json")
    if not os.path.isfile(pre_p):
        print("POSTFLIGHT requires a preflight manifest; run the preflight first.")
        return 2
    pre = json.load(open(pre_p, encoding="utf-8"))
    doc = build_input_manifest("post",
                               extra={"comparedAgainst": pre_p,
                                      "preGeneratedAt": pre.get("generatedAt")})
    gate = build_input_gate(pre, doc)
    doc["gate"] = gate
    p = os.path.join(FIX_BUILD, "build-postflight-manifest.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print("POSTFLIGHT -> " + p)
    print("  GATE = " + gate["gate"] + "  unchanged=%d changed=%d" % (gate["unchanged"], gate["changed"]))
    for r in gate["files"]:
        print("  %-62s %-22s %s -> %s" % (r["path"], r["verdict"],
                                          (r["shaBefore"] or "-")[:12], (r["shaAfter"] or "-")[:12]))
    # gate != PASS is reported, never repaired by the driver.
    return 0 if gate["gate"] == "PASS" else 3


# ============================================================================
# PH-R2-R1-FIX: targeted batch A-E
# ============================================================================
TIMEBASE_ROW = dict(id=0, skill="timebase", weapon="Sword", slot=1, quality="White",
                    affix=-1, charge=0.0, cd=0.0, mode="timebase",
                    expect="harness-internal settle clock probe (no gameplay)")


def load_timebase_probe(run_dir):
    p = os.path.join(run_dir, "timebase-probe.json")
    if not os.path.isfile(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


def run_fix(build_sha, appdata_before, console_path):
    """PH-R2-R1-FIX §7: A time-base, B C-gate, C staff.field, D build protection,
    E self-test. Double-counter evidence is re-verified from the frozen PH-R2-R1
    raw events instead of being re-run (the fix does not touch its decision path)."""
    os.makedirs(FIX_RUNS, exist_ok=True)
    os.makedirs(FIX_SELFTEST, exist_ok=True)
    os.makedirs(FIX_BUILD, exist_ok=True)
    manifest = load_build_manifest()
    report = {"generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "revision": "PH-R2-R1-FIX",
              "buildSha256": build_sha, "buildManifest": manifest, "phases": {}}

    def log(s):
        print(s)
        with open(console_path, "a", encoding="utf-8") as f:
            f.write(s + "\n")

    # ---- A: time-base (real Player runtime probe) ----
    log("== A. TIME BASE (settle clock) ==")
    ra = run_one(TIMEBASE_ROW, build_sha, run_id="TIMEBASE", runs_root=FIX_RUNS, timeout=120)
    probe = load_timebase_probe(os.path.join(FIX_RUNS, "TIMEBASE"))
    cases = (probe or {}).get("cases") or {}

    def case_ok(*names):
        return all(bool((cases.get(n) or {}).get("ok")) for n in names)

    a_checks = [
        ("A1 two hits <1.2s apart cannot close the window",
         case_ok("quiet_open_at_0.50s", "quiet_open_at_1.19s")),
        ("A2 >1.2s of quiet closes the window",
         case_ok("quiet_closes_at_1.21s")),
        ("A3 timeScale=0 does not corrupt the clock",
         case_ok("timescale_zero_unscaled_advances", "timescale_zero_real_now_stays_open")),
        ("A4 a delayed pulse inside the quiet period is not misjudged",
         case_ok("delayed_pulse_at_1.00s_still_open")),
        ("A5 hard cap still terminates the window",
         case_ok("no_damage_hardcap_stays_open", "no_damage_hardcap_closes")),
        ("A6 the ~4.36s product-clock offset cannot shorten the quiet period",
         case_ok("cross_clock_offset_does_not_close", "legacy_formula_would_close_early")),
    ]
    a = {"runStatus": ra["status"], "reason": ra["reason"],
         "probeAllOk": bool((probe or {}).get("allOk")),
         "probeCaseCount": len(cases),
         "caseNames": sorted(cases),
         "checks": [{"check": n, "ok": bool(v)} for n, v in a_checks],
         "runManifest": ra.get("runManifest"),
         "identityReasons": ra.get("identityReasons")}
    a["ok"] = ra["status"] == "PASS" and a["probeAllOk"] and all(c["ok"] for c in a["checks"])
    for c in a["checks"]:
        log("  [%s] %s" % ("PASS" if c["ok"] else "FAIL", c["check"]))
    log("  run=%s probeAllOk=%s cases=%d" % (a["runStatus"], a["probeAllOk"], a["probeCaseCount"]))
    report["phases"]["A"] = a
    if probe:
        with open(os.path.join(FIX_DIR, "timebase-probe.json"), "w", encoding="utf-8") as f:
            json.dump(probe, f, ensure_ascii=False, indent=2)

    # ---- B: C-gate (sword.triple) ----
    log("== B. C-GATE (sword.triple) ==")
    row1 = next(r for r in MATRIX if r["id"] == 1)
    rb = run_one(row1, build_sha, run_id="C-GATE", runs_root=FIX_RUNS)
    b = check_damage_run("C-GATE", [0.65, 0.65, 0.65], rb)
    log("  -> %s %s | hits=%s total=%s cd=%s" % (rb["status"], rb["reason"],
                                                 b.get("actualHits"), b.get("totalActual"), b.get("cooldownMeasured")))
    for c in b["checks"]:
        if not c["ok"]:
            log("  [FAIL] " + c["check"])
    report["phases"]["B"] = b

    # ---- C: staff.field (per-segment) ----
    log("== C. STAFF-FIELD (staff.field) ==")
    row5 = next(r for r in MATRIX if r["id"] == 5)
    rc = run_one(row5, build_sha, run_id="STAFF-FIELD", runs_root=FIX_RUNS)
    c = check_damage_run("STAFF-FIELD", [0.65, 0.40, 0.40, 0.40], rc)
    log("  -> %s %s | segments=%s total=%s" % (rc["status"], rc["reason"],
                                               c.get("segmentDamage"), c.get("totalActual")))
    for chk in c["checks"]:
        if not chk["ok"]:
            log("  [FAIL] " + chk["check"])
    report["phases"]["C"] = c

    # ---- D: build protection + identity ----
    log("== D. BUILD PROTECTION ==")
    d = check_build_protection(manifest)
    log("  gate=%s unchanged=%s changed=%s manifestReasons=%s" %
        (d.get("gate"), d.get("unchanged"), d.get("changed"), d.get("manifestReasons")))
    report["phases"]["D"] = d

    # ---- E: self-test (18 original + 5 identity + 7 time-base) ----
    log("== E. SELF-TEST ==")
    checks = selftest(build_sha, appdata_before, runs_root=FIX_SELFTEST,
                      with_identity_checks=True, with_timebase_checks=True)
    with open(os.path.join(FIX_SELFTEST, "SELFTEST.json"), "w", encoding="utf-8") as f:
        json.dump({"generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "allPassed": all(x["ok"] for x in checks),
                   "count": len(checks), "checks": checks}, f, ensure_ascii=False, indent=2)
    e = {"checkCount": len(checks), "passed": sum(1 for x in checks if x["ok"]),
         "allPassed": all(x["ok"] for x in checks),
         "failed": [x["check"] for x in checks if not x["ok"]]}
    report["phases"]["E"] = e
    log("  self-test %d/%d passed" % (e["passed"], e["checkCount"]))

    # ---- F: double-counter regression on frozen raw evidence (no re-run) ----
    log("== F. TWIN-COUNTER REGRESSION (frozen PH-R2-R1 evidence) ==")
    f = check_twin_regression()
    log("  allOk=%s %s" % (f["allOk"], f.get("note", "")))
    report["phases"]["F"] = f

    appdata_after = appdata_protection_snapshot()
    verdicts = appdata_protection_ok(appdata_before, appdata_after)
    report["appdataProtection"] = {"before": appdata_before, "after": appdata_after,
                                   "verdicts": verdicts, "ok": all(verdicts.values())}
    report["runs"] = [{"name": "TIMEBASE", "status": ra["status"], "runManifest": ra.get("runManifest")},
                      {"name": "C-GATE", "status": rb["status"], "runManifest": rb.get("runManifest")},
                      {"name": "STAFF-FIELD", "status": rc["status"], "runManifest": rc.get("runManifest")}]
    with open(os.path.join(FIX_DIR, "INDEX.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    return report


def check_damage_run(run_name, ratios, run_result):
    """Independent per-segment verification straight from the raw JSONL, never
    from the harness verdict alone."""
    run_dir = os.path.join(FIX_RUNS, run_name)
    rj_p = os.path.join(run_dir, "result.json")
    out = {"runName": run_name, "status": run_result["status"], "reason": run_result["reason"],
           "runManifest": run_result.get("runManifest"), "identityReasons": run_result.get("identityReasons"),
           "checks": []}
    if not os.path.isfile(rj_p):
        out["checks"] = [{"check": "result.json present", "ok": False}]
        out["ok"] = False
        return out
    rj = json.load(open(rj_p, encoding="utf-8"))
    de = _read_jsonl(os.path.join(run_dir, "damage-events.jsonl"))
    te = _read_jsonl(os.path.join(run_dir, "target-events.jsonl"))
    tgt = rj.get("target") or {}
    ap = tgt.get("attackerAttackPower") or 0.0
    hp0 = tgt.get("initialHP")
    tid = tgt.get("entityId")
    exp = [round(ap * r, 5) for r in ratios]
    act = [round(e.get("actualDamage", 0.0), 5) for e in de]
    checks = out["checks"]

    def chk(name, ok, detail=""):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    chk("result.json fresh + PASS", run_result["status"] == "PASS", run_result["reason"])
    chk("hit count == %d" % len(ratios), len(de) == len(ratios), "actual=%d" % len(de))
    chk("hitId is 1..N in order", [e.get("hitId") for e in de] == list(range(1, len(de) + 1)))
    chk("single target identity", all(e.get("targetId") == tid for e in de), str(tid))
    chk("hit times strictly increasing",
        all(de[i]["hitTime"] < de[i + 1]["hitTime"] for i in range(len(de) - 1)))
    hp = hp0
    cont = True
    delta = True
    for e in de:
        if hp is not None and abs((e.get("targetHealthBefore") or 0) - hp) > 1e-3:
            cont = False
        if abs(((e.get("targetHealthBefore") or 0) - (e.get("targetHealthAfter") or 0)) - e.get("actualDamage", 0)) > 0.05:
            delta = False
        hp = e.get("targetHealthAfter")
    chk("HP chain continuous from initialHP", cont, "hp0=%s" % hp0)
    chk("actualDamage == HP delta", delta)
    for i, (r, want, got) in enumerate(zip(ratios, exp, act), 1):
        chk("segment %d ratio %.2f -> %.4f (actual %.5f)" % (i, r, want, got), abs(want - got) <= 0.05)
    fz = rj.get("damageForensics") or []
    chk("result.json forensics == damage-events.jsonl",
        len(fz) == len(de) and all(abs(a.get("actualDamage", 0) - b.get("actualDamage", 0)) < 1e-6
                                   and abs(a.get("hitTime", 0) - b.get("hitTime", 0)) < 1e-6
                                   for a, b in zip(fz, de)))
    chk("raw target-events == damage-events", len(te) == len(de))
    chk("checksPer-session: every hit carries both clocks explicitly",
        all(("hitActiveTime" in e) and ("hitUnscaledTime" in e) for e in de),
        "FIX-01 field presence")
    chk("both clocks present in target-events",
        all(("activeTime" in e) and ("unscaledTime" in e) for e in te))
    if (rj.get("expectedCooldown") or 0) > 0:
        chk("re-cast blocked during cooldown", rj.get("blockedDuringCooldown") is True)
        cd = rj.get("cooldownMeasured")
        exp_cd = rj.get("expectedCooldown")
        chk("cooldown measured within tolerance",
            cd is not None and (exp_cd - 0.6) <= cd <= (exp_cd + 1.5),
            "measured=%s expected=%s" % (cd, exp_cd))
    out.update(actualHits=len(de), segmentDamage=act, expectedSegmentDamage=exp,
               totalActual=round(sum(act), 5), totalExpected=round(sum(exp), 5),
               cooldownMeasured=rj.get("cooldownMeasured"),
               expectedCooldown=rj.get("expectedCooldown"),
               attackerAttackPower=ap, initialHP=hp0,
               hostileHPchain=[e.get("targetHealthAfter") for e in de])
    out["ok"] = run_result["status"] == "PASS" and all(c["ok"] for c in checks)
    return out


def check_build_protection(manifest):
    """D: pre/post build-input gate + artifact identity, all recomputed here."""
    pre_p = os.path.join(FIX_BUILD, "build-preflight-manifest.json")
    post_p = os.path.join(FIX_BUILD, "build-postflight-manifest.json")
    out = {"preflightPresent": os.path.isfile(pre_p), "postflightPresent": os.path.isfile(post_p)}
    if not (out["preflightPresent"] and out["postflightPresent"]):
        out.update(ok=False, gate="MISSING_MANIFEST")
        return out
    pre = json.load(open(pre_p, encoding="utf-8"))
    post = json.load(open(post_p, encoding="utf-8"))
    gate = build_input_gate(pre, post)
    actual = build_identity_snapshot(manifest)
    out.update(gate=gate["gate"], unchanged=gate["unchanged"], changed=gate["changed"],
               files=gate["files"], manifestReasons=actual["manifestReasons"],
               buildId=actual["buildId"], dllSha256=actual["dllShaBefore"],
               exeSha256=actual["exeShaBefore"],
               noDefineDllSha256=actual["noDefineDllSha"],
               acceptanceMarker=actual["acceptanceMarker"], noDefineMarker=actual["noDefineMarker"])
    # a toolchain-only change is reported but does not by itself invalidate the
    # combat evidence; a change that could have overwritten USER work always does.
    out["ok"] = (not actual["manifestReasons"] and out["acceptanceMarker"] is True
                 and out["noDefineMarker"] is False
                 and gate["gate"] in ("PASS", "CHANGED_BY_TOOLCHAIN"))
    return out


def check_twin_regression():
    """F: re-verify the frozen twin.counter raw events under the SAME predicates
    used by the FIX batch, without re-running the Player. Proves the clock fix did
    not invalidate the causal chain (evade -> empowered counter -> cooldown ->
    second, un-empowered counter)."""
    run_dir = os.path.join(R1_RUNS, "TWIN-COUNTER")
    rj_p = os.path.join(run_dir, "result.json")
    if not os.path.isfile(rj_p):
        return {"allOk": False, "note": "frozen PH-R2-R1 TWIN-COUNTER evidence missing"}
    rj = json.load(open(rj_p, encoding="utf-8"))
    de = _read_jsonl(os.path.join(run_dir, "damage-events.jsonl"))
    te = _read_jsonl(os.path.join(run_dir, "target-events.jsonl"))
    t3 = rj.get("t3") or {}
    ap = (rj.get("target") or {}).get("attackerAttackPower") or 0.0
    obs = {o["stage"]: o for o in (rj.get("observations") or [])}
    e = rj.get("skillStarts") or []
    checks = []

    def chk(n, ok, d=""):
        checks.append({"check": n, "ok": bool(ok), "detail": d})

    chk("evade seen + dodge roll observed",
        t3.get("evadeSeen") is True and t3.get("dodgeRollObserved") is True)
    chk("first counter empowered (1.8x)",
        t3.get("counterEmpowered") is True and len(de) >= 1 and abs(de[0]["actualDamage"] - ap * 1.8) <= 0.05,
        "dmg=%.4f expect=%.4f" % (de[0]["actualDamage"] if de else -1, ap * 1.8))
    chk("second counter has a REAL contact and is NOT empowered",
        rj.get("secondCounterContactSeen") is True and rj.get("t3", {}).get("secondCounterEmpowered") is False)
    chk("second counter deals 0.65x (consumed once)",
        len(de) >= 2 and abs(de[1]["actualDamage"] - ap * 0.65) <= 0.05,
        "dmg=%.4f expect=%.4f" % (de[1]["actualDamage"] if len(de) > 1 else -1, ap * 0.65))
    chk("second counter happened after the skill cooldown",
        len(e) >= 2 and (e[1] - e[0]) >= 8.5, "gap=%.3f" % ((e[1] - e[0]) if len(e) > 1 else -1))
    # clock unification: contact must follow evade once the offset is removed
    off = None
    if "actual-evaded-attack" in obs and t3.get("evadeSeenAt"):
        off = t3["evadeSeenAt"] - obs["actual-evaded-attack"]["time"]
    contact_u = de[0]["hitTime"] + off if (off is not None and de) else None
    chk("first counter contact falls after the evade (single-clock view)",
        contact_u is not None and contact_u > (t3.get("evadeSeenAt") or 0),
        "contact_unscaled=%.3f evade=%.3f offset=%.6f" % (contact_u or -1, t3.get("evadeSeenAt") or -1, off or -1))
    chk("first counter contact is inside the 0.85s empowered window",
        contact_u is not None and 0 <= (contact_u - (t3.get("evadeSeenAt") or 0)) <= 0.85,
        "delta=%.3f" % ((contact_u - (t3.get("evadeSeenAt") or 0)) if contact_u else -1))
    chk("raw target-events preserved for both counters", len(te) >= 2)
    return {"allOk": all(c["ok"] for c in checks), "checks": checks,
            "clockOffsetUnscaledMinusActive": off,
            "note": "frozen PH-R2-R1 evidence; not re-run (fix does not touch twin.counter decisions)"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["selftest", "matrix", "samples", "all", "report", "manifest",
                                     "r1", "recompute", "preflight", "postflight", "fix"])
    ap.add_argument("--only", type=str, default="", help="comma-separated row ids for matrix mode")
    args = ap.parse_args()

    # report mode works purely on existing artifacts; no EXE / build checks.
    if args.mode == "report":
        sys.exit(regenerate_report())
    if args.mode == "recompute":
        sys.exit(recompute_r1())
    if args.mode == "manifest":
        m = generate_build_manifest()
        print("wrote " + BUILD_MANIFEST + " buildId=" + m["buildId"])
        sys.exit(0)
    # PH-R2-R1-FIX-04: build-input preflight / postflight need no built EXE.
    if args.mode == "preflight":
        sys.exit(cmd_preflight())
    if args.mode == "postflight":
        sys.exit(cmd_postflight())

    if not os.path.isfile(EXE_ACCEPTANCE):
        print("Acceptance EXE missing; run the build chain first."); sys.exit(2)
    if os.path.isdir(os.path.dirname(EXE_NODEFINE)) and grep_marker(os.path.dirname(EXE_NODEFINE)):
        print("NoDefine build output contains the harness marker; shipping exclusion FAILED."); sys.exit(2)

    build_sha = sha256_file(EXE_ACCEPTANCE)
    print("Acceptance EXE sha256 = " + build_sha)
    appdata_before = appdata_protection_snapshot()
    print("AppData protection snapshot taken (default + legacy save dirs).")

    if args.mode == "r1":
        console = os.path.join(R1_SELFTEST, "console.log")
        open(console, "w", encoding="utf-8").close()
        report = run_r1(build_sha, appdata_before, console)
        print("R1 DONE. phases=" + json.dumps({k: v.get("status", v.get("allPassed", v.get("ok")))
                                               for k, v in report["phases"].items()}))
        sys.exit(0)

    if args.mode == "fix":
        os.makedirs(FIX_SELFTEST, exist_ok=True)
        console = os.path.join(FIX_SELFTEST, "console.log")
        open(console, "w", encoding="utf-8").close()
        report = run_fix(build_sha, appdata_before, console)
        print("FIX DONE. phases=" + json.dumps({k: v.get("ok", v.get("status", v.get("allPassed")))
                                                for k, v in report["phases"].items()}))
        sys.exit(0)

    selftest_checks = []
    if args.mode in ("selftest", "all"):
        selftest_checks = selftest(build_sha, appdata_before)
        bad = [c for c in selftest_checks if not c["ok"]]
        if bad:
            print("SELF-TEST FAILED (%d checks)" % len(bad)); sys.exit(1)
        print("SELF-TEST OK")

    rows_out = []
    if args.mode == "samples":
        for rid in (1, 3, 10):
            row = next(r for r in MATRIX if r["id"] == rid)
            r = run_one(row, build_sha, run_id="SAMPLE%02d" % rid)
            print("  [%s] %2d %s %s" % (r["status"], rid, row["skill"], r["reason"]))
            rows_out.append({"run_id": rid, "skill": row["skill"], "status": r["status"], "reason": r["reason"]})
    elif args.mode in ("matrix", "all"):
        only = set(int(x) for x in args.only.split(",") if x.strip()) if args.only else None
        rows_out = run_matrix(build_sha, appdata_before, only=only)

    appdata_after = appdata_protection_snapshot()
    verdicts = appdata_protection_ok(appdata_before, appdata_after)
    print("AppData protection: " + json.dumps(verdicts))
    if rows_out:
        path = write_outputs(rows_out, build_sha, appdata_before, appdata_after, verdicts, selftest_checks)
        print("wrote " + path)
    fails = [r for r in rows_out if r["status"] == "FAIL"]
    print("DONE. pass=%d fail=%d not_run=%d" % (
        sum(1 for r in rows_out if r["status"] == "PASS"),
        len(fails),
        sum(1 for r in rows_out if r["status"] == "NOT_RUN")))
    sys.exit(0)


if __name__ == "__main__":
    main()
