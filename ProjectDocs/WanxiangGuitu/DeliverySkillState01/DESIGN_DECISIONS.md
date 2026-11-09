# SKILL-STATE-01 设计决定与冻结判据（测试之前冻结）

> 生效顺序：本文件 → 静态审计 → 修复前真实 Player 复现 → 仅当负例成立才最小修复 → 复验 → 交付。
> 本文件在**任何 Player 运行之前**写入。所有判据、阈值、状态定义与通过/失败规则在此冻结，
> 不因运行结果事后调整。

## 0. 授权范围与硬边界

| 项 | 约束 |
|---|---|
| 基线 | `28d9fc529ba3bc621f0f7e73a183a18fba69f867`（R2 tip） |
| 分支 | `fix/skill-state-01`（独立，不合并 main、不覆盖旧分支） |
| 目标 | 审计并**仅在复现成立时**修复技能/弹体/待命中记录的状态与时钟一致性 |
| 禁止新增 | 新技能、新字段、新存档版本、依赖升级、CI、CI 脚本 |
| 禁止修改 | 伤害、技能次数、冷却数值、瞄准、护甲、经验、经济、v9 存档格式、评分权重 |
| 禁止修改产品表现（除非复现） | 不得把 3 秒 TTL 简单放大到 30 秒；不得清空一切已释放弹体来规避问题；不得重构技能系统 |
| 保护对象 | `main` / B1 / B2 / R1 / R2 历史、用户场景、`ProjectSettings`、真实存档、旧证据、未提交修改 |
| 证据分层 | `PASS-STATIC`（源码）／`PASS-MODEL`（确定性复算）／`PASS-PLAYER`（真实观测 Player）／`NOT_RUN`／`INCOMPLETE`，不得互相冒充 |
| 证据关联 | 沿用 R1 `r1_correlate.py` 硬规则：跨 Run 事件不 join；null 时间与缺失事件不得计 PASS |

主计划第 6 节（任务书）授权范围："验证现有 `staff.field` 的 pending registry 与弹体生命周期"。
本批用户追加审计 5 项，见下。

---

## 1. 冻结的产品事实（源码读取，不是运行结论）

