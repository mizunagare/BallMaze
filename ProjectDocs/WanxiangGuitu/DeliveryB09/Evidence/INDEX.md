# B09 证据索引

**当前验收只取 FinalAll（All5），其余目录是历史失败、早期输入或对照，不继承PASS。** 测试均用工程外唯一合成根。PNG为实际运行原图；日志脱敏发布，manifest同时保留原始/发布SHA，原始日志保留本机。没有上传真实玩家存档、完整save封装/分页、构建二进制或缓存。

## 最终完整运行

- [结果JSON](FinalAll/results.json) / [CSV](FinalAll/results.csv) / [原编排报告](FinalAll/REPORT.md) / [计数](FinalAll/counts.json) / [B09派生摘要](FinalAll/b09-summary.json)。138 PASS、2预期探针FAIL、7 NOT_RUN、2 UNRESOLVED，0非预期FAIL。
- [协调退出观察](FinalAll/B09Diagnostics/b09-coordinator-observation.json)、[挂起进程清单](FinalAll/preserved-processes.json)、[测试计划](FinalAll/test-plan.json)。不是只凭协调exit0判验收。
- [正常AI轨迹/审计](FinalAll/B4Diagnostics/)及[真实结算摘要](FinalAll/SettlementSummaries/)；7策略×3进程，Editor玩家bot与正常NPC AI，不是原生键鼠或人工。
- [Entry检查点1](FinalAll/B08Diagnostics/Normal-Entry/b08-checkpoint-1.json)、[检查点2](FinalAll/B08Diagnostics/Normal-Entry/b08-checkpoint-2.json)、[检查点3](FinalAll/B08Diagnostics/Normal-Entry/b08-checkpoint-3.json)；[实际Title回调审计](FinalAll/B09Diagnostics/Normal-Entry/entry-audit.jsonl)。同一后继Run/布局/随机流/装备/来源账/教程最终精确一致，第二次出征确有新Run。
- [最终Player进程1](FinalAll/B09PlayerDiagnostics/B09-Entry/process-1.json)、[进程2](FinalAll/B09PlayerDiagnostics/B09-Entry/process-2.json)、[关闭/保存严格分析1](FinalAll/B09PlayerDiagnostics/B09-Entry/analysis-1.json)、[分析2](FinalAll/B09PlayerDiagnostics/B09-Entry/analysis-2.json)、[恢复断言1](FinalAll/B09PlayerDiagnostics/B09-Entry/b08-analysis-1.json)、[恢复断言2](FinalAll/B09PlayerDiagnostics/B09-Entry/b08-analysis-2.json)、[完整退出保存审计](FinalAll/B09PlayerDiagnostics/B09-Entry/storage-audit.jsonl)。实际非开发D3D11、受控gameplay入口、后台WM_CLOSE；不是原生菜单/标题栏操作。
- [规则与事务记录](FinalAll/B09Diagnostics/Rules/b09-rules.txt)、[真实Pending/Committed加载](FinalAll/B09Diagnostics/Rules/b09-cases.txt)、[设置试件断言](FinalAll/B09Diagnostics/Rules/b09-preferences-check.txt)、[启动前隔离门禁](FinalAll/B09Diagnostics/Rules/b09-isolation-check.txt)、[受控渲染/按钮与动作断言](FinalAll/B09Diagnostics/Rules/B09Visual/b09-visual.txt)。journal与preferences若发布，仅为显式合成事务元数据/数值试件。

## 最终正式标题（不带gameplay绕过）

以下6张是最终非开发Player的实际ScreenCapture，已逐张查看，严格检查非空白/非青色、Title场景、0个CombatSession、集合字节未变化、审计与退出码。显示仅位于未激活的测试桌面；没有原生输入。

