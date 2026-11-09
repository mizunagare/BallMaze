# UX-PROGRESSION-01 · 交付报告

> 分支 `design/ux-progression-01`，起点 `09e2a6eb486ee36cc6d85a60ab4f629d0c522581`
> （`verify/cp06-integration-player-02-R1` 的 tip，即 CP06-INTEGRATION-02-R1 复审接受点）。
> 本批是**产品设计与源码审计**，不是实现批次：`Assets/**`、`ProjectSettings/**`、`Packages/**` 零改动。

---

## 1. 范围

| 做 | 不做 |
|---|---|
| 读取现有实现，标注已有 / 缺失 / 需决策 | 不写产品代码、不改玩法 |
| 五主题设计：出征目标、七武器八技能、装备成长制造、三地区定位、长期循环 | 不重复开发三地区集成验证、不重跑弓自然释放测试 |
| 玩法循环图、系统关系图、阶段路线图 | 不改 v9 / 经济 / 掉落 / 随机流 / 护甲 / 经验曲线 / 武器伤害 / 技能冷却 |
| 可量化验收标准（含反例） | 不升级依赖、不新增 CI、不改用户文件 |
| 15 条待决设计决策 | 不合并 main、不 force push |

---

## 2. 方法

1. **只读审计**：`Grep`/`Read` 遍历 `Assets/CombatPrototype`（142 个运行时脚本）与 `Resources`（RecipeData 29 / ItemData 25 / QualityData 5 / ContainerData 6），逐条记录 `文件:行号`。
2. **证据优先**：任何"已有"结论必须能落到代码行；任何"缺失"结论必须能给出"没有对应字段/分支"的反证。
3. **不发明数值**：目标卡阈值、制造成本梯度、地区容量全部由现有常量推算（矿点均值 4.5、宝箱数 6/3/2、配方公式），不做平衡调整。
4. **设计可实施性自检**：每个设计点标注是否触碰禁区（`DESIGN.md` §9），并把"需要新字段"的部分隔离到 P2。
5. **交付可复核**：全部文件生成 SHA256 清单（`Evidence/PROTECTION_HASHES.tsv`）。

---

## 3. 关键发现（10 条）

| # | 发现 | 证据 |
|---|---|---|
| 1 | 底层循环已闭环，无需重做 | `AdventureFlow.Depart/BeginExtraction/CommitSettlement`、`AdventureRules.Plan` |
| 2 | 出征目标"有枚举、有写入、无闭环" | `ExpeditionGoal` 三值（`AdventureState.cs:21`）、写入 `RunState.goal`（`AdventureFlow.cs:130`），但无达成判定/回执 |
| 3 | 目标只影响路线评分与一行文案 | `RouteScoring.cs:84-89`、`CraftingTargets.cs:108-111` |
| 4 | **局内完全看不到本局目标** | HUD 标题按 `mode` 分支，遗迹/洞窟同为 `ForestExploration`，故三种地区都不显示（`AdventureFlow.UI.cs:19`、`AdventureFlow.cs:121-122`） |
| 5 | 产品自认"暂无主线成果" | `AdventureFlow.UI.cs:21` 原文 |
| 6 | 技能槽选择不持久化、无热键 | `CombatSaveData.cs` 无字段；`PlayerBindings.cs:21` 技能仅 F；`WeaponSkillPanel.cs:5` 仅鼠标点击 |
| 7 | 旧/新武器两套技能语义 | `WeaponSkillExpansion.cs:8-17,38` vs `NewWeaponCombat.cs:10,22,50-51` |
| 8 | 装备有制造与铭刻，但无单件升级；新武器无配方 | `RecipeData/` 29 条无新武器；`AdventureLoadout.cs:124,168-183` |
| 9 | 三地区差异真实存在但未表达为目标 | 森林 7 POI/42 矿点/2 首领；遗迹 5 阶段机关链/0 矿点；洞窟 9 POI/4 矿脉/1 首领（`ForestLayout.cs:19-52`、`RuinsLayout.cs:12-29`、`CrystalCavernLayout.cs:39-168`） |
| 10 | 元进度薄但自洽：局内等级清零，长期只留装备/材料/配方/藏品 | `AdventureRules.cs:34`、`AdventureState.cs:12-18` |

---

## 4. 设计结论摘要

### 4.1 出征目标

把 `ExpeditionGoal` 升级为**可判定契约**：条件全部由现有信号只读推导（`earnedRemaining` / `events.used` / `enemies.health` / `resources.health` / `gear.origin`），
产出 **3 目标 × 3 地区 = 9 张目标卡**，每张卡给出"做多久、差多少、为了什么"。
**反刷硬规则**：计数只用"本局所得"，否则带材料出征即可刷满（D-08）。

### 4.2 七武器与八技能

构筑分四层：武器身份 → 技能槽 → 词缀/铭刻 → 局内基础技能。
现状 L1/L3/L4 已成立，**L2 只是"没被承认"**：选择不持久、无热键、无取舍说明。
因此不新增技能（避开冷却/伤害禁区），只做：统一语义（2 扩展槽）、持久化、`1/2` 热键、参数取舍条、7 张武器角色卡。

### 4.3 装备成长与制造

三条追求线（品质/词缀/藏品）+ 一条保底线（守护者紫装、守望者紫新武器）。
成本梯度：紫 ≈ 3.3 矿点 + 2 晶，金 ≈ 4.4 + 3，红 ≈ 5.6 + 4 晶 + 2 首领核心——**瓶颈不是材料而是"决定做哪件"**。
补上闭环最后一步：制造后自动给出"下一目标"（规则化，无随机）。

