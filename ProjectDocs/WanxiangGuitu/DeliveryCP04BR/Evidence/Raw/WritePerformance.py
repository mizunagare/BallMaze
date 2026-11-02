from pathlib import Path
import json
p=Path('H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04BR');r=Path('I:/WGCombat/CP04BR-1102-A');g=json.loads((r/'editor-allocation-analysis.json').read_text())
text='''# GC 与 CPU 测量

完整 Player 逐 Solve 字节指标 **NOT_RUN**，不是零。Editor 逐作用域采样已校准，有效范围如下。

## 接口与校准

Unity 6000.6.5f1 / Mono v4.0.30319、64位。GC.GetAllocatedBytesForCurrentThread 在已知 new byte[65536] 下仍返回0，判定不可信。ProfilerRecorder GC.Alloc 的 Value 是 TimeNanoseconds，不是字节；非开发 Player 甚至 recorder 不可用。Physics Queries 的同步 CurrentValue 无法反映已知 Raycast/OverlapSphere/SphereCastAll 控制，查询数 NOT_RUN，不解释成0。

可靠 Editor 方法：ProfilerDriver.profileEditor + RawFrameDataView 在唯一 BRScoped.NNNN 样本的递归子节点中读取 GC.Alloc metadata[0]。它是实际已编译 CombatAim.Solve，未放影子实现，未改 Aim 插桩；委托和记录数组在作用域外创建。场景是独立、可复现的物理夹具，输入复用 CP04-B 实际骨骼发射点，**不是实时动画、实际发射或人工场景**。完整战斗功能另测。

每版本8次空操作、8次正分配、8次释放引用，再4距离各32次Solve（各16次预热）。正控均65568B；空和释放控均0。释放引用是负向控制，不期望“负分配”；GC.Collect在作用域外。152条 marker 与152条raw样本唯一对应，错误0。未用整帧GC减法推导Solve。

依据：[RawFrameDataView](https://docs.unity3d.com/cn/current/ScriptReference/Profiling.RawFrameDataView.html)、[metadata API](https://docs.unity3d.com/ja/6000.0/ScriptReference/Profiling.RawFrameDataView.GetSampleMetadataAsLong.html)、[Recorder options](https://docs.unity3d.com/cn/6000.0/ScriptReference/Unity.Profiling.ProfilerRecorderOptions.html)。原始 profiler.data 压缩归档与导出逐调用事件一并保留。

## Editor 配对结果

同硬件、同几何、同预热/采样配置，顺序运行。表中距离是夹具玩家至目标位置，不等于枪口到表面距离；0.35m修复版仍返回防倒射拒绝原因，此处不宣称极近命中通过。

|版本|距离 m|n|字节 min/median/max|CPU median / p95 μs|
|---|---:|---:|---|---|
'''
for version in ['Baseline','Fixed']:
 for x in g[version]['groups']:text+=f"|{version}|{x['distance']}|{x['n']}|{x['bytesMin']}/{x['bytesMedian']:g}/{x['bytesMax']}|{x['cpuNsMedian']/1000:g} / {x['cpuNsP95']/1000:g}|\n"