| 编号 | 事实 | 源码位置 |
|---|---|---|
| P-1 | `staff.field` 释放时登记 `fields[c.id] = PendingField{cast=c, expires=Time.time+3}` | `WeaponSkillExpansion.cs:45` |
| P-2 | `LateUpdate()` **在任何门禁之前、无条件**按 `Time.time >= expires` 删除到期记录 | `WeaponSkillExpansion.cs:35` |
| P-3 | 弹体 `AdventureProjectile.Update()` 在 `hero.GameplayPaused || Time.timeScale<=0` 时**直接 return**，不减 `life`、不移动、不触发命中 | `AdventureCombat.cs:279` |
| P-4 | 弹体 `life = 2.5s`，`speed = 16`（杖），`Dispose()` 自然销毁时**不发** `resolved` 观察事件 | `AdventureCombat.cs:271,290` |
| P-5 | 弹体 `Impact()` 发 `resolved`；`WeaponSkillExpansion.Projectile()` 用 `fields.TryGetValue(AttackId)` 决定是否 `SkillImpactField.Spawn()` 并发 `field-created` | `AdventureCombat.cs:301`、`WeaponSkillExpansion.cs:47` |
| P-6 | `GameplayPaused` 是**计算属性**：`HudPanelOpen \|\| HudClosedFrame==frame \|\| SaveMenuOpen \|\| Inventory.IsOpen \|\| Progression.IsChoosing \|\| Progression.ClosedFrame==frame` | `ThirdPersonHero.cs:29` |
| P-7 | 真实 UI 入口 `PlayerHudPresenter.SetDetails(page)` 打开面板时**同时**置 `HudPanelOpen=true` 与 `Time.timeScale=0`；关闭时恢复 `oldTime` | `PlayerHudPresenter.cs:67-68`（R2 已实测） |
| P-8 | `Ready` 含 `!hero.GameplayPaused && Time.timeScale>0 && !hero.Dodge.IsRolling && !Dead && ...`；`ExpandedContextReady = Ready && !PlayerInput.Suspended` | `AdventureCombat.cs:136`、`WeaponSkillExpansion.cs:56` |
| P-9 | `LateUpdate()` 若 `!ExpandedContextReady` 或武器/id 变化 → `CancelSequence()`（`active=null`，`Phase="Cancelled"`）；`CancelSequence()` **不清** `fields` | `WeaponSkillExpansion.cs:36,50` |
| P-10 | `OnDisable()` → `CancelSequence()` + `fields.Clear()` + 清理贯矢弹/符阵 + 退订 `AdventureProjectile.Observed` | `WeaponSkillExpansion.cs:52` |
| P-11 | `OnApplicationFocus(false)` → `CancelSequence()` | `WeaponSkillExpansion.cs:51` |
| P-12 | 存档 `CombatSaveData` 只含 `weaponSkillCooldown`、`skills`(等级数组)、`gear`、`mainWeapon` 等；**不含** `Selected`、`fields`、`active`、弹体、符阵 | `CombatSaveData.cs:15-27`、`CombatSaveSystem.cs:116-119` |
| P-13 | `RestoreCooldown()` 只恢复 `skillAt/attackAt/switchAt` + `CancelPending()`；存档版本 `version=9` | `AdventureCombat.cs:220`、`CombatSaveData.cs:41` |
| P-14 | 蓄力技能：`spear.charge`(`charge=.85`)、`bow.pierce`(`charge=1`)；`ChargeFraction=(Time.time-started)/charge`；按住 `PlayerInput.Held(Skill)` 且 `elapsed<charge` 时持续，松开或到上限后 `charge-locked` → `Release` | `WeaponSkillExpansion.cs:24,38` |
| P-15 | `SkillImpactField` 用 `next=Time.time+.25f`，每 `.6s` 一次脉冲、共 3 次；同样在 `GameplayPaused || timeScale<=0` 时 return | `SkillPhysicalEffects.cs:20-23` |
| P-16 | `SkillPiercingProjectile` `life=2.5s`，同样在暂停时 return | `SkillPhysicalEffects.cs:6` |

**推导（未实测）**：`Time.time` 是缩放时钟，`timeScale=0` 时冻结；UI-only 暂停
（`GameplayPaused=true && timeScale=1`）时 `Time.time` 继续增长而弹体冻结，
故 3 秒后 `fields` 记录过期、弹体仍存活 → 恢复后命中无符阵。这是主计划 F4 的
**条件性风险**，本批不得凭源码直接标 `FAIL`，必须真实 Player 复现。

---

## 2. 五类合同的冻结判据

### 2.1 法杖余烬符阵：弹体命中与延迟生成

| 判据 | 冻结规则 |
|---|---|
| C1-1 | 一次 `staff.field` 释放必须产生恰好 1 个 `AdventureProjectile`（`stage=spawn`）与恰好 1 条 `fields` 登记 |
| C1-2 | 弹体 `resolved` 且非 `resolved-blocked-origin`、且 `!hero.Health.Dead` 时，必须恰好产生 1 次 `field-created` 与 1 个 `SkillImpactField` |
| C1-3 | `resolved-blocked-origin`（实体遮挡）不得生成符阵 |
| C1-4 | 符阵生成位置 = `from - projectile.Direction*0.2f`；伤害 `c.power*0.4f`、半径 `c.def.reach` 保持产品原值 |
| C1-5 | 不暂停基线：弹体 `life=2.5s` < 记录 `TTL=3s`，因此正常情况必须**有**符阵 |

### 2.2 弓蓄力：开始 / 持续 / 释放 / 取消

