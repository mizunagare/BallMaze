# DAMAGE_MODEL — PH-R2-R1 伤害模型与逐段校验

> 本文件回答：**"伤害数字对不对？"** 以及 **"是不是只对了总数？"**
> 结论：三个 Run 的 40 项数值断言逐条通过，其中 `staff.field` 已按
> `{0.65, 0.40, 0.40, 0.40}` **逐段**校验，不再用统一 `expectedPerHit` 蒙总数。

---

## 1. 缺陷回顾（R1-03）

PH-R2 的 `Staff.field` 校验用单一 `expectedPerHit`：

```
expectedPerHit = 0.65 × AP = 21.45
expectedTotal  = 21.45 × 4 = 85.80     ← 错
```

产品实际是 **1 段 65% + 3 段 40%**（`WeaponSkillExpansion.cs` 定义：
`power=.65f, pulses=3, pulsePower=.40f`），真实总伤 **61.05**。
统一模型会让每一段都记 `expectedDamage=21.45`，第 2–4 段必然"不匹配"，
于是只能退化成"只查总伤害"——这正是审计指出的问题。

**修正**：按命中序号取倍率数组，逐段比对。

```csharp
float[] expectedHitRatios = { 0.65f, 0.40f, 0.40f, 0.40f };
// RecordDamageHit / FinalizeDamageForensics:
float expected = expectedHitRatios[hitIndex] * attackerAttackPower;
```

---

## 2. 三个 Run 的实测数值

固定条件：目标 `c1:elite`（Elite），`initialHP=140`，`attackerAttackPower=33`。

### 2.1 C-GATE — `sword.triple`（基线对照，3 段均 65%）

| hitId | HP before | HP after | actualDamage | expectedDamage | 实际倍率 | hitTime |
|---|---|---|---|---|---|---|
| 1 | 140.00 | 118.55 | 21.45 | 21.45 | 0.650 | 1.992439 |
| 2 | 118.55 | 97.10 | 21.45 | 21.45 | 0.650 | 2.217359 |
| 3 | 97.10 | 75.65 | 21.45 | 21.45 | 0.650 | 2.438195 |
| **合计** | 140 → 75.65 | | **64.35** | **64.35** | ratio **1.000** | |

- 每段 = 33 × 0.65 = 21.45，三段全等 → 与 PH-R2 的 `140→118.55→97.10→75.65` 完全一致（可复现）。
- 冷却 `measured=7.10633s` vs 期望 7.00s（容差 −0.6/+1.5）→ 通过；冷却中重按被拦截 `blockedDuringCooldown=true`。

### 2.2 STAFF-FIELD — `staff.field`（**本批重点**，0.65 + 0.40×3）

| hitId | HP before | HP after | actualDamage | expectedDamage | 实际倍率 | hitTime |
|---|---|---|---|---|---|---|
| 1 | 140.00 | 118.55 | **21.45** | **21.45** | **0.650** | 2.139926 |
| 2 | 118.55 | 105.35 | **13.20** | **13.20** | **0.400** | 2.391986 |
| 3 | 105.35 | 92.15 | **13.20** | **13.20** | **0.400** | 2.995885 |
| 4 | 92.15 | 78.95 | **13.20** | **13.20** | **0.400** | 3.597335 |
| **合计** | 140 → 78.95 | | **61.05** | **61.05** | ratio **1.000** | |

- result.json 中 `expectedHitRatios = [0.65, 0.4, 0.4, 0.4]`、`expectedPerHit=0.65`（首段语义）、`expectedTotal=61.05`。
- 逐段 expected 全部命中（13.20 = 33 × 0.40），**不是**用 21.45 去凑总数。
- 冷却 `measured=9.106946s` vs 期望 9.00s → 通过。

#### 反证：如果沿用旧模型会怎样

| 校验方式 | 第2段 expected | 第2段 actual | 判定 |
|---|---|---|---|
| 旧（统一 0.65） | 21.45 | 13.20 | ✗ 不匹配 |
| 旧（只看总数 85.80） | — | 61.05 | ✗ 不匹配 |
| 旧（只看总数但改成 61.05） | — | 61.05 | ○ 通过，但**掩盖了第1段与后3段混同** |
| **新（逐段 ratio）** | **13.20** | **13.20** | **✓ 且能区分 0.65 与 0.40** |

### 2.3 TWIN-COUNTER — `twin.counter`（强化 1.8× / 基线 0.65×）

> **修订（PH-R2-R1-FIX-02）**：本表原先把 `hitTime`（产品时钟 `Time.timeAsDouble`）与
> `evadeSeenAt`（Harness 时钟 `Time.unscaledTime`）并列，读者会得出"contact 早于 evade"的错误结论。
> 现改为**双时钟分列 + 统一换算列**，换算偏移由两条独立事件流各自推导（见 §2.3.1）。
> 伤害数值未变，仅修正呈现方式。

| hitId | 阶段 | HP before | HP after | actualDamage | 期望公式 | 实际倍率 | `activeTime`（产品钟） | `unscaledTime`（统一后） |
|---|---|---|---|---|---|---|---|---|
| 1 | counter（第1次，强化） | 140.00 | 80.60 | **59.40** | 33 × 1.8 = 59.40 | **1.800** | 3.444509 | **7.803075** |
| 2 | counter（第2次，已消费） | 80.60 | 59.15 | **21.45** | 33 × 0.65 = 21.45 | **0.650** | 12.941937 | **17.300503** |
| **合计** | 140 → 59.15 | | **80.85** | **80.85** | ratio **1.000** | | |

