# PERF-01 验收表

这里的PASS是本批**采集/审计交付项**，不是性能预算或独立审核通过。原始首轮15 PASS/7 FAIL/6 NOT_RUN始终保留；最终样本选择与所有失败分开列。完整数据见[证据索引](Evidence/INDEX.md)、[逐窗口统计](Evidence/Run-1027-224456/AnalysisFinal/MEASUREMENTS.md)。

|ID|验收项|结果|证据及边界|
|---|---|---|---|
|PF01|归档PLAYER02固定SHA复审|PASS|Reviews原文/归档；限定条件接受，不冒称审核方Windows重跑|
|PF02|冻结源码、工作区覆盖层、硬件、配置与产物|PASS|owner、ReadOnlyAudit、hardware、BuildProof、每例header/config/fixture-before；输入含用户覆盖层，只公开哈希|
|PF03|8场景各3次独立完整采样窗口|PASS|AnalysisFinal/accepted-runs、suite与recovery；24个窗口，额外3个Title OFF；Loop可变链、战斗混合负载，不称持续攻击|
|PF04|保留失败、原始帧与离群值|PASS|首轮、Pass1、所有Attempts、失效/超出窗口帧、outliers；无损归档MANIFEST|
|PF05|CPU主线程/渲染P50/P95/P99|PASS|FTM各自分布与有效/缺失计数；Profiler主线程另列，帧间隔不替代CPU；不承诺每一帧有新FTM值|
|PF06|GPU每帧完整计时覆盖|UNRESOLVED|有GPU有效子集P50/P95/P99，但有非正/无新timestamp；原始缺失保留，不填CPU或0|
|PF07|GC集合、托管/Unity/Windows进程内存|PASS|原始帧GC0、托管堆、Unity分配、精确PID系统CSV；Mono进程内0无效，不重计三个GC代|
|PF08|每帧GC Alloc及工具自分配字节|NOT_RUN|Release无对应Recorder；Mono已知64KiB探针仍0；不能将0解释为无分配|
|PF09|可用显存/进程GPU内存|NOT_RUN|GPUProcessMemory无有效实例，保留3次有界错误；SystemInfo容量非可用显存|
|PF10|实际标题/继续/后继加载与恢复边沿|PASS|entry-audit、perf-events、loading字段、3次Resume身份断言；包含调度/输入/等待的范围明确|
|PF11|纯区域生成耗时剖分|NOT_RUN|没有独立生成marker；不把出征UI到ready时长重命名为纯生成|
|PF12|采样开销的有限对照|PASS|同V3 Title ON/OFF各3次、自身耗时；只关闭额外Recorder/FTM调用，不是无观测发行包或因果上限|
|PF13|91条发行警告逐条风险审计|PASS|WarningAudit原文/源码位置/API/风险/建议/回归；86+3+2全覆盖，91项仍OPEN，不自动修改|
|PF14|临时驱动隔离与非开发构建|PASS|Release0错91警告，PerfV3/V4各0错120警告，BuildOptions.None；PE+143模块+源码排除，不含UnityEditor引用|
|PF15|保护用户数据、场景、设置与依赖|PASS|source-protection逐项1152哈希；只提交ProjectDocs；无真实档/升级/CI/强杀/桌面激活|
|PF16|目标硬件性能预算验收|NOT_RUN|尚无预算；这些数据建立基线，不声称性能达标|
|PF17|原生U16、独立人工与发行包无观测完整冒险|NOT_RUN|仅临时非开发验收包、虚拟输入与非活动桌面消息；不冒充物理键鼠/人工/标题栏关闭|
|PF18|历史引擎问题根因关闭|UNRESOLVED|D3D12 UNKNOWN、Editor青色帧、Search、JobTempAlloc继续开放；无新因果证据，不复做试探实验|

本表18项：**11 PASS /0 FAIL /5 NOT_RUN /2 UNRESOLVED**。这是交付项口径，不能与进程/窗口/逐指标或旧All行数相加。所有本轮首次失败另见FAILURE_HISTORY与原始case结果。没有删除任何失败或降低业务断言；独立复审结论待定。
