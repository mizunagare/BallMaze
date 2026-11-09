# CP06-C24-B2 设计决定（先冻结，后测试）

本文件在任何产品源码修改、任何测试运行之前写入。所有参数、容差、切线口径与判定分层在本文件内固定；
**不得为通过历史样本事后修改本文件的容差**。若实测与本文件冲突，先登记差异，再按版本化设计变更处理。

- 基线：`a013c15aae15e17af6a7596a022f01f56a745c34`
- 分支：`fix/cp06-crystal-warden-b2`
- 设计合同版本：`C24-B2-RING-1` / `C24-B2-PROJECTION-1`
- 适用范围：仅 C2.4 晶脊守望者的 HollowRing（空心晶环）与 C24 只读路线收益投影。
- 机器可读冻结副本：`Evidence/Tools/RingContract/contract.json`（与本文件同批、在任何测试运行之前写入；其 SHA256 记录在 `Evidence/INDEX.md`）。

---

## 1. B2-01 只读收益投影合同 `C24-B2-PROJECTION-1`

### 1.1 精确身份（六项同时成立）

只有下列条件**全部**成立时，敌人才从「通用敌人收益分支」切换到「C24 专用投影分支」：

| # | 条件 | 来源 |
|---|---|---|
| 1 | `run.region == CrystalCavernLayout.Region` | `RunState` |
| 2 | `run.contentRevision == CrystalCavernLayout.Content24` | `RunState` / `CrystalCavernLayout` |
| 3 | `run.generationVersion == CrystalCavernLayout.Generation24` (13) | `RunState` / `CrystalCavernLayout` |
| 4 | `CrystalCavernLayout.HasBoss(map)`：`revision==10 && mapAssetVersion=="C2.4-CAVERN-1"` | 布局校验 |
| 5 | `enemy.entityId == CrystalCavernLayout.BossId` 且 `archetype == Boss` | 稳定 Boss ID |
| 6 | `enemy.GetComponent<CrystalCavernBossBrain>() != null` | 专用 Brain |

即复用 `CrystalCavernBossRules.Exact(map, enemy)`（覆盖 4/5/6），再叠加 `CrystalCavernBossRewards.Enabled(run)` 的 1/2/3。
**不按名字、不按通用 Boss 枚举、不按 `ForestBossBrain` 判断。**

### 1.2 普通掉落投影（名义均值，不是本局哈希结果）

| 字段 | 工厂分布 | 名义均值 | 投影值 |
|---|---|---:|---:|
| `MonsterHide` 兽皮 | 不掉落 | 0 | 0 |
| `Ore` 铁矿 | `2 + hash%3` → 2/3/4 | 3 | 3 |
| `CrystalShard` 晶石 | `3 + hash%3` → 3/4/5 | 4 | 4 |
| `Gear` 装备机会 | 恰好 1 件新武器 | 1 | 1 |
| `BossCore` | 不掉落 | 0 | 0 |

- 共享定义落在 `CrystalCavernBossRewardProjection`：`OreBase=2, OreVariants=3, CrystalBase=3, CrystalVariants=3, GearCount=1`。
  真实工厂 `CrystalCavernBossRewards.Drop` 改用同一组常量，**表达式结构不变**：`OreBase + (int)(Number("/ore") % OreVariants)`。
  该替换对任意 `uint` 哈希值逐位等价（`%3` 的残数集合恒为 {0,1,2}），因此确定性掉落完整载荷不变。
- 只读投影**不调用** `Drop` / `Earn`，不写盘、不创建物品/地面对象、不推进随机流、不发首奖、不改 revision。
- 永久首奖 `c24.special.crystal-warden-first` 归 Profile，三种状态（未获得/待领/已领）都不进入每局普通收益。
- Boss 死亡后 `localEnemies` 已过滤 `Health.Dead`，不再预测未来击杀收益；地面物按 `!Collected` 计一次，拾取后自动移除。
- 「未挑战」不是无风险可领资源：`map.points` 中该 POI 的 label 由 B1 起已含「可选挑战」，本批不新增字段、不改 label、不改风险函数、权重或挑战门禁。
- 评分权重、排序、六份旧地图（森林/遗迹/C21/C22/C23 闭桥/C23 开桥）字段与顺序合同保持不动。

### 1.3 明确不做

不改真实掉落、首奖、随机流、评分权重、武器、护甲、经验、v9 存档格式；不改 `RouteEvaluation` 字段集合（避免破坏 B1 逐字段对照）。

