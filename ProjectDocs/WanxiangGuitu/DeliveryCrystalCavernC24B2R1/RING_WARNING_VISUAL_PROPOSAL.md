# CP06-C24-B2-R1 · 晶环预警可读性最小设计方案

状态：**DESIGN_ONLY / NOT_IMPLEMENTED**（本批只提交设计与可视化验证方案，不修改产品代码）
合同版本：`C24-B2-RING-1`（几何参数冻结，见 `DeliveryCrystalCavernC24B2/DESIGN_DECISIONS.md`）
适用范围：仅 C2.4 晶脊守望者 `HollowRing` 蓄力阶段的预警表现。

---

## 1. 问题

当前 `CrystalCavernBossBrain.ShowWarning()` 的 HollowRing 分支只画两条**地面二维圆环**：

```csharp
var ground = CrystalCavernRingContact.WarningPlane(AttackOrigin);   // origin + up*0.08
for (int j = 0; j < 2; j++) { ... radius = j == 0 ? InnerRadius : OuterRadius; ... }
```

它表达的是水平 `[2.2m, 6.0m]` 环带在地面上的投影。但真正造成伤害的是**有限高的环形柱体**：

| 判定维度 | 冻结值 | 二维地面环是否表达 |
|---|---|---|
| 内半径 | `InnerRadius = 2.2` | 是 |
| 外半径 | `OuterRadius = 6` | 是 |
| 竖直攻击带 | `origin.y ± HalfHeight = ±1.2m` | **否** |
| 闭集切线 | `dr² + vgap² ≤ (r + ε)²`，`ε = 1e-4` | 否（判定容差，不应可视化） |
| 预警平面偏移 | `WarningGroundOffset = .08` | 隐含 |

因此玩家可能站在正确水平环带内、但处于攻击带**上方或下方**（例如跳跃、平台高差、地形起伏），看到圆环却无法从预警推断竖直危险性；反之亦然。这是**信息差异**，不是几何错误。

## 2. 设计约束（不可协商）

- 不修改 `InnerRadius` / `OuterRadius` / `HalfHeight` / `ContactEpsilon` / 闭集切线 / 原始伤害 `22`。
- 不修改预警时长 `1.6s`、`Active` 窗口、恢复时长、伤害入口 `CombatHealth.Damage`、护甲公式、LOS 遮挡、翻滚免疫、一次伤害机会合同。
- 不扩展全局 Boss 警告系统，不改 `CombatFeedback.BossWarning`。
- 视觉只做**表现层**，判定仍完全由 `CrystalCavernRingContact` 与 `HitArea()` 决定。
- 不遮挡 Boss 与玩家：不写深度、不铺满屏幕、不使用不透明面片。

## 3. 最小视觉设计

### 3.1 保留层（不变）

两条地面圆环 `LineRenderer`，各 65 点，`warningMaterial`（URP/Unlit，橙 `Color(1,.55f,.12f)`），
平面 = `CrystalCavernRingContact.WarningPlane(AttackOrigin)`。这是玩家已熟悉的水平锚点。

### 3.2 新增层 A：上下高度边界环

在 `origin.y - HalfHeight` 与 `origin.y + HalfHeight` 各画一条**半透明水平环线**，
半径仍为 `InnerRadius` / `OuterRadius`（共 4 条，或简化为各 1 条外环 = 2 条）。
它们与地面环构成"可见的柱体上下盖"，直接把 ±1.2m 变成可读的高度区间。

| 元素 | 数量 | 半径 | y | 线宽 | 颜色 / alpha |
|---|---|---|---|---|---|
| 地面内/外环（保留） | 2 | 2.2 / 6.0 | `origin.y + .08` | `.09` | 橙 / 1.0 |
| 高度边界外环 | 2 | 6.0 | `origin.y ± 1.2` | `.06` | 橙 / **0.35** |
| 高度边界内环（可选） | 2 | 2.2 | `origin.y ± 1.2` | `.05` | 橙 / **0.28** |

`warnings` 数组当前长度为 3，需增加到 5–7 条；纯表现层扩容，不改判定。

### 3.3 新增层 B：垂直晶柱（高度连接线）

