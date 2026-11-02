# CP04-BR2 专项调查交付

基准 `d8fede51ba719060c1d1f719295ce40bb21768d0`；独立分支 `verify/cp04-staff-acceptance-br2`。产品仍是 cc9 的 CombatAim 修复，main 仍为 `72db192a527bd256e2ba18cd7ab334d8334051da`。本文件所在最终提交为复审输入，完整 SHA 由提交后回执给出。不合并 main，不修改产品。

## 结果

|专项|状态|结论|
|---|---|---|
|本机 native 写回路径定位|PASS（限定样本）|匹配 PDB/二进制 + 原生反汇编 + 活体谓词对照，定位构建回调及 CrashReporting/EngineDiagnostics 桥接；未采集硬件写入断点调用栈|
|Bee Services 绑定|PASS|UnityConnect=true、CrashReporting=true、Insights=true；Analytics/PerformanceReporting=false，已按本轮目标输出路径筛选|
|实际外部发送/完整发行行为等同性|UNRESOLVED|标志和发送能力不能证明网络实际载荷、同意状态或所有条件下行为相同|
|Editor 分配来源|PASS|232/232作用域、校准通过，解释2516→4460B的1944B差额|
|非开发测试Player逐调用分配方法|PASS|原生Mono回调在两个独立进程各完成152作用域，正/零/释放引用校准通过|
|CPU数据汇总|PASS（测量整理）|分清单次Solve、整帧和并发；采样模式不同不作速度提升结论|
|实际性能预算验收|NOT_RUN|目标设备/帧率/画质/预算尚未确定，不自行设阈值|
|产品和历史保护|PASS|2329保护文件、889 CP04-B历史文件、848 BR历史文件均无差异；规范化Aim IL也相同|

上述8项为6 PASS（含限定范围）、1 UNRESOLVED、1 NOT_RUN。**不是整体游戏验收通过**。原生UI、人工试玩和历史引擎问题未关闭，旧BR状态不追溯改写。

## 新证据

Unity 6000.6.5f1 安装中有匹配的 Unity_x64.pdb（GUID/age与Unity.dll一致）。`OnEditorBuildStartedStatic` 调用 `UpdateServiceRequestingCoreStats`，根据服务的实际 GetEnabled 与 requiresCore 标志写回聚合 enabled。本样本旧Cloud开关为0，但CrashReporting的原生覆写 getter考虑Engine Diagnostics，返回1，因此请求Core Stats。不是产品CombatAim代码启用云服务。[UnityConnect](UNITYCONNECT.md)

当前1.5m的4460B中：物理API返回数组336B，剩余4124B由闭包、LINQ、排序/迭代相关分配组成。两套独立采集通道结果一致。新增安全检查及最终命中路径解释1944B增量，不删除安全检查来降低分配。[分配分析](ALLOCATION_ANALYSIS.md)

提出单次Solve内复用重叠结果、去LINQ及有界NonAlloc缓冲的量化方案；均**未实施、等待另行授权**。没有改变真实释放、碰撞、伤害、随机流、经济或存档。[性能提案](PERFORMANCE_PROPOSAL.md)

## 运行与边界

- Allocation6：Editor真实产品Solve/公共helper，232作用域完整；不是战斗或人工测试。
- MonoPlayer、MonoPlayerRepeat：BuildOptions.None、测试专用define，两个新进程各152作用域，实际Mono分配事件；不是未插桩纯发行性能。
- 两次纯发行构建均0错/96警告；测试Player构建0错/97警告。全部警告、失败导出、编译缺依赖和预启动占用保留。
- 纯发行程序集没有BR2驱动及UnityEditor引用；测试程序集含BR2MonoProbe和测试原生桥引用。所有CombatAim方法规范化IL与BR纯发行一致，非影子实现。
- 本批没有重新运行完整战斗/原生输入/人工试玩，也不继承旧293PASS为本批PASS。

[验收](ACCEPTANCE.md) · [失败历史](FAILURE_HISTORY.md) · [复跑](TESTING.md) · [证据索引](Evidence/INDEX.md)。交付后暂停等待独立复审。
