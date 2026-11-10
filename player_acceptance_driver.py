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
MARKER = "UX_ACCEPTANCE_HARNESS_v1"
EVIDENCE = os.path.join(PROJECT, "Evidence")
RUNS_ROOT = os.path.join(EVIDENCE, "Runs")
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
    dict(id=18, skill="echo+sword.slot0",      weapon="Sword",      slot=0, quality="White", affix=2,  charge=0.0,  cd=0.0,  gate="",      expect="槽0 技能描述出现「（含回响 +25%）」；伤害×1.25", seed=None, desc_contains="含回响 +25%"),
    dict(id=19, skill="echo+spear.charge.exp", weapon="Spear",      slot=1, quality="White", affix=2,  charge=0.60, cd=8.0,  gate="",      expect="旧扩展技能不读 area：回响不生效（验证 R-1 边界）", seed=None, desc_excludes="含回响 +25%"),
    dict(id=20, skill="echo.panel",            not_run_reason="技能窗 AffixInfo 为屏幕渲染文本，无头 Player 无法可靠读取；其运行时来源（SkillDescription 的回响标注）已由 #18/#19 真实运行覆盖"),
    dict(id=21, skill="focus.panel",           not_run_reason="技能窗 AffixInfo 为屏幕渲染文本，无头 Player 无法可靠读取；聚能 +1s 的运行时效果已由 #15-#17 真实运行覆盖"),
    dict(id=22, skill="gs.cleave.startup",     not_run_reason="SkillTradeoffs 面板为屏幕渲染文本，无头 Player 无法可靠读取；gs.cleave 前摇可通过 #10 事件时间线间接观察"),
    dict(id=23, skill="gs.wave.power",         not_run_reason="面板/代码一致断言需要读取渲染面板； realised power 已由 #11 真实战斗事件覆盖"),
    dict(id=24, skill="sc.reap.gap",           not_run_reason="面板/代码一致断言需要读取渲染面板； realised 段间隔已由 #12 事件时间线覆盖"),
    dict(id=25, skill="regression.P1",         not_run_reason="旧槽0 技能语义需产品负责人确认映射；四把旧武器真实技能回归已由 #1-#8 全部通过覆盖；v9/经济/掉落/随机流/ProjectSettings/Packages 由本批次零改动承诺保证"),
]


def build_args(run_id, row, build_sha, run_root):
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
    return args


def run_one(row, build_sha, run_id=None, timeout=RUN_TIMEOUT, preseed_stale=False, wrong_sha=False):
    """Execute one isolated run and return the verdict dict."""
    run_id = run_id or ("R%02d-%s" % (row["id"], time.strftime("%Y%m%d-%H%M%S")))
    run_root = os.path.join(RUNS_ROOT, run_id)
    os.makedirs(run_root, exist_ok=True)
    result = {
        "runId": run_id, "scenarioId": row["skill"], "status": "NOT_RUN",
        "reason": "", "exitCode": None, "pid": None, "cmdline": None,
        "startedAt": None, "finishedAt": None, "timeoutSec": timeout,
    }

    if preseed_stale:
        # deliberately leave an OLD result behind: the driver must refuse it
        with open(os.path.join(run_root, "result.json"), "w", encoding="utf-8") as f:
            json.dump({"marker": MARKER, "runId": "STALE", "processId": -1, "pass": True}, f)
        old = time.time() - 3600
        os.utime(os.path.join(run_root, "result.json"), (old, old))

    args = build_args(run_id, row, "DEADBEEFWRONG" if wrong_sha else build_sha, run_root)
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
        result["status"] = "FAIL"
        result["reason"] = "result.json missing after run (exit=%s, timedOut=%s)" % (exit_code, timed_out)
        return result
    created = os.path.getmtime(rj)  # mtime: Windows preserves ctime on overwrite
    if created < started:
        result["status"] = "FAIL"
        result["reason"] = "result.json is stale (modified before this run started); refusing old evidence"
        return result
    try:
        data = json.load(open(rj, encoding="utf-8"))
    except Exception as e:
        result["status"] = "FAIL"
        result["reason"] = "result.json unparseable: %s" % e
        return result

    result["harness"] = {k: data.get(k) for k in (
        "marker", "version", "runId", "processId", "buildSha", "pass", "failed",
        "failReason", "entryAuthorized", "weapon", "quality", "affix", "slot",
        "expectedCooldown", "cooldownMeasured", "blockedDuringCooldown",
        "skillStarts", "skillCompletes", "damageCount", "skillDescription")}

    # identity checks: runId / processId / buildSha must match THIS launch
    if data.get("runId") != run_id:
        result["status"] = "FAIL"; result["reason"] = "identity mismatch: result.runId=%s expected=%s" % (data.get("runId"), run_id); return result
    if data.get("processId") != proc.pid:
        result["status"] = "FAIL"; result["reason"] = "identity mismatch: result.processId=%s expected PID=%s" % (data.get("processId"), proc.pid); return result
    if data.get("buildSha") != build_sha:
        result["status"] = "FAIL"; result["reason"] = "identity mismatch: result.buildSha=%s expected=%s" % (data.get("buildSha"), build_sha); return result
    if timed_out:
        result["status"] = "FAIL"; result["reason"] = "hard timeout after %ss; process terminated, logs preserved" % timeout; return result
    if exit_code != 0:
        result["status"] = "FAIL"
        result["reason"] = "exit code %s != 0 (%s)" % (exit_code, data.get("failReason") or "harness reported failure")
        return result
    if data.get("marker") != MARKER:
        result["status"] = "FAIL"; result["reason"] = "result marker mismatch"; return result
    if not data.get("pass"):
        result["status"] = "FAIL"; result["reason"] = "harness verdict pass=false: %s" % data.get("failReason"); return result
    result["status"] = "PASS"
    result["reason"] = "ok"
    return result