| 状态 | 实际PNG | 分析与退出 |
| --- | --- | --- |
| 无档 | [PNG](FinalAll/B09Screens/B09-Title-Missing/title-player.png) | [完整检查](FinalAll/B09Diagnostics/B09-Title-Missing/b09-title-analysis.json) / [进程](FinalAll/B09Diagnostics/B09-Title-Missing/process.json) / [审计](FinalAll/B09Diagnostics/B09-Title-Missing/entry-audit.jsonl) |
| 有效在途 | [PNG](FinalAll/B09Screens/B09-Title-Ready/title-player.png) | [完整检查](FinalAll/B09Diagnostics/B09-Title-Ready/b09-title-analysis.json) / [进程](FinalAll/B09Diagnostics/B09-Title-Ready/process.json) / [审计](FinalAll/B09Diagnostics/B09-Title-Ready/entry-audit.jsonl) |
| 损坏 | [PNG](FinalAll/B09Screens/B09-Title-Corrupt/title-player.png) | [完整检查](FinalAll/B09Diagnostics/B09-Title-Corrupt/b09-title-analysis.json) / [进程](FinalAll/B09Diagnostics/B09-Title-Corrupt/process.json) / [审计](FinalAll/B09Diagnostics/B09-Title-Corrupt/entry-audit.jsonl) |
| 不兼容 | [PNG](FinalAll/B09Screens/B09-Title-Incompatible/title-player.png) | [完整检查](FinalAll/B09Diagnostics/B09-Title-Incompatible/b09-title-analysis.json) / [进程](FinalAll/B09Diagnostics/B09-Title-Incompatible/process.json) / [审计](FinalAll/B09Diagnostics/B09-Title-Incompatible/entry-audit.jsonl) |
| 待确认 | [PNG](FinalAll/B09Screens/B09-Title-Pending/title-player.png) | [完整检查](FinalAll/B09Diagnostics/B09-Title-Pending/b09-title-analysis.json) / [进程](FinalAll/B09Diagnostics/B09-Title-Pending/process.json) / [审计](FinalAll/B09Diagnostics/B09-Title-Pending/entry-audit.jsonl) |
| 已保存待回营 | [PNG](FinalAll/B09Screens/B09-Title-Committed/title-player.png) | [完整检查](FinalAll/B09Diagnostics/B09-Title-Committed/b09-title-analysis.json) / [进程](FinalAll/B09Diagnostics/B09-Title-Committed/process.json) / [审计](FinalAll/B09Diagnostics/B09-Title-Committed/entry-audit.jsonl) |

两种错误隔离根的[截图参数拒绝](FinalAll/B09Diagnostics/B09-Reject-entry-evidence/b09-rejection-analysis.json)、[gameplay拒绝](FinalAll/B09Diagnostics/B09-Reject-test-gameplay/b09-rejection-analysis.json)：实际exit2、无超时、无强杀、normalCloseFallback=false。预期错误退出不称为正常退出。

## 受控布局、角色和场景图

[B09图像清单/28张原始SHA与尺寸](FinalAll/b09-screens.json)；其中22张受控Editor、6张正式Player标题，分类不混淆。

- 菜单：[1280×720](FinalAll/B09Screens/B09Visual/b09-menu-1280x720-主菜单.png)、[1920读取](FinalAll/B09Screens/B09Visual/b09-menu-1920x1080-读取存档.png)、[3440设置](FinalAll/B09Screens/B09Visual/b09-menu-3440x1440-设置.png)、[新游戏确认](FinalAll/B09Screens/B09Visual/b09-new-game-confirmation.png)。4种分辨率的12页图及边界断言；Editor退出安全测试提示不是Player错误。
- 营地：[稳定旧基线](../../DeliveryB08/Evidence/FinalAll/B08Screens/b08-ui-1280x720-100-camp.png) / [本轮](FinalAll/B09Screens/B09Visual/b09-camp-after.png)；[森林](FinalAll/B09Screens/B09Visual/b09-forest-after.png)。早期Before的青色图不用作场景质量基线。
- 动作：[走](FinalAll/B09Screens/B09Visual/b09-walk-camp.png)、[跑](FinalAll/B09Screens/B09Visual/b09-run.png)、[攻击](FinalAll/B09Screens/B09Visual/b09-attack.png)、[程序化翻滚](FinalAll/B09Screens/B09Visual/b09-dodge-procedural.png)、[受击](FinalAll/B09Screens/B09Visual/b09-hit.png)、[死亡0.2秒](FinalAll/B09Screens/B09Visual/b09-death.png)、[动作后正常结算](FinalAll/B09Screens/B09Visual/b09-death-settlement.png)。受控真实伤害/位移/姿态，不是正常AI胜利或完整人工动作验收。
- [实际骨骼/全部剪辑绑定审计](History/Before/B09Diagnostics/Rules/b09-model-audit.txt)、[KayKit许可](../../../../Assets/FantasyArt/Licenses/KayKit-Adventurers.txt)。角色6个Skinned、246个骨骼引用、Legacy曲线解析；不是新Humanoid/完整骨骼翻滚。
- [既有UI92图清单](FinalAll/screens.json)、[B08夹具](FinalAll/b08-screens.json)、[Boss可读性](FinalAll/readability-screens.json)独立归档。

