from pathlib import Path
p=Path('H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04BR')
(p/'TESTING.md').write_text('''# 复跑与证据解释

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
''',encoding='utf8')
(p/'Evidence/INDEX.md').write_text('''# CP04-BR 证据索引

所有新运行独立保存。发布压缩不是覆盖原件；[manifest](Raw/manifest.json) 记录源文件及发布SHA、大小、脱敏标记。原件根 `I:/WGCombat/CP04BR-1102-A`。原始Profiler data/raw均gzip归档；原始二进制不上传，逐文件哈希清单可核对。

- [保护前清单](Raw/protected-before.json)、[历史清单](Raw/history-before.json)、[保护后](Raw/protection-after.json)。2329+889差异0，Aim完全一致。
- [冷打开](Raw/FixedOpen2/results.json)、[冷build](Raw/FixedBuildAudit/build.json)、[暖纯发行](Raw/FixedWarmPureBuild/build.json)、[修复验收build](Raw/FixedAcceptanceBuild/build.json)、[基线验收build](Raw/BaselineAcceptanceBuild/build.json)。每目录Stages含5文件原字节，Unity.log.gz含完整构建日志。
- [字段diff](Raw/field-differences.diff)、[阶段分析](Raw/build-phase-analysis.json)、[Bee实际services](Raw/bee-services.json)、[IL消费者](Raw/connect-consumer-field.json)、[只读包源码索引](Raw/package-source-audit.json)。
- [程序集剔除/IL](Raw/assembly-audit.json)、[二进制哈希](Raw/binary-manifests.json)、[冷暖对比](Raw/build-comparison.json)。
- [Fixed Editor逐作用域原数据](Raw/FixedScoped/scoped-events.json)、[Baseline](Raw/BaselineScoped/scoped-events.json)、[原Profiler fixed](Raw/FixedScoped/scoped-profiler.data.gz)、[原Profiler baseline](Raw/BaselineScoped/scoped-profiler.data.gz)。各目录command/desktop/exit/Unity.log.gz。
- [配对GC分布](Raw/editor-allocation-analysis.json)、[工具自测10项](Raw/allocation-tool-selftests.json)、[Player测量](Raw/FixedPlayers/PlayerProbe/probe.json)、[Player分析](Raw/player-performance-analysis.json)。
- [本轮Editor293断言](Raw/FixedEditorCore/presentation.json)、[真实进程](Raw/FixedEditorCore/CP03Editor.Run.exit.json)、[Player293断言](Raw/FixedPlayers/PlayerCore/presentation.json)、[Player真实进程](Raw/FixedPlayers/PlayerCore/CP04BRPlayerCore.exit.json)。
- [早期Profiler失败](Raw/FixedEditorProbe/profiler.raw.gz)、[reader失败](Raw/profiler-reader-failure.json)、[基线15分钟失败](Raw/BaselineEditorProbe/exception.txt)、[编译失败窗口](Raw/scoped-window-inventory.json)、[基线Player中断](Raw/BaselinePlayers/PlayerProbe/interruption.json)。不因普通关闭exit0改成PASS。
- [硬件](Raw/hardware.json)、[原生空表](Templates/native-input.csv)、[人工空表](Templates/human-playtest.csv)。空白表不是已执行结果。

旧 CP04-B 原数据仍在原交付目录，本批只读，不重复发布成新结果。所有分类与 [ACCEPTANCE](../ACCEPTANCE.md) 对齐。
''',encoding='utf8')
print('testing/index written')