---

## 2. B2-02 晶环接触合同 `C24-B2-RING-1`

### 2.1 语义变更声明（不伪称旧行为不变）

旧实现以**玩家根点**（`target.transform.position`）的水平距离与根点 y 差判断：
`2.2 <= |flat| <= 6 && |delta.y| <= 1.2`。
B1 证据显示 inner≈2.1、outer≈6.1 两组真实 CharacterController 胶囊已与环带相交，但根点在安全侧，HP 保持 48→48。

**本批正式改为「实际受击体接触环带」**。这会缩小擦边安全余量，是玩法语义变更，不是等价修补、不是物理 API 修补。
只改 C24 HollowRing；CrossLines / Claw / Volley / 旧森林 Boss / 玩家武器几何 / 数值一律不动。

### 2.2 冻结参数（单一来源：`CrystalCavernRingContact`）

| 参数 | 冻结值 | 说明 |
|---|---:|---|
| 内半径 `InnerRadius` | 2.2 m | **不缩小** |
| 外半径 `OuterRadius` | 6.0 m | **不扩大**；等于 `Definition(HollowRing, _).range` |
| 竖直半高 `HalfHeight` | 1.2 m | 相对**冻结攻击原点** `AttackOrigin.y`，带为 `[y-1.2, y+1.2]`；**不扩大攻击带** |
| 预警 `windup` | 1.6 s | `CrystalCavernBossRules.Definition`，不改 |
| 激活 / 恢复 | 0.15 s / 1.8 s | 现有值，不改 |
| 原始伤害 | 22 | 现有值，不改；护甲经 `ArmorMitigation.Incoming` |
| 环心 / 冻结时刻 | `AttackOrigin` | 在 `Begin()` 冻结，`ShowWarning` 与 `HitArea` 读同一字段 |
| `WarningGroundOffset` | 0.08 m | 2D 指示圆的地面投影高度，由 `WarningPlane()` 约束在带内 |
| `ContactEpsilon` | `1f / 10000` = 0.0001 m | **测试前冻结**；仅吸收 float 误差，不是玩法容差 |
| broad-phase 半径 | `sqrt(6² + 1.2²) + ContactEpsilon` ≈ 6.1189 m | 保证任何与环形柱体相交的 Collider 都在球内 |

### 2.3 有效受击体（effective hit body）

- 取 `target.gameObject.GetComponents<Collider>()` 中 **enabled 且非 trigger** 的 Collider，按引用去重。
- 仅 **`CharacterController` / `CapsuleCollider`(Y 轴) / `SphereCollider`** 视为受击体，各自换算为世界空间胶囊：
  `center = TransformPoint(本地 center)`；`radius = 本地 radius * max(|scale.x|,|scale.z|)`；
  `height = max(本地 height * |scale.y|, 2*radius)`。
- **只读根物体上的 Collider**；子物体（武器模型、Renderer、装饰 MeshCollider）一律不是受击体。
  这是「持武器模型不成为额外受击体」的结构性保证，不依赖截图或给定站位。
- **不使用 Renderer、不使用 `Collider.bounds` / AABB 相交**作为 narrow phase 判定依据。
- 不使用硬编码 `0.4`：半径、高度、中心全部取自当前真实 Collider。

### 2.4 narrow phase：胶囊 × 环形柱体精确相交

把环带视为有限环形柱体 `A = { q : 2.2 <= ρ(q) <= 6, |q.y - O.y| <= 1.2 }`（轴为过 `O` 的竖直线）。
胶囊为「竖直线段 `S` 与半径 `r` 球的 Minkowski 和」，其中 `S` 的 y 区间为
`[c.y - (h/2 - r), c.y + (h/2 - r)]`，水平距离为 `d`。

对任意 `p ∈ S`，`dist(p, A) = sqrt(dr² + dy²)`，其中

```
dr   = d < 2.2 ? 2.2 - d : d > 6 ? d - 6 : 0
vgap = max(0, (O.y - 1.2) - S.maxY, S.minY - (O.y + 1.2))
```

因 `S` 是竖直线段、`d` 恒定，`dy` 的最小值即 `vgap`。故

> **接触 ⇔ `dr² + vgap² <= (r + ContactEpsilon)²`**

该式同时正确处理：完全内侧安全区、完全外侧、内/外切线、中心空洞、跨竖直攻击带、以及胶囊上下端盖。
`dr=0` 且 `vgap=0` 时恒接触（根点也在带内的旧样本不会退化）。

