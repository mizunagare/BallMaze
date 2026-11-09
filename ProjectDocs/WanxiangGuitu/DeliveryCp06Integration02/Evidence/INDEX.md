# CP06-INTEGRATION-02 · 证据索引

全部证据为**独立隔离真实 Player run** 的原始归档（未改写、未拼接）。每个 run 目录含：
`Player.command.json`（启动命令/EXE SHA/驱动 SHA/存储根）、`process.json`、`Player.exit.json`、
`Player.log`、`Player.stdout/stderr`、`assertions.tsv`（逐断言判定）、`int-events.jsonl`
（带身份三元组 runId/processId/buildSha 的产品事件）、`int-frames.tsv`、`complete.txt`、
`run-summary.json`、`entry-audit.jsonl`、`storage-audit.jsonl`、`exe-sha256.txt`。

全量文件 SHA256 清单：[PROTECTION_HASHES.tsv](PROTECTION_HASHES.tsv)（370 行）。
驱动注入记录（编译器/注入前后状态）：[Tools-records/](Tools-records/)。
验证工具源码（build_driver.py / run_player.py / IntDriver.cs.txt）：[Tools/](Tools/)。

## 1. 通过的关键 run（9 个模式，12 个 run）

| run | 模式 | PID | 退出码 | 判定 | 驱动 SHA（前 12） |
|---|---|---|---|---|---|
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

## 2. 保留的失败历史（12 个 FAIL run，原样保留不改写）

| run | 模式 | PID | 退出码 | 首个失败断言 |
|---|---|---|---|---|
| [forest-loop](Player/forest-loop) | forest-loop | 7560 | 2 | forest-combat-real-damage（damage=0） |
| [forest-loop-2](Player/forest-loop-2) | forest-loop | 35832 | 2 | 同上（dist=2.43） |
| [forest-loop-3](Player/forest-loop-3) | forest-loop | 36156 | 2 | 同上（began=0，stale 状态） |
| [forest-loop-4](Player/forest-loop-4) | forest-loop | 34992 | 2 | 同上（uiBlocked 同帧冲突） |
| [forest-loop-5](Player/forest-loop-5) | forest-loop | 32604 | 2 | 同上（诊断确认 uiBlocked） |
| [forest-loop-6](Player/forest-loop-6) | forest-loop | 33896 | 0 | PASS（英雄随后死亡为合法战果） |
| [ruins-loop](Player/ruins-loop) | ruins-loop | 20484 | 2 | ruins-gather-vein-present |
| [ruins-loop-2](Player/ruins-loop-2) | ruins-loop | 31776 | 2 | 同上（available 空） |
| [weapon-smoke-1](Player/weapon-smoke-1) | weapon-smoke | 1324 | 2 | strike-Sword（过渡期瞬态） |
| [skill-smoke-1](Player/skill-smoke-1) | skill-smoke | 2804 | 2 | skill-use-cavern-s2（共享冷却） |
| [skill-smoke-2](Player/skill-smoke-2) | skill-smoke | 17860 | 2 | staff-projectile-forest（计数过滤） |
| [fail-paths-1](Player/fail-paths-1) | fail-paths | 12500 | 2 | forest-depart（未 ack） |

驱动 SHA 演进（注入记录见 Tools-records/driver-injection.json）：`2be68005` → `441e478e` →
`42b9b638` → `f7b90bff` → `9741ccf8` → `f8c27e13` → `702f1438` → `405e8a2f` → `639be115` →
`fb396110` → `bf239bed` → `ec19ecde` → `8093348a` → `4d36a70f` → `4b69547b`（最终）。
每次演进对应 [REPORT.md](../REPORT.md) §3.2 的一项根因修复。

## 3. 构建身份证据

- 纯构建身份 sidecar 与哈希：[../PLAYABLE_CANDIDATE_BUILD.md](../PLAYABLE_CANDIDATE_BUILD.md)
- 每个 run 的 `Player.command.json` 记录当次 `exeSHA256`（全部等于纯构建
  `001aeebf…`）与 `driverDllSHA256`（仅观察副本注入）。

## 4. 保护证据

- 全部 run 存储根隔离（`I:/WGInt02Runs/<run>`），`fail-isolated-save` PASS；
  xproc-2 存档复制字节一致性：`Player/xproc-2/storage-copy-manifest-{before,after}.txt` diff 为空。
- 产品源码零改动：交付时 `git status` 仅本交付目录为未跟踪新增。
