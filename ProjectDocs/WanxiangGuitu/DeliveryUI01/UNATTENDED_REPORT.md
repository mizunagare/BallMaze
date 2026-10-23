## 2026-10-24 当前收尾复验

本轮基线 `b3b7f6f75602aec127a44cf7fe1e650c8451de98`。[当前收尾报告](FOLLOWUP_REPORT.md)优先于下方历史记录。固定微软签名ProcDump经单份→exit1、双份→exit2、无效PID→-2校准；保留rawExit1且同时校验工具身份、完成数量和转储结构，未知工具/错误码/截断仍FAIL。旧失败不改写。

新根完整All -FullRegression实际结束：65 PASS / 2预期故障探针FAIL / 20 NOT_RUN / 1 UNRESOLVED，非预期FAIL=0。后台退出9/9、恢复4/4通过。完整All执行PASS，整体验收仍UNRESOLVED；旧UNKNOWN未解决，真实标题栏新复现、原生U16和人工理解NOT_RUN。B2未开始。

以下是旧轮记录，不继承为本轮PASS。

# 本机无人值守验证与关闭诊断

开始基线、本轮开始及结束前核对的远端 main：`913528a9f086b92d0ba8e393b5cc52de5328b78d`。最终交付 SHA 以本报告所在的固定提交 URL 与推送后的 ls-remote 为准。保留源工程 ProjectSettings.asset 的既有工作区标记，不提交它。没有 reset、force push、CI、B2～B4/B07 或业务系统改写。

入口：[Invoke-LocalValidation.ps1](Automation/Invoke-LocalValidation.ps1)，[一条命令复跑与参数](Automation/README.md)。运行规则、Play Mode、正常 AI、非开发构建、独立 Player 关闭/恢复与受控 UI 矩阵；结果持续写 JSON/CSV/Markdown，不等待用户操作。NativeProbe 是 Assets 外的独立工具，正式构建无运行验证驱动。Unity/URP/Input System/uGUI 版本维持原值。

## 最后验收状态（优先于下方开发轮次）

最终代码增加了每个子进程的 command/exit 回执，以及辅助监视器退出码汇总；没有修改产品代码。

- **完整 All 试运行已执行**：`20261024-002532-6b61e119`，[完整结果](Evidence/Unattended/Full/results.json)、[CSV](Evidence/Unattended/Full/results.csv)、[报告](Evidence/Unattended/Full/REPORT.md)。15 项回归、正常 AI/Resume、92 帧受控 UI、非开发构建（0 错52警告，74.35秒）通过；[Player 关闭9/9、恢复4/4](Evidence/Unattended/Full/matrix-summary.json)通过。实际入口持续执行到结束，无用户点击。正常 AI 再出征使用既有波次测试模式。
- **不能将该 All 的 exit0 当成全部通过**：其原始计数48 PASS / 2预期探针FAIL / 34 NOT_RUN / 1 UNRESOLVED，随后审计发现漏记 ProcDump exit1。这是编排缺陷证据，不改写原结果。审计增补后重跑 [AuditMatrix](Evidence/Unattended/AuditMatrix)，Player仍9/9通过，但完整辅助回执暴露相同非零码。
- **修复后定向复测**：[Diagnostic](Evidence/Unattended/Diagnostic/results.json)以 `-n 1` 运行真实 ProcDump，已写出终止 dump 且显示 Dump count reached，但仍 exit1；入口正确记 `dump.Default-dump=FAIL, exitCode=1`，整体实际 exit1。因此不是单纯“要求2份只得到1份”的原因，工具退出含义/根因 **UNRESOLVED**；没有据此放宽断言、忽略失败或归责 Player。
- **故障传播回归 PASS**：[MonitorFailure](Evidence/Unattended/MonitorFailure/assertion.json)使用独立 FaultMonitor（立即 exit7，不附加调试器、不访问游戏状态），真实记 FAIL/7、协调器 exit1；依赖无关的 Player 退出分析随后仍 PASS。这个负例是工具回归，不是游戏 FAIL，也不是伪造原生 UI。另有 [命令/退出回执自检](Evidence/Unattended/Full/ReceiptSelfTest/result.json)。
- **保留 NOT_RUN / UNRESOLVED**：原生 UI 完整语义、独立人工理解仍 NOT_RUN；旧 UNKNOWN 根因 UNRESOLVED。最后两项审计/辅助汇总修改后，完整 All 单次重跑 NOT_RUN，只定向复测了受影响路径；没有把旧 All 拼成最终全 PASS。

完整轮正常 AI 木材计数实际为4，修复扣2剩2，结算后取2制造，仓库余额木0；最终材料数组 `0,0,0,0,4,0`（石4），见 Full/Normal/expected-normal.txt。下方 Business 轮的木2石3是另一轮实际结果，不套用于本轮，不修改掉落凑数。

