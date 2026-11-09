# CP06-INTEGRATION-02 · 证据索引

全部证据为**独立隔离真实 Player run** 的原始归档（未改写、未拼接）。每个 run 目录含：
`Player.command.json`（启动命令/EXE SHA/驱动 SHA/存储根）、`process.json`、`Player.exit.json`、
`Player.log`、`Player.stdout/stderr`、`assertions.tsv`（逐断言判定）、`int-events.jsonl`
（带身份三元组 runId/processId/buildSha 的产品事件）、`int-frames.tsv`、`complete.txt`、
`run-summary.json`、`entry-audit.jsonl`、`storage-audit.jsonl`、`exe-sha256.txt`。

全量文件 SHA256 清单：[PROTECTION_HASHES.tsv](PROTECTION_HASHES.tsv)（494 个文件 = 32 个 Run 目录 484 个原始文件 + 工具/记录/本索引）。
驱动注入记录（编译器/注入前后状态）：[Tools-records/](Tools-records/)。
验证工具源码（build_driver.py / run_player.py / IntDriver.cs.txt / r1_ledger.py）：[Tools/](Tools/)。

**计数唯一来源**：[../RUN_LEDGER.csv](../RUN_LEDGER.csv)（`Tools/r1_ledger.py` 机械生成）。
本索引与账本一致的口径：**32 个 Run = 17 PASS + 15 FAIL**，其中 `phase=R0` 24 个
（13 PASS / 11 FAIL）、`phase=R1-02` 8 个（4 PASS / 4 FAIL）。
本节 §1/§2 的旧标题「12 个 run / 12 个 FAIL」已按 [../ERRATA.md](../ERRATA.md) 勘误
（forest-loop-6 原被误放入失败表，实为 PASS；R1-02 新增 Run 见 §1.2 / §2.2）。

## 1. 通过的关键 run（R0：9 个模式，13 个 run）

| run | 模式 | PID | 退出码 | 判定 | 驱动 SHA（前 12） |
|---|---|---|---|---|---|
| [forest-loop-6](Player/forest-loop-6) | forest-loop | 33896 | 0 | PASS（历史尝试，被 -7 取代） | 702f14388009 |
| [forest-loop-7](Player/forest-loop-7) | forest-loop | 28376 | 0 | PASS | 702f14388009 |
| [ruins-loop-3](Player/ruins-loop-3) | ruins-loop | 34172 | 0 | PASS | 639be1150848 |
| [cavern-loop-1](Player/cavern-loop-1) | cavern-loop | 21948 | 0 | PASS | 639be1150848 |
| [cavern-boss-1](Player/cavern-boss-1) | cavern-boss | 16688 | 0 | PASS | fb39611031dd |
| [cross-region-chain-1](Player/cross-region-chain-1) | cross-region-chain | 5372 | 0 | PASS | fb39611031dd |
| [xproc-1](Player/xproc-1) | xproc-1 | 21412 | 0 | PASS | fb39611031dd |
| [xproc-2](Player/xproc-2) | xproc-2 | 28352 | 0 | PASS | fb39611031dd |
| [weapon-smoke-2](Player/weapon-smoke-2) | weapon-smoke | 36572 | 0 | PASS | bf239bedd49f |
| [skill-smoke-3](Player/skill-smoke-3) | skill-smoke | 31384 | 0 | PASS | 8093348a0166 |
| [reward-loop-2](Player/reward-loop-2) | reward-loop | 32912 | 0 | PASS | 4d36a70f5885 |
| [fail-paths-2](Player/fail-paths-2) | fail-paths | 33936 | 0 | PASS | 4b69547b8a1b |
| [reward-loop-1](Player/reward-loop-1) | reward-loop（材料不足版） | 36628 | 0 | PASS（crafted=False 如实记录） | 8093348a0166 |

### 1.2 R1-02 新增：弓蓄势贯矢自然释放（4 PASS）

| run | 模式 | PID | 退出码 | 判定 | 断言 PASS/FAIL/SKIP | 说明 |
|---|---|---|---|---|---|---|
| [bow-pierce-natural-4](Player/bow-pierce-natural-4) | bow-pierce-natural | 31824 | 0 | PASS（被 -8 取代） | 55 / 0 / 1 | 首次干净自然释放；无共线对，多目标断言 SKIP |
| [bow-pierce-natural-6](Player/bow-pierce-natural-6) | bow-pierce-natural | 33076 | 0 | PASS（被 -8 取代） | 55 / 0 / 0 | 两发各贯穿 2 目标；cast-2 目标列表因窗口关闭过早未记录 |
| [bow-pierce-natural-7](Player/bow-pierce-natural-7) | bow-pierce-natural | 9088 | 0 | PASS（被 -8 取代） | 55 / 0 / 0 | 窗口修正后 cast2DistinctTargets=1；第二发被升级暂停截断 |
| **[bow-pierce-natural-8](Player/bow-pierce-natural-8)** | bow-pierce-natural | 37188 | 0 | **PASS（采信）** | **56 / 0 / 0** | 半蓄力 + 满蓄力两发自然释放、各贯穿 2 目标、冷却被拒、两发弹体均销毁（含选卡后恢复） |

## 2. 保留的失败历史（R0：11 个 FAIL run，原样保留不改写）

