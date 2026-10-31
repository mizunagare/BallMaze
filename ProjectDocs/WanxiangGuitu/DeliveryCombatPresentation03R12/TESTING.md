# R1.2 复跑

所有输出必须全新，测试工程/存档在owned I盘根；原50/33脚本不改，使用新目录适配副本，保留数量和断言。

```powershell
$base = 'H:/unity/WanxiangGuitu-CP03-R1/ProjectDocs/WanxiangGuitu'
$tools = "$base/DeliveryCombatPresentation03"
$r12 = "$base/DeliveryCombatPresentation03R12"
$py = 'C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $py "$r12/Legacy/SelfTest-R1-R12.py" --output 'I:/WGCombat/CP03-R1-NEW/Legacy50-Final' --original-root 'I:/WGCombat/CP03-1031-A'
& $py "$r12/Legacy/SelfTest-R11-R12.py" --output 'I:/WGCombat/CP03-R1-NEW/Legacy33-Final'
& $py "$r12/SelfTest-R12.py" --output 'I:/WGCombat/CP03-R1-NEW/ProcessTests-Delivery'
```

预期各exit0、50/33/60 PASS。所有进程schema夹具明示合成，不冒充实际运行。必需负例均检查状态/退出码/JSON/CSV/Markdown及错误原因；API非法字符串类型与CLI布尔语法的控制分开记录。

先按旧入口复制全新隔离 P/Project、检查占用/内存/磁盘，再实际重跑：

```powershell
& "$tools/Invoke-ReviewEditor.ps1" -Project 'I:/WGCombat/CP03-R1-NEW/P/Project' -Output 'I:/WGCombat/CP03-R1-NEW/Editor'
& "$tools/Invoke-Runtime.ps1" -Build 'I:/WGCombat/CP03-1031-A/AcceptanceBuild2/Release' -Output 'I:/WGCombat/CP03-R1-NEW/Runtime' -FixtureSave 'I:/WGCombat/CP03-1031-A/Final2/Game/ForestRuins/save.json'
```

进程预期0，整体仍BLOCKED/2。两包装器只传真实运行器快照和NativeProbe文件，不手工传PASS/0。外层 `exit $LASTEXITCODE` 保留分类码；不强杀超时进程、不抢占桌面。

直接只读分类：

```powershell
& $py "$tools/Receipt.py" --receipt 'I:/WGCombat/CP03-R1-NEW/Runtime/presentation.json' --output 'I:/WGCombat/CP03-R1-NEW/Reaudit' --profile Runtime --contract "$base/DeliveryCombatPresentation03R11/Contracts/Runtime.json" --process-receipt 'I:/WGCombat/CP03-R1-NEW/Runtime/process-results.json' --exit-receipt 'I:/WGCombat/CP03-R1-NEW/Runtime/CP03Runtime.exit.json'
& $py "$r12/Check-RealEvidence.py" 'I:/WGCombat/CP03-R1-NEW' --output 'I:/WGCombat/CP03-R1-NEW/RealEvidenceChecks'
```

第二条创建显式工具断言副本，原真实回执不改；输出不是新Unity运行。源已存在合成副本时拒绝覆盖，整轮用新根。

```powershell
& $py "$r12/Verify-R12.py" 'I:/WGCombat/CP03-R1-1031-C' --output 'I:/WGCombat/CP03-R1-NEW/consistency.json'
```

快速核对本轮已存完整归档预期38 PASS。重新整轮还需Before、保护、输入和语法/锁定审计清单，结构见证据；缺件不能继承旧PASS。正式输入必须有状态、exitCode、timedOut、时间/作用域/命令/原生退出等字段，详细合法性见 [合同](PROCESS_EVIDENCE.md)。缺证或矛盾一律INCOMPLETE/3；有效2UR为BLOCKED/2；有效失败为FAIL/1。

本轮没有新构建、原生UI、人工或Profiler结论。日志原字节留I根，发布只遮盖凭据值并记录原/发布SHA；通过已有LFS上传gzip，不把指针当日志字节。