当前可无人值守执行规则、AI、受控UI、后台正式Player关闭/恢复；若启用本机 ProcDump，当前会真实返回诊断 FAIL，而非虚假绿色。未提供可用 ProcDump 时仅该实验 NOT_RUN。完整原生 U16 仍需专用交互测试会话和可靠语义观察，不能以当前后台测试替代。B2未开始。

## 开发过程中各轮实际运行

| 运行 | 结果 | 证据与边界 |
|---|---|---|
| Business：20261023-235913-583d98d8 | 15 项回归 PASS | [结果](Evidence/Unattended/Business/results.json)；包括装备容器、双武器冷却、工作台、B1 Run/Resume/路线、森林、分页边界、保存故障、A1 四项和 UI01Rules；其余历史项目明确 NOT_RUN，没有继承 30/30 |
| 非开发 Windows 构建 | PASS | [摘要](Evidence/Unattended/Business/BuildSummary.txt)：0 错误 / 52 警告，114016597 bytes，52.95 秒，BuildOptions.None；新副本导入，复用同版本 ShaderCache，不能声称本轮干净 Shader 编译 |
| 正常 AI 与新进程恢复 | PASS | [断言](Evidence/Unattended/Business/Normal/normal-results.txt)、[实际退出](Evidence/Unattended/Business/Normal/process-result-Resume.json)、[轨迹](Evidence/Unattended/Business/Normal/normal-ai.csv)；攻击、采集、修复、引导、未清场撤离、入库、取材制造、再次出征；不是原生 UI 或人工试玩 |
| 受控 UI | PASS | [92 帧矩阵](Evidence/Unattended/Business/ControlledScreens/visual-layout.jsonl)、[完成标记](Evidence/Unattended/Business/ControlledScreens/visual-result.txt)；E/H 一致、费用、取消/受伤、焦点、冷却和结算由原规则验证；受控 NPC/故障与虚拟输入不冒充原生输入 |
| Matrix：20261024-001858-2d0dace2 | 严格退出 9/9 PASS；恢复 4/4 PASS | [汇总](Evidence/Unattended/matrix-summary.json)、[完整结果](Evidence/Unattended/Matrix/results.json)、[CSV](Evidence/Unattended/Matrix/results.csv)；协调器实际 exit0，未遗留进程 |
| 无干扰原生 UI 全流程 | NOT_RUN | 非输入私有桌面拒绝 SendInput；没有要求用户点击，没有用领域方法冒充原生 E/H/按钮行为 |
| 人工可理解性 | NOT_RUN | 没有独立试玩人员，自动截图不能代替 |
| UNKNOWN 根因 | UNRESOLVED | 新矩阵未复现旧日志标记；未取得能与旧 UNKNOWN 对应的因果调用栈，没有修改产品来“消除”异常 |

早期 Business 轮不是“最新版 All 整条无中断 PASS”：Business 的规则/AI/视觉完成后，中止了仍加载旧 UTC 比较函数的开发协调器，保留取消记录；随后用成功的同一构建、完整合成夹具在全新根运行阶段矩阵，9 次均结束。两部分结果分开，不将旧阶段改写为新一次运行。修正后的矩阵可独立复跑，业务断言未重写。

正常 AI 本轮实际木材拾取 6，修渡口扣 2 后 4，再取木 2 制造；最终仓库材料数组 `0,0,0,2,3,0`，即木 2、石 3，以 expected-normal.txt 为准，不套用旧轮余额。该流程实际战斗且没有冻结所有敌人；合成空遭遇夹具只用于关闭矩阵。

## 关闭诊断

同一非开发构建/合成完整夹具，默认 D3D12 与 D3D11 各两组，每组进程 1 正常关闭后启动进程 2。另有一组默认 D3D12 单独附加 ProcDump。日志确认 RTX 3060、默认 Direct3D 12 与强制 Direct3D 11。所有进程启动前即有 `-wanxiang-storage-root`，未访问真实玩家档。

| 条件 | Player 次数 | 严格退出 | 新进程恢复 | 退出保存修订 |
|---|---:|---|---|---|
| 默认 D3D12，无监视器 | 4 | 4 PASS | 2 PASS | 每组 4→5→6 |
| D3D11，无监视器 | 4 | 4 PASS | 2 PASS | 每组 4→5→6 |
| 默认 D3D12，独立 ProcDump | 1 | Player 分析 PASS；诊断根因 UNRESOLVED | NOT_RUN（此实验不复开） | 4→5 |

退出码均 0，无超时/强杀；quit→before-exit→save 顺序、主档 SHA256 与修订递增逐项检查。恢复比较同 Profile、Run、区域、两种种子、出口回执、物品 ID、库存、入场/新增来源账和世界摘要。[每轮分析、审计、进程及时间顺序](Evidence/Unattended/Matrix)分别保存，所有完整 Player 日志位于 logs-redacted.zip。时间线是轮询首次观察的 UTC 边界，不伪造异常发生的精确时间。

关闭矩阵夹具位于未付费渡口，回执为空值；它验证未修复状态维持一致，不冒充原生修复后的非空回执验收。实际修复及保存回执恢复由本轮 B1 规则和正常 AI 路线覆盖，二者与原生输入分开。

