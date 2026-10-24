# B4 验收记录

最终独立完整 All：`20261024-132834-3bcdc2ee`，2026-10-24。原始结果 [JSON](Evidence/FinalAll/results.json)、[CSV](Evidence/FinalAll/results.csv)、[逐项报告](Evidence/FinalAll/REPORT.md)。

**77 PASS / 2 预期探针 FAIL / 19 NOT_RUN / 1 UNRESOLVED；非预期 FAIL 为 0。** 协调器实际 exit0，无遗留测试进程；不等同于全部验收通过。两个预期 FAIL 是 nonzero(exit7) 与 timeout（无正常退出码，进程保留后自行结束）；它们检验失败传播，不是产品失败。首次失败和定向运行保留在 Attempts。

| 项目 | 本轮状态 | 证据与范围 |
|---|---|---|
| 30 seed 数据合法与同 seed 一致 | PASS | B4Checks.Topology，重复 JSON 相同，27 个图签名 |
| 有意义的路线差异 | PASS | 湖岸存在必须经过精英点及可绕开精英点的不同图；稳定连通骨架 |
| 30 个不同合法布局物理导航 | PASS | B4Physics：31 次请求，30 个不同实际 seed；全部 POI/边/出口实际行走，42 节点与11遭遇完整路径；仅此专项关闭 NPC |
| 有界重试、原因和 fallback | PASS | 请求8失败 node:32，重试实际9；CSV 分列。未触发三次全失败后的 fallback，备用分支故障注入由历史路线回归覆盖，非宣称本次随机样本走到 fallback |
| 五类地点实际收益 | PASS | B2Rules.Run/Resume，真实地面奖励与据点额外掉落；既有概率不改 |
| 耗尽/已开/已清除不误报 | PASS | B4StateRules，未拾取装备仍可推荐，拾取后移除 |
| 真实制造缺口、前置费及路线 | PASS | B2Rules + B4StateRules；查询前后全局/本局状态及奖励流不变 |
| 遗迹概率边界/重复敌掉落/重复开箱 | PASS | B3StreamRules/B3Checks/B2Rules + B4 拾取专项 |
| B1 单次扣费、回执与来源账 | PASS | WGB1Check/Resume/Routes 与实际 Gather 修复、重复调用拒绝 |
| Pending/Committed/ack 唯一结算、死亡放弃 | PASS | 原 FullRegression 场景与故障测试；三策略确认后重复 Commit 不增奖 |
| 正常 AI：采集、修渡口、撤离 | PASS | Gather 三进程；采集6木，扣2木，入仓4木，取2木制造，仓库余2木 |
| 正常 AI：遗迹寻宝、免费撤离 | PASS | Treasure 三进程；真实拾取1装备，材料收益皮1/晶7/木8/矿2，免费入口；木取2后仓库余6 |
| 正常 AI：绕精英、保留收益撤离 | PASS | Bypass 三进程；精英最近75.85913米且未触发，免费祭坛；木5入仓、取2后余3 |
| 新进程与再次森林出征 | PASS | 九个 AI 进程 exit0；每策略两次恢复完整快照断言，包括仓库/配方、第一局仅一次提交；后继 mode=ForestExploration |
| revision1/2/3 与历史存档 | PASS | B4StateRules 保存快照原样恢复、历史 v1～v9/分页/迁移及装备容器回归；没有重抽旧布局 |
| 非开发 Windows 构建 | PASS | BuildOptions.None，0错误/69警告，BuildSummary 与完整脱敏日志保留 |
| 正式 Player 后台退出/新进程恢复 | PASS | 4组×2进程，8次 exit0、无超时无强杀；退出审计、校验和/修订与状态对照。仅 WM_CLOSE，不是标题栏路径 |
| 原生 UI / U16 | NOT_RUN | 没有安全独立交互环境，原生相关17条 NOT_RUN，不抢用户桌面 |
| 受控 UI 截图 | PASS | 本轮92张哈希索引，选定1280/1920截图和3张正常AI结算图发布；不冒充原生 |
| 人工理解 | NOT_RUN | 未安排独立人工试玩 |
| D3D12 UNKNOWN 根因 | UNRESOLVED | 保留历史样本，不从后台关闭或exit0推导已修复；本轮未做新标题栏/转储实验 |
| ProcDump 单元 | NOT_RUN | 本次未配置可用工具；不继承旧工具校准为本轮运行 |
| 源码/副本/构建哈希 | PASS（有披露差异） | 73产品C#规范化一致；777输入逐项哈希，运行后隔离副本6个设置资产有序列化/构建派生差异；详见报告，不声称全部字节一致 |

规则40 PASS、正常AI9 PASS、受控截图1 PASS；后台关闭类16 PASS（关闭请求与分析各8），其余为工具/环境/编排自身检查，不能把77项全部称作游戏用例。19 NOT_RUN=17原生相关+1人工+1可选转储。UI-01历史65/2/20/1另存，不覆盖、不继承。

B4交付等待固定提交复审；原生交互和UNKNOWN保持开放，不开发B07。
