# 无人值守收尾复验（2026-10-24）

开始基线、本地与远端 main 均为 `b3b7f6f75602aec127a44cf7fe1e650c8451de98`，没有后续提交。既有 ProjectSettings.asset 工作区标记保留，不暂存；没有 reset、force push、引擎/包升级、CI 或 B2～B4/B07。最终交付 SHA 见本文件所在固定提交与推送后的远端核对。

## ProcDump：限定二进制的实测分类

原始失败原样保留在 Evidence/Unattended/Diagnostic、AuditMatrix、MonitorFailure；不修改它们的 FAIL/exit1/exit7。之前把所有正退出码按常规程序规则视为失败，对此工具不够准确；不是游戏被修复了。

对 **微软有效签名、12.02、SHA256 `22C2A2B09ADE73A342A18DAB838354385F73FC98E324B9903FD61FFF949C5124`** 做了独立合成 Win32 窗口实验，未加载 Unity、未使用游戏存档：

| 控制实验 | 实际退出码 | 有效转储 | 结果 |
|---|---:|---:|---|
| 单次快照 | 1 | 1 | 与转储数量一致 |
| `-n 2 -s 1` | 2 | 2 | 与转储数量一致 |
| 合成窗口正常结束，`-e -t -n 1` | 1 | 1 | 目标进程 exit0，监视器返回1 |
| 明确不存在的 PID | -2 | 0 | 正确错误对照 |

