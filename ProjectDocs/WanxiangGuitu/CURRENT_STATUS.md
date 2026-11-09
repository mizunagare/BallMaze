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

## 2c. 本批：CP06-INTEGRATION-02（交付后暂停等待复审）

交付目录：[DeliveryCp06Integration02/](DeliveryCp06Integration02/)；原验证分支
`verify/cp06-integration-player-01`（自统一候选 tip `2964ad7413d2644f23c12a8c82e1d439e2884a01`
建立，仅新增本交付目录）；R1 修订分支 `verify/cp06-integration-player-02-R1`
（自 `verify/cp06-integration-player-01` tip `cebec9af68db7f60eb448faa2668883683976363` 建立，
同样只改本交付目录，候选 `2964ad741…` 与 `main` `72db192a…` 均未移动）。

| 文档 | 用途 |
|---|---|
| [PLAYABLE_CANDIDATE_BUILD.md](DeliveryCp06Integration02/PLAYABLE_CANDIDATE_BUILD.md) | 候选纯发行构建身份（EXE SHA256 `001aeebf…` 确定性、隐私门禁、零验证注入） |
| [THREE_REGION_RUN_MATRIX.csv](DeliveryCp06Integration02/THREE_REGION_RUN_MATRIX.csv) | 森林/遗迹/洞窟真实完整出征循环矩阵（含历史 FAIL 保留） |
| [CROSS_REGION_STATE_MATRIX.csv](DeliveryCp06Integration02/CROSS_REGION_STATE_MATRIX.csv) | 跨地区状态切换 + 跨进程在途恢复矩阵 |
| [WEAPON_SKILL_SMOKE_MATRIX.csv](DeliveryCp06Integration02/WEAPON_SKILL_SMOKE_MATRIX.csv) | 七武器×八技能真实输入组合矩阵（含 R1-02 弓自然释放 5 行） |
| [REPORT.md](DeliveryCp06Integration02/REPORT.md) | 范围、方法、32 个 Player run 结果与根因、保护边界、风险 |
| [ACCEPTANCE.md](DeliveryCp06Integration02/ACCEPTANCE.md) | INT02-01～06 逐项验收（含遗迹采集 SKIP 定性 + R1 追加验收项） |
| [TESTING.md](DeliveryCp06Integration02/TESTING.md) | 复现命令、驱动-产品交互契约、不可用项 |
| [RUN_LEDGER.csv](DeliveryCp06Integration02/RUN_LEDGER.csv) | **R1-01 计数唯一来源**：32 个 Run 逐行分类（phase/runId/pid/exitCode/category/firstFailure） |
| [NON_RUN_ATTEMPTS.csv](DeliveryCp06Integration02/NON_RUN_ATTEMPTS.csv) | 20 条构建/工具尝试（全部不计入 Player Run） |
| [ERRATA.md](DeliveryCp06Integration02/ERRATA.md) | 旧统计 14/12/12 的勘误依据与最终值（R0 24 = 13 + 11） |
| [FOREST_RUN_ID_PROVENANCE.md](DeliveryCp06Integration02/FOREST_RUN_ID_PROVENANCE.md) | 森林 Run ID 来源（**DIRECT**，含原始文件行号与 SHA256） |
| [Evidence/INDEX.md](DeliveryCp06Integration02/Evidence/INDEX.md) | 原始证据索引 + 全量 SHA256 清单（PROTECTION_HASHES.tsv） |

结果：INT02-01～06 全部 PASS（遗迹采集按产品设计 SKIP）。**R1 修订后的计数口径**（唯一来源 RUN_LEDGER.csv）：
**32 个独立真实 Player run = 17 PASS + 15 FAIL**，其中 R1 开工前的 `phase=R0` 24 个为
**13 PASS + 11 FAIL**（旧报告的 14/12/12 三处矛盾已按 [ERRATA.md](DeliveryCp06Integration02/ERRATA.md) 勘误），
R1-02 新增 8 个弓自然释放 Run 为 4 PASS + 4 FAIL（4 个 FAIL 均为验证驱动缺陷，非产品缺陷）。
零产品源码改动、真实 AppData 存档从未被触碰、纯构建零验证注入（驱动仅入观察副本）。
完成后推送独立 R1 验证分支 `verify/cp06-integration-player-02-R1` 并按完整 SHA 复核，
**不自动合并 main**。

### 2c-R1. R1 追加内容（同批，待复审）

| 项 | 结论 | 证据 |
|---|---|---|
| R1-01 统一 24 个原始 Run 分类 | 24 = 13 PASS + 11 FAIL（runId 唯一 24，分类闭合自检通过） | [RUN_LEDGER.csv](DeliveryCp06Integration02/RUN_LEDGER.csv)、[ERRATA.md](DeliveryCp06Integration02/ERRATA.md) |
| 构建/工具尝试与 Run 分离 | 20 条，`playerRunCounted=no` 全数 | [NON_RUN_ATTEMPTS.csv](DeliveryCp06Integration02/NON_RUN_ATTEMPTS.csv) |
| R1-02 弓蓄势贯矢自然释放 | **PASS**：两发均由真实松键释放（半蓄力 0.504 / 满蓄力 1.0），各唯一 release+spawn，各贯穿 2 目标（60→5.43→0），冷却 10.17s 且冷却期施放被拒，两发弹体均销毁 | `Evidence/Player/bow-pierce-natural-8`（56 断言 0 FAIL） |
| 手动取消证据 | 保留不改写（`skill-smoke-3`），仅作历史记录 | [WEAPON_SKILL_SMOKE_MATRIX.csv](DeliveryCp06Integration02/WEAPON_SKILL_SMOKE_MATRIX.csv) |
| R1-03 森林 Run ID 溯源 | **DIRECT**（`int-events.jsonl:2 productRunId=2582537b…`；settle 行另有 `settlementId`/`committedRun`） | [FOREST_RUN_ID_PROVENANCE.md](DeliveryCp06Integration02/FOREST_RUN_ID_PROVENANCE.md) |

## 3. 开放项（不因本批关闭）

| ID | 状态 | 说明 |
|---|---|---|
| `SKILL-STATE-01` | **已交付（限定范围有条件接受）** | 法杖符阵「待碰撞记录」与弹体暂停时钟一致性已修复并验证；保留全部历史 FAIL/NOT_RUN |
| `CP06-INTEGRATION-01` | **已交付（待复审）** | 建立单一可复现可玩候选、整理入口/构建身份/跨区域回归；不合并 main、不丢弃历史分支 |
| `CP06-INTEGRATION-02` | **本批交付 + R1 修订（待复审）** | 统一候选真实 Player 纵向集成验证：三地区完整循环、跨区/跨进程、七武器八技能、奖励制造、失败路径全部通过；R1 统一计数（32 = 17 + 15）、溯源森林 Run ID、补齐弓自然释放；R1 分支 `verify/cp06-integration-player-02-R1` 暂停复审 |
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
