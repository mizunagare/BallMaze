# CP06-C24-B2-R2 验收表

状态口径：`PASS-STATIC` / `PASS-MODEL` / `PASS-EDITOR` / `PASS-PLAYER` /
`NOT_RUN` / `INCOMPLETE` / `UNRESOLVED`。**不把多层结果汇总成无解释的 PASS**。
基线 `c388e9b7ecf9b5619a65fac81227eba68f61b832`；产品源码零修改。

## 1. 通用验收

| ID | 要求 | 状态 | 证据 |
|---|---|---|---|
| R2-00-1 | 开工重新核对远端完整 SHA，R1 未前进 | **PASS-STATIC** | `Evidence/After/remote-verification.json`、`git ls-remote` |
| R2-00-2 | 从 R1 tip 建立独立 R2 分支，main/B1/B2/R1 历史保护 | **PASS-STATIC** | `protection.json` |
| R2-00-3 | 纯发行包零验证 Boot | **PASS-EDITOR** | `Evidence/Runs/PureBuild1/Editor.exit.json`；`RuntimeInitializeOnLoads.json` 28 项 / 验证 0 |
| R2-00-4 | sidecar 只注入隔离副本，沿用 R1 启动链、不依赖 pwsh | **PASS-EDITOR** | `build_driver.py` / `run_player.py` 与 R1 SHA 一致；各 `driver-injection.json` 的 `copyOnly=true` |
| R2-00-5 | 每用例独立 Run、禁止跨 Run join | **PASS-STATIC** | `r2-strict-correlation.json`：`crossRunJoins=0` |
| R2-00-6 | null/missing 不能 PASS，逐项记录输入行/表达式/结果 | **PASS-STATIC** | `r2_analysis.py` 规则；`r2-player-checks.tsv` |
| R2-00-7 | 保留初始失败、工具失败与所有 NOT_RUN，不覆盖 R1 的 7/7 | **PASS-STATIC** | `Evidence/Player/*-FAILED/`、`DriverBuild1/driver-compile-failed-1.log` |
| R2-00-8 | 冻结合同参数未被事后调整 | **PASS-PLAYER** | 27 个 run 的 `ring-probes.jsonl`：2.2 / 6.0 / 1.2 / 1e-4 / 22 一致 |
| R2-00-9 | 用户文件 / 真实存档 / 历史保护 | **PROTECTION_PASS** | `protection.json`，违规 0 |
| R2-00-10 | 未改产品几何、奖励投影、状态机、伤害、预警、随机流 | **PASS-STATIC** | 纯包 EXE/Assembly SHA 与 R1 逐字一致 |

## 2. R2-01 竖直高度（10/10 PASS-PLAYER）

| ID | 用例 | 期望 `geometry` | 实测 | `applied` | 状态 |
|---|---|---|---|---|---|
| R2-01-1 | `h-in-cc` | TRUE | TRUE | 1 | **PASS-PLAYER** |
| R2-01-2 | `h-tangent-top-cc` | TRUE（闭集切线） | TRUE | 1 | **PASS-PLAYER** |
| R2-01-3 | `h-tangent-bottom-cc` | TRUE（闭集切线） | TRUE | 1 | **PASS-PLAYER** |
| R2-01-4 | `h-just-out-cc` | FALSE（超出 > ε） | FALSE | 0 | **PASS-PLAYER** |
| R2-01-5 | `h-above-cc` | FALSE | FALSE | 0 | **PASS-PLAYER** |
| R2-01-6 | `h-in-cap` | TRUE | TRUE | 1 | **PASS-PLAYER** |
| R2-01-7 | `h-tangent-top-cap` | TRUE | TRUE | 1 | **PASS-PLAYER** |
| R2-01-8 | `h-tangent-bottom-cap` | TRUE | TRUE | 1 | **PASS-PLAYER** |
| R2-01-9 | `h-just-out-cap` | FALSE | FALSE | 0 | **PASS-PLAYER** |
| R2-01-10 | `h-above-cap` | FALSE | FALSE | 0 | **PASS-PLAYER** |