| 判据 | 冻结规则 |
|---|---|
| C2-1 | `bow.pierce` 选中 slot 2；`TryCast()` 后 `Phase` 依次出现 `Startup`→`Charging`→`charge-locked`→`Release`→`Recovery`→`complete` |
| C2-2 | 蓄力期间 `ChargeFraction` 单调不减且 ∈[0,1]；`PlayerInput.Held(Skill)` 保持时不超过 `charge=1s` 不锁定 |
| C2-3 | 松开或到上限后必须锁定一次并生成 `SkillPiercingProjectile`（`pierce-spawn`） |
| C2-4 | 蓄力中 `CancelSequence()`（切槽/换武器/失焦/暂停/闪避/死亡）必须发 `cancel`，`Phase="Cancelled"`，**不得**产生后续 `pierce-spawn` 或伤害 |
| C2-5 | 不改变 `charge` 上限、`1+.85*f` 系数、贯穿 3 目标上限 |

### 2.3 生命周期：UI 暂停 / 死亡 / 闪避 / 切换武器 / 场景卸载

| 判据 | 冻结规则 |
|---|---|
| C3-1 | **全局暂停**（真实 UI 入口 `SetDetails` → `timeScale=0`）：玩家可正常进入；`Time.time` 与弹体 `life` 均冻结；恢复后状态连续 |
| C3-2 | **UI-only 暂停**（`GameplayPaused=true && timeScale=1`）：真实玩家菜单不可达（P-7），只能作为**受控状态注入**验证产品已支持的状态合同；必须显式标注 `CONTROLLED_STATE_INJECTION`，不得写成"玩家正常菜单已复现" |
| C3-3 | 死亡：弹体/贯矢弹/符阵在下一帧销毁；`fields` 在 `TTL` 内有界清理，不得无限残留；不得有补发伤害 |
| C3-4 | 闪避（`IsRolling`）：`ExpandedContextReady=false` → 进行中的 `active` 取消；**已释放**弹体不应因闪避被销毁 |
| C3-5 | 切换武器 / 切换技能槽：`CancelSequence()` 取消 `active`；已释放弹体与 `fields` 登记不被无差别清空 |
| C3-6 | 场景卸载（`GameEntry.ReturnToTitle`）：`fields.Clear()`、弹体/贯矢弹/符阵全部销毁，无补发伤害、无跨场景 `field-created` |

### 2.4 时间一致性：已释放弹体 / 等待命中记录 / 后续效果

| 判据 | 冻结规则 |
|---|---|
| C4-1 | 冻结阈值：`fields TTL = 3.0s`、`projectile life = 2.5s`、暂停时长必须 **>3.0s**（本批用 4.0s 与 2.0s 对照） |
| C4-2 | 判定式：`(弹体在恢复后仍存活) ∧ (release 后经历的有效玩法时间 ≥ TTL) ⇒ 恢复后第一次真实命中仍必须生成符阵` |
| C4-3 | `field-created` 与 `resolved` 必须**同一 Run / 同一 attackId**；一次 release 最多 1 个符阵 |
| C4-4 | 后续效果 `SkillImpactField` 的 `next/pulses` 也使用 `Time.time`，须一并检查 UI-only 暂停是否造成脉冲计时跳变 |
| C4-5 | 不得通过"延长 TTL""清空已释放弹体""禁用暂停"来规避 |

### 2.5 新进程恢复：技能状态与存档合同

| 判据 | 冻结规则 |
|---|---|
| C5-1 | 存档仅持久化 `weaponSkillCooldown`（以及等级/装备），v9 字段集合不变 |
| C5-2 | 新进程读档后 `Selected` 回槽 0（**CP06-A 明示的当前设计限制**，主计划 3 节明示不得擅自加 v9 字段或宣布为缺陷） |
| C5-3 | 读档后不得存在任何 `fields` 残留、弹体、`SkillPiercingProjectile`、`SkillImpactField`、进行中 `active` |
| C5-4 | `SkillRemaining` 必须与存档中的 `weaponSkillCooldown` 一致（受 `RestoreCooldown` 语义约束） |
| C5-5 | 读档后不得自动释放一次技能或补发伤害 |

---

## 3. 复现方案（先复现，后修复）

