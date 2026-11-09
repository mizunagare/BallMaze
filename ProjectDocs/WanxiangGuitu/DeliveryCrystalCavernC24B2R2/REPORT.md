# CP06-C24-B2-R2 交付报告：晶环剩余四项 Player 合同补测

状态：**已完成、已推送、暂停等待复审**
分支：`fix/cp06-crystal-warden-b2-r2`
基线：`c388e9b7ecf9b5619a65fac81227eba68f61b832`（R1 tip）
范围：只补 R1 明确列出的四项 `NOT_RUN`；**产品源码零修改**；不重做 R1 已通过的 7/7 核心矩阵。

---

## 1. 完整 SHA 与分支

| 对象 | 完整 SHA | 状态 |
|---|---|---|
| `origin/main` | `72db192a527bd256e2ba18cd7ab334d8334051da` | 开工/收尾均未移动 |
| `origin/fix/cp06-crystal-warden-b1` | `a013c15aae15e17af6a7596a022f01f56a745c34` | 未变 |
| `origin/fix/cp06-crystal-warden-b2` | `98924a34b6df817aa5a979b50439a4515881744b` | 未变 |
| `origin/fix/cp06-crystal-warden-b2-r1`（基线） | `c388e9b7ecf9b5619a65fac81227eba68f61b832` | 开工核对未前进、收尾未变 |
| 本批分支 tip | 见 `Evidence/After/remote-verification.json` | 推送后 `git ls-remote` 复核 |

## 2. 构建链（沿用 R1，不依赖 PowerShell 7）

| 项 | 值 |
|---|---|
| Unity | `6000.6.5f1`，`WanxiangBuild.ValidateBuild` 退出码 0，`result=Succeeded errors=0 warnings=2` |
| 正式纯包 | `I:/WGCombat/C24B2R2-1109-A/PureBuild1/Release` |
| 纯包 EXE SHA256 | `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a` |
| 纯包 `Assembly-CSharp.dll` SHA256 | `3763776a762c00d25761d952b7cb4d881203fc3a43c568f1550eec7c412e6002` |
| 纯包验证 Boot 条目 | **0**（`RuntimeInitializeOnLoads.json` 共 28 项） |
| 与 R1 纯包 | EXE / Assembly SHA **逐字一致**，证明 R2 未改产品源码 |
| sidecar | `build_driver.py` / `run_player.py` 与 R1 版本哈希一致；仅 `R2Driver.cs.txt` 为本批新增，只注入隔离副本 |

`Bodies()` 仅用于记录受击体快照（`body-dump.tsv`），**判定完全来自真实 `RingProbe.geometry`**；
未用 `Touches()` 模型代替 Player，未写 private 字段伪造暂停，未 `Destroy` 对象绕过生命周期。

## 3. R2-01 竖直攻击带与不同高度受击体 —— **10/10 PASS-PLAYER**

水平位置固定 `origin + dir*3.2`（`dr=0`），差异只来自高度。
`body.center.y = origin.y(0.08) + Collider.center.y`，`stem=0.6`，`reach=radius+ε=0.4001`。

| 用例 | 受击体 | world center.y | `geometry` | `applied` | HP |
|---|---|---|---|---|---|
| `h-in-cc` | CharacterController | 1.08 | TRUE | 1 | 24→2 |
| `h-tangent-top-cc` | CharacterController | 2.28 | **TRUE**（上端闭集切线） | 1 | 24→2 |
| `h-tangent-bottom-cc` | CharacterController | −2.12 | **TRUE**（下端闭集切线） | 1 | 24→2 |
| `h-just-out-cc` | CharacterController | 2.29 | FALSE（`vgap=0.41>reach`） | 0 | 24→24 |
| `h-above-cc` | CharacterController | 3.08 | FALSE | 0 | 24→24 |
| `h-in-cap` | 根 CapsuleCollider | 1.08 | TRUE | 1 | 24→2 |
| `h-tangent-top-cap` | 根 CapsuleCollider | 2.28 | TRUE | 1 | 24→2 |
| `h-tangent-bottom-cap` | 根 CapsuleCollider | −2.12 | TRUE | 1 | 24→2 |
| `h-just-out-cap` | 根 CapsuleCollider | 2.29 | FALSE | 0 | 24→24 |
| `h-above-cap` | 根 CapsuleCollider | 3.08 | FALSE | 0 | 24→24 |

每个用例记录真实 Transform / Collider 类型 / `center` / `height` / `radius` / `lossyScale` /
world body / `RingProbe` 全字段 / HP 前后 / runId / PID / buildSha / frame / time / release。
冻结参数 `2.2 / 6.0 / 1.2 / 1e-4 / 22` 逐用例一致，**未事后调容差或半径**。

