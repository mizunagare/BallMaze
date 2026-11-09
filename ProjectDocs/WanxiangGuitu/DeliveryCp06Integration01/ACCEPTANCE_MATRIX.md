# CP06-INTEGRATION-01：验收矩阵

> 本矩阵把**统一候选的完整循环**与**五个重点检查**映射到**已有交付证据**。
> 状态沿用全局定义：`PASS` / `PASS-PLAYER` / `PASS-EDITOR` / `PASS-STATIC` /
> `FAIL` / `NOT_RUN` / `INCOMPLETE`。
>
> **关键原则**：本批次**不重新执行**任何 Unity/Player 测试；只把已有、分散在各交付目录中的
> 验证结果**收口映射**到统一候选。历史 `FAIL` / `NOT_RUN` / `INCOMPLETE` **原样保留并显式列出**，
> 不改写为 PASS，也不被大量历史 PASS 稀释。

---

## 1. 完整循环验收（9 阶段）

| # | 阶段 | 验收判据 | 现有证据 | 状态 |
|---|---|---|---|---|
| ① | 营地准备 | 新游戏/继续、自动档读取、七武器+八技能配置入口 | `DeliveryCP06B`（七武器）、`DeliveryCP06A`（八技能）、`DeliverySkillState01` C5（读档 Selected 回槽 0）、`DeliveryCrystalCavernC22` C2.1（旧在途档读取） | **PASS**（组件级） |
| ② | 出征 | 区域选择：森林/遗迹/洞窟 | `DeliveryCrystalCavernC22` C2.1（森林与遗迹入口）、`DeliveryCrystalCavernC24B2`（洞窟入口） | **PASS**（组件级） |
| ③ | 探索 | 区域导航、C21/C22/C23 检查点、旧检查点恢复不升级地图 | `DeliveryCrystalCavernC22`（关门/桥/机关/宝箱 PASS）、`feature/cp06-crystal-cavern-c23` | **PASS**（组件级） |
| ④ | 战斗 | 七武器普攻/默认技能对活体真实命中、扩展技能释放/取消/冷却 | `DeliveryCrystalCavernC22`（七武器各自命中 PASS）、`DeliveryCP06A`、`DeliveryCP06B`、`DeliverySkillState01` C1/C2（法杖/弓 PASS-PLAYER） | **PASS-PLAYER**（抽样） |
| ⑤ | Boss | C2.4 首奖、HollowRing 实际接触、跨半血阶段 | `DeliveryCrystalCavernC24B1`（首奖/名称）、`DeliveryCrystalCavernC24B2`（收益投影/晶环接触）、`R1`（同 Run C05 10/10 PASS-PLAYER）、`R2`（晶环 25/27 PASS-PLAYER + 2 NOT_RUN） | **PASS-PLAYER + 残留 NOT_RUN** |
| ⑥ | 撤离 | 撤退返回、挑战失败返回、免费出口 | `DeliveryCrystalCavernC22`（实际撤离后新出征 PASS）、`DeliveryCrystalCavernC24B2`（不挑战可返回） | **PASS** |
| ⑦ | 结算 | 普通掉落拾取、首奖待领/领取、无重复预测 | `DeliveryCrystalCavernC24B2`（B2-01/02/03 无重复、首奖独立 PASS）、`DeliveryCrystalCavernC22`（铁矿/晶石采集、跨进程撤离入仓 PASS） | **PASS** |
| ⑧ | 制造 | 装备成长、新武器追加掉落材料入仓 | `DeliveryCP06B`（背包/仓库/品质接入）、`DeliveryCrystalCavernC22`（材料入仓 PASS） | **PASS**（组件级） |
| ⑨ | 再次出征 + 存档恢复 | 新进程读档无瞬态残留、旧在途档继续 | `DeliverySkillState01` C5（新进程读档 PASS-PLAYER）、`DeliveryCrystalCavernC22` C2.1（旧在途档森林/遗迹读取 PASS） | **PASS-PLAYER** |

---

## 2. 五个重点检查（用户指定）