[完整命令、原始输出发布副本及控制结果](Evidence/Followup/Controls)、[签名/哈希/结构校验依据](Evidence/Followup/Controls/calibration-proof.json)。这是**本机固定二进制的经验校准**，不冒称微软公开承诺所有版本都采用此退出约定。[微软文档](https://learn.microsoft.com/en-us/sysinternals/downloads/procdump)说明捕获参数，但未提供足以直接判定此次退出1的合同。

新分类同时要求：校准依据 SHA 正确、当前工具签名有效且 SHA/版本相同、正退出码等于新生成转储数量、完成日志数量一致、数量不超预算、文件结构校验通过。始终保留 rawExitCode=1；不是放行任意工具的 exit1。未来工具变更必须重新实验并审阅校准依据。局部 .gitattributes 对证明文件禁用换行转换，以保留执行时校验的原始字节，不改用户 Git 全局配置。

转储验证包括 MDMP 头/版本、目录范围、线程/模块/系统流、线程栈和上下文范围、模块名字串及内存列表范围。允许规范中的空 UnusedStream 保留槽；非空非法槽和截断范围仍拒绝。[结构参考](https://learn.microsoft.com/en-us/windows/win32/api/minidumpapiset/ns-minidumpapiset-minidump_header)、[线程结构](https://learn.microsoft.com/en-us/windows/win32/api/minidumpapiset/ns-minidumpapiset-minidump_thread)。SHA 用于固定证据，不把它当成有完整语义内存或已取得因果栈的证明。

定向回归涵盖：有效单份、退出码与数量不符、文件截断、未知二进制；后三者必须 FAIL。真实监视器重新运行与故障监视器 exit7 的进程级结果分别保存，故障后无关 Player 分析继续。最初检查器误拒绝空保留槽、测试准备读取不存在旧工具信息的失败单列保存，没有改动原转储或游戏数据。

## 游戏关闭：仍 UNRESOLVED

保留 [历史 D3D12 标题栏关闭样本](Evidence/CloseInvestigation/NativeEmpty/player1.log)及 [原调查](CLOSE_INVESTIGATION.md)。同一旧运行 exit0、有 quit→before-exit→save 与校验修订，仍在 Input System Shutdown 之后出现 `Got a UNKNOWN while executing native code`，随后 CodeReloadManager destroyed；Managed Stacktrace 为空。它是 Player，不是 Editor Search 异常。

本轮独立隔离运行使用后台自有 UnityWndClass 的 WM_CLOSE。每轮记录完整日志、实际退出码/超时、UTC 观察时间线、退出审计、校验/修订和转储结构；D3D12、D3D11、附加监视器分开。**没有新的真实标题栏点击证据**，不能拿后台通过替代该路径或宣布旧问题消失。

终止转储包含可读线程/模块/上下文，但不等于捕获旧 UNKNOWN 发生瞬间。没有可用 cdb/WinDbg/dumpchk，也没有与旧异常对应的可符号化因果栈。本轮不改产品销毁顺序、不默认切换 D3D11、不删除日志或压制异常。`-e -t -n 1` 不做窄字符串过滤，但只覆盖未处理异常/终止，可能遗漏被 Mono 自行处理的异常；无异常转储不能证明无异常。E06D7363/CoreUI 消息没有足够依据归因游戏。

## 原生交互环境：NOT_RUN

[只读环境检查](Evidence/Followup/interactive-environment.json)：当前只有使用中的 guan console 会话；没有提供已授权独占测试会话或测试机。未发现运行中的 Hypervisor、Sandbox 可执行文件或 VM 管理工具；mstsc 存在和 TermService 运行不等于有可用测试主机。不自动登录、启用系统功能、激活/切换私有桌面、改 Snipaste 或发 Esc；没有请求用户守候。

可重复原生测试应在预先配置的专用 Windows 机器/独占交互会话进行，记录会话租约、桌面/前台/PID/程序哈希、GPU/DPI/分辨率，焦点失配即停止输入。VM 的图形后端必须另行核实，不能拿软件渲染结果替代本机 RTX/D3D12 对照。当前 Unity 自定义 Canvas 也缺少已验证的原生语义观察器；只发出输入或受控截图不够验收按钮效果。以上是部署要求，不是已实现的远程执行能力。

原生 U16、真实标题栏复现与独立人工理解分别 NOT_RUN。人工理解必须由未参与实现者无提示试玩，不能由正常 AI 或截图代替。

## 最终完整 All

本轮使用新建根 `20261024-014418-042bbf7d`，`-Phase All -FullRegression`；没有用定向复测替代。自动化源码在启动时记录哈希并冻结，后续仅更新文档与证据。只复用同版本 ShaderCache，没有复用旧编译程序集、测试结果、构建或玩家存档；不声称干净 Shader 编译。

本轮实际结束、协调器exit0，原始计数 **65 PASS / 2 FAIL / 20 NOT_RUN / 1 UNRESOLVED**。两个FAIL仅为预期harness-negative探针，非预期FAIL=0。[结果](Evidence/Followup/FinalAll/results.json)、[CSV](Evidence/Followup/FinalAll/results.csv)、[报告](Evidence/Followup/FinalAll/REPORT.md)、[源码冻结核对](Evidence/Followup/source-freeze-check.json)。

| 分项 | 状态 | 本轮实际证据 |
|---|---|---|
| 计划30方法 | PASS | 29规则/Play Mode＋正式构建30/30；额外夹具1项，共31个controlled阶段通过 |
| 非开发构建 | PASS | 0错误/52现有警告，114016597 bytes，50.29秒；完整Release哈希自动记录在build-manifest.json |
| 正常AI/恢复 | PASS | Normal/Resume实际exit0；战斗采集、修复、未清场撤离、入库制造、波次模式再次出征与恢复 |
| 受控UI | PASS | 本轮92帧；不是原生输入/人工理解 |
| 后台关闭/恢复 | PASS | [9次关闭、4次恢复](Evidence/Followup/FinalAll/player-summary.json)，实际exit0、无超时、审计/主档校验/修订通过；无UNKNOWN标记 |
| ProcDump工具 | PASS（限定校准） | 本轮rawExit1仍保留，当前签名/SHA、一份完成转储及结构相匹配；分类器exit0 |
| 游戏关闭异常 | UNRESOLVED | 历史标题栏D3D12失败保留；本轮只有后台协议，没有因果异常栈 |
| 原生U16 / 人工理解 | NOT_RUN / NOT_RUN | 未提供独占主机，缺少Canvas原生语义观察；没有独立人工试玩 |
| 最终All | 执行PASS，整体验收UNRESOLVED | 完整新运行结束，但不能以exit0宣布全部验收通过 |

本轮exe SHA256：`001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`。转储无异常流，不能解释旧UNKNOWN。木材实际计数6，修复扣2后4，取2制造后仓库木2；最终数组`0,0,0,2,4,0`（石4），以本轮expected-normal.txt为准。关闭夹具未修复、回执为空；非空回执由本轮B1/正常AI回归验证，不能冒充原生修复操作。

冻结源码核对全部相同。本轮没有后改代码再用定向结果拼接All。打包首次LF转换触发证明SHA断言，已恢复原始字节并用局部Git属性固定；原运行结果不改。独立诊断辅助脚本的空PID列表呈`[[]]`，原样保留，没有PID数值；退出回执齐备，最终All的正式preserved-processes.json为`[]`。该辅助格式小限制不改已冻结运行版本。

完整 Release 文件哈希由入口自动写 build-manifest.json，关联本轮所有 Player 命令。规则/Play Mode、正常 AI、受控 UI、后台关闭/恢复、原生 UI 与人工分开。预期 exit7/超时探针原样 FAIL，scope=harness-negative；其被正确记录并继续的自检另记 PASS。编排器 exit0 不等于全部验收通过。

超时只记录并保留进程，不强杀、不覆盖用户程序或真实玩家档。完整原始日志和转储留唯一测试根；仓库只放脱敏日志发布副本、哈希、结构与断言摘要，不放完整存档、二进制、Library、Temp 或内存。
