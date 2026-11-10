# UX-PROGRESSION-03A-R1 · Player 验收标准（规格，不执行）

基线 `design/ux-progression-03a-r1` ← `design/ux-progression-03a` @ `95d8337c`
适用对象：**后续实现批**。本批未启动任何 Player 进程，未重跑 P1/P1C。

> **R1 口径**：T1/T2（12 项）与 T3（2 项）分开验收；模型通过只能称 `MODEL_PASS`；
> `twin.counter` / `sc.pull` 数值冻结，用专属指标验收，不纳入 B/η 统计。

---

## 1. 三层验收门槛（必须全部满足）

| 层 | 判据 | 复算方式 |
|---|---|---|
| **A 模型层** | T1/T2 共 **12 项 `MODEL_PASS`**（`B`/`η` 落入 `CALC_MODEL.md §3` 目标带）；**T3 两项 `N/A (T3)`**；恒等式 `η=1+(B−1)×W/C` 内部误差 <1e−12；`MODEL_SUMMARY.csv` 的计数与脚本 7 条 `assert` 全部成立 | `python Evidence/Tools/build_balance_model.py --out .` |
| **B 真实 Player 层** | 每条 Run `PLAYER_RUN_COMPLETED`：`exitCode=0`、`complete.txt=PASS`、`assertions.tsv` 中 **0 FAIL** | 真实 `WanxiangGuitu.exe` + 注入驱动，禁止 Editor / 模型推算 / 直写伤害 |
| **C 回归层** | P1C 三条挑战闭环原样通过（角标 `目标达成 · 拔点/守誓/试锋 · 地区`），且 3 条 Run 与回归 3 条共用**同一版驱动 DLL SHA** | `build_driver.py -deterministic` |

**`MODEL_PASS` 只表示离线模型落入目标带，不是真实战斗通过。** 任一层不通过即整批不通过，
不允许用模型达标代替 Player 实测。

---

## 2. T1/T2 与 T3 的验收分离（R1）

| 组 | 项数 | 指标 | 本批状态 |
|---|---|---|---|
| **T1** 无独占输出 | 1（`sword.triple`） | `B ≥ 1.10`、`η ≥ 1.01` | `MODEL_PASS`（离线） |
| **T2** 独占输出 | 11 | `B ≥ 1.00`、`η ≥ 1.00` + 至少一个场景优于槽 0 | `MODEL_PASS` 11/11（离线） |
| **T3** 条件反击 / 纯控制 | 2（`twin.counter`、`sc.pull`） | **专属指标（§4.3）**，不产出 η | **全部 NOT_RUN** |

- T3 的 B/η 只保留在 `SKILL_VALUE_MODEL.csv` 的附录列（`APPENDIX_ONLY (T3)`），**不得计入通过率**；
- 不得把 T3 的 9 项专属指标与 12 项 `MODEL_PASS` 合并成一个数字；
- `8/14 B<1` 是含 2 个 T3 的全量计数；**T1/T2 是 6/12** —— 验收报告必须写清口径。

---

## 3. Run 预算

| 类别 | 条数 | 说明 |
|---|---|---|
| 七武器 × 稳定/高风险 | 14 | 见 `WEAPON_BUILD_VERIFICATION_MATRIX.csv`；每把武器至少 1 条训练场 + 1 条三地区远征 |
| 三档品质补充 | 2 | 至少白 + 红各 1 条，验证品质缩放不对称（**品质专属本身 `DESIGN_ONLY`，不验收其生效**） |
| E-A 聚能对称 | 2 | 有/无聚能各 1 条，验证 8 个旧扩展技能冷却 `+1s` 且 `SkillRemaining` 同步 |
| 回响 R-1 明示 | 2 | 有/无回响各 1 条，验证普攻命中体积一致、技能命中体积按规则变化 |
| T3 专项（`sc.pull` + `twin.counter`） | 2 | 只记录专属指标，不改数值、不算 η |
| P1C 闭环回归 | 3 | 森林 / 遗迹 / 洞窟各 1 条，原样重跑 |
| **合计** | **≥25 条** | 每条独立 Run ID、独立证据目录，禁止复用/覆盖 |

> 03A 初版写 ≥23 条；R1 增加 2 条 T3 专项 Run，统一为 **≥25 条**。

---

## 4. 逐项验收断言清单

### 4.1 全 Run 通用（每条必须有）

| 断言 | 判据 |
|---|---|
| `ux03a-input-path` | `KeyboardState` / `MouseState` 经 `InputSystem.QueueStateEvent` 注入；`attackPressFrames>0`、`skillPressFrames>0` |
| `ux03a-real-melee-damage` | `MeleeObservation` 或 `WeaponSkillExpansion.Observation` 记录 `before>after` |
| `ux03a-no-harness-heal` | `healEvents <= levelChoices`；驱动不得调用 `Heal` / `RestoreHealth` |
| `ux03a-no-teleport` | 归一化速度 `step/dt <= 12 m/s` 且单帧 `step < 2.5m`；记录 dt 与帧号 |
| `ux03a-no-written-state` | 驱动内 0 处 `RestorePosition` / `Respawn` / `Health.Current =` / `.Dead =` / 直写目标账本 |
| `ux03a-final-run-closed` | `complete.txt=PASS` 且 `exitCode=0` |

### 4.2 T1/T2 技能数值（按 `WEAPON_BUILD_VERIFICATION_MATRIX.csv`）