text+='''
[完整校准与分布](Evidence/Raw/editor-allocation-analysis.json)、[Baseline逐调用](Evidence/Raw/Baseline-solve-allocations.json)、[Fixed逐调用](Evidence/Raw/Fixed-solve-allocations.json)。1.5m新安全检查路径比旧提前拒绝路径更多工作，不是同一语义的优化对照。采样有Profiler开销，无未插桩CPU预算结论；没有通过任何产品改动消除分配。

## 非开发 Player

修复版实际真实释放后采样128次Solve，CPU中位数：0.35m 68.55μs、1.5m 96.55μs、6m 79.55μs、20m 69μs；各n32。同步字节计数正控失败、GC recorder UNAVAILABLE，字节全部NOT_RUN，不能填0。

实际并发攻击6模拟秒（720帧）：13次Spawn、峰值5枚，Main Thread正样本中位数3.2152ms；这是整帧并发负载上下文，不能作为逐Solve CPU/GC。真实初始命中33点伤害，Flight3590条、sweep-contact1、resolved1。详细 [player-performance-analysis](Evidence/Raw/player-performance-analysis.json)、[原始probe](Evidence/Raw/FixedPlayers/PlayerProbe/probe.json)。

基线非开发Player出现缺失脚本警告、未完成probe，已用普通WM_CLOSE中断自己的隔离进程。其退出0不是测量成功。基线Player CPU、字节与配对并发比较NOT_RUN，原因未确认，不归咎于产品。无有效GPU、显存或准确逐Solve物理查询数据，不报告性能优良。

## 已知工具风险

早期play-mode profiler捕获532MB但无法LoadProfile；之后基线play-mode15分钟有界超时；错误API导致独立隔离副本Safe Mode，修工具后另开运行目录；均保留。成功 edit-mode 原始 profiler 文件约771/776MB，gzip只作传输，未改变样本。没有用这些工具失败覆盖历史CP04数据。

[失败历史](FAILURE_HISTORY.md)。下一步如必须取得发行Player逐调用分配字节，需要能可靠正校准且提供分配大小的独立事件通道；不修改CombatAim来迎合测量，也不以Editor字节外推Player。
'''
(p/'PERFORMANCE.md').write_text(text,encoding='utf8')
(p/'ACCEPTANCE.md').write_text('''# CP04-BR 验收

整体 **BLOCKED**；七分项3 PASS（CPU仅有限测量）、3 NOT_RUN、1 UNRESOLVED。退出码、断言和整体验收分开，不以编排器0覆盖缺失。

|项|状态|证据|
|---|---|---|
|五文件逐字段/阶段审计|PASS|[阶段](Evidence/Raw/build-phase-analysis.json)、[字段](Evidence/Raw/field-differences.json)|
|构建输入行为等同性（必需）|UNRESOLVED|[构建报告](BUILD_INPUT_AUDIT.md)，native开关及最终数据等价未证明|
|Editor分配校准/真实Solve|PASS|[校准](Evidence/Raw/editor-allocation-analysis.json)，两版本各152作用域|
|非开发Player逐Solve字节|NOT_RUN|[原始控制](Evidence/Raw/FixedPlayers/PlayerProbe/probe.json)，不能采信0|
|GC Alloc完整要求|NOT_RUN|Editor有效，Player必需项未完成|
|CPU有限实测|PASS|[性能](PERFORMANCE.md)，不代表性能预算通过|
|基线Player/修复Player配对CPU与并发|NOT_RUN|基线missing-script，无完成回执|
|准确逐Solve查询次数|NOT_RUN|已知查询控制失败，未用静态估计冒充|
|本轮Editor功能|PASS|[presentation](Evidence/Raw/FixedEditorCore/presentation.json)，293PASS、exit0、未超时|
|本轮非开发验收Player功能|PASS|[presentation](Evidence/Raw/FixedPlayers/PlayerCore/presentation.json)，293PASS、exit0、未超时|
|纯发行构建/驱动剔除|PASS|[程序集](Evidence/Raw/assembly-audit.json)，纯发行0errors96warnings|
|原生输入|NOT_RUN|[脚本](NATIVE_INPUT.md)，无物理操作|
|人工体验|NOT_RUN|[空表](HUMAN_PLAYTEST.md)，无独立试玩者结果|
|冻结Aim/用户/旧证据|PASS|[保护](Evidence/Raw/protection-after.json)，2329+889，差异0|

上述明细是独立检查，不能与七分项或586功能断言混算。历史UNRESOLVED不追溯修改；自动化不是人工体验。
''',encoding='utf8')
(p/'FAILURE_HISTORY.md').write_text('''# 失败与未完成历史

所有原始文件保留，成功重跑没有覆盖旧目录。外层进程0只说明退出，不将中断或缺失语义证据变为PASS。

|尝试|实际结果|处理/剩余|
|---|---|---|
|FixedOpen|未启动Unity，缺B06LocalChecks|保留tool-failure-01；补全现有helpers，另跑FixedOpen2|
|FixedEditorProbe|进程0；线程正分配返回0；GC字节未取得|保留probe与profiler.raw；只承认CPU/原始事件数，不承认字节|
|ReadFixedProfile|LoadProfile=false，Deserializer error，后等待无进展|只关闭已核对的隔离Editor，reader-cleanup；不是Player/native验收|
|Cleanup helper --no-restore|NETSDK1004缺assets文件|保留tool-failure-02；源文档目录误生成的两项ignored obj文件核对创建时间/SHA后移入ToolGeneratedRecovery，不删旧文件|
|BaselineEditorProbe|实际exit1，15分钟有界deadline|原exception/log不改；后独立BaselineScoped成功，不覆盖此失败|
|FixedEditorProbe2|工具CS0117：SetProfilingEnabled不可访问；Safe Mode|保存Unity.log与窗口清单；精确自有隐藏对话框普通关闭。exit0只是清理，不是测量成功|
|首两次关闭助手|Add-Type用法错误 / 跨desktop句柄不匹配 / attach failed|没有发送输入；独立新进程附加自有非活动desktop后才发送WM_CLOSE，safe-mode-normal-close2保留|
|BaselinePlayers/PlayerProbe|缺失脚本警告，无probe；普通关闭中断|进程0不能证明运行成功；性能NOT_RUN，根因未确认，不归因游戏|
|AnalyzeInputs / AnalyzeBuild|Python默认GBK解码错误|改工具显式UTF-8，未改输入|
|Protect首次|历史清单schema假定fullPath，KeyError|修工具按已存在path读取，再核验全部2329+889|
|所有build/运行警告|URP stripping、JobTempAlloc等|完整BuildReport/Unity.log保留；未批量修复、未过滤成PASS|

[原始目录](Evidence/Raw/)、[发布清单](Evidence/Raw/manifest.json)。错误命令可由当前聊天工具记录与原始日志核查；部分早期工具源码在本批开发中迭代，未保存逐次完整源码快照，不能宣称每个失败均有冻结源码包。保留的原始错误日志与输入哈希不改写。

CP04-B旧889项哈希一致；原法杖两项历史失败、CP03旧失败及D3D12 UNKNOWN不变。没有新增授权产品修复。
''',encoding='utf8')
print('performance/acceptance/history written')
