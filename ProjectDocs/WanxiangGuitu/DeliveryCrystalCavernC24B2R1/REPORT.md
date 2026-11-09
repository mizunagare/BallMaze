# CP06-C24-B2-R1 交付报告：Boss 阶段证据闭环与晶环 Player 验证

状态：**已完成、已推送、暂停等待复审**
分支：`fix/cp06-crystal-warden-b2-r1`
基线：`98924a34b6df817aa5a979b50439a4515881744b`（B2 tip）
范围：仅补齐 B2 的证据缺口；**产品源码零修改**。

---

## 1. 完整 SHA 与分支

| 对象 | 完整 SHA | 说明 |
|---|---|---|
| `origin/main` | `72db192a527bd256e2ba18cd7ab334d8334051da` | 开工/收尾均核对，未移动 |
| `origin/fix/cp06-crystal-warden-b1` | `a013c15aae15e17af6a7596a022f01f56a745c34` | 未变 |
| `origin/fix/cp06-crystal-warden-b2`（基线） | `98924a34b6df817aa5a979b50439a4515881744b` | 未前进、未变 |
| 本批分支 tip | 见 `Evidence/After/remote-verification.json` | 推送后 `git ls-remote` 复核 |

开工 `git ls-remote --heads` 与任务书基线完全一致，B2 未前进，故按计划从 B2 tip 建立独立 R1 分支；
未 reset、未覆盖、未强推、未合并 `main`。

## 2. 先修正证据关联工具（R1-00，先于任何 Player 结论）

新建 `Evidence/Tools/r1_correlate.py`，四条硬规则：

| 规则 | 内容 |
|---|---|
| R1 | 每个事件必须有完整身份三元组 `runId / processId / buildSha`；缺失即 UNIDENTIFIED，永不计入 PASS |
| R2 | 只有身份三元组**完全相等**的事件才能 join 成一条时间线；不同 Run 一律隔离到 `quarantinedCrossRunEvidence` |
| R3 | `frame` / `time` 为 null 或缺失 → `INCOMPLETE`；事件缺失 → `NOT_RUN`；两者**永不计入 PASS** |
| R4 | 每项 check 必须列出输入事件行、比较表达式、操作数与状态；不产生无解释的「10/10」汇总 |

自测 `r1-tool-selfcheck.json` = `TOOL_RULES_ENFORCED`，三个构造用例全部通过：
`null_time_cannot_pass`、`cross_run_cannot_be_joined`、`missing_event_is_not_run`。

**B2 严格重审**（`b2-reevaluation.json`，只读，不改 B2 文件）：

| 发现 | 事实 |
|---|---|
| B2 verdict | `C05_CHAIN_CORRELATED` |
| `PlayerWindupA2` | 3 项 **false**：`realHitCrossesHalfInWindup`、`fullOriginalRecovery`、`recoveryTransitionOrder` |
| chain | 跨半血与 Transition 的 `frame/time/bossHP/state` 为 **null** |
| `p2NextAttack.sameRun` | **False**；B2 自述 `phase-releases.tsv` 来自另一个 Run |
| 身份 | 历史 TSV 无 `runId/processId/buildSha` 列，无法构成同 Run 身份 |
| 结论 | `B2_10_OF_10_CLAIM_NOT_SUPPORTED_AS_SAME_RUN_PROOF` |

B1 的 C05 `INCOMPLETE`、B2 的 `c05-correlation.json` 与「10/10」声明**全部原样保留**。

## 3. R1-01：同一 Run 的 C05 完整阶段时间线

真实观测 Player（非 Editor、非模型）：
`Evidence/Player/r1-c05-A3/`，PID `32980`，`complete.txt=PASS`，原生退出码 `0`。

| 字段 | 值 |
|---|---|
| runId | `ce7b7cd3442e4b8ba628f34d887d0391` |
| processId | `32980` |
| buildSha | `3763776a762c00d25761d952b7cb4d881203fc3a43c568f1550eec7c412e6002` |
| bossInstanceId | `c24:boss:crystal-warden:ForestRuins:ce7b7cd…` |
| 事件 | 18 条，**1 个身份三元组**，**0 个 null 时间** |

时间线（全部来自同一 Run 的原始事件）：

| 步骤 | frame | Time.time | 事件 |
|---|---|---|---|
| 1 | 2576 | 6.4866 | P1 Claw Begin / Warning，Boss HP **195 > 180** |
| 2 | 2871 前 | 前摇内 | 真实 `AdventureCombat.Strike` 命中，Boss HP 跨半血 195→162（非直接写 HP、非 SetHP） |
| 3 | 2871 | 7.6881 | 已开始的攻击按**冻结 P1 参数**释放：`phase=1 / Claw / rawDamage=16` |
| 4 | 2871 | 7.6881 | 同帧 `HealthObservation` 100→84；`correlationId` 与 release 严格相等 |
| 5 | 3208 | 9.0342 | P1 Recovery 完整结束（`remaining=0`，独立事件） |
| 6 | 3209 | 9.0384 | **Recovery 之后**才 Transition（frame 严格大于） |
| 7 | 4067 | 12.3054 | 同一 Run 的 P2 下一招 `CrossLines / phase=2 / damage=20` |

