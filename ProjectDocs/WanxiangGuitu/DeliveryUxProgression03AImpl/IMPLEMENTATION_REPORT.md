# UX-PROGRESSION-03A 默认实施包 · 实施报告

- 状态：**待评审（暂停，未合入 main，未进入 03B）**
- 实施分支：`feature/ux-progression-03a`（独立分支，从 `design/ux-progression-02 @ 1dba04623` 拉出）
- 规格来源：`WanxiangGuitu_UX_PROGRESSION_03A_Implementation_Task.md` + R1 冻结版（`design/ux-progression-03a-r1 @ 600c3dbac`）
- 报告日期：本次交付

---

## 0. 门禁（Gate）核验
| 项 | 结果 |
|---|---|
| 产品基线包含 P1 (`ff81eb1cb`) | ✅ `git merge-base --is-ancestor ff81eb1cb HEAD` |
| 产品基线包含 P1C (`4550348f1`) | ✅ `git merge-base --is-ancestor 4550348f1 HEAD` |
| 未对 main / UX-02 / 03A / 03A-R1 做任何 merge 或 cherry-pick | ✅ 仅 `feature/ux-progression-03a` 孤立前进 |
| 基线选择说明 | `integration/cp06-playable-candidate` 仅是 P1/P1C 的共同祖先，**不**包含二者；选用 `design/ux-progression-02`（已集成 P1+P1C+UX-02）满足「包含 P1/P1C」且不引入任何 merge/cherry-pick |

---

## 1. 默认包内容（已实现，4 个可回滚批次）
| 批次 | 范围 | 提交 | 说明 |
|---|---|---|---|
| **A** | P-01 技能数值（12 项 T1/T2 常量） | `78f43ca8a` | 8 旧扩展技能 + 巨剑前摇拆分 + 镰刀段间隔 |
| **B** | P-02 聚能 E-A 给 8 个旧扩展技能补 +1s 冷却 | `efa1c38fd` | `PrepareExpanded` 与 `SkillDuration` 对称补齐 |
| **C** | P-03/P-04 回响 R-1 范围澄清 + 词缀/冷却 UI | `d4e90342a` | U-01…U-06，纯文案/枚举/面板，未改判定路径 |
| **D** | 回归证据 + 文档 | （本提交） | 本报告及 ACCEPTANCE / TESTING / Evidence |

### 1.1 P-01 数值（冻结后值，已逐行 grep 核验与源码一致）
| 技能 | 字段 | 前→后 |
|---|---|---|
| sword.triple | cd | 8 → **7** |
| sword.circle | cd / gap / power | 11/.48/.55 → **10/.30/.85** |
| spear.charge | cd / charge | 9/.85 → **8/.60**（伤害不动） |
| spear.sweep | cd / gap / power | 10/.30/.80 → **9/.24/.85** |
| staff.field | cd | 10 → **9** |
| staff.echo | gap / power | .32/.55 → **.22/.70** |
| bow.burst | gap / power | .22/.55 → **.18/.62** |
| bow.pierce | cd / power / charge | 11/1.15/1.0 → **10/1.35/.70** |
| gs.cleave | startup | .80 → **.65**（共用常量按 wave 分支拆开） |
| gs.wave | startup / power | .80/.95 → **.60/1.30** |
| sc.reap | gap | .28 → **.24** |

### 1.2 P-02 聚能 E-A 对称补齐
- `WeaponSkillExpansion.TryCast`：`PrepareExpanded(def.cooldown)` → `+ (聚能?1:0)`
- `AdventureCombat.SkillDuration`：旧扩展技能分支补 `+ (聚能?1:0)`
- 槽0 既有 `+1s`（`AdventureCombat.cs:151`）为原 E-A 行为，**未改**。

### 1.3 P-03 / P-04（U-01…U-06，纯规则/文案/UI）
- **U-01** 回响描述补「不适用于普攻与旧武器扩展技能」（`WeaponTraits.cs:6`）
- **U-02** 聚能描述「全部技能冷却增加 1 秒」
- **U-03** `WeaponSkillPanel.AffixInfo`：技能窗暴露回响适用/不适用、聚能 +1s、冷却读数
- **U-04** 旧武器 4 个槽0 技能描述追加「（含回响 +25%）」（仅 area>1）
- **U-05** T3 冻结文案：灵魂牵引「0 伤害 · T3 冻结」；双刃反击「0.85s 强化窗可强化」
- **U-06** 取舍面板补三行（独占机制 / 有效距离带 / T3 专属指标）；巨剑前摇 `.65/.60` 与代码同步