## 构建与输入

[构建摘要](FinalAll/build-summary.json)、[逐文件构建SHA](FinalAll/build-manifest.json)、[全部warning原始行](FinalAll/build-warning-lines.json)、[实际源/副本构建输入](FinalAll/source-build-provenance.json)、[94份产品与测试来源封存](FinalAll/frozen-product-proof.json)、[用户文件保护](FinalAll/user-input-proof.json)、[正式程序集剔除](FinalAll/release-entry-check.json)、[异常完整清点](FinalAll/exception-inventory.json)。源码冻结输入6ec68a88；87 BuildReport警告、73 Editor.Search内部异常起点均保留。6个副本输入差异见provenance，不能冒称干净Git场景/设置逐字一致。

完整脱敏日志：[规则/编译/构建等](FinalAll/Logs/logs-redacted.zip)、[B09规则与正式Player日志](FinalAll/B09Logs/logs-redacted.zip)、[B08规则](FinalAll/B08Logs/logs-redacted.zip)、[B07规则](FinalAll/B07Logs/logs-redacted.zip)。各目录manifest标记原始与发布字节的差异。Git暂存证明见最终staged-byte-proof.json（不自包含）。

## 历史失败与有边界对照

- [早期审计/编译/夹具/首轮All与资源门槛历史](History/attempts.json)。
- [第二轮All编译失败](AdditionalHistory/attempts.json)。
- [第三轮较早输入](PreSafetyAll/attempts.json)，不继承其PASS；其旧标题空白检测也不足。
- [第四轮原编排结果](BeforeBlankCapture/All4/results.json)及[原138/2/7/2](BeforeBlankCapture/All4/counts.json)，未重写；其6个黑帧视觉PASS由独立FAIL复审撤回。
- [严格6个黑帧FAIL与相同二进制显示条件对照](BlackFrameProbe/comparison.json)、[失败原记录](BlackFrameProbe/StrictBefore/)、[只在未激活桌面显示后的实际PNG](BlackFrameProbe/title-shown-inactive.png)、[其过程/审计](BlackFrameProbe/ShownInactive/)、[完整日志](BlackFrameProbe/ShownLogs/logs-redacted.zip)。仅修正SW_HIDE捕获条件，不宣称UNKNOWN/cyan根因解决，不替代FinalAll。
- [全部失败说明](../FAILURE_HISTORY.md)。每个目录有独立源快照或冻结输入，早期版本不冒充当前版本。

## 仍开放

原生U16、B09原生键鼠和人工可理解性NOT_RUN；D3D12 UNKNOWN、Editor青色帧根因UNRESOLVED。当前显示桌面不是输入桌面，不能用WM_CLOSE/截图冒充真实标题栏点击。未验证全视角足锁定、遮挡或干净Git场景完全同输入；具体限制见[报告](../REPORT.md)与[验收](../ACCEPTANCE.md)。本批后暂停复审，不开始B10。