本轮关闭方式是独立工具对确属目标 PID 的 `UnityWndClass` 排队 WM_CLOSE，**不是物理标题栏点击，也没有先点帮助**；私有非输入桌面亦不同于旧复现环境。故不能用这 9 次未复现推导旧问题已修复或归因 D3D12。旧错误原文 `Got a UNKNOWN while executing native code` 及空栈证据在既有 CloseInvestigation 中继续保留。

早期 ProcDump 使用 `-mm -e -t -n 2`（最终定向实验改为 `-n 1`，实际非零仍保留），未用窄过滤；输出记录 E06D7363 / `MessagingValidationException...Microsoft.CoreUI` 等异常描述，随后正常 exit0，并写出 **1 个终止 dump，37255848 bytes**。这些不是与旧 UNKNOWN 对应的因果栈，不据名称归责。没有可用 cdb/WinDbg/dumpchk，本轮符号化栈分析 NOT_RUN。dump 本地保留，提交[大小/哈希清单](Evidence/Unattended/Matrix/dump-local-manifest.json)和完整监视输出；终止 dump 不等于崩溃，没有异常 dump 也不等于无异常。

Editor 视觉日志另有 `UnityEditor.Search.SearchDatabase.EnumerateAll` 的 ArgumentOutOfRangeException、合成保存失败及退出分配器提示；保留在编辑器日志中，与 Player 日志分开，不据此归因产品关闭。

## 工具故障与防误报

1. Pilot 出现重复正常 AI 驱动 CS0111；改为在同一隔离副本中交接既有驱动，保留原失败编译日志，修后正常 AI/Resume exit0。
2. JSON utc 被 PowerShell 解析成 DateTime，与格式化字符串比较产生假超时；改为 UTC DateTime 比较，并加入边界自检。[Pilot 时间戳证据](Evidence/Unattended/Pilot/timestamp-regression.json)保留；开发协调器被取消，不能标正常退出 PASS。测试 Player 后续只发自有窗口关闭消息清理，不能追补被取消轮的退出码。
3. [WindowFailure](Evidence/Unattended/WindowFailure/results.json)首次矩阵因 MainWindowHandle 选到同 PID 的可见 50×50 `UAC_InputIndicatorOverlayWnd` 而超时；存档/进程仍在，未强杀；其余矩阵自动记录冲突 NOT_RUN。增加窗口清单，限定 UnityWndClass/测试夹具类，正常关闭遗留测试窗口，再新根复跑成功。WM_CLOSE 排队成功本身不算进程退出通过。
4. 每轮故意 exit7 与超时探针保留为 harness-negative 的 FAIL；自检另验后续任务继续。最终矩阵原始计数 **27 PASS / 2 FAIL / 23 NOT_RUN / 1 UNRESOLVED**；2 FAIL 均预期探针，非预期 FAIL=0。不能把协调器 exit0 解读为全部验收 PASS。
5. [WrongVersion](Evidence/Unattended/WrongVersion/results.json)用 cmd.exe 代替 Unity 的负例 exit1、提前拒绝；没有启动/升级工程。缺工具、空间不足和隔离路径非法同样提前阻断；不自动安装系统组件。

所有生成文件与进程仅在唯一测试根。源用户程序没有被关闭；两次开发协调器取消记录单列，Player 超时从未计作正常退出。最终未遗留 Player/ProcDump。[业务轮取消记录](Evidence/Unattended/Business/development-cancellation.json)与最终矩阵的空 preserved-processes.json 可查。

## 构建对应、证据与限制

[源码/资源核对](Evidence/Unattended/source-build-correspondence.json)：730 项中 728 字节相同，包括运行 C# 与 Packages manifest/lock/版本；隔离 Unity 导入/构建改写了 PC_RPAsset 的派生预过滤/序列化字段及 URP 全局 RuntimeSettings 列表，差异另存，不伪称所有资源字节相同。没有把这些生成变化写回原工程，也没有升级包。所有关闭对照仍使用同一个已构建产物。[构建与工具哈希](Evidence/Unattended/Matrix/code-provenance.json)可复核。

原日志本地保留；发布副本移除许可证命令参数，UTF-8 格式统一，manifest 同时记录原始与发布 SHA，不声称压缩副本原字节不变。不上传完整合成/玩家存档、Library、Temp、构建、凭据、ProcDump 二进制或内存转储。

可继续无人值守运行领域/AI/后台退出恢复诊断，无需用户每批守候。仍阻断完整 U16 的是专用输入测试会话与可靠原生 UI 语义观察；需后续专用测试机器/会话，不在本轮擅改系统。完整物理鼠标键盘步骤、人工理解、旧 UNKNOWN 根因以及最终完整 All 单次修后运行仍未完成。建议保留 UI-01 未完全验收状态，先补这些条件，再决定 B2；本轮没有进入 B2。

推送成功不代表复审通过或发布验收通过。
