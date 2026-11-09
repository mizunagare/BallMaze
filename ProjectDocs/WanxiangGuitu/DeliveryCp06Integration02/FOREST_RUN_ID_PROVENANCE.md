# FOREST_RUN_ID_PROVENANCE · forest-loop-7 的 Run ID 来源核查（R1-03）

> 结论：**DIRECT（同一 Run 内的直接观测）**。
> 不是从存档推导，也不是从后续事件反推。
> 旧标注 `PASS(deduced later)` 属过度保守的误标，勘误见
> [ERRATA.md](ERRATA.md)；本文件给出可直接核对的原文位置。

## 1. 结论摘要

| 项目 | 值 |
|---|---|
| 被核查 Run | `forest-loop-7`（mode=`forest-loop`） |
| 产品 Run ID | `2582537b781d4607b82740bef2defc9d` |
| 来源类型 | **DIRECT** — 出征帧内直接读取 `AdventureFlow.ActiveRun.runId` 并写入事件，与同一 Run 的结算字段互相印证 |
| 身份三元组 | driver `runId=int02-5cb6d85811a74242b64fcf8e51113041`，`processId=28376`，`buildSha=4ce1624c…`（`Assembly-CSharp.dll`；EXE 为 `001aeebf…`） |
| 观测帧 | `frame=12`（出征）/ `263`（真实击杀）/ `466`（拾取）/ `3189`（结算+回营+再出征） |
| 再出征新 Run ID | `da9614b1196840cbb67108bbb9372981`（与前者不同，证明“再次出征”产生新冒险） |

## 2. 直接证据（原文位置）

文件：`Evidence/Player/forest-loop-7/int-events.jsonl`
SHA256：`d5f28248adc1e43318a9fd8fc63c3aefb97d33b13dc54592460d0b7cca4069d6`

| 行号 | kind/stage | 关键字段（原文值） |
|---|---|---|
| 1 | `identity`/`driver-start` | `runId=int02-5cb6d85811a74242b64fcf8e51113041`，`processId=28376`，`buildSha=4ce1624c77141e2da6878c29082b8e62e7ac26a5cce3b03518a201992fb4a4e3` |
| **2** | `region-depart`/`entered` | `frame=12`，**`productRunId=2582537b781d4607b82740bef2defc9d`**，`regionId=ForestRuins`，`seed=37898320`，`genVersion=8`，`contentRevision=NWD1:3\|B06-B4-R1` |
| 3 | `combat`/`real-hit` | `frame=263`，`productRunId=2582537b…`（逐事件携带同一身份），`detail=enemy=enemy:0,damage=33,strikes=3,began=2` |
| 4 | `gather`/`picked` | `frame=466`，`productRunId=2582537b…`，`detail=kind=Wood,amount=5` |
| **5** | `settle`/`returned-to-camp` | `frame=3189`，`productRunId=2582537b…`，**`settlementId=2582537b781d4607b82740bef2defc9d:terminal`**，**`committedRun=2582537b781d4607b82740bef2defc9d`**，`outcome=Death` |
| 6 | `region-depart`/`entered` | `frame=3189`，`productRunId=da9614b1196840cbb67108bbb9372981`（再出征，新 Run） |

文件：`Evidence/Player/forest-loop-7/assertions.tsv`
SHA256：`149e8198f4166d0f1977d9472681791ed123fa7716fb8dbf6b6c61f7d159eacb`

| 行号 | 断言 | 判定 | 原文 detail |
|---|---|---|---|
| 8 | `forest-run-id` | PASS | `2582537b781d4607b82740bef2defc9d` |
| 29 | `forest-redeploy-new-run` | PASS | `old=2582537b781d4607b82740bef2defc9d,new=da9614b1196840cbb67108bbb9372981` |

## 3. 为什么算 DIRECT 而不是 DERIVED

- 该值在**出征当帧**由 `DepartRegion()` 从产品的运行态字段
  `session.Flow.ActiveRun.runId` 读取并立即写入 `region-depart` 事件
  （`IntDriver.cs.txt` 中 `Emit(new Ev{ kind="region-depart", …, detail="runId="+productRunId+… })`），
  同时 `Emit()` 无条件写入 `productRunId` 字段——即“观测点 = 产品运行态”，
  不是事后从存档或后续事件推断。
- 存在**第二个独立的产品侧字段**互相印证：结算事件的 `settlementId` 前缀与
  `committedRun` 均为同一 `runId`。若该 ID 是驱动自造或反推，不可能同时出现在
  结算标识里。
- 该 ID 在 Run 内 **4 个不同帧**（12/263/466/3189）的 4 条事件上保持一致，
  且再出征后变为新 ID——排除“单点偶然值”。

**边界声明（不夸大）**：候选产品本身**不向日志输出 runId**（`Player.log` 中该字符串出现 0 次；
`entry-audit.jsonl` 的 `run` 字段为空）。因此“DIRECT”指的是**同 Run 内对产品运行态的直接观测**，
而非“产品自带遥测日志”。这一点与 `DERIVED`（存档/后续事件反推）有本质区别，故不降级。

## 4. 其它文件的核查结果（均不含 runId，避免误引）

| 文件 | SHA256 | 是否含 `2582537b…` | 说明 |
|---|---|---|---|
| `run-summary.json` | `70bdda465cbb784e73653fee8f743ef970ed7620ad5901665c14c499701f259c` | 0 次 | 该文件为 `run_player.py` 的**启动/退出归档摘要**（含 pid/exitCode/EXE SHA/驱动 SHA），不含产品 Run ID |
| `int-frames.tsv` | `90cf87223e814641bfb1bfb8f843bf58d586801ad62b7c7b24dc1d044624b631` | 0 次 | 逐帧状态（phase/fields/spawns），无身份字段 |
| `entry-audit.jsonl` | `45241538bc0b9ce0a3c99397aa2836f8a17699bb5e9829480f6ef27a5e46f27c` | 0 次 | 只有 boot/title/game-ready 相位，`run` 字段为空 |
| `Player.log` | `6a703a7df2faca7b0048ca340e30453ebb4ff40cd4ce1556400c1403c45e5595` | 0 次 | 产品日志不含 runId |
| `Player.command.json` | `b7665bdbdedc34120a61989a13053ff181e5c19cffe2051be2cd206f28fd354c` | 0 次 | 启动参数 + `exeSHA256=001aeebf…` + `driverDllSHA256=702f1438…` |
| `process.json` | `0422a8a21ac688e381c6a9c715ef44309b75b068beba7c91da05edd228cb6dee` | 0 次 | pid/退出码 |
| `complete.txt` | `2f9acb02faa121bb2a3621951f57b4c690655337edee2e5ac350be2b3be88ea8` | 0 次 | `PASS` |

## 5. 对交付文档的处置

- `THREE_REGION_RUN_MATRIX.csv` 中该行的 `runId` 列由 `PASS(deduced later)`
  更正为 **`DIRECT(int-events.jsonl:2 productRunId=2582537b…;also settle settlementId/committedRun)`**。
- 未为此重跑森林完整循环（Run ID 已可安全关联，无需新 Run）。
- 其它 Run 的 Run ID 来源沿用同一判定口径：只要 `int-events.jsonl` 的 `region-depart`
  （或 `xproc` `resumed-part2`）行携带 `productRunId`，即记 **DIRECT**；
  `xproc-2` 的产品 Run ID 由 `CombatSaveSystem.InspectReadOnly` 读盘并与
  `xproc-expect.txt` 比对，来源类型记 **DIRECT-DISK**（跨进程，明确区分）。
