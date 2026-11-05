# 性能记录口径

实际场景对象、Collider、材料和同步出征耗时见scene-metrics.json。ProfilerRecorder原始逐帧采样另存；只有有效单位、有效非零样本才记录实测，未设性能通过预算。观察器写日志自身开销包含在内，不当作纯产品微基准。

GC正分配65536字节与零分配对照必须校准；无效0不认定零分配。整帧采样不当作逐业务调用GC。GPU无受控负载校准则NOT_RUN。原生内存漂移、JobTempAlloc和MapMagic商店2.1.20/源码2.1.19/meta2.1.17继续开放，不修改供应商源码，不过滤警告。保留完整构建日志、各次失败和资源清理前后快照；缓存对象存在不直接证明泄漏。

性能预算与人工卡顿评价NOT_RUN，等待目标硬件预算与真实试玩。

## 本次真实采样

硬件：i5-12400F（6核12线程）、47.79GB可见内存、RTX3060，驱动32.0.16.1742，Windows10.0.26200。Player日志实际D3D12 level12.2/RTX3060；机器另有虚拟显示适配器，不能拿它们的AdapterRAM当显存测量。

FullEditorFinal1与FullPlayer1都是1280×720、五区已加载、NPC受控、观察器/HUD及日志I/O包含在内，100帧原始记录丢前20取80有效CPU样本。Main Thread单位TimeNanoseconds，Draw Calls单位Count。Editor均值7.69048125ms、1115 draws；非开发测试Player均值2.59247375ms、约1130.43 draws。不是同一二进制的性能改善对照，也不换算为FPS或声称达标。

Player同步出征Stopwatch206.99ms，含地图搭建/NavMesh/保存，不是MapMagic运行时生成。实际地图根1209 Transform、428 Collider、4敌人、26种共享Material。对象/DrawCall偏多是后续分项Profiler风险，未经因果采样不能全部归因新地图或直接改旧角色资源。

两个环境GC正分配65536控制都返回0，校准无效；zero=0只是原始失败控制值。GPU本负载未校准（Player FrameTiming功能为false），显存未测量。逐调用GC、GPU、长时间多敌战斗及最终预算NOT_RUN。

恢复/回营快照有activeTerrain0、NavMeshData0；缓存TerrainData4仍被Resources引用。整机/原生保留量不能由这些活跃对象计数完整解释，原生漂移继续UNRESOLVED。旧MapTools03已有控制实验不继承为本游戏性能PASS。完整原日志中的JobTempAlloc和Editor.Search异常未过滤，见warning-index.csv及失败历史。

四处隔离设置差异（见Evidence/isolated-settings-differences.json）仍限制输入等同性；性能数据仅适用于本次记录的实际隔离配置。后续先定义目标硬件/场景/预算，再用同配置做优化配对，不在本批擅改相机、目标评分或供应商源码。