| run | 模式 | PID | 退出码 | 首个失败断言 |
|---|---|---|---|---|
| [forest-loop](Player/forest-loop) | forest-loop | 7560 | 2 | forest-combat-real-damage（damage=0） |
| [forest-loop-2](Player/forest-loop-2) | forest-loop | 35832 | 2 | 同上（dist=2.43） |
| [forest-loop-3](Player/forest-loop-3) | forest-loop | 36156 | 2 | 同上（began=0，stale 状态） |
| [forest-loop-4](Player/forest-loop-4) | forest-loop | 34992 | 2 | 同上（uiBlocked 同帧冲突） |
| [forest-loop-5](Player/forest-loop-5) | forest-loop | 32604 | 2 | 同上（诊断确认 uiBlocked） |
| [ruins-loop](Player/ruins-loop) | ruins-loop | 20484 | 2 | ruins-gather-vein-present |
| [ruins-loop-2](Player/ruins-loop-2) | ruins-loop | 31776 | 2 | 同上（available 空） |
| [weapon-smoke-1](Player/weapon-smoke-1) | weapon-smoke | 1324 | 2 | strike-Sword（过渡期瞬态） |
| [skill-smoke-1](Player/skill-smoke-1) | skill-smoke | 2804 | 2 | skill-use-cavern-s2（共享冷却） |
| [skill-smoke-2](Player/skill-smoke-2) | skill-smoke | 17860 | 2 | staff-projectile-forest（计数过滤） |
| [fail-paths-1](Player/fail-paths-1) | fail-paths | 12500 | 2 | forest-depart（未 ack） |

### 2.2 R1-02 新增：弓自然释放过程中的 4 个驱动缺陷 Run（原样保留）

| run | PID | 退出码 | 首个失败断言 | 根因（驱动侧，非产品缺陷） |
|---|---|---|---|---|
| [bow-pierce-natural-1](Player/bow-pierce-natural-1) | 36880 | 2 | bow-pierce-contact-1（contacts=0,blocked=1） | 用敌人自身 Y 取射击点 → 英雄在地形以下，弹体撞地；冷却断言置于飞行等待之后 |
| [bow-pierce-natural-2](Player/bow-pierce-natural-2) | 11400 | 2 | bow-muzzle-height（muzzle.y=0.3128） | 假设弓 Muzzle 在胸口，实际弓弦源约 +0.30m |
| [bow-pierce-natural-3](Player/bow-pierce-natural-3) | 22280 | 2 | bow-charging-2（timeout=5） | 冷却后未重新 `PlayerInput.Focus(true)`，按键无 Down 边沿 |
| [bow-pierce-natural-5](Player/bow-pierce-natural-5) | 9696 | 2 | bow-projectile-lifecycle-2（timeout=8） | 未考虑产品在 `timeScale=0` 时按设计冻结弹体；重复命中用了跨弹体全局计数 |

## 2.3 其它交付文档

| 文件 | 作用 |
|---|---|
| [../RUN_LEDGER.csv](../RUN_LEDGER.csv) | 32 个 Run 的唯一分类账本（含 runId/pid/exitCode/category/firstFailure/evidencePath） |
| [../NON_RUN_ATTEMPTS.csv](../NON_RUN_ATTEMPTS.csv) | 20 条构建/工具尝试，全部 `playerRunCounted=no` |
| [../ERRATA.md](../ERRATA.md) | 旧统计 14/12/12 的勘误、原因与最终值；R1-02 追加口径 |
| [../FOREST_RUN_ID_PROVENANCE.md](../FOREST_RUN_ID_PROVENANCE.md) | forest-loop-7 的 Run ID 来源（**DIRECT**，含行号与 SHA256） |

驱动 SHA 演进（注入记录见 Tools-records/driver-injection.json）：`2be68005` → `441e478e` →
`42b9b638` → `f7b90bff` → `9741ccf8` → `f8c27e13` → `702f1438` → `405e8a2f` → `639be115` →
`fb396110` → `bf239bed` → `ec19ecde` → `8093348a` → `4d36a70f` → `4b69547b`（R0 最终）。
每次演进对应 [REPORT.md](../REPORT.md) §3.2 的一项根因修复。

R1-02 驱动演进（回执与编译日志在 `Evidence/driver-injection.json` / `Evidence/driver-compile.log`，
因为 `build_driver.py --evidence` 指向 `Evidence/`；R0 的旧回执保留在 `Tools-records/` 未动）：

| 阶段 | driverDllSHA256（前 16） | 变更 |
|---|---|---|
| R1-02 iter 1～7 | 逐次覆盖（未单独归档） | 见 [../NON_RUN_ATTEMPTS.csv](../NON_RUN_ATTEMPTS.csv) DRV-04～DRV-11 |
| 最终（采信） | **`558c7b1b19a42279…`** | 引用 `UnityEngine.UI/UIModule/TextRenderingModule`；`WaitLifecycle` 遇产品冻结先记录再经 `HeroProgression.SelectChoice` 恢复；`bow-pierce-natural-8` 的 `Player.command.json` 记录同一 SHA |

（`bow-pierce-natural-6` 为 `014bf19f…`、`-7` 为 `e841e01f…`、`-8` 为 `558c7b1b…`，
每次 Run 的 `Player.command.json` 都记录当次注入的驱动 SHA，可逐 Run 复核。）

## 3. 构建身份证据

- 纯构建身份 sidecar 与哈希：[../PLAYABLE_CANDIDATE_BUILD.md](../PLAYABLE_CANDIDATE_BUILD.md)
- 每个 run 的 `Player.command.json` 记录当次 `exeSHA256`（全部等于纯构建
  `001aeebf…`）与 `driverDllSHA256`（仅观察副本注入）。

## 4. 保护证据

- 全部 run 存储根隔离（`I:/WGInt02Runs/<run>`），`fail-isolated-save` PASS；
  xproc-2 存档复制字节一致性：`Player/xproc-2/storage-copy-manifest-{before,after}.txt` diff 为空。
- 产品源码零改动：交付时 `git status` 仅本交付目录为未跟踪新增。