### 2.5 切线与容差规则（先冻结）

1. 环带是**闭集**：恰好相切（`dr == r` 或 `vgap == r`）算接触（比较用 `<=`）。
2. 超出 `r` 超过 `ContactEpsilon` 才算不接触；`ContactEpsilon` 不随样本调整。
3. B1 的 inner/outer/band/safe 四组只作为**验收样本**，不参与参数拟合；不得为使其通过而改半径或容差。
4. 历史样本按 `ring-release.json` 的精确值判定，不使用四舍五入表格值。
5. **运行前校正记录**：竖直切线用例的 centerY 初稿按 `origin.y=0` 写成 2.2/2.201；
   在写入 `contract.json` 后、运行任何测试之前，按本批实际 `origin.y=0.08` 解析校正为 2.28/2.281。
   `InnerRadius` / `OuterRadius` / `HalfHeight` / `ContactEpsilon` / 闭集切线规则**均未改变**，
   这不是为通过样本事后拟合容差。

### 2.6 判定分层与一次伤害机会

| 层 | 变量 | 失败时后果 |
|---|---|---|
| broad phase | `contact`：`Physics.OverlapSphere(...).Any(parent hero == target)` | 只筛候选，不触发伤害 |
| narrow phase | `geometry`：`CrystalCavernRingContact.Touches(...)` | 不触发伤害 |
| 实体遮挡 | `clear`：现有 `Physics.RaycastAll` 视线检查 | 不触发伤害 |
| 翻滚免疫 | `evaded`：`Dodge.IsInvulnerable` | `CombatHealth.Damage` 自行返回，**0 伤害不是几何测试失败** |
| 实际扣血 | `applied`：`HealthObservation` / HP 前后差 | 与几何分开记录 |

- 伤害只能经 `target.Health.Damage(def.damage, ...)`，不直接改 HP；有防御时以 `ArmorMitigation.Incoming(22, defense)` 计算预期扣血，**不固定期待 22**。
- 保留 `hit` 一次机会合同：同一次释放对同一角色最多一次 `Damage`。
- 暂停（`GameplayPaused` / `timeScale<=0`）只顺延 `until`；死亡、离开 arena、`OnDisable` 走 `CancelIntent`/`StopDeath`，不补放旧晶环、不重复命中。
- 每次 Active 帧的 HollowRing 判定发出只读 `RingProbe` 观测（几何/遮挡/免疫/实际扣血/受击体数量分别成列），不影响伤害决策；重复 Collider 与已消费的多帧同样记录。

### 2.7 冻结的验收样本期望（写入测试前）

统一条件：`O=(116,0.08,410)`，`r=0.4`，`h=2.0`，胶囊中心 y=1.08（地面站位），无遮挡、无翻滚。

| ID | 水平距离 d | 期望接触 | 说明 |
|---|---:|---|---|
| `b1-inner` | 2.100006 | **TRUE** | B1 inner，胶囊 1.700006–2.500006 |
| `b1-outer` | 6.100006 | **TRUE** | B1 outer，胶囊 5.700006–6.500006 |
| `b1-band` | 3.199982 | **TRUE** | B1 band，原实现已命中 |
| `b1-safe` | 7.0 | **FALSE** | B1 safe，胶囊 6.6–7.4 |
| `hole-center` | 0.0 | FALSE | 完全在中心空洞内 |
| `inner-full-safe` | 1.7 | FALSE | `d+r=2.1 < 2.2-ε` |
| `outer-full-safe` | 6.5 | FALSE | `d-r=6.1 > 6+ε` |
| `inner-tangent` | 1.8 | **TRUE** | `d+r=2.2` 精确内切线 |
| `inner-just-out` | 1.799 | FALSE | 超出 `r` 0.001 > ε |
| `outer-tangent` | 6.4 | **TRUE** | `d-r=6.0` 精确外切线 |
| `outer-just-out` | 6.401 | FALSE | 超出 `r` 0.001 > ε |
| `height-above` | 3.199982，中心 y=3.0 | FALSE | 竖直脱离攻击带 |
| `height-tangent` | 3.199982，中心 y=2.28 | **TRUE** | `0.08+1.2+0.4+0.6`，`vgap == r` 精确切线 |
| `height-just-out` | 3.199982，中心 y=2.281 | FALSE | `vgap=0.401 > r+ε` |
| `wall-behind` | 3.199982 | TRUE（几何） | 遮挡层 `clear=FALSE` ⇒ 不扣血 |
| `roll-immune` | 3.199982 | TRUE（几何） | 免疫 ⇒ 0 扣血，不判几何失败 |
| `duplicate-bodies` | 3.199982 | TRUE（去重） | 多 Collider 只结算一次 |
| `repeat-frame` | 3.199982 | — | 同释放多帧不再伤害 |