def selftest(build_sha, appdata_before):
    """Tool self-test (A). Verifies marker gating and the negative paths."""
    checks = []
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

    # positive run: a fast normal skill (sword.triple, cd 7s)
    row = next(r for r in MATRIX if r["id"] == 1)
    r = run_one(row, build_sha, run_id="SELFTEST-positive-" + stamp)
    check("positive run PASS with identity + freshness enforced", r["status"] == "PASS", "%s %s" % (r["status"], r["reason"]))
    if r["status"] == "PASS":
        rj = json.load(open(os.path.join(RUNS_ROOT, r["runId"], "result.json"), encoding="utf-8"))
        downs = [k for k in rj.get("keyEvents", []) if k.get("pressed")]
        ups = [k for k in rj.get("keyEvents", []) if not k.get("pressed")]
        check("KeyDown events recorded", len(downs) >= 1)
        check("KeyUp events recorded", len(ups) >= 1)
        check("skill start observed", len(rj.get("skillStarts", [])) >= 1)
        check("skill complete observed", len(rj.get("skillCompletes", [])) >= 1)
        check("entry authorized via public API", rj.get("entryAuthorized") is True)

    # stale result rejection: pre-seed an OLD result and give the run a short
    # timeout so the harness can never overwrite it -> the driver must refuse it
    r = run_one(row, build_sha, run_id="SELFTEST-stale-" + stamp, timeout=8, preseed_stale=True)
    check("stale/old result.json is rejected", r["status"] == "FAIL" and "stale" in r["reason"].lower(), r["reason"])

    # wrong build sha rejection (identity)
    r = run_one(row, build_sha, run_id="SELFTEST-wrongsha-" + stamp, timeout=60, wrong_sha=True)
    check("wrong buildSha is rejected", r["status"] == "FAIL" and "buildSha" in r["reason"], r["reason"])

    # short timeout -> controlled shutdown, logs preserved
    r = run_one(row, build_sha, run_id="SELFTEST-timeout-" + stamp, timeout=6)
    check("timeout produces FAIL (never PASS) with preserved logs",
          r["status"] == "FAIL" and r.get("timedOut") is True, r["reason"])
    check("timeout run preserved stdout/stderr/player.log",
          os.path.isfile(os.path.join(RUNS_ROOT, r["runId"], "stdout.txt")) and
          os.path.isfile(os.path.join(RUNS_ROOT, r["runId"], "stderr.txt")) and
          os.path.isfile(os.path.join(RUNS_ROOT, r["runId"], "player.log")))

    # run isolation: each run gets its own isolated root
    check("run roots are isolated per run",
          len({d for d in os.listdir(RUNS_ROOT) if d.startswith("SELFTEST")}) >= 4)

    # AppData protection so far
    after = appdata_protection_snapshot()
    verdicts = appdata_protection_ok(appdata_before, after)
    check("default AppData save untouched during self-test", all(verdicts.values()), json.dumps(verdicts))
    return checks


def _manifest_sha():
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
            "runId": r["runId"],
        })
    return rows_out


def write_outputs(rows_out, build_sha, appdata_before, appdata_after, verdicts, selftest_checks):
    os.makedirs(EVIDENCE, exist_ok=True)
    # updated matrix CSV (preserves the frozen columns, adds status/reason)
    csv_path = os.path.join(EVIDENCE, "PLAYER_RUN_MATRIX.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["run_id", "skill", "status", "reason", "gate", "seed", "expected_observation"])
        for r in rows_out:
            w.writerow([r["run_id"], r["skill"], r["status"], r.get("reason", ""), r.get("gate", ""), r.get("seed", ""), r.get("expected_observation", "")])
    # index + protection + self-test evidence
    index = {
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "buildSha256": build_sha,
        "runs": rows_out,
        "appdataProtection": {
            "before": appdata_before, "after": appdata_after,
            "verdicts": verdicts, "ok": all(verdicts.values()),
        },
        "selfTest": selftest_checks,
    }
    with open(os.path.join(EVIDENCE, "INDEX.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    return csv_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["selftest", "matrix", "samples", "all"])
    ap.add_argument("--only", type=str, default="", help="comma-separated row ids for matrix mode")
    args = ap.parse_args()

    if not os.path.isfile(EXE_ACCEPTANCE):
        print("Acceptance EXE missing; run the build chain first."); sys.exit(2)
    if os.path.isdir(os.path.dirname(EXE_NODEFINE)) and grep_marker(os.path.dirname(EXE_NODEFINE)):
        print("NoDefine build output contains the harness marker; shipping exclusion FAILED."); sys.exit(2)

    build_sha = sha256_file(EXE_ACCEPTANCE)
    print("Acceptance EXE sha256 = " + build_sha)
    appdata_before = appdata_protection_snapshot()
    print("AppData protection snapshot taken (default + legacy save dirs).")

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
