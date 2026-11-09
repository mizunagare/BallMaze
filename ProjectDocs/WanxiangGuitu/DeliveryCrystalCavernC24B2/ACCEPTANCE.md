# CP06-C24-B2 验收（分层，不把模型冒充运行）

基线 `a013c15aae15e17af6a7596a022f01f56a745c34`；分支 `fix/cp06-crystal-warden-b2`。
本批**交付后暂停等待复审**，不宣称运行层全部通过。

## 0. 状态口径

| 标记 | 含义 |
|---|---|
| `PASS-RUN` | 有本批真实 Unity Editor 运行输出，且结果符合冻结合同 |
| `PASS-MODEL` | 确定性公式/源码控制流/冻结原始事件再关联，非运行 |
| `PASS-STATIC` | 源码级门禁或等价证明，非运行 |
| `PARTIAL` | 静态/Editor 已证，但运行层未覆盖 |
| `NOT_RUN` | 本批未产生该层运行证据，不推断通过 |
| `UNCHANGED` | 本批未触及该实现，引用历史证据，不重新判定 |

> 本机无 PowerShell 7 (`pwsh`)，历史 `Invoke-Editor.ps1` / `Invoke-Player.ps1` 编排链不可直接复跑。
> 本批用 Unity 可执行文件直接做了一次 batchmode Editor 运行，**没有**产生新的观测 Player / 纯包 / 原生输入 / 独立人工运行。
> 这些项如实登记 `NOT_RUN`，绝不用 Editor 结果代替。

---

## 1. 退出条件表（任务书 5.5）

| ID | 必须证明 | 本批结论 | 依据 | 层级 |
|---|---|---|---|---|
| B2-01 | C24 普通收益投影与专用规则一致 | **PASS-MODEL**（4/4 字段修正）+ **PASS-RUN**（Editor 校验共享常量/工厂派生 14/14） | `Evidence/After/route-fields-after.json`、`Evidence/Runs/Editor-RingContract-A1/ring-contract.json` | 模型 + Editor |
| B2-02 | 死亡/地面拾取后无重复预测，首奖独立 | **PASS-STATIC**；运行层 `NOT_RUN` | `RouteScoring.cs` 中 `localEnemies` 已过滤 `Health.Dead`、`loot` 已过滤 `Collected`；`RuinsSpecialRewards.Earn` 只在 `Drop` 内，投影分支不调用 | 源码控制流 |
| B2-03 | 查询不写盘、不创建物品、不消耗 RNG | **PASS-STATIC**；运行层 `NOT_RUN` | `CrystalCavernBossRewards.Project` 只写 `float[]` 与 `out float`；不调用 `Drop`/`Earn`/`Number`/`Spawn`/`Queue*` | 源码控制流 |
| B2-04 | 六份旧布局评分及排序不变 | **PASS-STATIC**；新 Editor 对照 `NOT_RUN` | `ProjectionApplies` 六项门禁（region / contentRevision / generationVersion / HasBoss / BossId / Brain）使森林、遗迹、C21、C22、C23 闭桥/开桥全部走原通用分支；`RouteScoring.json` 未改 | 源码门禁证明 |
| B2-05 | 晶环实际接触与预警几何统一 | **PASS-RUN** 14/14 + **PASS-STATIC** 单一常量来源 | `DESIGN_DECISIONS.md`、`contract.json`、`ring-contract.json`；`ShowWarning` 与 `HitArea` 共用 `InnerRadius/OuterRadius/WarningPlane(AttackOrigin)` | Editor |
| B2-06 | 遮挡、免疫、高差、多帧/多 Collider 合同正确 | **PARTIAL** | Editor：内/外/竖直切线、完全内外侧、有效世界半径、子武器模型排除、重复 Collider、trigger 排除 6/6；遮挡 / 翻滚免疫 / 同次窗口多帧 / 七武器站位为源码控制流 + `NOT_RUN` | Editor + 静态 |
| B2-07 | 跨半血攻击、恢复及转阶段关联证据完整 | **PASS-MODEL**（冻结原始事件只读关联，10/10 检查） | `Evidence/After/c05-correlation.json`、`phase-timeline.json` | 历史原始事件再关联 |
| B2-08 | 不挑战可返回、挑战保存失败不启战 | **UNCHANGED** | 本批未改 `Challenge()` / 门禁；历史 `PlayerWindupB2/assertions.tsv` 中 `dormant-choice`、`choice-interactable`、`failed-save-no-battle`、`failed-save-disk-preserved`、`retry-challenge`、`challenge-durable` 为 PASS | 历史证据引用 |
| B2-09 | B1 提示成功时机 / 首奖幂等不退化 | **UNCHANGED** + **PASS-STATIC** 工厂载荷等价 | `Evidence/After/reward-factory-equivalence.json`（归一化后与基线源码逐字相等）；B1-01/02/03 保持原 PASS | 源码等价 |
| B2-10 | Editor / 观测 Player / 纯包证据分层，纯包无驱动 | **PASS**（分层登记如实） | Editor `PASS-RUN`；观测 Player / 纯包 / 原生输入 / 独立人工全部 `NOT_RUN`；未构建新纯包，也未向任何包注入驱动 | 分层登记 |
| B2-11 | 用户文件、原存档、旧证据、依赖保护通过 | **PASS** | `Evidence/After/protection.json`；`git diff` 仅含本批授权文件；`ProjectSettings/`、场景、`Library`、旧交付目录、真实存档均未写入 | 保护核验 |

