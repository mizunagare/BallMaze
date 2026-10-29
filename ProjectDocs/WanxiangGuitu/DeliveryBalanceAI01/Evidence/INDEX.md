# 本轮证据索引

所有文件来自本轮独立隔离根，未继承旧PASS。`manifest.json`逐文件记录源/公开SHA256、大小和路径；`.log/.stdout/.stderr`原文压缩为`.gz`，仅对可能凭据做定向脱敏，不过滤错误。旧失败原位置不回写。未提交用户场景、ProjectSettings与Recovery原文件不上传。

| 目录/文件 | 内容 |
|---|---|
| Before、Before02、Before03 | 编译失败与实际规则负例；原HP/间距/暂停余量 |
| AfterRulesBaseline | 同一13项修复后首次检查与实际新配置 |
| Rules、RulesRetry、RulesResume、Compatibility | 资源NOT_RUN、一次重试、实际v9旧余量/技能/待选恢复 |
| MatrixBefore、MatrixBeforeWarm | 初始探索性108+108行，不能冒充严格配对 |
| BeforeObservationInputs、FrozenBeforeInputs、FrozenAfterInputs | 每个原始/临时观测C#与SHA；第一版冻结输入 |
| MatrixBeforeFrozen、MatrixAfterFrozen、Summary | 第一版冻结216行；保留Boss错时策略未实际触发的限制 |
| FrozenBeforeFinalInputs、FrozenAfterFinalInputs | 最终观测代码与原始产品输入SHA |
| MatrixBeforeFinal、MatrixAfterFinal | 最终各9 Run/108行，逐样本事件、XP源、初始/末尾随机状态、Profile/Run身份与完整布局 |
| SummaryFinal | 420当前断言、最终216行配对核对、分布/删失、升级时点与全部1815事件、历史过程状态 |
| VisualBefore、VisualAfter | 普通/远程/精英各两分辨率，12张实际受控相机图与相机/实体/时间记录；非原生/人工 |
| Final | 首次最终序列（包含UX02错误无图形启动），旧回归、B07、三进程正常AI与首次0E96W构建 |
| UX02GraphicsRetry | 有图形的正确启动；60项及实际截图 |
| BossStore | B07跨进程Running/Pending/Committed/acknowledged等真实标记与合成存档 |
| TrackedReplay、TrackedCompatibility | 已提交场景的13+47+4规则与新进程恢复 |
| TrackedFinal | 已提交场景的正常AI三进程、0E96W非开发构建、全警告CSV/原消息、所有输入和PE/程序哈希 |
| Prepare/fixtures | 本轮安装的合成历史格式夹具；不是本轮全部旧迁移用例已执行的声明 |
| Bindings | 开工/清理/每轮源码、用户5哈希、首次场景绑定FAIL、最终110 C#绑定、源码冻结提交绑定与保护检查 |

## 直接查看

- [最终机器汇总](SummaryFinal/summary.json)、[当前断言CSV](SummaryFinal/assertions.csv)、[配对核对](SummaryFinal/paired-check.json)。
- [固定提交场景构建原消息](TrackedFinal/Build/build-report-messages.json)、[96条警告](TrackedFinal/Build/warnings.csv)、[发行程序集/程序SHA](TrackedFinal/Build/release-assembly-audit.json)。
- [正常AI首程](TrackedFinal/Normal-Gather/process-result-Normal.json)、[继续](TrackedFinal/Normal-Gather/process-result-Resume.json)、[再次出征恢复](TrackedFinal/Normal-Gather/process-result-FinalResume.json)。业务明细/来源账在同目录checkpoint、settlement、score、轨迹和日志中。
- [修复前13项](Before03/baseline-checks.json)、[固定提交场景13项复验](TrackedReplay/RulesBaseline/baseline-checks.json)。
- [近战预警前](VisualBefore/Melee-1280.png)、[后](VisualAfter/Melee-1280.png)、[远程后](VisualAfter/Ranged-1280.png)、[精英1920后](VisualAfter/Elite-1920.png)。
- [最终输入绑定](Bindings/source-bindings.json)、[源码冻结提交](Bindings/code-commit-binding.json)、[用户保护](Bindings/protection-check.json)。

构建二进制、Library、缓存、转储和真实玩家存档不上传。发行Player本批实际操作、原生U16、人工与性能仍NOT_RUN；这些证据不能替代它们。[首个发布检查失败](publication-check-first-fail.json)与[通过的暂存完整性复检](publication-check.json)分别保留。远端完整SHA以交付回复重新读取值为准。
