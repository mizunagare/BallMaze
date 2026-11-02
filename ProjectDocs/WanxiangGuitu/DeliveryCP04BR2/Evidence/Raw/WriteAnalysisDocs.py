from pathlib import Path
p=Path('H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04BR2')
(p/'ALLOCATION_ANALYSIS.md').write_text('''# 分配来源与非开发Player采集方法

## 当前有效采样

- Editor Allocation6：232/232唯一作用域，错误0。8正控均65568B（65536字节内容+对象开销），8零控和8释放引用控均0；4距离各32次真实产品Solve，10种公共helper/API各8次。
- MonoPlayer及MonoPlayerRepeat：两个独立非开发测试进程，各152作用域，同样正/零/释放引用控制通过。nativeInit=1，无非法size事件；每距离各32次真实产品Solve。
- 校验器自测12PASS（含截断、重复marker、正控失败、零控失败、原生接口未启用等负例）。这是工具自测，不计作游戏功能PASS。

[Editor原始样本/调用栈](Evidence/Raw/Allocation6/scoped-events.json)、[分解](Evidence/Raw/allocation6-analysis.json)、[Player](Evidence/Raw/MonoPlayer/mono-probe.json)、[独立新进程](Evidence/Raw/MonoPlayerRepeat/mono-probe.json)、[自测](Evidence/Raw/validation-selftests.json)。

## 1.5m 的 1944B 增量

同BR物理夹具：真实产品CombatAim.Solve；发射点复用CP04-B的实际骨骼采样，目标为同一胶囊，侧置相机(5,4,-5)，输入世界坐标完整保留。此处是重放输入的物理测试，不是角色实际释放或人工体验。

|组成|旧路径B|当前路径B|依据|
|---|---:|---:|---|
|Solve本层相机射线及LINQ|756|756|当前调用栈；旧分支前源码相同|
|InitialContact|2×656=1312|3×656=1968|当前实际公共helper各8次|
|枪管Sweep|224|224|同一helper实测|
|新增安全Sweep|0|756|当前guard helper实测|
|最终Sweep|224|756|旧camera方向helper224；当前指向真实表面helper756|
|总计|2516|4460|与BR旧完整Solve历史采样、BR2完整Solve实测分别一致|

增加量=656+756+(756-224)=**1944B**。旧完整Solve数字是BR冻结历史，不假称本轮重新运行旧产品；本轮单独执行未改动公共Sweep、使用旧fallback方向的helper，并未实现影子Solve。guard增加了真实检查；最终扫掠从旧方向未接触到当前方向实际接触，产生不同数组和排序成本。

当前完整Solve按首个产品栈帧归属：Solve本层756B、InitialContact合计1968B、Sweep合计1736B。物理返回数组合计336B（RaycastAll80、OverlapSphere3×32、非空SphereCastAll2×80），其余4124B落在闭包/委托、Where/OrderBy/ThenBy、迭代器、sorter、key/map/buffer等相关栈。InitialContact本夹具656B中仅32B是OverlapSphere数组；其余624B是包装/查询逻辑相关分配。

这是固定目标密度样本，不是森林最坏情况上界；All查询结果随Collider数量增长。不能通过删掉guard、忽略墙体或改变距离来优化。

## AimPreview 调用频率

`AdventureCombat.LateUpdate`先AdvanceAttacks；当本帧释放时复用LastReleaseAim，否则远程武器且Ready时调用一次Solve。Release对一次远程动作计算一次Solve，弓多箭复用该解，不是每箭Solve；HUD只读AimPreview，不再Solve。

因此静态频率是：每个启用的AdventureCombat，**每个符合条件的非释放LateUpdate一次 + 每次实际远程释放一次**；释放帧不再额外做预览。若同帧多个释放则按实际释放次数计算。Ready会检查死亡、菜单/暂停、翻滚、焦点、UI屏障、关闭界面当帧等。待机远程且Ready也会每帧计算，非只有攻击时才分配。

[源码行号/哈希](Evidence/Raw/frequency-source-audit.json)。没有采集真实玩家会话的逐秒预览频率，不把刷新率当成现场测量。只作算术：若每秒F个符合条件预览，则本夹具约4460F B/s，增量1944F B/s；F=60时267600B/s、F=120时535200B/s。这两个F不是目标帧率或预算。Projectile自身的Overlap/碰撞、UI、声音等分配另计，不含在Solve样本中。

## 非开发Player方法

旧线程字节接口正控返回0、ProfilerRecorder不可用的历史结论保留。新方法不依赖它们：隔离测试专用C++桥注册Mono gc_allocation回调，调用实际mono_object_get_size；thread_local标记仅统计Begin/End之间的当前线程。回调本身无托管回调、无heap分配；结束后移除自己的callback。仅使用当前Mono导出的接口，不写或替换CombatAim。

两个进程正控均1事件/65568B、零控0；真实Solve四距离字节中位数分别2180、4460、3048、3048，与独立Editor metadata通道一致。原生DLL、Mono模块和程序集SHA已记录；所有CombatAim方法规范化IL与BR纯发行相同。

[桥源码](Tests/BR2AllocationNative.cpp.txt)、[测试驱动](Tests/BR2MonoProbe.cs.txt)、[导出接口](Evidence/Raw/mono-exports.json)、[运行时身份](Evidence/Raw/runtime-identity.json)、[驱动剔除](Evidence/Raw/native-bridge-audit.json)、[IL一致](Evidence/Raw/protection-and-il.json)。API声明依据Mono公开MIT接口：[profiler.h](https://raw.githubusercontent.com/mono/mono/main/mono/metadata/profiler.h)、[allocation事件](https://raw.githubusercontent.com/mono/mono/main/mono/metadata/profiler-events.h)。不是将上游实现等同本机：本机导出检查及两次实际校准才是有效性依据。

限制：当前仅Windows x64/Mono；IL2CPP或缺少导出时必须NOT_RUN。测试构建BuildOptions.None但有CP04BR2_PROBE和外置桥，**不是未插桩纯发行性能**。启用Mono分配事件会有开销；没有测得采集器的完整CPU开销，不据此判断优化效果。反复校准失败或size事件异常必须停止字节结论。

## 量化优化提案（未实施）

1. 单次Solve内复用guard已取得的同origin重叠结果，保持真实释放仍全新Solve：本样本可省一次656B检查，规划值4460→3804B。需要先验证同次调用中的世界状态/自动同步合同，不能跨帧缓存代替新鲜遮挡查询。
2. 用保留距离、Priority和原始索引稳定tie规则的选择逻辑替代LINQ链：本样本4124B为相关分配的量化机会，物理数组336B仍在。336B是样本估算剩余，不是实现后保证。
3. 再评估有界NonAlloc缓冲。溢出必须完整fallback，不截断候选；NonAlloc与All的相等距离顺序也须配对证明。上下文所有权、重入、多英雄/场景和清理需设计，不新增v9字段。
4. 降低跨帧预览刷新属于可见性/延迟变更，暂不优先；任何方案不能复用旧预览作为实际释放解。

以上均等待产品修改授权，没有实施或宣称零分配。未来必须覆盖原24组发射点/方向、近距/墙体/初始重叠/密集Collider/饱和fallback、四武器、暂停、换武器、死亡及场景清理，并重新正/零校准。
''',encoding='utf8')
(p/'PERFORMANCE_PROPOSAL.md').write_text('''# 性能数据与预算提案

## 硬件和配置

本机i5-12400F、6核12线程、约48GB可见内存、RTX3060，Windows11 10.0.26200。Player日志确认D3D12、驱动32.0.16.1742、12113MB显存。驱动报告的App VRAM Budget不是本项目批准的显存预算。机器还装有虚拟显示适配器，不由库存列表推断实际渲染GPU。

[硬件](Evidence/Raw/hardware.json)、[实际Player日志](Evidence/Raw/MonoPlayer/Player.log.gz)。请求1280×720私有非活动桌面；未另外采集本轮运行时画质、VSync、实际客户区与电源状态，因此不能宣称严格全场景同条件性能基准。

## 单次Solve CPU（μs中位数，各距离n32）

|运行|0.35m|1.5m|6m|20m|口径|
|---|---:|---:|---:|---:|---|
|BR历史Editor基线|64.3|68.0|72.9|70.95|历史Profiler采样，不是本轮重跑|
|BR历史Editor修复|68.4|81.65|73.15|72.15|历史同组对照|
|BR历史修复Player|68.55|96.55|79.55|69.0|历史逐帧测试驱动|
|BR2 Editor|244.4|467.7|324.45|363.2|开启分配调用栈，有显著工具开销|
|BR2非开发测试Player A|10.15|10.15|7.35|10.8|原生分配回调，集中在一帧的重复查询|
|BR2非开发测试Player B|9.5|14.85|10.65|9.25|独立新进程，方法相同|

[本轮min/p95/max](Evidence/Raw/cpu-current.json)、[带原始SHA的历史引用](Evidence/Raw/br-reference-measurements.json)。工具、采样时机和场景负载不同，**不能把表中较小数字称为产品提速，也不能把Editor较大数字称为产品退化**。产品Aim源码/规范化IL未改变。

## 整帧与并发

BR历史修复Player的6模拟秒/720帧负载，最大5枚并发弹体、13次Spawn，Main Thread中位数3.2152ms。该数据是整帧上下文，不是单次Solve；本轮没有重新跑该并发负载，也没有继承其PASS。

本轮只采集函数局部CPU和分配。没有新的完整冒险、复杂森林、持续战斗、场景切换全帧分布或无采集器对照，GPU帧时间/显存使用/整帧GC也未取得。它们均NOT_RUN，不填0。

## 尚缺的预算输入

- 批准的最低/推荐CPU、GPU、内存与显示分辨率。
- 目标帧率、VSync/帧率限制、画质与图形API策略。
- 标准负载：敌人、弹体、Collider密度、特效/音效、菜单与恢复流程。
- 主线程、渲染线程、GPU的median/p95/p99预算及可接受尖峰窗口。
- 逐帧/每秒GC预算、内存/显存上限、启动与恢复耗时预算。
- 采集器开销的可接受范围与无采集器对照方法。

没有这些输入，本轮不擅自设置通过阈值；**实际性能预算验收NOT_RUN**。

## 建议的后续对照（未授权实施产品优化）

先选定固定输入和目标负载，再用相同硬件、构建、图形设置、暖机、采集方法和运行顺序进行配对。分开“无采集器CPU基准”“带原生分配事件的字节采样”“Editor调用栈归因”，不相互替代。加入空操作和固定分配校准、密集Collider与长时间场景卸载样本；保留失败与分布，不只看均值。

优化候选的字节机会见[分配提案](ALLOCATION_ANALYSIS.md)。它们是待验证预测，不是批准预算或已完成收益。不修改伤害、发射合同、随机流和v9。若另行授权，再先做修复前负例与配对验证。
''',encoding='utf8')
# Explicitly connect native byte offset semantics to the named setter.
with (p/'UNITYCONNECT.md').open('a',encoding='utf8') as f:f.write('\n字段+0x68的含义另由命名为SetEnableCloudDiagnosticsReporting的本机setter写入指令确认，非仅凭字段位置猜测：[字段证明](Evidence/Raw/native-cloud-field-proof.json)。本批没有调用该setter。\n')
print('allocation/performance docs written')