附加检查（每用例）：`controlledHitBodyHeightRecorded`（world center.y 与 `origin.y+centerY` 一致）、
`colliderTypeMatchesCase`（CC / 根 CapsuleCollider）、`horizontalPositionFixed`（半径恒 3.2）、
`bodyCountIsOne`、`singleDamagePerRelease`、`frozenParametersUnchanged` 全部 PASS。
记录真实 Transform / Collider 类型 / center / height / radius / lossyScale / world body。

## 3. R2-02 GameplayPaused（3/3 PASS-PLAYER）

| ID | 用例 | 阶段 | 暂停帧 / 跨度 | Remaining 冻结 | HP / releases | 恢复后 | 状态 |
|---|---|---|---|---|---|---|---|
| R2-02-1 | `pause-warning` | Warning | 584 / 2.22s | 1.59493542 不变 | 24 / 3 恒定 | 3→4 | **PASS-PLAYER** |
| R2-02-2 | `pause-active` | Active | 595 / 2.21s | 0.149999619 不变 | 2 / 4 恒定 | 4→5 | **PASS-PLAYER** |
| R2-02-3 | `timescale-only`（对照） | Warning | 581 / 2.22s | 1.592906 不变 | 24 / 3 恒定 | 3→4 | **PASS-PLAYER** |

| ID | 要求 | 状态 | 说明 |
|---|---|---|---|
| R2-02-4 | 经实际 UI 暂停入口，不写 private 字段 | **PASS-PLAYER** | `PlayerHudPresenter.SetDetails("帮助")` / `SetDetails("")`；`ui-panel-open PASS` |
| R2-02-5 | 记录 until / Remaining / Time.time / unscaledTime / timeScale / HP / state | **PASS-PLAYER** | `pauseBegin`/`pauseEnd`/`pauseResult` + `state-frames.tsv` |
| R2-02-6 | 暂停 ≥2s，期间无扣血、无提前释放 | **PASS-PLAYER** | 上表 paused 帧常量 |
| R2-02-7 | 预警期与 Active 期分别测试 | **PASS-PLAYER** | `bothPhasesCovered=true` |
| R2-02-8 | 不用 timeScale=0 替代 UI-only，两者分别标注 | **PASS-PLAYER** | 对照 case 实测 `GameplayPaused=False`，明确标注 CONTROL |
| R2-02-9 | 「GameplayPaused=true 且 timeScale>0」的 UI-only 组合 | **NOT_RUN** | 产品 UI 入口同时置 `timeScale=0`，该组合无法经产品入口安全进入；未伪造 |

> 产品事实：真实 UI 入口同时产生 `HudPanelOpen=true` 与 `Time.timeScale=0`，
> BossBrain 的 `GameplayPaused || timeScale<=0` 两条件在 UI 路径下不可分离。

## 4. R2-03 取消生命周期（6/8 PASS-PLAYER，2 NOT_RUN）

| ID | 用例 | 阶段 | 取消后 applied | 状态 | 判定 |
|---|---|---|---|---|---|
| R2-03-1 | `cancel-death-w` | Warning | 0 | `Ready` | **PASS-PLAYER** |
| R2-03-2 | `cancel-death-a` | Active | 1（取消前首帧） | `Ready` | **PASS-PLAYER** |
| R2-03-3 | `cancel-leave-w` | Warning | 0 | `Returning` | **PASS-PLAYER** |
| R2-03-4 | `cancel-leave-a` | Active | 1（取消前首帧） | `Returning` | **PASS-PLAYER** |
| R2-03-5 | `cancel-boss-w` | Warning | 0 | `Dead` | **PASS-PLAYER** |
| R2-03-6 | `cancel-boss-a` | Active | 1（取消前首帧） | `Dead` | **PASS-PLAYER** |
| R2-03-7 | `cancel-unload-w` | Warning | 0 | UNLOADED | **NOT_RUN** |
| R2-03-8 | `cancel-unload-a` | Active | 1（取消前首帧） | UNLOADED | **NOT_RUN** |