> 「墙后 / 翻滚免疫 / 重复 Collider / 同次窗口多帧 / 七武器配对」属于**运行态合同**。
> 本批若无法产生新的 Unity Editor / 观测 Player 运行，这些项按 `NOT_RUN` 登记，
> 只保留源码控制流证明与几何模型结果，绝不把模型算作运行证据。

### 2.8 竖直范围的版本化记录

旧实现的 `|delta.y| <= 1.2` 以**根点**相对 `AttackOrigin` 度量；新实现把同一 1.2 解释为
「相对冻结攻击原点的攻击带半高」，并要求**受击胶囊**与之相交。对地面站位两者等价；
对腾空/高差站位，新语义更严格且明确。此差异是本设计决定的一部分，**不是扩大攻击带**，
也未把旧根点口径偷偷保留。现有两条 2D 圆环指示线只表达水平环带在地面上的投影，
不能图形化表达竖直带；这一可视化限制登记为开放项，不在本批用改数值的方式掩盖。

---

## 3. B2-03 证据合同 `C24-B2-C05-CORRELATION-1`

- 不改写历史报告；`WindupNewAudit1/audit.json` 的 `INCOMPLETE` 与 `toolVersion 2.0` 原样保留。
- 本批新增的是**冻结原始逐帧事件的只读关联**，证据层级为「历史原始事件再关联」，不是新 Unity/Player 运行。
- 关联键：`frame` + `time` + 招式名 + `Releases` 计数 + HP 变化，四份独立 TSV 交叉核对：
  `windup-health.tsv`（Boss HP）、`windup-release.tsv`（`Released` 事件）、
  `windup-hero-health.tsv`（`HealthObservation`）、`windup-timeline.tsv`（只读逐帧状态）、
  `windup-transition.tsv`（独立转阶段帧）。
- 消解历史「无共享 attackId」限制的方式：整个观测窗口内 `windup-release.tsv` **恰有 1 行**、
  `windup-hero-health.tsv` **恰有 1 行 Damage**，且损伤行记录了当时的 `boss.Attack` 与 `boss.Releases`；
  在唯一性约束下不存在第二个可归因来源。不新增存档字段、不新增遥测外发、不新建测试平台。
- 消解「无独立恢复结束事件」的方式：`windup-timeline.tsv` 的最后一帧 Recovery（`Remaining>0`）
  与 `windup-transition.tsv` 的首帧 Transition 是两份**独立写入**的逐帧记录，不使用
  `windup-summary.json` 中由 driver 同时赋值的 `recoveryObserved`/`transition` 对。
- 时间链：P1 Claw `Begin` → 前摇期间 Boss HP 真实跨半血 → 本次 `Release` 仍为 P1 参数
  → 同帧 `Damage` 回执 → P1 完整 Recovery → Transition → P2 下一招（`Next(0,true)=CrossLines`，
  源码模型 + 同构建 `phase-releases.tsv`；**不是同一次运行**，据此标注）。
- 不改状态机、不改旧 C02/C04 严格三维起点 FAIL、不改旧严格逐值比较口径。

---

## 4. 证据分层与保护

| 层级 | 本批可用手段 | 可否标为「已运行」 |
|---|---|---|
| 静态源码审查 / 控制流模型 | 直接读取源码 | 是（静态） |
| 公式/几何模型（确定性脚本） | Python 复算 | 是（模型层，非运行层） |
| Unity Editor | 视本机可用性 | 仅当实际产生 Editor 日志与输出 |
| 非开发观测 Player | 视本机可用性 | 仅当实际产生 Player 日志与输出 |
| 纯发行包 / 原生输入 / 独立人工 | 本批不执行 | `NOT_RUN` |

保护：不改用户场景、`ProjectSettings`、未提交修改、真实存档、旧证据；不升级依赖、不新增 CI、
不 force push、不自动合并 `main`；不提交 `Library` / Player 二进制 / 凭据 / 受限供应商源码。

后续批次 `SKILL-STATE-01`、`CP06-INTEGRATION-01`、`UX-PROGRESSION-01` 不在本批启动。