- 统一时钟下两次接触间隔 `17.300503 − 7.803075 = 9.497s`，覆盖 `twin.counter` 9.5s 冷却 → "技能冷却结束"这一条成立。
- 第 2 次伤害回落到 **0.65×基线**（而非 1.8×）是"强化状态已被消费"的数值侧旁证。

#### 2.3.1 时钟定义与换算偏移

| 字段族 | 时钟 | 来源 |
|---|---|---|
| `keyEvents` / `skillStarts` / `skillCompletes` / `casts` / `t3.evadeSeenAt` / `harness.log` 前缀 | `Time.unscaledTime` | Harness 内部统一使用 |
| `damage-events.hitTime`(`hitActiveTime`) / `target-events.activeTime` / `observations.time` | `Time.timeAsDouble` | `CombatHealth.cs` → `HealthObservation.activeTime` |

偏移量由**两条互不相同的事件流**各推一次（不是同一来源的重复读取）：

| 推定路径 | `unscaledTime` | `activeTime` | 偏移 |
|---|---|---|---|
| 技能 start（首次施放） | 7.520294 | 3.161727 | **4.358567** |
| actual-evaded-attack | 7.187345 | 2.828779 | **4.358566** |
| | | | 两路差 **1e-6 s** |

换算公式：`unscaled = activeTime + 4.358567`（本 Run 专用常数；不同进程启动时刻不同，不可跨 Run 复用）。

#### 2.3.2 统一时钟下的完整因果序列

| 序号 | 事件 | 统一 `unscaledTime` | 依据 |
|---|---|---|---|
| 1 | 翻滚（i-frames，强化窗口开启） | **7.187** | `t3.evadeSeenAt` |
| 2 | 反击 F 按下 | 7.515 | `casts[2].at` |
| 3 | **第一次 contact** | **7.803** | 换算（Δ = +0.616s ≤ 0.85s 强化窗）→ 59.40 = 33×1.8 |
| 4 | 反击 complete | 8.047 | `skillCompletes[0]` |
| 5 | 第二次 F 按下 | 17.015 | `casts[3].at`（距首次 F 按下 **9.500s** ≈ 冷却 9.5s） |
| 6 | **第二次 contact** | **17.301** | 换算 → 21.45 = 33×0.65，`secondCounterEmpowered=false` |

帧号（无时钟依赖）提供第三重印证：翻滚帧 703/717 < 首次命中帧 903；命中 #1 帧 903 ∈ F 按下/抬起窗口 [815, 904]；命中 #2 帧 3732 ∈ [3647, 3733]。
原始数据：`Evidence/PH-R2-R1-FIX/recompute/twin-timeline.json`。

---

## 3. 校验维度（不止"总数"）

每个 Run 都跑同一套 11 项结构校验（`python player_acceptance_driver.py recompute`）：

| # | 校验项 | 含义 |
|---|---|---|
| 1 | hit count matches product definition | 命中数与产品定义一致（3 / 2 / 4） |
| 2 | raw target-events count == damage-events count | 两路原始证据互相印证（防单路伪造） |
| 3 | hitId sequence is 1..N | hitId 唯一且连续 |
| 4 | all hits share one targetId | 目标一致，无串怪 |
| 5 | hitTime strictly increasing | 时序正确 |
| 6 | HP chain continuous | `before[i] == after[i-1]`，且首段从 `initialHP` 开始 |
| 7 | actualDamage == HP delta | 应用伤害与 HP 差值一致（防"报数不改血"） |
| 8 | per-segment expectedDamage == AP × ratio[i] | **逐段倍率**（本轮核心修正） |
| 9 | total == sum of per-segment | 总数只作为副产物，不作为唯一依据 |
| 10 | cooldown realised within tolerance | 冷却真实计时（7.106 / 9.107） |
| 11 | re-cast during cooldown blocked | 冷却期重按被拦 |
| 12–18 | T3 专属（仅 TWIN）：evade / roll / 1.8× / 冷却间隔 / 第二次 contact / 非强化 / 0.65× | 见 ACCEPTANCE.md |

实测：C-GATE 11/11、TWIN 18/18、STAFF 11/11 → **40/40 通过**（`Evidence/PH-R2-R1/RECOMPUTE.json`）。

---

## 4. 判定公式

单段：

```
expected_i = AP × ratio[i]
actual_i   = HP_before_i − HP_after_i
ok_i       = |actual_i − applied_i| ≤ 0.05  ∧  |actual_i − expected_i| ≤ 0.05
total_ok   = |Σ actual_i − Σ expected_i| ≤ 0.05
damageOk   = ∀i ok_i  ∧  total_ok  ∧  HP 链连续
```

整体（含身份）：

```
PASS = ¬failed ∧ completes ≥ 1 ∧ cooldownOk ∧ descOk ∧ zeroDamageOk
       ∧ T3VerdictOk ∧ damageOk ∧ identityVerified ∧ ¬incomplete
```

> 数值不做四舍五入取整比较：全部以 float 原始值（如 `97.10001`、`59.39999`）落盘，
> 比较用统一容差，避免"看起来相等"掩盖累积误差。

---

## 5. 未改动声明

| 对象 | 状态 | 证据 |
|---|---|---|
| `Assets/CombatPrototype/WeaponSkillExpansion.cs` | 未修改 | `git diff` 无该文件 |
| `Assets/CombatPrototype/NewWeaponCombat.cs` | 未修改 | 同上 |
| 冷却数值 / 1.8× 强化倍率 / 0.65 基线 | 未修改 | 同上 |
| AppData 存档（default + legacy） | 未触碰 | `INDEX.json → appdataProtection` |

本批只改"**怎么验**"（Harness / Driver），没有改"**验什么**"（产品数值）。
