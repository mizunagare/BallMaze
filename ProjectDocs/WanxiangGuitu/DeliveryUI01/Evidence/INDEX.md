## 最后追加证据

Unattended/Full：一次完整All从新副本准备到报告结束，15项、正常AI/恢复、构建、92帧、9次关闭/4次恢复。原始48/2/34/1计数漏了监视器退出1，不能据此说整体PASS。

Unattended/AuditMatrix：通用子进程命令/退出回执增补后的矩阵；保留ProcDump实际退出1。

Unattended/Diagnostic：真实ProcDump -n1仍退出1，修复后的汇总记FAIL/1，协调器exit1；dump成功产生不覆盖非零码。Unattended/MonitorFailure：独立故障监视器exit7，协调器exit1、Player分析继续PASS，assertion.json验证失败传播。

完整原生UI/人工理解NOT_RUN，UNKNOWN和工具非零根因UNRESOLVED。最后审计修复后全All未重跑，只有定向检查。下方各轮原始结果与失败均保留，不覆盖。

## 2026-10-24 无人值守验证

[本轮报告](../UNATTENDED_REPORT.md)、[矩阵摘要](Unattended/matrix-summary.json)。Unattended/Business 保存15项、正常AI/Resume、92帧受控布局、构建与取消旧协调器记录；Matrix 保存最终9进程的退出/恢复分析、完整审计、时间线、窗口选择、JSON/CSV/Markdown与日志；Pilot、WindowFailure、WrongVersion 保存首次故障、窗口误选超时与预期拒绝，不能抹去。

Matrix 的原始计数27 PASS / 2 FAIL（预期harness-negative）/ 23 NOT_RUN / 1 UNRESOLVED；协调器exit0不等于U16全PASS。原生完整交互/人工理解NOT_RUN，UNKNOWN根因UNRESOLVED。日志zip为脱敏UTF-8发布副本，manifest列原始和发布哈希，原始日志本地保留；不提交存档、构建或内存。source-build-correspondence与isolated-generated-settings.diff.txt如实列出隔离Unity生成的两项URP设置差异。

以下是此前证据，保持原样。

# 本轮证据索引

## 收尾诊断（b673203后，无产品代码改动）

`CloseInvestigation/` 单独保存原生Player关闭日志、进程/审计/存档修订与恢复摘要：

- Native：上轮独立Player的UNKNOWN样本，关闭动作未明确核实，不当干净退出证据。
- NativeEmpty：pid23856正常点击×，exit0/无超时/保存93但UNKNOWN；pid52952 D3D11对照正常点击×、保存146且无UNKNOWN。close1-analysis应为false，close2-analysis应为true；后者含新进程恢复比较。raw player日志与审计、真实鼠标截图分开保留。
- DX12Repeat：本轮默认图形重复，正常点击×，exit0但再次UNKNOWN，严格分析false。
- D3D11Repeat：不附加监视器的第二对照，按独立运行结果判断，不用别轮PASS补齐。
- D3D11Dump：微软ProcDump完整原始输出logs.zip与去NUL阅读副本；未捕获过滤的严重异常转储。不能把空输出解释为全部异常不存在。
- source-and-build、player-driver-name-check：本轮源码/资源与原出包对应、关键二进制哈希及运行程序集无测试类型名检查；后者是辅助证据，配合Editor目录/构建来源，不替代程序集审查。
- synthetic-snapshot-hashes：只提交合成快照校验/修订与摘要，不提交完整档。旧保存回执是save尝试，最终主档校验和修订另查。
- FailedFixture/FailedLaunchCollision：批处理夹具初始化等待超时/项目重复打开的失败历史，仅Editor准备失败，不能归为Player关闭异常。

见 [关闭调查](../CLOSE_INVESTIGATION.md)及 [验收表](../ACCEPTANCE.md)。正常AI、受控92帧、人工理解和原生Player流程不混用；人工理解仍NOT_RUN。

## 原UI-01证据（保留）

- CleanVerified：最终 fresh copy，30方法全部退出0、无超时；results.json、summary、ui01-results、旧领域结果。logs.zip 为本轮原始日志。
- FinalCurrent：最终产品代码的针对规则、B1 Run/Resume与非开发构建；根 BuildSummary 与 build-hashes 记录实际构建。
- NormalLatest：原工程正常AI自动完整路线和独立进程Resume，4+实际游戏截图、CSV、日志与启动到退出存档审计；不是人工试玩。
- LatestRejectMissing / Relative / LocalLow：本次预Play隔离拒绝，预期exit1，无审计，合成哨兵不变。
- BeforeEvidence：3574基线8张真实受控截图、退出0。baseline-source-proof比较关键旧源码。
- ScreensFinal：最终92张实际受控截图，visual-layout记录帧/尺寸/缩放/可见组/目标，退出0。NPC关闭；uncertain/save-failed为合成故障，非真实档损坏。
- ReleaseUI：无运行验证驱动的正式包启动真实窗口；F1被外部Snipaste截获，后续原生操作/正常退出/继续NOT_RUN。hidden launch和被清理进程非正常退出证明。
- Rules / Full / Full2 / Verified / Screens：早期失败与超时原始记录。不可当作最终通过证据；具体修正及最终重跑见REPORT。
- runtime-source-correspondence：最终源工程与出包隔离工程非Editor C#及Resources逐项字节一致。源码SHA是未归一工作文件哈希，不作为Git自动换行后的通用哈希。

没有提交完整合成存档或真实玩家存档。日志中的绝对路径属于当次隔离根；复跑参数见TESTING。压缩日志原字节保留。未验证项不能用旧批PASS覆盖。
