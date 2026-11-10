# 证据索引 · UX-PROGRESSION-03A

基线 `design/ux-progression-03a` ← `design/ux-progression-02` @ `1dba0462`

本批是**规格批**：证据不是 Player Run，而是「源码行号 + 配置数值 + 可复算模型 + 对 P1/P1C 既有证据的引用」。
**本批未启动任何 Player 进程，未重跑 P1/P1C。**

---

## 1. 文件树

```
DeliveryUxProgression03A/
├── REPORT.md                              总报告
├── IMPLEMENTATION_SPEC.md                 四层详细实施规格
├── CALC_MODEL.md                          计算模型与恒等式
├── D24_COMPARISON.md                      D-24 只读对照
├── QUALITY_EXCLUSIVE_PROPOSAL.md          9 条品质专属提案
├── RISK_REGISTER.md                       21 条风险 + 停手信号
├── PLAYER_ACCEPTANCE.md                   三层验收 / ≥23 条 Run / 断言清单
├── SKILL_VALUE_MODEL.csv                  25 行模型读数
├── BEFORE_AFTER_MATRIX.csv                40 行前后对照
├── AFFIX_RULE_MATRIX.csv                  25 类攻击的词缀适用规则
├── SENSITIVITY.csv                        162 行 N/H 敏感度
├── FOCUS_SYMMETRY_IMPACT.csv              8 行聚能 +1s 叠加影响
├── WEAPON_BUILD_VERIFICATION_MATRIX.csv   15 行（14 构筑 + 1 回归）
└── Evidence/
    ├── INDEX.md                           本文件
    ├── ERRATA_P02.md                      UX-02 矩阵 5 处勘误
    └── Tools/
        ├── build_balance_model.py         可复算脚本（含源码参数表）
        └── model-run.json                 参数表 SHA + 4 张 CSV SHA + 行数
```

---

## 2. 源码锚点总表（逐条可 grep 复核）

| 事实 | 位置 |
|---|---|
| `P = 25 + Equipment.AttackBonus + Progression.AttackBonus` | `ThirdPersonHero.cs:22` |
| `attackCooldown=.5 / attackReach=1.8` | `ThirdPersonHero.cs:9-10` |
| `ActionDuration` 夹到 ≤0.55s | `AdventureCombat.cs:62` |
| `SpearCadence 1.30 / SpearPower 1.25 / SpearReach 3.1 / SpearHalfWidth .4` | `AdventureCombat.cs:70` |
| `BasicInterval` / `BasicPower` | `AdventureCombat.cs:71-72` |
| `a.area = Has(id2)?1.25:1` 写入 `AttackAction` | `AdventureCombat.cs:81` |
| `basicRelease=(.35,.40,.45,.40)` / `skillRelease=(.40,.45,.50,.45)` | `AdventureCombat.cs:37` |
| `MeleeGeometry.InDirection/Contact`（dot 与 width 语义） | `AdventureCombat.cs:6-27` |
| 普攻分支不读 `area`（长剑 dot .25 / 长枪 .88 / 法杖 .9 / 弓 0） | `AdventureCombat.cs:181` |
| 槽 0 品质专属（4 把旧武器） | `AdventureCombat.cs:186-189`；`BowHalfCount :108`；`StaffBlastRadius :109` |
| `SkillDuration`（扩展技能直接返回 `def.cooldown`） | `AdventureCombat.cs:104` |
| `UseSkill` 槽 0 的 7+聚能1 秒 | `AdventureCombat.cs:151` |
| `Melee` 去重与 `WeaponHit.Apply` 调用 | `AdventureCombat.cs:193-207` |
| 弹体 `life=2.5f`、速度由 `Fire` 传入 | `AdventureCombat.cs:266-271` |
| 词缀 6 条名称与描述、品质专属说明 | `WeaponTraits.cs:5-6,10` |
| 全部伤害词缀乘算（`锐利/聚能/猎首/汲取`） | `WeaponHit.cs:7-11` |
| 8 个旧扩展技能定义（cd / startup / pulses / gap / power / reach / dot / width / charge） | `WeaponSkillExpansion.cs:9-16` |
| `TryCast` → `PrepareExpanded(def.cooldown)`（**聚能缺口**） | `WeaponSkillExpansion.cs:39` |
| 蓄力 `scale = 1 + .85×min(1,elapsed/charge)` | `WeaponSkillExpansion.cs:46` |
| 扩展技能 `finish = +.22f` 收招 | `WeaponSkillExpansion.cs:48-49` |
| `ExpandedMelee` 直接传 `def.reach`（**回响缺口**） | `WeaponSkillExpansion.cs:52`；`AdventureCombat.cs:71` |
| 贯穿上限 3、实心障碍即停 | `SkillPhysicalEffects.cs:9-14` |
| 留场 0.25s 首脉冲 + 0.6s 间隔 + 3 次 | `SkillPhysicalEffects.cs:18-25` |
| 双刃三段 `.42/.42/.85`、Interval `.30`、六段 `.40`、反击 `.65/1.80` | `NewWeaponCombat.cs:20,41,43-44` |
| `ConsumeEvade` 0.85s 窗口 | `NewWeaponCombat.cs:20` |
| `TwinHit` 的 `seen` 与 `phase>=10` 回响分支 | `NewWeaponCombat.cs:32` |
| 训练装备架 → `SpawnTrainingArsenal` → 真实拾取 | `NewWeaponCombat.cs:35`；`WeaponSkillPanel.cs:6` |
| `SkillDuration`（新武器 7/8、9/10、8/11 + 聚能1） | `NewWeaponCombat.cs:11` |
| 巨剑 `Interval 1.05` / `power 1.05` / 技能 `1.70` / 波 `.95` | `GreatswordCombat.cs:3,5,6` |
| 冲击波 `area=Has(id2)?1.25:1` → radius/limit 放大 | `GreatswordCombat.cs:19` |
| 镰刀 `Interval .80` / `power .80` / 收割 `3×.45` / 牵引 0 伤害 | `ScytheCombat.cs:3,5,6`；`NewWeaponCombat.cs:10` |
| 控制免疫（Boss / ForestBoss）与 Break/Pull 时长 | `EnemyWeaponControl.cs:4-8` |
| 盘内叠加 `Active.Sum(i=>i.Attack)`（**D-24 未授权**） | `AdventureLoadout.cs:19,22` |
| 真实制造入口 `Craft(GearType,GearQuality)` | `AdventureLoadout.cs:172-186` |
| 品质 Power 白8/绿19/紫43/金78/红132 | `QualityData/*.asset` |
| 配方 29 个（9 类 × 3 品质 + 2 容器） | `RecipeData/*.asset` |