在内/外环各取 8 个等角采样点（`i * 45°`），用细 `LineRenderer` 或细长 Mesh 连接
`origin.y - 1.2` 与 `origin.y + 1.2`，形成 16 根短"晶柱"。它们只暗示竖直范围，
**不是**碰撞体、不是判定边界、不参与 `Physics` 查询。

- 线宽 ≤ `.045`，alpha `0.25`，`useWorldSpace = true`。
- 与 `AttackOrigin` 同一冻结环心；不使用 `transform.position`（避免 Boss 位移造成视觉/判定错位）。
- 渲染：`ZWrite Off`，透明队列，`sharedMaterial` 复用，不产生新的每帧分配。

### 3.4 动画与可读性

- 蓄力 `1.6s` 内，高度层 alpha 从 `0 → 目标值` 线性渐显（用 `Remaining / def.windup` 驱动），
  地面环保持常亮，避免"突然出现一堵墙"造成误判。
- 释放瞬间 `HideWarning()` 统一隐藏所有层，与现有 `Active` 窗口对齐。
- 不使用屏幕空间闪烁、全屏染色或 UI 遮罩；不遮挡 Boss 模型与玩家角色。
- 颜色全部沿用现有橙色，仅用 alpha 区分"水平锚点 / 高度提示"，避免引入新的语义色。

## 4. 视觉边界与冻结几何的对应关系

| 视觉元素 | 对应冻结常量 | 是否参与伤害判定 |
|---|---|---|
| 地面内环 | `InnerRadius = 2.2` | 否（判定用 `dr`） |
| 地面外环 | `OuterRadius = 6` | 否（判定用 `dr`） |
| 上/下高度环 | `origin.y ± HalfHeight`，`HalfHeight = 1.2` | 否（判定用 `vgap`） |
| 垂直晶柱长度 | `2 * HalfHeight = 2.4` | 否 |
| 地面平面 | `WarningPlane(origin)`，`offset = .08` | 否 |
| `ContactEpsilon = 1e-4` | **不可视化** | 是（仅浮点噪声容差） |

> 关键：`ε` 是判定容差，不是玩家应感知的安全余量；把它画出来会诱导玩家"贴边试探"，
> 因此刻意不表达。闭集切线同理，只由几何公式保证。

## 5. 明确不改动清单

- `CrystalCavernRingContact.cs`：常量、`Touches()`、`Bodies()`、`TouchesAny()`、`WarningPlane()` 全部不变。
- `CrystalCavernBossBrain.HitArea()`：broad/narrow phase、`RingProbe`、`hit` 一次机会、`CombatHealth.Damage` 全部不变。
- `CrystalCavernBossRules.Definition(HollowRing)`：windup `1.6`、recovery `1.8`、damage `22`、range `6` 全部不变。
- `CrystalCavernBossRewards` / `CrystalCavernBossRewardProjection` / `RouteScoring` 全部不变。
- 真实掉落、首奖、随机流、评分权重、武器/护甲/经验、v9 存档格式全部不变。

## 6. 本批验证范围与后续

本批**只交付设计与可视化验证清单**，不实现、不改产品源码。

后续若复审批准实现，最小可视化验证（独立批次）应包含：

| 检查 | 层级 | 说明 |
|---|---|---|
| 高度环 y 严格等于 `origin.y ± 1.2` | PASS-EDITOR | 隔离 Editor 读取 LineRenderer 世界坐标 |
| 内外环半径严格 `2.2 / 6.0` | PASS-EDITOR | 同上 |
| 环心严格等于冻结 `AttackOrigin` | PASS-EDITOR | 预警与判定共享环心，不随 Boss 位移漂移 |
| 蓄力 1.6s 内 alpha 单调渐显 | PASS-PLAYER | 需观测 Player 截帧，本批 `NOT_RUN` |
| 释放时所有层同时隐藏 | PASS-PLAYER | 同上 |
| 不遮挡 Boss / 玩家（ZWrite Off、线宽上限） | PASS-STATIC | 材质与线宽源码审查 |
| 判定结果与 B2 冻结合同逐样本一致 | PASS-EDITOR | 复用 B2 `ring_contract.py` 14/14 用例 |

> 本批状态：`DESIGN_ONLY`；上述 PASS-PLAYER 项在 R1 均标 `NOT_RUN`，
> 不以 Editor 或静态模型冒充观测 Player 结果。