| 断言族 | 必须证明 |
|---|---|
| `skill-release` / `charge-locked` / `charge-fraction` | 真实按键释放；蓄力类记录 `elapsed/charge` |
| `melee-contact` / `sector-contact` / `field-contact` | 每次 Release 的真实碰撞与去重（`seen`） |
| `6-phase-contact` / `3-phase-sector` / `combo-3-phase` | 多段技能每段独立结算；第 3 段同目标只 1 次 |
| `cooldown-observed` / `SkillRemaining` 回读 | 面板显示与 `skillAt` 一致；E-A 后 8 个旧扩展技能为 `def.cooldown+1` |
| `interrupted-pulse-count` / `skill-cancel-observed` | 翻滚 / UI / 换武器打断时后续段确实不造成伤害 |
| `arrow-count` / `pierce-contact×N` / `pierce-blocked` | 槽 0 箭数与品质档一致；贯穿上限 3、实心障碍即停 |
| `guard-broken` / `control-immune` | 破防对普通/精英生效、对 Boss 免疫 |
| `ux03a-t3-frozen` | `twin.counter` 与 `sc.pull` 的 `startup/C/伤害` 与源码常量逐项一致，无 L1 改动 |

### 4.3 T3 专属指标（不折算 η，不与 T1/T2 合并）

**`sc.pull` 灵魂牵引（5 项）** —— 数值维持 `startup=0.40`、`cooldown=11`、`D=0`：

| 指标 | 记录方式 |
|---|---|
| 普通敌牵引成功率 | `pull-start` 事件数 /  eligible 目标数（排除 `control-immune`） |
| 牵引后距离 | `int-frames.tsv` 逐帧记录目标与英雄距离，验证收敛到 ≤1m |
| 控制持续时间 | `EnemyWeaponControl.PullRemaining` 或 `pull-start`→`pullLeft=0` 的时间差（源码 1s） |
| AI 恢复行为 | 牵引结束后敌人重新进入攻击/移动的帧号 |
| Boss 免疫反馈 | `control-immune` / `pull-obstructed` 事件必须成对出现且目标为 Boss |

**`twin.counter` 双刃反击（4 项）** —— 数值维持 `startup=0.28`、`C=8`、常态 `0.65×` / 强化 `1.80×`、窗 `0.85s`：

| 指标 | 记录方式 |
|---|---|
| 未触发真实 `AttackEvaded` 的普通反击 | 伤害 = `0.65×P`，无 `actual-evaded-attack` 事件 |
| 0.85s 窗口内的强化反击 | 伤害 = `1.80×P`，`actual-evaded-attack` 与 `counter-consumed` 成对 |
| 超窗后不能错误强化 | 闪避事件后 >0.85s 释放，伤害仍为 `0.65×P` |
| 同一闪避事件不能重复消费 | 连续两次释放只出现 1 次 `counter-consumed`、1 次强化 |

`zero-damage-assert`：`sc.pull` 自身伤害恒为 0，**不得被计入 D，也不得据此判定 η**。

### 4.4 词缀规则

| 断言 | 判据 |
|---|---|
| `ux03a-affix-echo-basic-unchanged` | 有/无回响时 7 套普攻命中体积与伤害完全一致（R-1） |
| `ux03a-affix-echo-skill-enumerated` | 10 个适用技能命中体积 ×1.25；15 个不适用技能不变 |
| `ux03a-affix-focus-damage-all` | 18 个技能伤害全部 ×1.25（含留场脉冲与地面波） |
| `ux03a-affix-focus-cooldown-all` | E-A 后 18 个技能冷却全部 `+1s` |
| `ux03a-affix-ui-consistent` | `WeaponTraits.Descriptions[2]/[5]` 与技能面板标注和实际行为一致 |

### 4.5 品质与回归

| 断言 | 判据 |
|---|---|
| `ux03a-quality-white-vs-red` | 槽 0 白→红 D 增长与模型一致；扩展技能 D 不变 |
| `ux03a-quality-design-only` | **9 条品质专属全部 `DESIGN_ONLY`，产品代码 0 生效；不得验收其「是否生效」** |
| `ux03a-regression-p1c-achieved` | 三条回归 Run 角标与 P1C 一致、`Extracted`、`complete.txt=PASS` |
| `ux03a-protection-boundary` | 产品树对象与基线相同；`AdventureLoadout.cs:22` 未变（D-24 未授权） |

---

## 5. 明确不允许的验收捷径

| 禁止 | 原因 |
|---|---|
| 用 Editor / 单元测试 / 模型推算代替真实 Player | 用户硬要求 |
| 直接设置敌人死亡 / 写血量 / 写目标状态 | 同上 |
| 补满生命 / 瞬移避敌 / 修改敌人 AI | 同上 |
| 只报命中帧、不报空枪与被打断 | `H` 与 `W` 是模型核心变量 |
| 把 T3 折算成 η 或并入 12 项通过率 | R1 硬规则 |
| 把 `MODEL_PASS` 写成「战斗通过」 | 离线模型 ≠ 真实战斗 |
| 把「倍率与槽 0 接近」写成通过 | 见 `RISK_REGISTER.md R-02` |
| 验收品质专属是否生效 | 9 条 `DESIGN_ONLY`，未授权 |

---

## 6. 验收状态表（本批全部 NOT_RUN）

| 类别 | 状态 |
|---|---|
| A 模型层 | **`MODEL_PASS` 12/12（离线复算）**；T3 2 项 `N/A (T3)`；恒等式误差 1.11e−16 |
| B 真实 Player 层 | **NOT_RUN**（本批只修订规格） |
| C 回归层 | **NOT_RUN**（不重跑 P1/P1C） |
| T3 专项 9 项指标 | **NOT_RUN** |
| 品质专属 9 条 | **`DESIGN_ONLY` / 未授权 / 不验收** |
| R-2 / R-3 / E-B / D-24 | **NOT_RUN / 需单独授权** |
| D-16 / D-19 / D-20 / D-23 | **NOT_RUN / 未授权** |

**本批交付的是「怎么验」，不是「验过了」。**
