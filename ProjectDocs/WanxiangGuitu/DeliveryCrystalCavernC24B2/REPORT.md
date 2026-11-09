# CP06-C24-B2 交付报告

**状态：实现完成、静态/模型/真实 Unity Editor 层通过；运行层部分 `NOT_RUN`；推送后暂停等待复审。**

## 1. 基线与完整 SHA

| 对象 | 完整 SHA | 说明 |
|---|---|---|
| `origin/main` | `72db192a527bd256e2ba18cd7ab334d8334051da` | 四武器表现批次；**不是** CP06 完成度 |
| `origin/fix/cp06-crystal-warden-b1` | `a013c15aae15e17af6a7596a022f01f56a745c34` | 本批唯一起点 |
| 本批基线 / 分支起点 | `a013c15aae15e17af6a7596a022f01f56a745c34` | 未从旧 `main` 重做 CP05/CP06 |
| 本批分支 | `fix/cp06-crystal-warden-b2` | 从上述 SHA 建立，未 force、未合并 `main` |
| 本批提交与远端复核 | 见 `Evidence/After/remote-verification.json` | 提交后才产生完整 SHA；内含推送后 `git ls-remote` 复核 |

开工核对：`origin/main...HEAD` 为 `0 38`，merge-base 即上述 `main` SHA；
远端当时不存在 `fix/cp06-crystal-warden-b2`。未回退、未覆盖旧分支。

## 2. 范围（严格限于 CP06-C24-B2 四部分）

1. **B2-01** C24 Boss 路线只读收益投影与专用普通掉落工厂对齐。
2. **B2-02** 按任务书落实「实际受击 Collider 接触晶环」判定合同。
3. **B2-03** 补齐 P1 前摇跨半血、原阶段释放、恢复结束后转阶段的定向证据。
4. **B2-04（文档）** 增量建立当前分支与开放项入口，不改写历史报告。

`SKILL-STATE-01`、`CP06-INTEGRATION-01`、`UX-PROGRESSION-01` **未启动**。

## 3. 修复前复现（先留证，后改码）

`Evidence/Before/reproduce_before.py` 在**任何产品源码修改之前**运行，只读、确定性，
不运行 Unity / 不写存档 / 不推进 RNG / 不创建物品 / 不产生 Player 日志。
25 个输入均以 SHA256 固定在 `inputs.json`。

| 缺陷 | 修复前结论 |
|---|---|
| F1 | B1 真实 C24 arena 样本：`expectedMaterials=[10,5,0,0,0,0]`、`expectedGear=0`、`expectedMaterialUnits=15`、`totalScore≈24.4198418`；通用敌人分支公式可复现；与专用工厂 4/4 字段不一致 |
| F2 | B1 四组真实世界胶囊：inner(2.100006)、outer(6.100006) 的胶囊与环带相交但旧根点判定安全，HP 48→48；band 48→26；safe 48→48 ⇒ 2 组语义冲突 |
| C05 | 历史 `WindupNewAudit1` v2.0 为 `INCOMPLETE`（`playerDamageAttribution` / `recoveryTransitionOrder`），原样保留 |

## 4. 产品改动（最小）

| 文件 | 改动 |
|---|---|
| `Assets/CombatPrototype/CrystalCavernBossRewardProjection.cs` **(新)** | 纯常量 + 确定性派生 `OreAmount/CrystalAmount` + 名义均值；真实工厂与只读投影共用，无 Unity 依赖 |
| `Assets/CombatPrototype/CrystalCavernRingContact.cs` **(新)** | 冻结环带常量、`BroadPhaseRadius`、`WarningPlane`、胶囊×环形柱体精确相交、真实根物体受击体提取 |
| `Assets/CombatPrototype/CrystalCavernBossRewards.cs` | 新增只读 `ProjectionApplies` / `Project`；`Drop` 的两个数量表达式改调共享定义（**载荷逐字等价**） |
| `Assets/CombatPrototype/RouteScoring.cs` | 敌人循环最前面加 C24 精确身份分支；其余分支一字未动 |
| `Assets/CombatPrototype/CrystalCavernBossBrain.cs` | HollowRing 的 broad/narrow phase、预警共享常量、只读 `RingProbe` 观测；CrossLines / Claw / Volley / 伤害入口 / `hit` 一次机会 / 状态机均未改 |
| 两个 `.cs.meta` **(新)** | 稳定 GUID，与仓库既有约定一致 |

**未改**：真实掉落、首奖、随机流、评分权重与排序合同、武器、护甲、经验、v9 存档格式、
`RouteEvaluation` 字段集合、`RouteScoring.json`、用户场景、`ProjectSettings`、旧证据、依赖。

### 4.1 B2-01 结果（真实 C24 样本，逐字段）

| 字段 | 修复前 | 修复后 | 专用工厂名义值 |
|---|---:|---:|---:|
| 兽皮 | 10 | **0** | 0 |
| 晶石 | 5 | **4** | 3–5 / 均值 4 |
| 铁矿 | 0 | **3** | 2–4 / 均值 3 |
| 装备机会 | 0 | **1** | 恰好 1 件 |
| `expectedMaterialUnits` | 15 | 7 | — |
| `expectedYield` | 0.375 | 0.375 | — |
| `targetMatch` | 0.375 | 0.175 | — |
| `totalScore` | 24.4198418 | **8.4198412** | — |
| 路线 UI | 野怪皮/晶石碎片 | **晶石碎片/铁矿/装备机会** | — |

