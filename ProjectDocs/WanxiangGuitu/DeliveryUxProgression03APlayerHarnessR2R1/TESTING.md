# TESTING — PH-R2-R1 测试与自检

> 本文件回答：**"这些结论是怎么测出来的？别人能不能重跑？"**

---

## 1. 环境

| 项 | 值 |
|---|---|
| Unity | `6000.6.5f1`（`C:\Program Files\Unity\Hub\Editor\6000.6.5f1\Editor\Unity.exe`） |
| 平台 | StandaloneWindows64，Development Build |
| 运行方式 | **窗口化真实 Player**（不加 `-batchmode`：`CombatSaveSystem.Start` 在 batch mode 下 `yield break`，存档系统不初始化 → 必然挂起） |
| Harness 版本 | `VERSION = 2` |
| 编译开关 | Acceptance 构建含 `UX_ACCEPTANCE`；NoDefine 构建不含 |
| Run 隔离 | 每次运行独立 `-data-root` / `-wanxiang-storage-root` / `-logFile` |
| 单 Run 硬超时 | 180s（自检中另有 6s / 8s / 60s / 90s 的定向超时用例） |

---

## 2. 测试批次入口

```bash
cd /i/unity/WanxiangGuitu

# 0) 重建（三段，任一段失败即中止）
#    SetAcceptanceDefine(true) → BuildAcceptance → BuildNoDefine
#    （本次构建日志：Builds/r1_set.log / r1_acc.log / r1_nodef.log，rc 均为 0）

# 1) 生成统一构建清单（从实际产物回读）
python player_acceptance_driver.py manifest

# 2) 定向批次 A–E
python player_acceptance_driver.py r1

# 3) 纯读复算（不启动 Player，可随时重跑）
python player_acceptance_driver.py recompute
```

产物：`Evidence/PH-R2-R1/{build,runs,selftest,protection}/`、`INDEX.json`、`RECOMPUTE.json`。

---

## 3. A–E 执行结果

| 阶段 | 内容 | 结果 |
|---|---|---|
| A | 构建身份冒烟 | `manifestReasons=[]`，marker 正确，buildId `phr2r1-318c66…` |
| B | `sword.triple`（C-gate） | **PASS**（15s，pid 10600） |
| C | `twin.counter` | **PASS**（19s，pid 5256） |
| D | `staff.field` | **PASS**（17s，pid 31932） |
| E | 自检 18 + 5 | **23/23 PASS** |

---

## 4. 自检 23 项明细（原始输出见 `selftest/SELFTEST.json` 与 `console.log`）

### 4.1 原有 18 项（PH-R1 起沿用，未删减）

| # | 检查项 | 结果 | 说明 |
|---|---|---|---|
| 1 | acceptance build output contains harness marker | PASS | DLL/EXE 双编码扫描 |
| 2 | NoDefine (shipping-equivalent) build output lacks harness marker | PASS | 出货等价隔离 |
| 3 | EXE sha matches build manifest | PASS | `b70442f9…` |
| 4 | C-gate positive run PASS with identity + freshness enforced | PASS | 真实 Player |
| 5 | KeyDown events recorded | PASS | 跨帧按键（同帧 down+up 会被 InputSystem 合并） |
| 6 | KeyUp events recorded | PASS | |
| 7 | skill start observed | PASS | |
| 8 | skill complete observed | PASS | |
| 9 | entry authorized via public API | PASS | 非后门注入 |
| 10 | C-gate: real target damage captured | PASS | `realDamageCaptured=true` |
| 11 | damage-events.jsonl artifact present | PASS | 原始证据落盘 |
| 12 | target-events.jsonl artifact present | PASS | 双路互证 |
| 13 | stale/old result.json is rejected | PASS | 预置 1 小时前的 result.json → 拒收 |
| 14 | wrong buildSha is rejected | PASS | 传 `DEADBEEFWRONG` → 身份不符 |
| 15 | timeout produces FAIL (never PASS) | PASS | 6s 超时，退出码 1 |
| 16 | timeout run preserved stdout/stderr/player.log | PASS | 失败证据不丢 |
| 17 | run roots are isolated per run | PASS | ≥4 个独立根目录 |
| 18 | default AppData save untouched during self-test | PASS | default + legacy 均未变 |