### 4.4 三地区定位

森林＝资源沙盘（唯一新武器掉落源）；遗迹＝机关链 + 永久收藏（无矿点，设计事实）；洞窟＝高价值矿脉 + 空间机关 + 可选强敌（矿/晶密度最高）。
用"一句话 + 三轴星级 + 推荐目标卡"表达，不改任何地形/敌人/掉落。

### 4.5 长期循环

五环嵌套（交战 5–15 s / 单局 8–15 min / 装备目标 2–5 局 / 地区精通 5–15 局 / 收藏长期）。
补 **6 个"下一局动机"生成器**（缺口/未开箱/未打首领/未解锁配方/未拿藏品/未达成目标），全部映射现有数据。
明确保持 roguelite 身份：**不引入持久等级**（D-06）。

---

## 5. 待决决策（15 条，详见 DECISIONS.md）

| 关键 | 决策 | 建议 | 阻塞 |
|---|---|---|---|
| D-01 | 目标达成是否给收益 | 先纯记录，再走既有解锁通道 | P2 |
| D-03 | 技能槽存哪 | 新增字段；冻结则退本地配置 | P2 |
| D-08 | 计数口径 | **本局所得（硬规则）** | P1 |
| D-15 | 存档修订窗口 | 一次性 v10，单独成批 | P2 前置 |
| D-06/D-10/D-12 | 持久等级 / 单件升级 / 遗迹矿脉 | 均不做 | — |

---

## 6. 交付清单

| 文件 | 用途 |
|---|---|
| [SOURCE_AUDIT.md](SOURCE_AUDIT.md) | 五系统源码审计：已有 / 缺失 / 需决策，含 `file:line` |
| [DESIGN.md](DESIGN.md) | 完整设计（含不变量、目标卡矩阵、成本梯度、地区三轴、五环） |
| [DECISIONS.md](DECISIONS.md) | 15 条决策：选项 / 建议 / 影响面 / 风险 |
| [ROADMAP.md](ROADMAP.md) | 阶段路线图（P0–P4 + 门禁 + 批次纪律） |
| [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md) | 可量化验收（A/B/C 三类 + 10 条反例） |
| [LOOP_DIAGRAM.svg](LOOP_DIAGRAM.svg) | 玩法循环图（状态机 + 目标闭环 + 五环） |
| [SYSTEM_MAP.svg](SYSTEM_MAP.svg) | 系统关系图（含禁区带） |
| [ROADMAP.svg](ROADMAP.svg) | 阶段路线图（可视化） |
| [Evidence/PROTECTION_AUDIT.md](Evidence/PROTECTION_AUDIT.md) | 零改动保护审计 |
| [Evidence/PROTECTION_HASHES.tsv](Evidence/PROTECTION_HASHES.tsv) | 交付目录全量 SHA256 |
| [.gitattributes](.gitattributes) | 本目录 `* -text`：按字节入库，保证哈希跨机器可复现 |

---

## 7. 保护审计

| 项 | 结论 |
|---|---|
| 产品源码 | `Assets/**` 改动 **0** 文件 |
| 场景 / 设置 / 包 | `ProjectSettings/**`、`Packages/**` 改动 **0** |
| v9 存档语义 | 未触碰（设计层明确只允许"向后兼容新增"，且需 D-15） |
| 经济 / 掉落 / 随机流 | 未触碰；设计中目标层**零 RNG 调用** |
| 护甲 / 经验 / 武器伤害 / 技能冷却 | 未触碰；相关需求全部列入"不做" |
| 用户文件 / 真实存档 | 未读取、未写入 |
| 历史交付 | 未删除、未移动、未改写任何历史证据 |

详细命令与输出见 [Evidence/PROTECTION_AUDIT.md](Evidence/PROTECTION_AUDIT.md)。

---

## 8. 风险与未关闭项

| 风险 | 说明 | 缓解 |
|---|---|---|
| 目标阈值可能偏松/偏紧 | 阈值由容量推算，未做真人试玩 | 阈值集中在单一定义处，可在 P1 复审时整体调整；不影响结构 |
| "下一目标"规则可能显得机械 | 纯规则、无随机 | 只在结算页出现一次，允许玩家忽略；不做强制引导 |
| P2 存档修订风险高 | 涉及 v9 → v10 | 单独分支、单独复审、双向证据（老档可读 + 回滚） |
| 展示层信息过密 | HUD 已有多块 | 字数上限（目标名 ≤8 字、进度 ≤12 字）+ 三层信息架构 |
| 人工可读性未验证 | 无真人评审 | C 类明确 `NOT_RUN`，不用推断代替 |

**未关闭项（如实保留）**：目标收益未设计（D-01）；技能槽持久化未实现（D-03）；地区精通未实现（D-07/D-14）；单件升级、新武器配方、第 3 技能、难度档均未设计（触碰禁区）；人工观感 `NOT_RUN`。

---

## 9. 分支与复核

| 项 | 值 |
|---|---|
| 分支 | `design/ux-progression-01` |
| 起点 | `09e2a6eb486ee36cc6d85a60ab4f629d0c522581` |
| 候选 `integration/cp06-playable-candidate` | `2964ad7413d2644f23c12a8c82e1d439e2884a01`（应保持未移动） |
| `main` | `72db192a527bd256e2ba18cd7ab334d8334051da`（应保持未移动） |

提交与推送后按**完整 SHA** 复核，并确认上述两条远端引用未移动。本批不合并 main，推送后暂停等待审核。
