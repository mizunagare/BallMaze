# 复跑说明

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