---

## 2. 冻结排除项（确认未实施）
- **T3**：`twin.counter`、`sc.pull` 数值保持冻结（仅事件验收，不折算 η，不纳入 T1/T2 通过率）。
- **9 条品质专属**：全部 DESIGN_ONLY，未进默认包（见 `QUALITY_ROWS`）。
- **R-2 / R-3 / E-B / D-24**：均未实施，需单独授权。

---

## 3. 静态校验
| 校验 | 结果 |
|---|---|
| Unity 批处理编译（真实编辑器 `6000.6.5f1`，-nographics -batchmode -quit） | ✅ 退出码 **0**，`script compilation time 7.48s`，**无 `error CS` / compilation failed** |
| 平衡模型复算（Layer A，`build_balance_model.py`） | ✅ **12/12 MODEL_PASS**，`b_lt1_t12=6`，`focus_pass=8`，身份误差 ≈ 1e-16 |
| 模型产物 SHA | ✅ 与 R1 冻结运行 **逐字节一致**（param `dee5a726…`，5 个 CSV SHA 全部匹配） |
| 源码 vs 冻结 PROPOSALS 一致性 | ✅ 全部 P-01/P-02 数值经 grep 逐项核对，与 `BEFORE_AFTER_MATRIX.csv` 后值一致 |
| 编译时点说明 | 编译在「全部代码已改」状态下执行，故等同于校验最终集成代码 |

> 注：编译所用为真实 Unity 编辑器；早期误用的 `AppData/Local/Unity/bin/Unity.exe` 是 WorkBuddy 的 CLI 包装，不接收 `-batchmode`，已纠正。

---

## 4. 保护清单（0 偏差）
`git diff --stat 1dba04623 HEAD` 仅包含以下 **8 个 `.cs`** 文件（32 增 / 23 删）：

`WeaponSkillExpansion.cs`、`GreatswordCombat.cs`、`ScytheCombat.cs`、`AdventureCombat.cs`、
`NewWeaponCombat.cs`、`WeaponTraits.cs`、`SkillTradeoffs.cs`、`WeaponSkillPanel.cs`

**未触碰**：P1 / P1C 集成点、v9、经济系统、掉落表、随机流、用户文件、`ProjectSettings`、`Packages`、
`Assets/Resources`（本次编译由 Unity 生成的 `Assets/Resources.meta` 为工具副产物，**未纳入提交**）。

8 个文件最终 SHA（blob）见 `Evidence/INDEX.md`。

---

## 5. 真机 Player 验收（诚实声明）
- 要求：≥25 次真实 `WanxiangGuitu.exe` 运行 + 注入输入（`InputSystem.QueueStateEvent`）。
- 本会话**未执行**该 25 次真机运行（构建并串行跑 25 个独立构建超出本次执行边界）。
- 已交付：**`Evidence/Tools/player_acceptance_harness.cs`**（参考 C# 注入器，位于 `Evidence/Tools` 不在 `Assets/`，不会编入游戏）+ **`Evidence/Tools/player_acceptance_driver.py`**（构建 + 串行跑 + 汇总）。
- `Evidence/PLAYER_RUN_MATRIX.csv`：25 行规划用例，状态全部 **`NOT_RUN`**（T3 两行标 `T3_FROZEN`），并附预期观测。
- 运行该驱动即可将上述行翻转为 `PASS-PLAYER` / `FAIL`。

---

## 6. 交付物
- 代码：4 个批次提交（A/B/C + 本 D），分支 `feature/ux-progression-03a`。
- 文档：`IMPLEMENTATION_REPORT.md`（本）、`ACCEPTANCE.md`、`TESTING.md`。
- 证据：`Evidence/INDEX.md`、`BEFORE_AFTER_MATRIX.csv`、`SKILL_VALUE_MODEL.csv`、

  `SENSITIVITY.csv`、`FOCUS_SYMMETRY_IMPACT.csv`、`MODEL_SUMMARY.csv`、`model-run.json`、
  `PLAYER_RUN_MATRIX.csv`、两个工具脚本。

---

## 7. 下一步（暂停待评审）
1. 评审方审阅本报告与 `BEFORE_AFTER_MATRIX.csv`。
2. 在评审方环境执行 `player_acceptance_driver.py` 完成 ≥25 次真机验收（翻转 `NOT_RUN`）。
3. **不**自动合入 main，**不**进入 03B；待评审通过后再决定推送/合入策略。