---

## 2. 冻结合同与「先写容差，后跑测试」

- `DESIGN_DECISIONS.md` 与机器可读 `Evidence/Tools/RingContract/contract.json` 均在**任何产品改动或测试运行之前**写入。
- 冻结值：内 2.2m / 外 6m / 竖直半高 1.2m / 预警 1.6s / 原始伤害 22 / `ContactEpsilon=0.0001` / 闭集切线。
- 运行前按 `origin.y=0.08` 对**竖直切线用例的 centerY** 做了一次解析校正（2.2→2.28、2.201→2.281），记录在设计文档 2.5 节；半径、半高、容差、切线规则均未改动。
- 未为通过任何历史样本事后改容差或改半径。

## 3. 结果

| 检查 | 结果 | 出处 |
|---|---|---|
| 修复前 F1 复现 | 4/4 普通收益字段不一致，通用分支公式可复现 | `Evidence/Before/route-fields-before.json` |
| 修复前 F2 复现 | inner / outer 两组胶囊接触环带但旧根点判定安全，HP 48→48 | `Evidence/Before/ring-matrix-before.json` |
| 修复前 C05 基线 | `WindupNewAudit1` v2.0 `INCOMPLETE` 原样保留 | `Evidence/Before/c05-timeline-before.json` |
| 修复后逐字段 | 兽皮 0 / 铁矿 3 / 晶石 4 / 装备 1；`expectedMaterialUnits=7`，`totalScore≈8.41984` | `Evidence/After/route-fields-after.json` |
| 工厂载荷等价 | 14 组 uint 哈希 + 源码归一化逐字相等 ⇒ `FACTORY_PAYLOAD_EQUIVALENT` | `Evidence/After/reward-factory-equivalence.json` |
| 冻结合同几何模型 | 14/14 | `Evidence/After/ring-matrix-after.json` |
| Unity Editor 真实运行 | `EDITOR_CONTRACT_PASS`：几何 14/14、受击体 6/6、奖励 14/14，脚本编译 0 error | `Evidence/Runs/Editor-RingContract-A1/` |
| C05 定向关联 | 10/10，`C05_CHAIN_CORRELATED`；历史 `INCOMPLETE` 不改写 | `Evidence/After/c05-correlation.json` |

### Editor 运行明细（`Unity 6000.6.5f1`，batchmode，退出码 0）

- 几何：B1 inner/outer/band/safe 四组按 `ring-release.json` 精确值 → 期望 TRUE/TRUE/TRUE/FALSE，实际一致；
  中心空洞、完全内/外安全、内/外精确切线、超出 0.001、竖直脱离/切线/超出全部一致。
- 受击体：真实 `CharacterController` 命中；子物体 `BoxCollider`（武器模型）**不**计入；
  重复根胶囊 OR 一次；`isTrigger` 排除；`lossyScale` 使有效世界半径 0.4→0.8 后 d=6.6 由不接触变接触；
  安全站位 + 接触环带的子模型仍安全。
- 奖励：14 个代表性 `uint` 哈希下 `OreAmount/CrystalAmount` 与基线 `2+(h%3)` / `3+(h%3)` 完全一致。
- 编译：`error CS` 0；`warning CS` 均为既有 `CS0618`（Unity 6 废弃 API）与 `CS0414`，新增两个源码文件**无**告警。

---

## 4. 明确未通过 / 未覆盖

| 项 | 状态 | 说明 |
|---|---|---|
| 非开发观测 Player 的同合同晶环测试 | `NOT_RUN` | 需要 PowerShell 7 编排与 sidecar 驱动；本机 `pwsh` 缺失，本批未伪造 |
| 墙后遮挡导致 `clear=FALSE` 的实际运行 | `NOT_RUN` | 仅源码控制流证明（`RaycastAll` 未改）与 `RingProbe.clear` 分层 |
| 翻滚免疫导致 0 伤害的实际运行 | `NOT_RUN` | `CombatHealth.Damage` 免疫早退未改；`RingProbe.evaded` 单独成列 |
| 同次窗口多帧 / 重复命中实际运行 | `NOT_RUN` | `hit` 一次机会未改；`alreadySpent` 探针已加 |
| 七武器各一组相同晶环站位回归 | `NOT_RUN` | 结构性证明：`Bodies()` 只读根物体 Collider，子武器模型不可能成为受击体 |
| 连续查询前后 Profile / Run / 三随机流 / 地面对象 / revision 不变 | `NOT_RUN` | 仅源码级证明投影为纯函数 |
| 六份旧布局新 Editor 评分对照 | `NOT_RUN` | 仅门禁静态证明；历史 `ScoreComparison2` 35 PASS 保持原结论 |
| 纯发行包、原生键鼠、独立人工、最终平衡、性能 | `NOT_RUN` | 不在本批运行 |
| 晶环竖直带可视化 | 开放项 | 现有 2D 指示圆不表达 ±1.2m 竖直带，登记在 `CURRENT_STATUS.md` |

## 5. 总结论

> 产品实现与冻结合同在**静态、确定性模型、真实 Unity Editor** 三层一致；
> 运行层（观测 Player / 纯包 / 原生输入 / 人工）**未跑，不予推断**。
> 本批按任务书要求推送后**暂停等待复审**，不自动开始 `SKILL-STATE-01`、
> `CP06-INTEGRATION-01` 或 `UX-PROGRESSION-01`。