严格检查：`noAppliedProbeAfterCancel` 按 `cancelTrigger.frame` 逐帧比较（8/8 PASS）、
`productLifecycleEntryUsed`（`hero-dead` / `outside-arena` / `boss-dead` / `return-to-title` 全 PASS）、
`cancelPhaseReached`、`stateAfterCancelNotAttacking` 全 PASS。

| ID | 要求 | 状态 | 说明 |
|---|---|---|---|
| R2-03-9 | 使用真实死亡 / 离场 / 卸载业务路径，不直接 Destroy | **PASS-PLAYER** | `CombatHealth.Damage`、`RestorePosition`、`GameEntry.ReturnToTitle` |
| R2-03-10 | 不补放旧攻击、不残留预警线/伤害窗口 | **PASS-PLAYER** | 触发帧之后无 applied probe；状态非 Warning/Active |
| R2-03-11 | 存档与结算不因诊断工具改变 | **PASS-STATIC** | 独立隔离根，`storage-audit.jsonl` 未越界 |
| R2-03-12 | 场景卸载后 Boss 状态 / Releases | **NOT_RUN** | `ReturnToTitle` 真实卸载并销毁 Boss 对象，`Releases` 不可观测；不编造 |

## 5. R2-04 多 Collider 去重（6/6 PASS-PLAYER）

| ID | 用例 | 组合 | bodyCount | geometry | applied | 状态 |
|---|---|---|---|---|---|---|
| R2-04-1 | `b-none` | 两有效胶囊均不接触 | 2 | FALSE | 0 | **PASS-PLAYER** |
| R2-04-2 | `b-first` | 仅第一个接触 | 2 | TRUE | 1 | **PASS-PLAYER** |
| R2-04-3 | `b-second` | 仅第二个接触 | 2 | TRUE | 1 | **PASS-PLAYER** |
| R2-04-4 | `b-both` | 两个均接触 | 2 | TRUE | 1 | **PASS-PLAYER** |
| R2-04-5 | `b-both-multi` | 双接触 + 27 帧 Active | 2 | TRUE | 1 | **PASS-PLAYER** |
| R2-04-6 | `b-trigger-child` | trigger / child 单独「接触」 | 2 | FALSE | 0 | **PASS-PLAYER** |

`triggerAndChildExcludedFromBodies` PASS：trigger 与子物体 Collider 存在但 `Bodies()` 只计
根对象 enabled 非 trigger 胶囊；每个 body 的 world center / radius / height 记录在
`body-dump.tsv`；任一有效 body 接触即 `geometry=true`，但一次 release 最多 Damage 一次。
未用模型断言代替 Player 运行。

## 6. 总体判定

| 合同 | 用例 | PASS-PLAYER | NOT_RUN | 类别状态 |
|---|---|---|---|---|
| R2-01 竖直高度 | 10 | 10 | 0 | **PASS-PLAYER** |
| R2-02 GameplayPaused | 3 | 3 | 0（另有 1 项 UI-only 组合 NOT_RUN 声明） | **PASS-PLAYER** |
| R2-03 取消生命周期 | 8 | 6 | 2 | **NOT_RUN** |
| R2-04 多 Collider | 6 | 6 | 0 | **PASS-PLAYER** |
| **合计** | **27** | **25** | **2** | `R2_PARTIAL_OR_NOT_RUN` |

**未发现任何产品行为与冻结合同冲突**，未提出最小产品修复，产品源码零修改。
未覆盖项保持 `NOT_RUN`，不伪造通过；R1 的 7/7 核心矩阵未被改写或重跑。

## 7. 复审重点

1. `cancel-unload-w/a` 的 `NOT_RUN` 子项：若需完整验证卸载后 Boss 状态，需在不销毁 Boss
   的前提下设计新的产品观测入口（本批未改产品）。
2. R2-02-9 的 UI-only 组合不可分离是产品事实，请确认是否需要独立设计批次。
3. `pause-warning-A1-FAILED` / `timescale-only-A1-FAILED` 的驱动断言修正记录，
   确认「仅修工具、未改产品/容差」的结论。