分数变化来自修正后的投影派生字段；权重、风险函数、排序与六份旧地图分支均未变。
工厂载荷等价证明：14 组 `uint` 哈希逐值一致，且当前工厂源码归一化后与
`a013c15a...` 基线**逐字相等**（`FACTORY_PAYLOAD_EQUIVALENT`）。

### 4.2 B2-02 结果

语义**明确变更**（不伪称旧行为不变）：从「玩家根点进入环带」改为「实际受击胶囊接触环带」，
擦边安全余量缩小。冻结参数：内 2.2m / 外 6m / 竖直半高 1.2m（相对冻结 `AttackOrigin`）、
预警 1.6s、原始伤害 22、`ContactEpsilon=0.0001`、闭集切线。
预警与判定共用同一环心、半径、竖直带定义；broad phase 只筛候选，narrow phase 用真实
`CharacterController` / `CapsuleCollider` 的世界中心、有效半径、高度做精确相交；
不使用 Renderer / AABB / 硬编码 0.4；不扩大外圈、不缩小内圈。

B1 四组按 `ring-release.json` 精确值：inner / outer / band → 接触，safe → 不接触；
另覆盖中心空洞、完全内/外安全、内外精确切线与超出 0.001、竖直脱离/切线/超出。
真实 Unity Editor 运行 **14/14 几何 + 6/6 受击体 + 14/14 奖励等价**，编译 0 error。

### 4.3 B2-03 结果

不改写历史、不改状态机。用冻结原始逐帧事件做只读关联，10/10 检查通过：
P1 Claw `Begin`(frame 2177) → 前摇内真实武器命中跨半血(2283, 195→162) →
`Release` 仍为 P1(`phase2=False`, Claw, 16) 于 2514 → 同帧 Hero `Damage` 100→84 →
401 帧完整 P1 Recovery（末帧 2914 `Remaining=0.0003414`）→ `Transition`(2915) →
P2 下一招 `Next(0,true)=CrossLines`（源码模型 + 同构建 `phase-releases.tsv`，**非同一次运行**）。

消解历史限制的方式：窗口内 `windup-release.tsv` 恰 1 行、`windup-hero-health.tsv` 恰 1 行 Damage，
且该行带 `boss.Attack`/`boss.Releases` 只读状态快照，四键（frame/time/attack/index）匹配；
恢复结束与转阶段来自两份独立逐帧 TSV，不使用 summary 中 driver 同时赋值的对。

## 5. 证据与构建身份

- 修复前：`Evidence/Before/`（脚本 + 5 份 JSON，含 25 输入 SHA256）。
- 冻结合同：`DESIGN_DECISIONS.md` + `Evidence/Tools/RingContract/contract.json`。
- 修复后：`Evidence/After/`（逐字段、工厂等价、晶环矩阵、C05 关联、阶段时间线、保护与哈希清单）。
- 真实 Editor：`Evidence/Runs/Editor-RingContract-A1/`（`Editor.command.json` / `Unity.log` /
  `ring-contract.json` / `Editor.exit.json` / stdout / stderr），Unity 6000.6.5f1，退出码 0，
  `EDITOR_CONTRACT_PASS`；`error CS` 0，告警全部为既有 `CS0618`/`CS0414`，新文件无告警。
- 保护哈希：`Evidence/After/protection.json`、`hash-manifest.json`。
- 远端复核：`Evidence/After/remote-verification.json`。

## 6. 当前风险与开放项

| 项 | 状态 |
|---|---|
| 观测 Player / 纯发行包 / 原生键鼠 / 独立人工 | `NOT_RUN`（本机无 `pwsh`，不伪造） |
| 墙后遮挡、翻滚免疫、同次窗口多帧、七武器站位的实际运行 | `NOT_RUN`；仅源码控制流 + Editor 受击体结构证明 |
| 连续查询前后 Profile / Run / 三随机流 / 地面对象 / revision 不变 | `NOT_RUN`；仅源码级纯函数证明 |
| 六份旧布局新 Editor 评分对照 | `NOT_RUN`；仅门禁静态证明，历史 `ScoreComparison2` 35 PASS 保持 |
| 晶环竖直带可视化 | 开放：2D 指示圆不表达 ±1.2m 竖直带，未用改数值掩盖 |
| 法杖符阵 / 弹体暂停时钟 | `SKILL-STATE-01`，仍是源码控制流推论，未实测 FAIL |
| 历史 C02/C04 严格三维起点失败、旧 C05 `INCOMPLETE` | 原样保留 |

## 7. 交付与暂停

按 `ACCEPTANCE.md` 分层判定：静态/模型/Editor 层通过，运行层未跑不推断通过。
分支推送后重新读取远端完整 SHA 并确认 `main` 未被本批移动，然后**暂停等待复审**。
后续三批不自动连续实施。

入口：`ProjectDocs/WanxiangGuitu/CURRENT_STATUS.md`；
`README.md` / `DEVELOPMENT_PLAN.md` 顶部各新增一条短指针，历史正文与 PASS/FAIL 全部保留。