| 重点 | 判据 | 证据 | 状态 |
|---|---|---|---|
| 跨地区状态 | 森林/遗迹/洞窟切换保持状态，旧检查点恢复不升级地图 | `DeliveryCrystalCavernC22` C2.1（森林与遗迹入口、在途读取 PASS）；主计划 §7.2 | **PASS**（组件级）/ 完整切换回归 **NOT_RUN** |
| 技能与武器配置 | 七武器 + 八技能可配置、释放/取消/冷却冒烟；Selected 回槽 0 设计限制明确 | `DeliveryCP06A`、`DeliveryCP06B`、`DeliverySkillState01` C1/C2/C5 | **PASS-PLAYER**（抽样） |
| 奖励与装备成长 | 收益投影与工厂一致、首奖独立、新武器追加掉落入仓 | `DeliveryCrystalCavernC24B2`（B2-01~B2-03）、`DeliveryCP06B` | **PASS** |
| 存档恢复 | v9 读档、新进程无瞬态残留、训练/正式隔离 | `DeliverySkillState01` C5（PASS-PLAYER）、`DeliveryCrystalCavernC22` C2.1、`DeliveryB08`（训练隔离） | **PASS-PLAYER**（抽样） |
| 纯发行 Player | 纯发行构建干净、可启动、完整手动循环原生试玩 | `DeliverySkillState01` A3-2（纯发行 errors=0、Boot=0 PASS-EDITOR）；完整手动循环原生键鼠试玩 **NOT_RUN** | **PASS-EDITOR** + 手动循环 **NOT_RUN** |

---

## 3. 历史非 PASS 状态清单（原样保留，不重写）

| 来源 | 历史状态 | 说明 |
|---|---|---|
| `DeliveryCrystalCavernC24B1` `B1-05` | **FAIL** | 路线预测与工厂不一致（已由 B2 修复投影侧；真实工厂未改） |
| `DeliveryCrystalCavernC24B2` 六份旧布局新 Editor 评分对照 | **NOT_RUN** | 仅门禁静态证明；历史 `ScoreComparison2` 35 PASS 保持原结论 |
| `DeliveryCrystalCavernC24B2` 纯发行包/原生键鼠/独立人工/平衡/性能 | **NOT_RUN** | 不在该批运行 |
| `DeliveryCrystalCavernC24B2R2` 晶环取消 2 用例 | **NOT_RUN** | `R2_PARTIAL_OR_NOT_RUN`：25/27 PASS-PLAYER + 2 NOT_RUN；未改产品 |
| `DeliverySkillState01` 修复前 `R-4` | **FAIL-PLAYER**（负例，已修复） | 修复后同 case 转 PASS-PLAYER；负例本身保留 |
| `DeliverySkillState01` 1 用例 | **NOT_RUN** | 13/14 PASS-PLAYER + 1 NOT_RUN |
| 历史 C02/C04 严格三维起点失败 | **FAIL**（保留） | 不因新容差试验改成 PASS |
| 历史 `WindupNewAudit1` C05 | **INCOMPLETE** | B2 只新增定向关联证据，不改写旧报告 |

---

## 4. 总体判定

| 维度 | 结论 |
|---|---|
| 组件级集成完整性 | **PASS**——候选 tip 包含七武器/八技能/森林/遗迹/洞窟/Boss（git 包含性证明） |
| 构建身份 | **PASS-EDITOR**——纯发行构建 errors=0、Boot=0，继承自查基线 |
| 完整手动循环原生试玩 | **NOT_RUN**——需原生操作者；不在本批次运行，不冒充 |
| 保护边界 | **PASS**——产品零改动（见 `Evidence/PROTECTION_AUDIT.md`） |
| 历史结论保护 | **PASS**——全部 FAIL/NOT_RUN/INCOMPLETE 原样保留 |

> **不声称**：本批次**未**执行一次由人类从标题走到再次出征的端到端纯发行试玩。
> 端到端原生试玩与最终平衡/性能验收仍标记为 `NOT_RUN`，等待独立复审与人工执行。
