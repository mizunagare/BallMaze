# UX-PROGRESSION-03A-R1 · 修订勘误（不覆盖旧历史）

基线分支：`design/ux-progression-03a-r1` ← `design/ux-progression-03a` @ `95d8337cf81408b82efdece10f0718bfdb031c7b`

本文件记录 **03A 初版 → R1 冻结版** 的 8 组口径冲突与处置。
**不修改、不删除、不 force push 已推送的 `design/ux-progression-03a` 分支**；
UX-02 的历史勘误仍单独保留在 `Evidence/ERRATA_P02.md`。
本批只修订规格与计算模型，产品代码 0 改动。

---

## E-01 · T3 被纳入 B/η 通过率统计

| 项 | 03A 初版 | R1 冻结版 |
|---|---|---|
| 表述 | 「12 项 T1/T2 全部入带 / 全部 `PASS`」，同时 T3 两项给 `N/A` | **T1/T2 = 12 项**是唯一使用 B/η 做目标判定的范围；**T3 = 2 项**（条件反击 1 + 纯控制 1）`N/A (T3)` |
| 通过名 | `PASS` | **`MODEL_PASS`**（离线模型，不是真实战斗通过） |
| 统计 | 未显式分离 | `MODEL_SUMMARY.csv` 逐项计数 + 脚本 `assert`：`total=14 / T1+T2=12 / T3=2 / model_pass=12` |
| T3 的 B/η | 与 T1/T2 同表同列展示 | 保留数值但标 `metric_status=APPENDIX_ONLY (T3)`，**不得作为目标判定、不得计入通过率** |

**影响文件**：`REPORT.md`、`CALC_MODEL.md`、`IMPLEMENTATION_SPEC.md`、`PLAYER_ACCEPTANCE.md`、
`SKILL_VALUE_MODEL.csv`、`MODEL_SUMMARY.csv`（新增）、`Evidence/Tools/build_balance_model.py`。

---

## E-02 · `8/14` 与 `6/12` 的统计解释

| 数字 | 03A 初版 | R1 冻结版 |
|---|---|---|
| `8/14 B<1` | 写成「8/14 扩展技能严格劣于同窗口一直普攻」，隐含 8 个都是输出技能 | **全 14 项（含 2 个 T3）的计数**；其中 `twin.counter`（0.666）与 `sc.pull`（0.000）不是输出技能。**不代表 8 个输出技能弱于普攻** |
| `6/12` | 未出现 | **T1/T2 输出技能的现状计数**（8 − 2 = 6），由脚本 `assert b_lt1_t12 == 6` 保证 |
| 通过率 | 未区分 | 提案后 **12/12 `MODEL_PASS`**（只统计 T1/T2） |

**影响文件**：`REPORT.md §3.1`、`CALC_MODEL.md §3.2/§5.2`、`MODEL_SUMMARY.csv`、
`IMPLEMENTATION_SPEC.md §2.1`、`RISK_REGISTER.md R-22`。

---

## E-03 · `sc.pull` 在 T3 不适用 η 却仍被提案调整数值（**矛盾核心**）

| 项 | 03A 初版 | R1 冻结版 |
|---|---|---|
| 提案 | `startup 0.40→0.30`、`SkillDuration 11→8`（`BEFORE_AFTER_MATRIX.csv` 该行有 ΔW/ΔC） | **整体撤销** |
| 理由 | 「验收按牵引成功次数而非 η」，但仍用 η 指导数值调整 | 既然 T3 不适用 η，就不应以模型为目标改常量 |
| 冻结值 | — | **`startup=0.40`、`cooldown=11`、`D=0`（0 伤害）、`W=0.75`** 全部维持源码原值 |
| 矩阵行 | `sc.pull` 有 after 数值 | `after=冻结：数值不变`、`Δ=0`、`needs_code=否（T3 冻结）`、`in_default_package=NO（T3 冻结）` |
| 未来验证 | 仅提到「牵引成功次数」 | **T3 专项 5 项**：普通敌牵引成功率、牵引后距离、控制持续时间、AI 恢复行为、Boss 免疫反馈；**未验证前保持原值** |

**影响文件**：`IMPLEMENTATION_SPEC.md §2.4/§2.5/§10`、`PROPOSALS` 表（删除 `sc.pull` 条目）、
`BEFORE_AFTER_MATRIX.csv`、`SKILL_VALUE_MODEL.csv`、`WEAPON_BUILD_VERIFICATION_MATRIX.csv`。

---

## E-04 · `twin.counter` 冻结但仍留在 η 表

| 项 | 03A 初版 | R1 冻结版 |
|---|---|---|
| 数值 | 不调数值（已正确） | 维持：`startup=0.28`、`recovery=0.24`、`C=8`、常态 `0.65×` / 强化 `1.80×`、强化窗 `0.85s` |
| 指标 | 仍列 η/B，`target_check=N/A`，但未说明「附录」 | `APPENDIX_ONLY (T3)`、`N/A (T3)`，不计入 12 项通过率 |
| 验收 | 拆「未强化 / 强化」双口径 | **4 项专属**：① 未触发真实 `AttackEvaded` 的普通反击；② 0.85s 窗内强化反击；③ 超窗后不能错误强化；④ 同一闪避事件不能重复消费 |

**影响文件**：`IMPLEMENTATION_SPEC.md §2.4`、`PLAYER_ACCEPTANCE.md §4.3`、
`WEAPON_BUILD_VERIFICATION_MATRIX.csv`、`SKILL_VALUE_MODEL.csv`。

---

