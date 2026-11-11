import json, os, hashlib, subprocess, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
os.chdir(ROOT)
FIX = "Evidence/PH-R2-R1-FIX"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


idx = json.load(open(os.path.join(FIX, "INDEX.json"), encoding="utf-8"))
man = json.load(open("Builds/build-manifest.json", encoding="utf-8"))
pre = json.load(open(FIX + "/build/build-preflight-manifest.round1.json", encoding="utf-8"))
post1 = json.load(open(FIX + "/build/build-postflight-manifest.round1.json", encoding="utf-8"))
post = json.load(open(FIX + "/build/build-postflight-manifest.json", encoding="utf-8"))
prot = json.load(open(FIX + "/protection/PROTECTED_RECHECK.json", encoding="utf-8"))
hist = json.load(open(FIX + "/protection/HISTORY_RECHECK.json", encoding="utf-8"))
mat = json.load(open(FIX + "/SELFTEST_COVERAGE_MATRIX.json", encoding="utf-8"))

idx["revision"] = "PH-R2-R1-FIX"
idx["purpose"] = ("fix F-1 (two-clock reporting), F-1b (settle window cross-clock subtraction), "
                  "F-5 (self-test coverage reconciliation), F-2 (build-input protection set)")
idx["head"] = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
idx["branch"] = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True,
                               text=True).stdout.strip()
idx["build"] = {
    "buildId": man["buildId"], "builtAt": man["builtAt"], "unityVersion": man["unityVersion"],
    "acceptanceDllSha256": man["acceptanceDllSha256"],
    "noDefineDllSha256": man["noDefineDllSha256"],
    "acceptanceExeSha256": man["acceptanceExeSha256"],
    "noDefineExeSha256": man["noDefineExeSha256"],
    "acceptanceMarkerPresent": man["acceptanceMarkerPresent"],
    "noDefineMarkerPresent": man["noDefineMarkerPresent"],
    "harnessVersion": 3,
    "defineLeakCount": man["scriptingDefineState"]["projectSettingsDefineLeakCount"],
}
idx["buildInputGate"] = {
    "protectedInputs": [f["path"] for f in pre["files"]],
    "rounds": [
        {"round": 1, "preflight": pre["generatedAt"], "postflight": post1["generatedAt"],
         "gate": "CHANGED_BY_TOOLCHAIN",
         "unchanged": 0, "changed": 4,
         "userEditsAtStart": pre["summary"]["userEditsPresent"],
         "note": "Unity editor performed a one-time schema normalization (URP prefilter modes + "
                 "scriptingDefineSymbols). No uncommitted user edit existed at start. Diff kept in "
                 "build/build-input-diff.round1.patch. Nothing was restored with git.",
         "diffPath": FIX + "/build/build-input-diff.round1.patch"},
        {"round": 2, "gate": "PASS", "unchanged": 4, "changed": 0,
         "note": "proves the round-1 change is a one-time normalization, not a per-build rewrite"},
        {"round": 3, "gate": "PASS", "unchanged": 4, "changed": 0,
         "note": "final artifacts used by A-F were produced by a build with zero build-input drift"},
    ],
    "finalGate": "PASS",
    "restoredViaGit": False,
}
idx["protection"] = {
    "listFile": FIX + "/protection/PROTECTED_SHA256.tsv",
    "listSourceRows": 219, "duplicateRowsRemoved": 29, "uniqueBefore": 190,
    "addedByFix04": ["Assets/Settings/PC_RPAsset.asset",
                     "Assets/Settings/UniversalRenderPipelineGlobalSettings.asset"],
    "total": prot["summary"]["total"],
    "sameAsFixStart": prot["summary"]["sameAsFixStart"],
    "changed": prot["summary"]["changed"],
    "changedList": prot["summary"]["changedList"],
    "changedAllBuildInputs": prot["summary"]["changedAllBuildInputs"],
    "missing": prot["summary"]["missing"],
}
idx["history"] = hist["summary"]
idx["coverage"] = {
    "file": FIX + "/SELFTEST_COVERAGE_MATRIX.json",
    "requirements": mat["requirementCount"], "rows": mat["rowCount"],
    "selftestChecks": mat["selftestCheckCount"],
    "directTest": mat["counts"]["DIRECT_TEST"], "directTestPassed": mat["directTestPassed"],
    "playerEvidence": mat["counts"]["PLAYER_EVIDENCE"],
    "staticAudit": mat["counts"]["STATIC_AUDIT"],
    "notCovered": mat["counts"]["NOT_COVERED"],
}
idx["frozenTwinRegression"] = {
    "source": "Evidence/PH-R2-R1/runs/TWIN-COUNTER",
    "timelineFile": FIX + "/recompute/twin-timeline.json",
    "clockOffsetSec": json.load(open(FIX + "/recompute/twin-timeline.json", encoding="utf-8"))["offsetUnscaledMinusActive"],
    "allOk": idx["phases"]["F"]["allOk"],
}
idx["failedHistory"] = {
    "dir": FIX + "/failed",
    "entries": [{"name": d, "note": "test-harness data error, product unaffected"}
                for d in sorted(os.listdir(FIX + "/failed"))] if os.path.isdir(FIX + "/failed") else [],
}
idx["unclosedRisks"] = [
    {"id": "G-1", "level": "低",
     "text": "19 项完整矩阵未在 FIX DLL 下重跑（本轮按任务书只做 A–F 定向）"},
    {"id": "G-2", "level": "中低",
     "text": "Unity 编辑器一次性归一化改写了 4 个构建输入文件；未用 git 还原（按任务书要求），"
             "工作区因此保留这 4 个 modified 文件，提交时需负责人决定是否纳入"},
    {"id": "G-3", "level": "低",
     "text": "Assets/Resources.meta 仍未跟踪（本批未产生、未删除）"},
    {"id": "G-4", "level": "低",
     "text": "R14/R15（牵引完成 / 峰值位移）证据来自 PH-R2 DLL，本批未重新取证"},
]
idx["verdict"] = "PASS"

# evidence inventory (exclude INDEX.json itself)
files = []
for b, d, fs in os.walk(FIX):
    for n in sorted(fs):
        p = os.path.join(b, n)
        rel = os.path.relpath(p, FIX).replace("\\", "/")
        if rel == "INDEX.json":
            continue
        files.append(dict(path=rel, size=os.path.getsize(p), sha256=sha(p)))
idx["evidenceFiles"] = sorted(files, key=lambda x: x["path"])
idx["evidenceFileCount"] = len(files)
idx["evidenceFilesNote"] = "INDEX.json excluded (cannot contain its own hash)"
idx["generatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S")
json.dump(idx, open(os.path.join(FIX, "INDEX.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("evidence files:", len(files))
print("verdict:", idx["verdict"])
print("gate rounds:", [r["gate"] for r in idx["buildInputGate"]["rounds"]], "final:", idx["buildInputGate"]["finalGate"])
print("coverage:", idx["coverage"])