> `correlationId` 是驱动从同一 Run 真实字段（`runId : boss.Releases : frame`）派生的**只读 join 键**；
> 产品 `HealthObservation` 没有 attackId，该键不写存档、不改产品行为、不来自第二个 Run。
> 每一步附 `sourceStack`（`CombatHealth.Observed` / `Released` 调用栈）与真实攻击来源。

严格关联结果：`c05-strict-correlation.json` = **`PASS-PLAYER_SAME_RUN_C05`**，
10 项检查全部 PASS（`c05-strict-checks.tsv` 逐项列出输入行与表达式）。

## 4. R1-02：晶环观测 Player 合同

7 个独立真实 Player run，每个有独立 runId / PID / EXE SHA / Build SHA / 命令 / 日志 / 退出回执。
原始 `ring-probes.jsonl` 记录 `RingProbe` **全字段**（contact / geometry / clear / evaded /
applied / alreadySpent / bodyCount / hpBefore / hpAfter / release / frame / time / bodyCenter /
bodyRadius / bodyHeight / origin / inner / outer / halfHeight / epsilon）。

| 样本 | 根半径 | geometry | clear | evaded | applied | HP | 判定 |
|---|---|---|---|---|---|---|---|
| `band` | 3.2000 | true | true | false | 1 | 24→2 | **PASS-PLAYER** |
| `inner-edge` | 2.2000 | true | true | false | 1 | 24→2 | **PASS-PLAYER** |
| `outer-edge` | 6.0000 | true | true | false | 1 | 24→2 | **PASS-PLAYER** |
| `inner-safe` | 1.5000 | **false** | true | false | 0 | 24→24 | **PASS-PLAYER** |
| `outer-safe` | 6.8000 | **false** | true | false | 0 | 24→24 | **PASS-PLAYER** |
| `wall` | 3.2000 | true | **false** | false | 0 | 24→24 | **PASS-PLAYER** |
| `dodge` | 3.6682 | true | true | **true** | 0 | 24→24 | **PASS-PLAYER** |

同一 release=4 的 20–24 个 Active 帧中，**最多一次 `applied=true`**（`appliedCount<=1`），
后续帧 HP 不变；冻结参数 `inner=2.2 / outer=6.0 / halfHeight=1.2 / ε=1e-4 / rawDamage=22`
逐样本一致，**未事后调整任何容差或半径**。

`ring-player-matrix.json` = **`RING_PLAYER_MATRIX_PASS`（7/7）**。

> **断言修正记录**：初始分析 `ring-player-matrix-initial.json` 为 4/7、3 项 FAIL，
> 原因是分析工具误把 `alreadySpent` 要求在无命中窗口为 true。产品语义是
> `alreadySpent` 只在**伤害机会已消耗**（`hit=true`）后才为 true；安全区、遮挡、
> 翻滚窗口保持 `hit=false` 并逐帧重新评估，因此 `alreadySpent=false` 是**正确产品行为**。
> 这是**测试断言错误，不是产品缺陷**；仅修正分析工具，产品源码与冻结合同均未改动，
> 初始失败结果原样保留。

### 本批 `NOT_RUN`（不伪造、不冒充）

| 未覆盖项 | 原因 |
|---|---|
| 竖直带内 / 切线 / 带外、不同高度受击体 | 驱动只在 arena 地面放置玩家，未构造可控高度的受击体；B2 的 height 用例属 Editor/模型层 |
| `GameplayPaused` 时钟冻结与 Active 窗口顺延 | 驱动未打开 UI 暂停面，无 pause-state 事件 |
| 玩家死亡 / 离开 Arena / Boss 死亡 / 场景卸载取消 | 未执行专门的取消 run；`CancelIntent` 仅静态控制流覆盖 |
| 多个 Collider 的受击体 | 所有样本 `bodyCount=1`（CharacterController），未附加第二个非 trigger 胶囊 |
| 原生键鼠 / 独立人工 / 纯包标题与存档保护 | 本批未运行 |

## 5. R1-03：晶环预警可读性

`RING_WARNING_VISUAL_PROPOSAL.md`，状态 **`DESIGN_ONLY / NOT_IMPLEMENTED`**：
保留地面二维圆环，新增 `origin.y ± 1.2` 半透明高度边界环 + 16 根短垂直晶柱，
蓄力 1.6s 渐显，颜色沿用橙色、ZWrite Off、线宽上限，不遮挡 Boss/玩家；
视觉边界严格对应冻结几何，`ε` 刻意不可视化；**不改伤害、预警时长、命中逻辑或全局警告系统**。

