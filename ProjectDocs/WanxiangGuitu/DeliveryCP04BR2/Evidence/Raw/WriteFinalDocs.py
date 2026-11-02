from pathlib import Path
p=Path('H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04BR2')
(p/'ACCEPTANCE.md').write_text('''# CP04-BR2 验收

专项调查交付完成，不宣称整体发行风险或性能验收通过。8项：6 PASS（限定测量/定位范围）、1 UNRESOLVED、1 NOT_RUN。

|项|状态|证据/边界|
|---|---|---|
|本机native写路径及触发服务定位|PASS|[身份](Evidence/Raw/native-identity.json)、[反汇编](Evidence/Raw/native-disassembly.json)、[原生getter](Evidence/Raw/ConnectControlBuild/Connect/001.json)；没有硬件写栈|
|Bee三项及Analytics区别|PASS|[明确DestinationPath](Evidence/Raw/bee-services-current.json)、[消费IL](Evidence/Raw/bee-services-il.json)|
|实际外部发送、同意及完整发行行为|UNRESOLVED|未抓取运行时请求/载荷，不从标志推断无影响|
|Editor分配来源和增量|PASS|[232作用域](Evidence/Raw/Allocation6/scoped-events.json)、[分解](Evidence/Raw/allocation6-analysis.json)|
|非开发测试Player方法有效性|PASS|[进程A](Evidence/Raw/MonoPlayer/mono-probe.json)、[进程B](Evidence/Raw/MonoPlayerRepeat/mono-probe.json)，各152作用域且独立校准|
|分层CPU汇总/量化提案|PASS|[数据](Evidence/Raw/cpu-current.json)、[提案](PERFORMANCE_PROPOSAL.md)；不是性能达标或优化已实现|
|性能预算验收|NOT_RUN|未获目标硬件、目标帧率、负载和预算，不自行设阈值|
|源输入/用户/历史保护|PASS|[2329+889+848保护](Evidence/Raw/protection-and-il.json)，Aim源码和规范化IL均一致|

新执行记录：Editor Allocation5 224/224、Allocation6 232/232；两个Player各152；离线工具自测12PASS。采样作用域不是游戏功能用例，不能与历史293PASS混算。

两次纯发行0errors/96warnings，非开发测试构建0errors/97warnings；[原始build](Evidence/Raw/ConnectBuild/build.json)、[control build](Evidence/Raw/ConnectControlBuild/build.json)、[probe build](Evidence/Raw/MonoBuild/probe-build.json)。纯发行无BR2驱动/原生桥引用，probe明确含测试驱动，见[桥依赖](Evidence/Raw/native-bridge-audit.json)。

未执行：无采集器纯发行逐Solve测量、完整并发战斗新基准、GPU专项、原生输入、人工体验。历史BR构建等同性、D3D12 UNKNOWN、Editor问题及所有旧失败不因本轮定位而被改写。产品优化方案待单独授权，本轮没有实施。
''',encoding='utf8')
(p/'FAILURE_HISTORY.md').write_text('''# 失败、修正与未执行项

旧CP04-B/BR证据均只读。新输出独立目录，不用后续成功覆盖失败。

|尝试|原始结果|处理|
|---|---|---|
|Allocation|缺CP03Cases辅助类，CS0103，Safe Mode|保留Unity.log/编译窗口；补齐现有辅助类。只普通关闭身份核对的自有测试对话框，不算原生验收|
|Allocation2|重启时旧进程尚未结束，预启动占用阻断|未启动第二个Unity，不强杀；等旧进程退出后另开Allocation3|
|Allocation3|进程0但仅56/224 raw作用域|INCOMPLETE，不采信工具旧的“有样本即成功”；完整Profiler原件也归档|
|Allocation4|进程1、140/224作用域|INCOMPLETE；采样同时导出导致导出器自身被分析，帧保留窗口不足；不作为有效配对|
|Allocation5|224/224，控制有效|采集和解码分离，停止Profiler后读取原始metadata/调用栈，另开目录保留旧失败|
|Allocation6|232/232，控制有效|新增8条旧fallback方向公共helper测量，解释532B剩余差额；未改旧Solve|
|native符号工具|非零模块基址并成功枚举；GetLastError遗留487|成功API后last-error不定义，不把该旧值当加载失败；另用PE/PDB GUID/age核验匹配|
|接口清点|首次查询不存在ProfilerModule.dll|实际API位于CoreModule，清点失败不是测量0|
|托管服务查询|首个PowerShell查询未执行成功|以FindManagedServices.ps1重跑，保存明确IL，不猜测结果|
|服务触发假设|最初怀疑普通Insights getter直接为true|实际getter为0，已否定；CrashReporting覆写getter为1，进一步读取EngineDiagnostics/旧Cloud字段定位桥接|
|Bee缓存归属|初始宽泛glob包含继承cache，并以所在工程标签归类|保留初始inventory但不能用于构建身份；以DestinationPath精确匹配本轮输出，另写current文件|
|构建与关闭日志|obsolete、JobTempAlloc等警告|原日志全保留，不过滤、不降低断言、不试探修改产品生命周期|

[初始编译日志](Evidence/Raw/Allocation/Unity.log.gz)、[窗口](Evidence/Raw/compile-window.json)、[56/224](Evidence/Raw/Allocation3/scoped-events.json)、[140/224](Evidence/Raw/Allocation4/scoped-events.json)、[完整原Profiler](Evidence/Raw/Allocation3/scoped-profiler.data.gz)、[缓存归属纠正](Evidence/Raw/bee-cache-inventory-note.json)。

原生写入硬件调用栈、真实网络载荷/同意行为、未插桩发行完整性能、原生输入和人工体验没有执行。旧D3D12等未解决项保持原状。所有新工具只在隔离环境中运行；没有产品修复或历史结果重分类。
''',encoding='utf8')
(p/'TESTING.md').write_text('''# 复跑说明

原根`I:/WGCombat/CP04BR2-1102-A`已冻结，不复用输出目录。源码工作树`H:/unity/WanxiangGuitu-CP04`，产品输入来自BR冻结版，用户工程只读。新建工程外唯一根、owner标记与合成输入；禁止指向真实存档或用户项目。

## 输入与入口

复用现有`DeliveryEncounterAI01/Invoke-Check.ps1`及其NativeProbe私有桌面运行器。实际版本副本/命令/desktop/exit/日志都在Evidence/Raw。把Tests的Editor工具复制到隔离工程Editor目录；补全已有B06LocalChecks及其CP03Cases依赖。工具只在隔离副本临时Assets里，仓库产品Assets不变。

- `BR2Allocation.Run`：真实产品Solve和公共helper，正/零/释放校准；采集期间不解码，关闭Profiler后导出，避免自分析反馈。最终232条完整，旧224条完整和失败输出都保留。
- `BR2Connect.Pure`：记录实际native只读状态、BuildPipeline阶段和纯发行BuildReport；不调用设置setter。
- `BR2Connect.Open`：干净副本不Build的对照，以及构建后只读getter审计。
- `BR2ProbeBuild.Run`：BuildOptions.None + CP04BR2_PROBE；不同于纯发行。
- `Invoke-MonoPlayer.ps1 -Output <新建BR2目录>`：启动测试Player，不注入键鼠或业务结果，默认固定本批build路径，复跑需明确调整到新副本。

命令形式：

```powershell
& <existing>/DeliveryEncounterAI01/Invoke-Check.ps1 -Project $isolatedProject -Output $freshOutput -Method BR2Allocation.Run -NonBatch
```

每次独立输出，不覆盖。Tools测试目录不等于可单独打开的完整Unity项目；缺依赖时必须记录失败，不能把空结果当成功。

## 原生桥

`Tests/BR2AllocationNative.cpp.txt`使用本机Mono导出，不链接Unity产品源码。实际cl命令和日志见Raw/Native、native-compile.log.gz；MSVC14.51.36231、SDK10.0.26100.0仅用于测试工具，无Unity/包升级。DLL不放正式产品Assets：测试驱动受CP04BR2_PROBE保护，引用工程外的测试DLL绝对路径；复跑应把常量路径调整为新根并重新编译测试副本。

两个进程各独立BR2Init/Begin/End/Stop及校准。若导出缺失、启用失败、正控未响应、零控分配或size非法，字节结论不能PASS。不要改CombatAim来迎合采样。

`ValidateEvidence.py`针对完整导出及12个正负例做离线校验。`AnalyzeAllocation.py`和其他诊断脚本固定到本批根，作为执行记录；复跑需显式换新根。它们不能代替Unity真实采样。

## 原生符号与风险

只读本机Unity.dll/PDB，经GUID/age/hash匹配后才解释地址。ReadSymbols/Disassemble/Lookup工具源在Raw；capstone5.0.6与pefile2024.8.26安装到独立PythonLib，不改工程依赖。BR2Connect的对象偏移/虚表调用仅适用已核验Windows x64二进制，不跨版本执行，不作通用产品API。

未启动WPR全局录制、未暂停用户程序、未模拟物理输入。超时不强杀；若采样缺失保留原件并标INCOMPLETE/NOT_RUN。纯发行/测试Player/Editor/原生输入/人工测试分开报告。

## 交付校验

核对产品/用户与CP04-B/BR历史哈希；核对纯发行无BR2类型及原生桥引用、probe存在预期驱动、所有CombatAim方法规范化IL一致。发布manifest逐文件原SHA/发布SHA；gzip仅传输压缩，日志若有凭据只移除凭据值并标记，不过滤错误。原始运行副本仍在唯一根。

最终只推verify/cp04-staff-acceptance-br2；main、CP04-B、BR不合并、不重写。推送后再读完整远端SHA。
''',encoding='utf8')
print('acceptance/history/replay written')