### 4.2 新增 5 项（身份）

| # | 检查项 | 方法 | 结果 |
|---|---|---|---|
| ID-1 | wrong DLL SHA is rejected by a real Player run | 真实启动 Player，`--expected-dll-sha` 传全零；Player 自算 `b3ce427c…` → `identityVerified=false` → `exitCode=1` | PASS |
| ID-2 | Player internal DLL SHA mismatch is rejected | 篡改 `loadedAssemblySha256` + `identityVerified=false` → `verify_run_identity` 返回非空 | PASS |
| ID-3 | DLL change before/after run is rejected | 篡改 `dllShaAfter` → 非空 | PASS |
| ID-4 | manifest vs actual DLL mismatch is rejected | 篡改 manifest `acceptanceDllSha256` → `verify_manifest` 非空 | PASS |
| ID-5 | run-manifest exitCode/identity/finalStatus recorded correctly | 校验 `exitCode=0 ∧ timedOut=false ∧ finalStatus=PASS ∧ identityVerified=true ∧ resultJsonSha256` 与实际文件一致 | PASS |

> ID-1 是**真实 Player 负向测试**，不是 mock。它同时证明了"Player 自己算 SHA"这件事：
> 若只是回写命令行，`loadedAssemblySha256` 会是全零且 `identityVerified=true`。

### 4.3 自检覆盖的失败路径

| 场景 | 期望 | 实测 |
|---|---|---|
| result.json 陈旧 | FAIL（拒收旧证据） | `result.json is stale (modified before this run started)` |
| buildSha 不符 | FAIL | `identity mismatch: result.buildSha=DEADBEEFWRONG` |
| DLL 期望值不符 | FAIL + identityNotes | `identityReasons=[…identityVerified is not true…]` |
| 超时 | FAIL（绝不 PASS） | `exitCode=1, timedOut=true`，日志保留 |
| 产物运行中变化 | FAIL（ID-3 覆盖） | 篡改即非空 |

---

## 5. 独立复算（40 项，不启动 Player）

`python player_acceptance_driver.py recompute` 只读 `result.json` + 两路 JSONL：

| Run | 校验数 | 通过 |
|---|---|---|
| C-GATE | 11 | 11 |
| TWIN-COUNTER | 18 | 18 |
| STAFF-FIELD | 11 | 11 |
| **合计** | **40** | **40** |

复算内容见 `DAMAGE_MODEL.md` §3。它的意义是：**报告的每个数字都能从原始证据重算**，
不需要相信 Harness 的 `pass` 字段。

---

## 6. 失败历史保留

| 项 | 状态 |
|---|---|
| PH-R1 证据（466 个 skip-worktree 文件） | 未覆盖，SHA 复核 311/311 一致 |
| PH-R2 证据（`Evidence/PH-R2/`、`Evidence/Runs/`） | 未覆盖，同上 |
| 本批失败运行 | 全部保留：`SELFTEST-stale-*`、`SELFTEST-wrongsha-*`、`SELFTEST-timeout-*`、`SELFTEST-wrongdllsha-*` |
| 唯一被覆盖的对象 | PH-R2 阶段的 `DeliveryUxProgression03APlayerHarnessR2/`（上一批交付物，按任务书要求由本批新报告取代；该目录未提交） |

**"删掉失败用例让报告变干净"是本项目明令禁止的操作**；本批的 4 个负向运行目录连同
`run-manifest.json`（`finalStatus=FAIL`）一并留档。

---

## 7. 可重复性说明

| 项 | 是否可逐位复现 | 说明 |
|---|---|---|
| DLL / EXE SHA | 是（同源代码 + 同 Unity 版本） | 本次构建三段 rc=0，产物指纹已记录 |
| 伤害数值 | 是 | 目标属性固定（AP=33，HP=140），倍率来自产品常量 |
| 冷却实测值 | 否（±毫秒级抖动） | 7.10633 / 9.106946 / 9.497；判定用容差 −0.6/+1.5 |
| 命中时刻 | 否（帧时序相关） | 只校验严格递增，不校验绝对值 |
| 身份链 | 是 | 三方 SHA 逐位比对 |

> 结论层面的可复现性来自"容差 + 结构校验 + 身份闭合"，而非"每次跑出同一串小数"。
