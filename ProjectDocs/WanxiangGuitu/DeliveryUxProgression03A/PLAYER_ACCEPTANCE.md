# UX-PROGRESSION-03A · Player 验收标准（规格，不执行）

基线 `design/ux-progression-03a` ← `1dba0462`
适用对象：**后续实现批**。本批未启动任何 Player 进程，未重跑 P1/P1C。

---

## 1. 三层验收门槛（必须全部满足）

| 层 | 判据 | 复算方式 |
|---|---|---|
| **A 模型层** | T1/T2 共 12 项 `PASS`（`B`/`η` 落入 `CALC_MODEL.md §3` 目标带）；T3 两项 `N/A`；恒等式 `η=1+(B−1)W/C` 误差 <5e−5 | `python Evidence/Tools/build_balance_model.py --out .` |
| **B 真实 Player 层** | 每条 Run `PLAYER_RUN_COMPLETED`：`exitCode=0`、`complete.txt=PASS`、`assertions.tsv` 中 **0 FAIL** | 真实 `WanxiangGuitu.exe` + 注入驱动，禁止 Editor / 模型推算 / 直写伤害 |
| **C 回归层** | P1C 三条挑战闭环原样通过（角标 `目标达成 · 拔点/守誓/试锋 · 地区`），且 3 条 Run 与回归 3 条共用**同一版驱动 DLL SHA** | `build_driver.py -deterministic` |

**任一层不通过即整批不通过**，不允许用「模型达标」代替 Player 实测。

---

## 2. Run 预算

| 类别 | 条数 | 说明 |
|---|---|---|
| 七武器 × 稳定/高风险 | 14 | 见 `WEAPON_BUILD_VERIFICATION_MATRIX.csv`；每把武器至少 1 条训练场（技能释放）+ 1 条三地区远征（真实装备获取与实战） |
| 三档品质补充 | 2 | 至少白 + 红两档各 1 条，用于验证 `CALC_MODEL.md §5.3` 的品质缩放不对称 |
| E-A 聚能对称 | 2 | 有/无聚能各 1 条，验证 8 个旧扩展技能冷却 +1s 且 `SkillRemaining` 同步 |
| 回响 R-1 明示 | 2 | 有/无回响各 1 条，验证普攻命中体积一致、技能命中体积按规则变化 |
| P1C 闭环回归 | 3 | 森林 / 遗迹 / 洞窟各 1 条，原样重跑 |
| **合计** | **≥23 条** | 每条独立 Run ID、独立证据目录，禁止复用/覆盖 |

---

## 3. 每条 Run 必须记录的身份与原始件

沿用 P1/P1C 口径，逐条落盘：

| 字段 | 来源 |
|---|---|
| 候选 SHA（`Assembly-CSharp.dll`） | 构建产物 |
| EXE SHA（`WanxiangGuitu.exe`） | 构建产物 |
| 驱动 DLL SHA + 驱动源码 SHA | `driver-injection.json`（`-deterministic`） |
| PID / Run ID / 起止 UTC / 命令行 | `run_player.py` |
| 原始 `Player.log`、`Player.exit.json`、`Player.command.json` | 归档，不裁剪 |
| `assertions.tsv`、`int-events.jsonl`、`int-frames.tsv` | 逐条断言、事件流、逐帧采样 |
| 战斗轨迹 TSV（frame/time/dist/hp/threat/attack/dodge/...） | 驱动 P1C 段已有格式 |
| `entry-audit.jsonl`（入口与存储审计） | 驱动已有格式 |
| `run-summary.json` + `complete.txt` | 驱动 finally 段 |

**失败与中间批次全部进 `Evidence/Player/_attempts/`，不删除、不改写为 PASS。**

---

## 4. 逐项验收断言清单

### 4.1 全 Run 通用（每条必须有）

| 断言 | 判据 |
|---|---|
| `ux03a-input-path` | `KeyboardState` / `MouseState` 经 `InputSystem.QueueStateEvent` 注入；`attackPressFrames>0`、`skillPressFrames>0` |
| `ux03a-real-melee-damage` | `MeleeObservation` 或 `WeaponSkillExpansion.Observation` 记录 `before>after`，命中数 >0 |
| `ux03a-no-harness-heal` | `healEvents <= levelChoices`；驱动不得调用 `Heal` / `RestoreHealth` |
| `ux03a-no-teleport` | 归一化速度 `step/dt <= 12 m/s` 且单帧 `step < 2.5m`；记录 dt 与帧号 |
| `ux03a-no-written-state` | 驱动内 0 处 `RestorePosition` / `Respawn` / `Health.Current =` / `.Dead =` / 直写目标账本 |
| `ux03a-final-run-closed` | `complete.txt=PASS` 且 `exitCode=0` |