## 4. R2-02 GameplayPaused 冻结与顺延 —— **3/3 PASS-PLAYER**

经**实际 UI 入口** `PlayerHudPresenter.Instance.SetDetails("帮助")` / `SetDetails("")`，
记录产品真实 `Time.timeScale`（UI 面板打开时为 0），暂停时长 ≥ 2 秒（用 `Time.realtimeSinceStartup` 计时）。

| 用例 | 阶段 | 暂停帧 | 跨度 | timeScale | Remaining（min=max） | HP | releases | 恢复后 |
|---|---|---|---|---|---|---|---|---|
| `pause-warning` | Warning | 584 | 2.22s | 0 | **1.59493542 冻结** | 24 恒定 | 3 恒定 | 3→4 正常释放 |
| `pause-active` | Active | 595 | 2.21s | 0 | **0.149999619 冻结** | 2 恒定 | 4 恒定 | 4→5 正常结束 |
| `timescale-only`（对照） | Warning | 581 | 2.22s | 0 | 1.592906 冻结 | 24 恒定 | 3 恒定 | 3→4 |

`until` 为 private，报告记录 `untilDerived = Remaining + Time.time`；同时记录
`Time.time` / `Time.unscaledTime` / `Time.timeScale` / Boss state / 玩家 HP。
暂停期间无扣血、无提前释放，恢复后剩余时长符合既有合同。

> **产品事实与对照结论**：真实 UI 入口会**同时**置 `HudPanelOpen=true` 与 `Time.timeScale=0`。
> `timescale-only` 对照明确记录 `timeScale=0` 但 **`GameplayPaused=False`**，证明
> 全局 `timeScale=0` **不等于** UI-only GameplayPaused；本批把两者分别标注，
> **没有**用 timeScale=0 冒充 UI 暂停结果。「`GameplayPaused=true` 且 `timeScale>0`」的
> 组合无法经产品 UI 入口安全进入，故未伪造该组合。

## 5. R2-03 取消生命周期 —— **6/8 PASS-PLAYER，2 项明确 NOT_RUN**

每种条件独立 Player Run，尽可能在 Warning 与 Active 两阶段分别触发，全部走真实业务入口：
`CombatHealth.Damage`（真实死亡）、`ThirdPersonHero.RestorePosition`（离场）、
`CombatEnemy` 死亡链 `StopDeadAttacks()→StopDeath()`、`GameEntry.ReturnToTitle()`（场景卸载）。

| 用例 | 触发阶段 | 取消后 probes / applied | 取消后 Boss 状态 | 判定 |
|---|---|---|---|---|
| `cancel-death-w` | Warning | 0 / 0 | `Ready` | **PASS-PLAYER** |
| `cancel-death-a` | Active | 1 / 1（首帧 HitArea 在取消前） | `Ready` | **PASS-PLAYER** |
| `cancel-leave-w` | Warning | 0 / 0 | `Returning` | **PASS-PLAYER** |
| `cancel-leave-a` | Active | 1 / 1 | `Returning` | **PASS-PLAYER** |
| `cancel-boss-w` | Warning | 0 / 0 | `Dead` | **PASS-PLAYER** |
| `cancel-boss-a` | Active | 1 / 1 | `Dead` | **PASS-PLAYER** |
| `cancel-unload-w` | Warning | 0 / 0 | UNLOADED | **NOT_RUN**（见下） |
| `cancel-unload-a` | Active | 1 / 1 | UNLOADED | **NOT_RUN**（见下） |

严格判定按 `cancelTrigger.frame` 逐帧比较：**触发帧之后没有任何 `applied=true` 的 RingProbe**。
Active 期的 1 次 applied 发生在取消触发之前（首帧 `HitArea`），不是补发。
`no-replay-release` 对 6 个可观测用例全部 PASS；`CancelIntent/StopDeath` 后状态为
`Ready` / `Returning` / `Dead`，非 Warning/Active，无残留伤害窗口。

> **`NOT_RUN` 说明（不伪造通过）**：`GameEntry.ReturnToTitle()` 真实卸载场景并销毁 Boss
> GameObject，因此 `boss.Releases` / `boss.State` 在卸载后**不可观测**。这两个用例的
> 「无补发伤害」已由 `noAppliedProbeAfterCancel` 从原始 probe 行严格证明（0 个 applied），
> 「场景卸载」有真实 `sceneUnloaded` 事件与 `return-to-title PASS` 断言，但
> `noReplayRelease` 子项保持 `NOT_RUN`，不编造卸载后的 Boss 状态。

存档与结算：每个 run 使用独立 `-wanxiang-storage-root` 隔离根，`storage-audit.jsonl`
未越界；诊断工具未改变存档或结算。