---

## 3. 既有证据引用（未重跑）

| 引用 | 来源 |
|---|---|
| P1C 三条挑战闭环（8/10/10 次真实命中，290/320/360→0，`Extracted`，角标一致） | `DeliveryUxProgression01P1C/Evidence/Player/p1c-*/assertions.tsv` |
| `bow.pierce` 历史 Player 证据（`pierceChain=2`） | `DeliveryCp06Integration02/Evidence/Player/bow-pierce-natural-7` |
| 七武器 / 14 技能 / 词缀 / 地区的 UX-02 审计矩阵 | `DeliveryUxProgression02/*.csv`、`*.md` |
| 本批对 UX-02 的 5 处勘误 | `Evidence/ERRATA_P02.md` |

---

## 4. 复算命令

```bash
# 1. 重建全部四张 CSV + model-run.json
python Evidence/Tools/build_balance_model.py --out .
# 期望：rows: skill_value_model=25 before_after=40 sensitivity=162 focus=8

# 2. 核对模型恒等式 η = 1+(B-1)W/C（CSV 保留 4 位小数，误差 < 5e-5）
python - <<'EOF'
import csv,io
rows=list(csv.DictReader(io.open('SKILL_VALUE_MODEL.csv',encoding='utf-8')))
print(max(abs(float(r['eta'])-(1+(float(r['B'])-1)*float(r['W'])/float(r['C'])))
          for r in rows if r['row_type']=='skill'))
EOF

# 3. 产品代码零改动
git diff --stat 1dba0462 -- Assets ProjectSettings Packages
git diff --name-only 1dba0462 HEAD | grep -E "\.cs$"    # 应为空

# 4. D-24 未授权：盘内叠加规则未变
git diff 1dba0462 -- Assets/CombatPrototype/AdventureLoadout.cs   # 应为空

# 5. 词缀缺口定位
grep -n "PrepareExpanded\|Definition.cooldown" Assets/CombatPrototype/WeaponSkillExpansion.cs Assets/CombatPrototype/AdventureCombat.cs
grep -n "area=WeaponTraits.Has(item,2)\|phase>=10&&WeaponTraits.Has" Assets/CombatPrototype/GreatswordCombat.cs Assets/CombatPrototype/NewWeaponCombat.cs
```

---

## 5. 证据缺口（本批无法补齐）

| 缺口 | 为什么 | 需要什么 |
|---|---|---|
| `cap`（形状覆盖目标数） | 源码只有形状参数，没有敌群密度实测 | 密集敌群 Player Run，逐帧记录去重后 contact 目标数 |
| `H`（弹体/蓄力/留场命中率） | 遮挡与打断只能在真实物理场景观察 | 每技能 ≥20 次真实释放，记录 `aim-rejected` / `pierce-blocked` / 蓄力被打断 |
| 三把新武器四档品质 | 本批零 Player | 白/紫/金/红各 1 条真实拾取 + 战斗 Run |
| 七武器两套构筑 | 本批零 Player | ≥14 条真实 Run（训练场 + 远征各半） |
| 重复性 / 洞窟开桥 / 装备成长后重打 | P1C 已列未做项 | 专项重复性批 |
| E-A 与 §2 提案合并后的实际冷却 | 实现批才落地 | 实现批复算 + Player 回读 `SkillRemaining` |