## 6. R1-04：B2-01 路线投影定向回归

`projection-regression.json` = **`PROJECTION_REGRESSION_PASS`**，8/8：

- 六项身份门禁齐全（region / contentRevision / generationVersion / HasBoss / BossId / Boss+Brain）。
- `Project()` 无任何副作用调用（无 Drop/Earn/Number/Spawn/Save/Queue/Random/revision/Profile）。
- `RouteScoring` C24 分支受门禁且 `continue`；通用分支仍保留。
- `enemies.Where(!Dead)` 与 `loot.Where(!Collected)` 保证 Boss alive/dead × 掉落 collected/uncollected 四态不重复计入。
- 旧森林、遗迹、C21/C22/C23 门禁全部失败 → 仍走原通用分支；未发现回归，**未重跑全量旧地图评分矩阵**。
- `OreAmount/CrystalAmount` 对**任意 uint** 与基线 `2+(h%3)` / `3+(h%3)` 代数恒等，
  19 个代表 uint 全部匹配，源码归一化后与基线逐字相等 → `FACTORY_PAYLOAD_EQUIVALENT`。

## 7. 构建链与证据分层

| 层 | 结果 | 证据 |
|---|---|---|
| 纯发行包构建 | Unity `6000.6.5f1` `WanxiangBuild.ValidateBuild`，退出码 0，`errors=0`，`result=Succeeded` | `Evidence/Runs/PureBuild2/` |
| 纯包纯净性 | `RuntimeInitializeOnLoads.json` 28 项、验证驱动 **0** | `PureBuild2` 收据 |
| sidecar 驱动 | 编译退出码 0，注入后 29 项、验证驱动 1；仅改隔离副本 | `Evidence/Runs/DriverBuild*/driver-injection.json` |
| 观测 Player | 10 次真实运行（含 2 次失败），各含 EXE/Build/驱动 SHA、PID、参数、日志、退出回执 | `Evidence/Player/` |
| 静态 / 模型 | R1-04 8/8、工具自测 3/3 | `Evidence/After/` |
| Editor | 本批**未重跑** B2 Editor 契约；B2 的 `PASS-EDITOR` 为历史结论 | 不合并入本批 verdict |

纯包 EXE SHA256 `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`，
`Assembly-CSharp.dll` SHA256 `3763776a762c00d25761d952b7cb4d881203fc3a43c568f1550eec7c412e6002`。

## 8. 失败历史（全部原样保留）

| 记录 | 内容 |
|---|---|
| `Evidence/Runs/PureBuild1-DISCARDED/` | 首次构建含 `B1RouteValidation.Driver.Boot` 与 `CavernValidation.Driver.Boot` 两个历史驱动，非纯包，弃用；移除脚本后重建 `PureBuild2` |
| `DriverBuild1/driver-compile-failed-1.log` | `CS0619 GetInstanceID` 废弃 API 编译失败 |
| `DriverBuild4/driver-compile-failed-1.log` | `CS0128` 重复局部变量编译失败 |
| `Evidence/Player/r1-c05-A1/` | 驱动在 `DepartCavern()` 前读 `ActiveRun.runId` → NRE，exit 2 |
| `Evidence/Player/r1-c05-A2/` | 未在挑战交互点附近调用 `Interact` → `challenge FAIL`，exit 2 |
| `Evidence/After/ring-player-matrix-initial.json` | 分析断言错误导致的 4/7 初始判定 |

## 9. 保护与禁止项

`protection.json` = **`PROTECTION_PASS`**，受保护路径违规 **0**：
未改 `ProjectSettings/`、用户场景、`Packages/`、B1/B2/C24B 历史报告与原始证据、真实存档。
产品源码 **零修改**（B2 已接受的奖励投影与晶环几何实现保持不变）。
未升级依赖、未新增 CI、未强推、未自动合并 `main`。

## 10. 结论与暂停

- R1-01：**PASS-PLAYER_SAME_RUN_C05**（10/10，同一 Run/PID/Build SHA）。
- R1-02：**RING_PLAYER_MATRIX_PASS**（7/7），NOT_RUN 项如实列出。
- R1-03：DESIGN_ONLY，未实现、未改产品。
- R1-04：**PROJECTION_REGRESSION_PASS**（8/8）。
- 无 Player 证据显示产品行为与冻结合同冲突，因此**未提出任何最小产品修复**。

本批到此暂停等待复审。`SKILL-STATE-01`、`CP06-INTEGRATION-01`、`UX-PROGRESSION-01` **均未启动**。
