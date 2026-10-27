# BUILD-01 复跑

在 Windows PowerShell 7、本机 Unity 6000.6.5f1 与既有私有非活动桌面 worker 下执行。无需人工点击；不切换桌面、不改系统设置、不关闭已有 Unity。所有根必须工程外、非 LocalLow、全新拥有者目录。

```powershell
Set-Location D:/unity/WanxiangGuitu
& ./ProjectDocs/WanxiangGuitu/DeliveryBuild01/Test-Preflight.ps1 -TestRoot D:/WGB01
& ./ProjectDocs/WanxiangGuitu/DeliveryBuild01/Invoke-Diagnostic.ps1 -Case Long -LongProjectLength 113 -TestRoot D:/WGB01
& ./ProjectDocs/WanxiangGuitu/DeliveryBuild01/Invoke-Diagnostic.ps1 -Case Short -TestRoot D:/WGB01
& ./ProjectDocs/WanxiangGuitu/DeliveryBuild01/Invoke-Diagnostic.ps1 -Case Repeat -TestRoot D:/WGB01
```

`WorkerFrom` 默认引用此前已核对的 INPUT-01 完整 All 所有者根；迁机需传入本机已审计的同类根，其 owner.source 必须与当前 SourceProject 一致。不存在有效 worker 时失败，不回退到活动桌面。

Long 是故意复现错误的诊断案例，不是建议配置。113 是本机历史项目前缀字符数，目标最终绝对路径 260；必须以 `asset-before.pathLength` 为准，不凭参数断言已经达到边界。251 字符探索对照使用了 `LongProjectLength 104`，属于修复前额外样本，仍可能令其他深层包导入失败。

每次入口复用现有协调器的 Step、超时、进程状态与真实退出码记录。每项 Unity 上限 1200 秒，超时保留进程并停止依赖；不会强杀并宣称正常退出。复制入口使用原 Invoke-Rules PrepareOnly，再将 `.cs.txt` 诊断源注入该独立工程 Editor 目录。所有构建调用现有 WanxiangBuild 的同一 Build 实现，BuildOptions.None。没有手工修改包、重置项目设置或过滤消息。

先检查 `results.json` 的工具执行结果，再检查 `Results/build-report-messages.json` 的真实计数和 `asset-before.json`。诊断案例进程 exit 0 仅表示取证完成，2 Error 的质量仍为 FAIL。不能只看协调器或 Unity 退出码。

只读审计及发布命令：

```powershell
$py = 'C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONUTF8 = '1'
& $py -B ./ProjectDocs/WanxiangGuitu/DeliveryBuild01/audit_inputs.py --source D:/unity/WanxiangGuitu --out '<新拥有者根>'
& $py -B ./ProjectDocs/WanxiangGuitu/DeliveryBuild01/collect_results.py --root D:/WGB01 --evidence '<本次全新发布目录>'
```

只在所有待采集进程结束后采集。collector 只复制回执、源码、日志、完整 BuildReport JSON 与产物哈希，不复制 Player 二进制、Library 或存档。外部根完整产物及 LastBuild.buildreport 原地保留，不清理历史根。每次实验的实际完整命令、UTC 时间、超时和退出码在对应 Runs 目录。

预检规则以锁定版本的具体深层 USS/UXML/URT 路径计算预算；不是全包普适路径证明。若改变 Unity/包版本需重新审计。不要通过开全局长路径、缩小日志、删包或改导入器取得绿色结果。普通 All 的 TestRoot 默认已改短，也可以显式传入短根；过长自定义根会在复制/导入前明确拒绝。

本批没有启动最终 Player、原生 UI、正常 AI、人工试玩或完整 All；不以它们的历史结果填补本轮证据。