## E-05 · 品质专属被混入默认实施包（且计数错误）

| 项 | 03A 初版 | R1 冻结版 |
|---|---|---|
| 默认包 | L1 表写「14 项技能 + **6 条品质专属**」；实施顺序步 4 = 6 条 L1、步 5 = 3 条 L2 | **9 条品质专属全部 `DESIGN_ONLY`，0 条进默认包**；步 4/5 整体移出实施顺序 |
| 计数 | L1 写 6（**实为 7**）、L2 写 3（**实为 2**） | 更正为 **7 条 L1 + 2 条 L2 = 9 条**；2 条 L2 继续标记需单独授权 |
| 授权 | 「品质专属单独授权后与 §2 数值包同批」 | **需品质专属单独授权**；回响叠乘上界必须先有明确上限决策 |
| 默认包定稿 | 未单列 | **P-01 12 项 T1/T2 L1 提案 + P-02 E-A + P-03 R-1 + P-04 L4** |

**影响文件**：`IMPLEMENTATION_SPEC.md §0.1/§1/§5/§10`、`REPORT.md §4`、
`QUALITY_EXCLUSIVE_PROPOSAL.md`、`BEFORE_AFTER_MATRIX.csv`（新增 `in_default_package` 列）、
`model-run.json`（`defaultPackage.quality_exclusive`）、`RISK_REGISTER.md R-21/R-23`。

---

## E-06 · `PASS` 命名暗示实战通过

| 项 | 03A 初版 | R1 冻结版 |
|---|---|---|
| 判定名 | `PASS` / `FAIL` | **`MODEL_PASS` / `MODEL_FAIL`**，只表示离线模型落入目标带 |
| 验收表 | A 模型层写「**PASS（离线复算）**」 | A 模型层写「**`MODEL_PASS` 12/12（离线复算）**」；B/C 明确 `NOT_RUN` |
| 风险登记 | 无 | 新增 `R-24`：出现「12 项通过 / 已验证」而不带 `MODEL_` 前缀即停手 |

**影响文件**：全部 CSV 的 `target_check` / `still_in_band` 列、`PLAYER_ACCEPTANCE.md`、
`RISK_REGISTER.md`、`CALC_MODEL.md`、`REPORT.md`。

---

## E-07 · 模型边界与假设未集中列明

| 项 | 03A 初版 | R1 冻结版 |
|---|---|---|
| 假设 | 散落在 `CALC_MODEL.md`、`IMPLEMENTATION_SPEC.md` 各处 | `CALC_MODEL.md §2.3` 与 `IMPLEMENTATION_SPEC.md §2.2` 单列：`W` 为技能占用且不能普攻的窗口、`C` 从施放开始、`C≥W`、冷却剩余按纯普攻、不考虑两技能交替/敌人移动/遮挡/打断/溢出/控制收益 |
| `cap` / `H` | 标 [疑] 但未逐行标注 | CSV 增 `cap_assumption` / `H_assumption` 列，全部「理论假设（非 Player 实测）」；`MODEL_SUMMARY.csv` 单列 7 条模型假设 |
| 表述 | 未声明 | 明确「**这些是模型边界，不是完整实战 DPS 模拟**」；不把控制收益、AOE、贯穿、命中率混成等效倍率 |

**影响文件**：`CALC_MODEL.md`、`IMPLEMENTATION_SPEC.md`、`SENSITIVITY.csv`、
`SKILL_VALUE_MODEL.csv`、`MODEL_SUMMARY.csv`。

---

## E-08 · 输出、SHA 与两份 CSV 的格式缺陷

| 项 | 03A 初版 | R1 冻结版 |
|---|---|---|
| 模型版本 | `UX03A-CALC-01`，4 张 CSV | **`UX03A-R1-CALC-02`，5 张 CSV**（新增 `MODEL_SUMMARY.csv`）；`model-run.json` 增 `statistics` 与 `defaultPackage` |
| `WEAPON_BUILD_VERIFICATION_MATRIX.csv` | 首行 `AdventureLoadout.Craft(Sword,Green)` 逗号未转义 → 列错位；末行缺 `main_risk`；含 BOM | 由 `csv.writer` 重建，15 行 × 20 列全部对齐；补 `band` / `metric_status` 两列与 T3 专属断言 |
| `AFFIX_RULE_MATRIX.csv` | 第 2 行 `StaffBlastRadius(q,area)` 逗号未转义 → 13 列变 14 列；含 BOM | 重建为 12 行 × 13 列；`authorization` 列统一标注默认包归属 |
| 全部 SHA | 4 个输出哈希 | **5 个输出哈希 + 参数表 SHA + 统计 + 默认包状态**，全部重算 |

**影响文件**：`Evidence/Tools/build_balance_model.py`、`Evidence/Tools/model-run.json`、
5 张 CSV、两份静态 CSV、`Evidence/INDEX.md`。

---

## 处置原则

| 原则 | 执行 |
|---|---|
| 不覆盖旧历史 | `design/ux-progression-03a` @ `95d8337c` 保持原样；`Evidence/ERRATA_P02.md` 保留 |
| 只改规格与模型 | 17 个交付文件全部在 `ProjectDocs/`，产品 `.cs` 0 改动 |
| 数字可复算 | `build_balance_model.py` 内 7 条 `assert` + `MODEL_SUMMARY.csv` 保证报告/CSV/规格/验收一致 |
| 不实施 | 本批未启动 Player、未重跑 P1/P1C、未进入产品实施 |

**状态：修订完成，推送后暂停等待复审。**
