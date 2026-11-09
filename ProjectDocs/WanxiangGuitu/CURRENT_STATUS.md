# 当前状态与入口（增量新增，不改写历史报告）

> 本文件只做**入口索引**。历史交付目录中的 PASS / FAIL / INCOMPLETE 与旧批次结论原样保留，
> 不因本文件而重新判定。「建立入口」不等于「实现已通过复审」。

## 1. 主线与开发链

| 项目 | 完整 SHA / 位置 |
|---|---|
| 主线 `main` | `72db192a527bd256e2ba18cd7ab334d8334051da`（四武器表现批次，**不是** CP06 完成度） |
| 上一候选 `fix/cp06-crystal-warden-b1` | `a013c15aae15e17af6a7596a022f01f56a745c34` |
| 历史候选 `fix/cp06-crystal-warden-b2` | 从 `a013c15aae15e17af6a7596a022f01f56a745c34` 建立；完整 SHA 见 [REPORT.md](DeliveryCrystalCavernC24B2/REPORT.md)（已交付，暂停复审） |
| **统一候选 `integration/cp06-playable-candidate`** | 从 `fix/skill-state-01`（`e93d6eeb…`）建立，包含七武器/八技能/森林/遗迹/洞窟/C2.4 Boss 全部功能；交付目录见 [DeliveryCp06Integration01/](DeliveryCp06Integration01/)；完整 SHA 收尾 `git ls-remote` 复核 |

`main` 不是当前游戏完成度。CP05 / CP06 的镜头、技能、七武器、遗迹、水晶洞窟与 C2.4 Boss 位于后继开发分支；
B1 相对 main 为 ahead 38 / behind 0，merge-base 即上述 main SHA。不要从旧 main 重做这些功能。

## 2. 本批：CP06-C24-B2（交付后暂停等待复审）

交付目录：[DeliveryCrystalCavernC24B2/](DeliveryCrystalCavernC24B2/)

| 文档 | 用途 |
|---|---|
| [DESIGN_DECISIONS.md](DeliveryCrystalCavernC24B2/DESIGN_DECISIONS.md) | 先冻结的晶环接触语义、参数、容差、切线规则与收益投影合同 |
| [REPORT.md](DeliveryCrystalCavernC24B2/REPORT.md) | 本批范围、改动、完整 SHA、风险 |
| [ACCEPTANCE.md](DeliveryCrystalCavernC24B2/ACCEPTANCE.md) | B2-01 ～ B2-11 逐项验收与限制 |
| [TESTING.md](DeliveryCrystalCavernC24B2/TESTING.md) | 分层证据、复跑命令、环境限制 |
| [Evidence/INDEX.md](DeliveryCrystalCavernC24B2/Evidence/INDEX.md) | 原始证据、哈希与保护清单 |

四部分范围：C24 路线只读收益与专用普通掉落工厂对齐；HollowRing 改为「实际受击 Collider 接触环带」；
补齐 P1 前摇跨半血 / 原阶段释放 / 恢复结束转阶段的定向证据；增量建立本入口。
真实掉落、首奖、随机流、评分权重、武器、护甲、经验、v9 格式均未改变。

## 2b. 本批：CP06-INTEGRATION-01（交付后暂停等待复审）

交付目录：[DeliveryCp06Integration01/](DeliveryCp06Integration01/)

| 文档 | 用途 |
|---|---|
| [INTEGRATION_CANDIDATE.md](DeliveryCp06Integration01/INTEGRATION_CANDIDATE.md) | 统一候选说明：身份、技术栈、构建身份、启动入口、包含清单、已知限制 |
| [STATE_DIAGRAM.md](DeliveryCp06Integration01/STATE_DIAGRAM.md) / [STATE_DIAGRAM.svg](DeliveryCp06Integration01/STATE_DIAGRAM.svg) | 完整循环状态图（营地→出征→探索→战斗→Boss→撤离→结算→制造→再次出征） |
| [INTEGRATION_PLAN.md](DeliveryCp06Integration01/INTEGRATION_PLAN.md) | 集成计划与分支整合方案、基线决策、分支映射、保护策略 |
| [ACCEPTANCE_MATRIX.md](DeliveryCp06Integration01/ACCEPTANCE_MATRIX.md) | 9 阶段循环 + 5 重点检查验收矩阵，保留历史 FAIL/NOT_RUN/INCOMPLETE |
| [EVIDENCE_INDEX.md](DeliveryCp06Integration01/EVIDENCE_INDEX.md) | Git 包含性证明、历史交付索引、构建身份、远端 SHA 复核基线 |
| [Evidence/PROTECTION_AUDIT.md](DeliveryCp06Integration01/Evidence/PROTECTION_AUDIT.md) | 产品零改动保护审计（v9/经济/掉落/随机流/用户文件） |

集成基线 = `fix/skill-state-01`（`e93d6eeb…`）。git 包含性证明：所有 feature 分支与 fix 链均为该 tip 祖先，
故单一分支即包含七武器/八技能/森林/遗迹/洞窟/Boss，无需合并 feature 分支或 cherry-pick。本批仅新增文档，
不改任何产品源码、v9、经济、掉落、随机流或用户文件。

## 3. 开放项（不因本批关闭）

| ID | 状态 | 说明 |
|---|---|---|
| `SKILL-STATE-01` | **已交付（限定范围有条件接受）** | 法杖符阵「待碰撞记录」与弹体暂停时钟一致性已修复并验证；保留全部历史 FAIL/NOT_RUN |
| `CP06-INTEGRATION-01` | **本批交付（待复审）** | 建立单一可复现可玩候选、整理入口/构建身份/跨区域回归；不合并 main、不丢弃历史分支 |
| `UX-PROGRESSION-01` | 排期草案 | 出征目标 / 技能配置可理解性 / 奖励动机；先设计后另批实施 |
| 晶环竖直带可视化 | 开放 | 现有 2D 指示圆只表达水平环带的地面投影，不图形化表达 ±1.2m 竖直攻击带 |
| 观测 Player / 纯包 / 原生输入 / 独立人工 | 按各交付 TESTING.md | 本批未运行时一律 `NOT_RUN`，不用 Editor 或模型代替 |
| 历史 C02 / C04 严格三维起点失败 | 保留 | 不因新容差试验改成 PASS |
| 历史 `WindupNewAudit1` C05 `INCOMPLETE` | 保留 | B2 只新增定向关联证据，不改写旧报告 |

## 4. 保护边界

不改用户场景、`ProjectSettings`、未提交修改、真实存档、旧证据；不升级依赖、不新增 CI、
不 force push、不自动合并 `main`；不提交 `Library` / Player 二进制 / 凭据 / 受限供应商源码。
每批交付后按固定完整 SHA 复审，并暂停等待下一授权。

## 5. 历史入口

历史批次见各 `Delivery*/REPORT.md` 与 [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) 原有正文。
本文件与 README / DEVELOPMENT_PLAN 顶部短指针均为**增量新增**，不覆盖任何历史状态描述。