### 4.2 技能数值（按 `WEAPON_BUILD_VERIFICATION_MATRIX.csv` 的 `required_real_assertions`）

| 断言族 | 必须证明 |
|---|---|
| `skill-release` / `charge-locked` / `charge-fraction` | 真实按键释放；蓄力类记录 `elapsed/charge`，不得跳过蓄力直接释放 |
| `melee-contact` / `sector-contact` / `field-contact` | 每次 Release 的真实碰撞与去重（`seen`），记录 `before/after` |
| `6-phase-contact` / `3-phase-sector` / `combo-3-phase` | 多段技能每段独立结算；第 3 段同目标只 1 次 |
| `cooldown-observed` / `SkillRemaining` 回读 | 面板显示与 `skillAt` 一致；E-A 后 8 个旧扩展技能为 `def.cooldown+1` |
| `interrupted-pulse-count` / `skill-cancel-observed` | 翻滚 / UI / 换武器打断时后续段确实不造成伤害 |
| `arrow-count` / `pierce-contact×N` / `pierce-blocked` | 槽 0 箭数与品质档一致；贯穿上限 3、实心障碍即停 |
| `guard-broken` / `control-immune` / `pull-start` / `pull-obstructed` | 控制对普通/精英生效、对 Boss 免疫；`sc.pull` 自身伤害恒 0 |
| `zero-damage-assert` | `sc.pull` 不得被计入 `D`，不得据此判定 η |
| `actual-evaded-attack` / `empowered-contact` / `counter-consumed` | `twin.counter` 强化必须由真实 `CombatHealth.AttackEvaded` 触发；**未强化与强化分两条记录** |

### 4.3 词缀规则

| 断言 | 判据 |
|---|---|
| `ux03a-affix-echo-basic-unchanged` | 有/无回响时 7 套普攻的命中体积与伤害完全一致（R-1） |
| `ux03a-affix-echo-skill-enumerated` | 10 个适用技能命中体积 ×1.25；15 个不适用技能不变 |
| `ux03a-affix-focus-damage-all` | 18 个技能伤害全部 ×1.25（含留场脉冲与地面波） |
| `ux03a-affix-focus-cooldown-all` | E-A 后 18 个技能冷却全部 +1s；8 个旧扩展技能不再白拿 |
| `ux03a-affix-ui-consistent` | `WeaponTraits.Descriptions[2]/[5]` 与技能面板标注和实际行为一致 |

### 4.4 品质与回归

| 断言 | 判据 |
|---|---|
| `ux03a-quality-white-vs-red` | 槽 0 白→红 D 增长与 `SKILL_VALUE_MODEL.csv` 一致；扩展技能 D 不变 |
| `ux03a-quality-exclusive-tier` | 每条已授权品质专属只在其品质档生效；L2 两条未授权项必须 `NOT_RUN` |
| `ux03a-regression-p1c-achieved` | 三条回归 Run 角标与 P1C 一致、`Extracted`、`complete.txt=PASS` |
| `ux03a-protection-boundary` | `Assets` / `ProjectSettings` / `Packages` 树对象与基线相同；`AdventureLoadout.cs:22` 未变（D-24 未授权） |

---

## 5. 明确不允许的验收捷径

| 禁止 | 原因 |
|---|---|
| 用 Editor / 单元测试 / 模型推算代替真实 Player | 用户硬要求；AOE、贯穿、遮挡、命中率只能在真实物理场景观察 |
| 直接设置敌人死亡 / 写血量 / 写目标状态 | 同上 |
| 补满生命 / 瞬移避敌 / 修改敌人 AI | 同上 |
| 只报命中帧、不报空枪与被打断 | `H` 与 `W` 是模型的核心变量，缺一即无法复算 |
| 把 T3 的 `sc.pull` / `twin.counter` 折算成 η | 0 伤害与条件触发另设口径 |
| 把「倍率与槽 0 接近」写成通过 | 断层来自 `W`、品质缩放与判定适用范围，见 `RISK_REGISTER.md R-02` |

---

## 6. 验收状态表（本批全部 NOT_RUN）

| 类别 | 状态 |
|---|---|
| A 模型层 | **PASS（离线复算）**：12 项 T1/T2 提案全部入带，恒等式误差 4.56e−05 |
| B 真实 Player 层 | **NOT_RUN**（本批只写规格） |
| C 回归层 | **NOT_RUN**（不重跑 P1/P1C） |
| 品质专属 6 条 L1 | **NOT_RUN / 待授权** |
| 品质专属 2 条 L2 | **NOT_RUN / 需单独授权** |
| R-2 / R-3 回响 L2 | **NOT_RUN / 需单独授权** |
| D-16 / D-19 / D-20 / D-23 / D-24 | **NOT_RUN / 未授权** |

**本批交付的是「怎么验」，不是「验过了」。**