1. 沿用 R1 的 `build_driver.py` / `run_player.py`（哈希沿用，不依赖 PowerShell 7）。
2. 构建**干净纯发行包**（验证 Boot = 0），sidecar 驱动只注入隔离副本；纯包不含任何验证代码。
3. 每个 case 一个**独立真实 Player 进程**，各自记录 `runId / PID / buildSha / EXE SHA / 驱动 SHA`、
   命令行、日志、原生退出回执；事件严格按同一 Run 关联。
4. 驱动只调用真实业务入口：`AskNew/ConfirmNew`、`AdventureLoadout.SelectMain`、`Expanded.Select`、
   `AdventureCombat.UseSkill`、`PlayerHudPresenter.SetDetails`、`GameEntry.ReturnToTitle`、
   `AdventureCombat.RestoreCooldown`；只订阅只读产品事件。
5. 暂停矩阵：
   - `no-pause`（基线对照）
   - `global-pause-4s`（真实 UI 入口，`timeScale=0`）
   - `ui-only-pause-4s`（**受控状态注入**，`GameplayPaused=true, timeScale=1`）
   - `ui-only-pause-2s`（TTL 内对照）
   - `switch-weapon` / `switch-slot` / `dodge` / `death` / `unload` / `natural-expire`
6. 观测：`AdventureProjectile.Observed`（spawn/flight/resolved/…）、
   `WeaponSkillExpansion.Observed`（start/windup/release/field-created/cancel/complete/charge-locked）、
   `SkillImpactField` 与 `SkillPiercingProjectile` 实例计数、
   `Time.time / unscaledTime / timeScale / GameplayPaused / life / fields.Count`。

> `fields` 为 private `Dictionary<long,PendingField>`。驱动用**只读反射**读取 `fields.Count`
> 与指定 `AttackId` 是否存在，作为辅助证据；主判定仍以产品公开事件
> `resolved` ↔ `field-created` 配对为准，不以反射值单独判 PASS。

## 4. 修复门槛与最小修复边界

**门槛**：只有当真实 `PASS-PLAYER` 证据出现
`resolved == true ∧ field-created == false ∧ 弹体在暂停期间存活 ∧ 暂停时长 > TTL`
时，才判定负例成立并允许最小产品修复。静态推导、模型复算、Editor 运行均不足以触发修复。

**允许的修复方向**（主计划第 6 节）：
- 让 `fields` 的有效到期判断与弹体使用**同一个有效玩法时钟**（暂停时不推进），
  或让 pending 记录绑定弹体实际存活；
- 暂停期间不先到期；自然销毁 / 死亡 / 卸载后仍**有界清理**，不泄漏；
- 不动普攻、技能伤害/次数/冷却、瞄准、护甲、经验、经济、v9；不重构技能系统。

**禁止**：把 `Time.time+3` 改成 `Time.time+30`；把 `fields.Clear()` 加进 `CancelSequence()`；
清空所有已释放弹体；改 `life=2.5` 或 `speed`；引入新存档字段。

若负例不成立：交付**有限结论**（`NO_PRODUCT_DEFECT_REPRODUCED`），不改产品源码，
把 UI-only 状态标注为受控注入/玩家不可达，并如实列出 `NOT_RUN` 项。

## 5. 证据与判定规则

| 状态 | 含义 |
|---|---|
| `PASS-PLAYER` | 真实独立 Player 进程，同一 Run 事件满足判据，输入行/表达式/结果齐全 |
| `FAIL-PLAYER` | 真实 Player 明确违反冻结判据 |
| `PASS-STATIC` / `PASS-MODEL` | 源码审查 / 确定性复算，仅作辅助 |
| `NOT_RUN` | 未运行（含环境不可达、状态不可安全进入、对象已销毁不可观测） |
| `INCOMPLETE` | 有事件但缺身份/时间/关键行，不得计 PASS |

历史批次（B1/B2/R1/R2）的 PASS/FAIL/NOT_RUN 一律不因本批改写。
