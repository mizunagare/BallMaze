# Player 关闭诊断（2026-10-23，继续收尾）

开始本地/远端 main 都是 `b67320315ea180b97d6ffe96b5cc00a2829065e2`，无之后提交。工作区既有 `ProjectSettings/ProjectSettings.asset` 修改标记（diff无实质内容）保留，未暂存。上轮未提交的合成UI夹具从 DeliveryB2/Tests 迁到 DeliveryUI01/Tests；没有B2产品实现。

**结论：UNRESOLVED。** 已确认非开发 Windows Player 在正常关闭的一次已确认操作中出现下列诊断；不能依据退出码0宣布关闭干净，不能依据D3D11单次干净对照宣布D3D12就是根因。本轮未升级依赖、未隐藏日志、未更改保存/HUD/结算生命周期或用户快捷键。

## 原始问题及阶段

```text
[Physics::Module] Cleanup current backend.
Input System module state changed to: ShutdownInProgress.
Input Polling Thread exited.
Input System module state changed to: Shutdown.
Native Crash Reporting
Got a UNKNOWN while executing native code. This usually indicates
a fatal error in the mono runtime or one of the native libraries
used by your application.
Managed Stacktrace:
<empty>
CodeReloadManager destroyed
```

原始完整 Player 日志见 Evidence/CloseInvestigation/NativeEmpty/player1.log，pid23856。用户确认点击窗口正常关闭；同次运行有独立持有进程句柄的观测结果 `observed-exit1.json`：exit0、未超时。应用审计记录 quit 14:17:26.231003Z、before-exit 14:17:26.2329227Z、save 14:17:26.2339035Z，进程观测退出14:17:27.6188229Z（本地时间加8小时）。最后主档通过SHA256封装校验，修订号80→93。**异常在应用退出保存回调之后、原生日志报告Input System关闭之后、进程退出之前；现有证据不能把它进一步定位为某个OnDestroy回调。**

这是Player，不是Editor。另一个独立Player日志 Native/player1.log 同样包含UNKNOWN和空Managed Stacktrace，配有exit0的原进程结果；该次关闭动作未取得明确人工确认，单独保留，不将其作为已确认正常关闭PASS。原UI-01提交内 ReleaseUI/logs.zip 的两份日志没有此标记，且其清理曾强制终止，不能拿来说明干净退出。Editor夹具日志的 UnityEditor.Search.SearchDatabase ArgumentOutOfRangeException 单列保存，不归因于这次Player关闭。

## 对照与诊断工具

| 运行 | 条件 | 实际结果 |
| --- | --- | --- |
| Native（上轮） | 原正式包、默认D3D12、正常敌人 | UNKNOWN；exit0；关闭动作未核实，非干净PASS |
| NativeEmpty pid23856 | 原正式包、D3D12、合法空遭遇合成布局 | 用户正常关闭，exit0且有退出保存；UNKNOWN；干净关闭FAIL |
| NativeEmpty pid52952 | 同一正式包/同一存档，新进程 `-force-d3d11`，末段附加ProcDump | 用户正常关闭，exit0、无超时、有保存审计，修订96→146；无UNKNOWN；本次干净关闭PASS；恢复断言PASS |
| DX12Repeat pid71364 | 同一正式包、初始同合成档、默认D3D12、不附加监视器 | 用户确认正常点击×；exit0/未超时/quit→before-exit→save；修订4→124；再次UNKNOWN；干净关闭FAIL |
| D3D11Repeat pid62280 | 同一正式包、同初始夹具、D3D11、无监视器 | 600秒未观察退出，timedOut=true / exitCode=null，未强杀；用户随后确认正常关闭，日志无UNKNOWN且有退出审计，但已错过进程退出码观测，不能补写0或计正常退出PASS |

D3D11首次同时改变了图形启动参数，并在关闭前附加诊断监视器，存在干扰变量。后续未附加监视器的D3D11日志也没有UNKNOWN，但它已超时且没有实际退出码，不能按完整正常退出PASS。默认D3D12两次已确认正常点击关闭都出现相同诊断；这些样本提示后端相关性，但不能锁定具体产品/引擎/驱动根因。进一步用相同条件重新取得未附加监视器D3D11的完整退出码，才能评价稳定规避。当前不修改默认Graphics API，不声称已经修复。

本机未找到cdb/windbg；Temp/DefaultCompany与UnityCBMCrashes未找到对应崩溃转储。Windows Application日志只找到该exe的 RADAR_PRE_LEAK_64 / 1001（22:11:25），不是附有故障模块/调用栈的Application Error，不能将它定为关闭根因。

使用微软签名有效的便携ProcDump12.02，仅附加pid52952；未安装全局异常处理器、未使用-i/-k、未强杀。命令、来源/哈希与完整输出保留：

```text
procdump64.exe -accepteula -mm -e 1 -f C0000005,C0000008,C000001D,C0000094,C00000FD -n 3 52952 <isolated-dump-folder>
```

该次输出有运行中已处理的 C++ E06D7363 / wil::ResultException；没有匹配过滤的严重异常转储，最后报告ExitCode0。它不能证明不存在其他异常或定位另一运行的UNKNOWN。完整调用栈仍**不可取得**，不编造栈或故障模块。原始输出及去NUL的阅读副本分开保存，不替换原件。工具用法依据 [Microsoft ProcDump文档](https://learn.microsoft.com/en-us/sysinternals/downloads/procdump)；D3D11是Unity公开的图形启动选项，参见[Player命令行文档](https://docs.unity3d.com/6000.6/Documentation/Manual/PlayerCommandLineArguments.html)。官方其他已知Issue未找到足够匹配证据，不将相似问题作为本项目根因。

## 影响与处理

本次主档校验、修订递增以及同Profile/Run/区域/种子/修复回执/物品ID/库存/来源账恢复已通过。它说明这些合成样本可恢复，不证明全部关闭路径或真实玩家数据绝对安全。正常AI与空遭遇样本均出现过诊断；Editor内部异常独立。字体、Sprite、音效等现有所有权代码已复核，没有足以锁定具体资源的调用栈，因此不试探性删除释放操作或重写生命周期。

新增只读退出分析器在exit0时仍检查原生错误、quit→before-exit→save顺序、主档SHA256和修订递增；恢复比较不修改任一存档。新增可复跑原生启动器要求显式新隔离根和SYNTHETIC夹具，超时仅记录失败，不强杀、不把退出码0直接当PASS。

窗口工具上轮曾报告物理Esc停止；本轮重新初始化后，激活仍连续失败 `failed to activate captured window`，停止重试并请用户协助正常关闭。随后用户只确认已将新窗口切到前台，工具在观察时再次报告物理Esc停止，未取得新的UI截图。这里只记录工具信号，不能据此断言用户实际按下了Esc；本次窗口自动操作已停止，未再发输入。未修改Snipaste/系统快捷键。用户按明确步骤操作不等于未参与者的无提示可理解性检查，F22继续NOT_RUN。

下一步需取得默认D3D12关闭的异常转储/符号栈，或在相同环境/关闭步骤下完成未附加监视器的多轮对照。若仍只有空栈，应提交引擎最小复现并保持UNRESOLVED，不升级引擎来绕过本轮约束。U16剩余原生步骤和F22未完成前，不建议进入B2验收。
