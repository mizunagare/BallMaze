# 复跑与证据解释

只在新建工程外唯一根运行，示例原根 `I:/WGCombat/CP04BR-1102-A` 已冻结，不复用、不覆盖。源工作树 `H:/unity/WanxiangGuitu-CP04`，用户工程只读。每个命令记录实际进程回执与独立输出。

## 输入准备

从 cc9 产品复制 Assets/Packages/ProjectSettings 到 Fixed/Project；Baseline 同一输入仅以 main72 的原始 CombatAim.cs 替换该独立副本。保留用户改动于用户原工程，不带入测试。记录全部输入哈希；不要把工作树用户场景变更当成发布输入。

复用 `DeliveryEncounterAI01/Invoke-Check.ps1`，完整复制原 B06LocalChecks 依赖，排除 CP04B 前缀 shadow helper。把 Tests 的 BRStages、BRScopedEditor 放隔离工程 Editor 目录；BRProbe、BRPlayer、CP03Cases 放隔离工程 BRValidation。运行时三者均由 `UNITY_EDITOR || CP04BR_ACCEPTANCE` 保护，纯发行剔除。保存当前 Tests 对应文件和哈希。BRProbeEditor.cs.txt 是保留的早期失败工具版本，正式逐调用重跑使用 BRScopedEditor.Run，不执行该旧入口。

## 实际入口

```powershell
# $project/$output 均指新建的隔离路径；禁止指用户工程/真实档。
& <existing>/DeliveryEncounterAI01/Invoke-Check.ps1 -Project $project -Output $output -Method BRBuildAudit.OpenOnly -NonBatch
& <existing>/DeliveryEncounterAI01/Invoke-Check.ps1 -Project $project -Output $output -Method BRScopedEditor.Run -NonBatch
& <existing>/DeliveryEncounterAI01/Invoke-Check.ps1 -Project $project -Output $output -Method BRBuildAudit.Pure -NonBatch
& <existing>/DeliveryEncounterAI01/Invoke-Check.ps1 -Project $project -Output $output -Method BRBuildAudit.Acceptance -NonBatch
& <existing>/DeliveryEncounterAI01/Invoke-Check.ps1 -Project $fixedProject -Output $output -Method CP03Editor.Run -NonBatch
```

每行需不同新目录；以上省略准备的 B06 helpers 不是独立可编译项目。`Invoke-Watched.ps1` + `WatchInputs.py` 外部只读监视五文件，spec/实际命令保留于证据。`Invoke-Players.ps1` 用私有非活动桌面及不可变 seed418 合成档副本，显式 `-br-acceptance`，Probe/Core 分组；属于受控 API，不是原生输入。副本 owner、fixture-copy、command、desktop-process、exit与日志均应保留。

四种有效构建的 BuildOptions.None 含义区分：Pure 无 acceptance define，Acceptance 有测试驱动。不得以验收 Player 代替纯发行类型剔除检查。Audit-Assemblies.ps1 只读 Cecil 检查真实编译程序集及Solve IL。

## 验证工具

`ValidateAllocation.py <fixed scoped-events.json> <baseline scoped-events.json> <fresh output.json>`：本轮真实导出正控两项、负例八项，10PASS；只验证导出归属和校准条件，不冒充 Unity 新采样。原始 GC metadata 的来源、作用域和局限见 PERFORMANCE。

当前诊断分析脚本固定到本轮唯一根，作为实际执行记录保留于 Evidence/Raw；复跑要明确改到新根，不能覆盖本轮。Publish.py 仅整理本轮所有原始日志与Profiler，日志可能移除凭据值，manifest记录原SHA/发布SHA与redacted；gzip无其他语义变化。原始文件保留本机。

超时不强杀；保留当前进程/命令。仅对身份完全核对、属于本任务且已失败的隔离进程可普通关闭。原生/人工按各自协议等待真人；不恢复用户键位，不激活私有desktop。