## 6. R2-04 多 Collider 去重 —— **6/6 PASS-PLAYER**

根对象配置主 `CharacterController` + 第二个 enabled 非 trigger Y `CapsuleCollider`；
`b-trigger-child` 另加 root trigger `SphereCollider` 与子物体装饰 `CapsuleCollider`。

| 用例 | 组合 | `bodyCount` | world body 记录 | `geometry` | `applied` | HP |
|---|---|---|---|---|---|---|
| `b-none` | 两有效胶囊均不接触 | 2 | 2 | FALSE | 0 | 24→24 |
| `b-first` | 仅第一个接触 | 2 | 2 | TRUE | 1 | 24→2 |
| `b-second` | 仅第二个接触 | 2 | 2 | TRUE | 1 | 24→2 |
| `b-both` | 两个均接触 | 2 | 2 | TRUE | 1 | 24→2 |
| `b-both-multi` | 双接触 + 多帧 Active（27 帧） | 2 | 2 | TRUE | 1 | 24→2 |
| `b-trigger-child` | trigger / child 单独「接触」 | 2 | 2 | FALSE | 0 | 24→24 |

`Bodies()` 只纳入根对象 enabled 非 trigger 胶囊：trigger 与 child Collider 存在但
`bodyCount` 仍为 2；多个有效 body 任一接触即 `geometry=true`，但**一次 release 最多 Damage 一次**。

## 7. 证据规则与严格关联

- 每个用例**一个独立 Player Run**：独立 runId / PID / EXE SHA / Build SHA / 驱动 SHA /
  命令行 / stdout / stderr / `Player.log` / 原生退出码 / 原始 `RingProbe`。
- `Evidence/Tools/r2_analysis.py`：**禁止跨 Run join**，`r2-strict-correlation.json` 记录
  `crossRunJoins=0`、`nullTimestampsCountedAsPass=0`；null/缺失字段 → `INCOMPLETE`，
  缺失事件/文件 → `NOT_RUN`，两者**永不计入 PASS**。
- 每项 check 记录输入行、比较表达式、操作数与结果（`r2-player-checks.tsv`）。
- `r2-player-matrix.json` = **`R2_PARTIAL_OR_NOT_RUN`**：25/27 用例 `PASS-PLAYER`，
  2 个场景卸载子项明确 `NOT_RUN`；**不把部分覆盖汇总成无解释的 PASS**。

## 8. 失败历史（全部原样保留）

| 记录 | 内容 |
|---|---|
| `Evidence/Runs/DriverBuild1/driver-compile-failed-1.log` | `CS7036` `Wait` 缺默认超时参数 |
| `Evidence/Player/pause-warning-A1-FAILED/` | 驱动断言误把「恢复后正常释放的伤害」计为暂停期扣血；实质证据（584 帧 HP 恒定、Remaining 冻结）仍完整 |
| `Evidence/Player/timescale-only-A1-FAILED/` | 驱动错误地要求对照 case 出现 `GameplayPaused=true`；该失败恰好证明 timeScale-only ≠ UI 暂停 |
| `Evidence/Runs/DriverBuild2`、`DriverBuild3` | 驱动断言修正与对照语义标注的版本演进 |

全部修正仅作用于 **sidecar 驱动 / 分析工具**，产品源码与冻结合同参数未改，未事后调容差。

## 9. 保护与禁止项

`protection.json` = **`PROTECTION_PASS`**：未改 `ProjectSettings/`、用户场景、`Packages/`、
B1/B2/R1 历史与原始证据、真实存档；未强推、未自动合并 `main`、未升级依赖、未新增 CI。
**产品源码零修改**（纯包哈希与 R1 一致）；未改晶环几何、路线收益投影、Boss 状态机、
伤害、预警时长、随机流、评分权重、v9 格式。

## 10. 结论与暂停

| 合同 | 结论 |
|---|---|
| R2-01 竖直高度 | **10/10 PASS-PLAYER** |
| R2-02 GameplayPaused | **3/3 PASS-PLAYER**（UI 入口 + 独立对照） |
| R2-03 取消生命周期 | **6/8 PASS-PLAYER**；2 个场景卸载子项 **NOT_RUN**（Boss 卸载后状态不可观测，无补发伤害已证） |
| R2-04 多 Collider | **6/6 PASS-PLAYER** |

**未发现任何产品行为与冻结合同冲突**，因此未提出最小产品修复，产品源码保持零修改。
未覆盖项如实 `NOT_RUN`，不伪造通过；R1 的 7/7 核心矩阵未被改写或重跑。

本批到此暂停等待复审。`SKILL-STATE-01`、`CP06-INTEGRATION-01`、`UX-PROGRESSION-01` 均未启动。
