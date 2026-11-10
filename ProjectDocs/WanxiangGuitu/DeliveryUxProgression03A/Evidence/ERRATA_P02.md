# UX-PROGRESSION-02 矩阵勘误（03A 复核时发现的源码事实偏差）

本批在逐行复核产品源码时，发现 UX-02 已交付矩阵里有 **5 处**与源码不一致。
**不修改 UX-02 的历史交付**（`design/ux-progression-02` 已推送、限定范围接受），只在此登记更正，供 03A 与后续实现批使用。

---

## E1 · `spear.charge` 的聚能冷却代价（错）

| 项 | 内容 |
|---|---|
| P02 原文 | `SKILL_BUILD_MATRIX.csv` 第 4 行 `trait_synergy`：「聚能 +25% 且 +1s（代价生效）」 |
| **源码事实** | `WeaponSkillExpansion.cs:39`：`TryCast()` 调 `combat.PrepareExpanded(def.cooldown)` → `AdventureCombat.cs:66` 只做 `skillAt=Time.time+cooldown`，**不读词缀**。`AdventureCombat.cs:104` 的 `SkillDuration` 对 `Expanded.Selected>0` 也直接返回 `def.cooldown`。 |
| 更正 | **8 个旧武器扩展技能全部不收 +1s 冷却**，但 `WeaponHit.cs:8` 仍给 `skill=true` 的伤害 ×1.25 → 白拿收益。这正是 03A 的 **E-A 对称性修正**要解决的问题。 |
| 影响 | P02 `EQUIPMENT_GAPS.md` G4 的结论「8 个扩展技能白拿 +25%」是对的；`SKILL_BUILD_MATRIX.csv` 的该单元格是错的。 |

## E2 · `bow.pierce` 的聚能冷却代价（错）

| 项 | 内容 |
|---|---|
| P02 原文 | `SKILL_BUILD_MATRIX.csv` 第 9 行 `trait_synergy`：「聚能 +25% 且 +1s」 |
| 更正 | 同 E1，**无 +1s**。 |
| 依据 | `WeaponSkillExpansion.cs:39,53`；`SkillPiercingProjectile.Contact` 走 `WeaponHit.Apply(...,true)` → +25% 伤害（`SkillPhysicalEffects.cs:14`）。 |

## E3 · 「回响不影响裂地冲击波」（错）

| 项 | 内容 |
|---|---|
| P02 原文 | `SKILL_BUILD_MATRIX.csv` 第 13 行 `trait_synergy`：「回响不影响波（半径固定 0.3m）」 |
| **源码事实** | `GreatswordCombat.cs:19`：`float area=WeaponTraits.Has(item,2)?1.25f:1; p.radius=.3f*area; p.limit=8*area;` |
| 更正 | **回响会把波半径 0.3→0.375m、行程 8→10m**。回响对 6 个新武器技能全部生效，包括巨剑的两个技能。 |
| 影响 | 03A `QUALITY_EXCLUSIVE_PROPOSAL.md §4` 已据此标注「巨剑金品质提案会与回响叠乘到 0.525m / 12.5m」，必须先拍板上界。 |

## E4 · `staff.field` 符阵伤害是否吃聚能（自相矛盾）

| 项 | 内容 |
|---|---|
| P02 原文 | `SKILL_BUILD_MATRIX.csv` 第 6 行：「聚能 +25% 只加弹体，符阵伤害不吃（WeaponHit 传 skill=true 实际上会吃）」 |
| **源码事实** | `SkillPhysicalEffects.cs:22`：`WeaponHit.Apply(hero,enemy,damage,point,...,source,true)` —— `skill=true`，`WeaponHit.cs:8` 无条件 ×1.25。弹体同样 `skill=true`（`WeaponSkillExpansion.cs:53`）。 |
| 更正 | **弹体 0.65× 与 3 次 40% 符阵脉冲都吃 +25%**，没有「只加弹体」这回事。P02 该单元格自己已写出矛盾，此处定稿。 |

## E5 · P02 对回响适用范围的描述不完整

| 项 | 内容 |
|---|---|
| P02 原文 | `EQUIPMENT_GAPS.md` G3：「回响对 4 把旧武器的普攻与全部 8 个扩展技能 0 作用（半失效）」 |
| 补充事实 | 回响**确实生效于 6 个新武器技能**（`NewWeaponCombat.cs:32`、`GreatswordCombat.cs:10,19`、`ScytheCombat.cs:10`）与 **4 个旧武器槽 0**（`AdventureCombat.cs:186-189`）。BeginAttack 甚至把 `a.area=Has(id2)?1.25:1` 写进了 `AttackAction`（`:81`），只是普攻分支不读。 |
| 更正 | 准确口径是「**10 个技能生效 / 7 套普攻 + 8 个旧扩展技能不生效**」的**专用词缀**，而不是「一半失效」。问题在 UI 没写明（`WeaponTraits.cs:6`），不在词缀本身。03A 的 R-1 就是把这个规则显式化。 |

## E6 · 「巨剑单发最高」容易误读（补充，非错误）

| 项 | 内容 |
|---|---|
| P02 原文 | `WEAPON_ROLE_MATRIX.csv` 巨剑 `strength`：「单发最高（1.05×）」；镰刀「三段收割总倍率低于巨剑单发」 |
| 补充 | 巨剑 `Interval=1.05s`（`GreatswordCombat.cs:3`）、镰刀 `0.80s`（`ScytheCombat.cs:3`），两者持续输出率 `R=1.000 ×P/s`，**只有长剑/法杖/弓（2.000）的一半**。它们是靠 65°/85° 扇形与 2.6/3.0m 距离换多目标覆盖。 |
| 影响 | 03A `CALC_MODEL.md §5.1` 已把七武器分成两个 R 梯队；任何「把巨剑倍率调到和长剑一致」都会破坏这个交换。 |

---

## 处置

| 项 | 处置 |
|---|---|
| UX-02 已推送分支 `design/ux-progression-02` @ `1dba0462` | **不修改、不 force push、不覆盖历史** |
| 03A 全部矩阵与规格 | 采用上述更正后的口径 |
| 后续实现批 | 以本文件 + `AFFIX_RULE_MATRIX.csv` + `SKILL_VALUE_MODEL.csv` 为准，不再引用 P02 的 `trait_synergy` 单元格 |

**保留全部历史结论，只登记更正 —— 与 P1/P1C 复审「保留历史证据」的要求一致。**
