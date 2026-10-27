# PERF-01 冻结测量口径（采样前）

这是性能基线，不是优化或性能预算验收。禁止修改游戏伤害、经济、地图、随机流、实体数或AI。玩家仅由已审计运行时输入驱动操作；不直接给奖励/改进度/传送/冻结。产品源码和用户设置不改。

## 输入与场景

基线6f2abca5f89fc80fc5d298623eda12f557654b78，1152项工作区覆盖层与硬件只读清单。沿BUILD-01短路径、新Library；发行构建默认不注入；Perf01只向隔离Acceptance工程加入partial测试扩展/采样器，并启用FrameTimingStats。与发行包不同的采样配置必须披露。

使用PLAYER-02实际运行产生的完整合成集合作为固定输入：Running来自后继森林Run；Camp来自Committed；不编辑正例JSON。每次独立Player复制同一集合，记录全部SHA和Profile/Run/region/seed/layout/装备/随机状态。循环测量的渡口准备也只能由实际采集/拾取/修复产生。后继Run由正常业务生成，GUID种子不同必须记录，不能当成同seed稳态对照。

至少3次独立进程：Title60秒、Camp60秒、Movement120秒、Gather120秒、Combat120秒、Boss120秒（不能稳定完成则未完成）、Loop真实撤离/结算/取材/制造/新出征可变时段、Resume后继Run加载+30秒窗口。先预热10秒；加载恢复在标题预热，窗口覆盖真实加载，不伪称世界稳态。另做Title采样关闭3次60秒对照。首次短探针仅校准工具，不计正式重复次数。

采集窗口含导航、攻击、拾取与10秒自然观察间隔，避免伪造持续攻击负载；普通/首领窗口明确记录接近、攻击、遭遇耗尽、死亡和实际活跃时间。若只能取得混合窗口，不把它冒充120秒连续战斗。没有目标或死亡后不补怪、不回血重置、不换弱场景凑数。

## 指标

- `frame_interval_ms`：托管LateUpdate间隔，含调度/等待；独立指标，**不能替代CPU或GPU时间**。
- FrameTimingManager：cpuFrameTime（含等待）、cpuMainThreadFrameTime、cpuRenderThreadFrameTime、gpuFrameTime、PresentWait分别保留，单位ms。只纳入新的非零timestamp，保留原始无效/重复行；4帧回传延迟记入限制。CPU/GPU零值视无有效计时，NOT_RUN；不以另一指标填补。
- ProfilerRecorder：保存可用计数器列表、类别和原始单位。Main/Render若可用以TimeNanoseconds记录，GC Allocated In Frame以Bytes、Draw Calls以Count记录；无效/未取样用-1而非0。有效的GC分配0和未可用-1须区分。
- 托管堆、Unity已分配、进程WorkingSet/PrivateBytes和GC.CollectionCount单列。进程内存约1秒刷新，记录间隔；不是纹理内存或显存的替代。
- 系统采样：精确拥有者PID，实际UTC/间隔/进程CPU增量、工作集/私有内存；有GPU进程计数器则记录其dedicated/shared usage，不称为剩余VRAM。工具不支持/查询失败则保留错误并NOT_RUN。
- 加载：从实际GameEntry.Loading边沿、sceneLoaded、game-ready和entry-audit取值；区别OS启动→标题、选择继续→世界就绪、区域生成与跨进程恢复。不将标题启动当作游戏FPS基准。

## 统计和有效性

固定窗口按monotonic时间取样，原始setup/warmup/超出窗口/失败行仍保留。每次分别P50/P95/P99（线性插值）、样本量、有效/缺失数、最小最大、超过P99的原始离群值索引。跨重复只作描述，不将不同场景/种子/计时API混为一条曲线。失败/死亡/提前结束的分布可以展示，但必须标PARTIAL/FAIL，不补成完整窗口。

记录分辨率1280×720、窗口、质量、VSync、帧率限制、图形API、实际GPU、前后台、timeScale。保持产品默认帧率/VSync，不为得到好数值调整。非活动私有桌面仍正常渲染；不激活桌面。其他用户负载未独占控制，不能宣称硬件实验室性能。

采样器记录上一帧自身耗时与分配（包括序列化/写出/刷新），并做同产物Title on/off各3次；关闭对照只评估额外计时采集，基础CSV/驱动仍在，FrameTimingStats构建开销未被完整剥离。观察差异不自动构成因果或发布包开销上限。

没有目标硬件预算，不能声称性能达标；没有安全原生/独立人员，U16与人工仍NOT_RUN。D3D12 UNKNOWN、青色帧、Search、JobTempAlloc仍UNRESOLVED，无新线索不扩展实验。

官方接口依据：[ProfilerRecorder支持Release Player](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Unity.Profiling.ProfilerRecorder.html)、[FrameTiming各计时含义](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/FrameTiming.html)、[延迟/平台限制](https://docs.unity3d.com/6000.0/Documentation/Manual/frame-timing-manager.html)。版本固定，以本机6000.6.5f1接口及实际可用性为准。
