# 性能与校准

硬件：i5-12400F（6核12线程）、RTX3060、驱动32.0.16.1742；Unity6000.6.5f1、URP17.6.0、D3D12。隔离非开发Windows64 Player，1280×720，Frame Timing Stats在独立工程启用。用户工程设置未改。不是正式战斗或最终美术负载，无目标帧预算授权，不设性能通过阈值。

## GC：NOT_RUN

每进程3次正控制各分配65536字节并强引用，3次无分配空读对照；GC.GetAllocatedBytesForCurrentThread的结果全部正控制=0、空读=0。不能识别已知分配，计数器无效。GC.Alloc事件在Player不可用；Editor为Valid但未捕获正控制。没有以空读0宣称零分配，没有将整帧GC混作逐调用分配。

原始gc-calibration.json和可用计数器名/单位在每次运行目录。GC.Collect确实执行，但不等同有效字节测量。要测真实分配还需要可靠Profiler allocation事件/快照与独立正、零控制。

## GPU：Editor限定校准PASS；Player NOT_RUN

使用FrameTimingManager。独立工程PlayerSettings.enableFrameTimingStats=true，GPU频率1GHz，实际返回正时长。控制为100帧基础、100帧自制有界512²双RT的4次Blit、100帧恢复；每阶段前20帧不纳入均值但原始值全部保留。每阶段至少30个有效样本；预先定义负载均值>基础1.2倍、恢复<负载0.85倍，仅判断采样能否响应控制，不是游戏性能预算。

| 运行 | 基础/负载/恢复 GPU ms | 校准 |
|---|---|---|
| Player Audit2 | 0.163620 / 0.147418 / 0.163430 | NOT_RUN：无正负载响应 |
| Player Audit3 | 0.163597 / 0.149274 / 0.163904 | NOT_RUN：无正负载响应 |
| EditorPlay1 | 0.186022 / 0.241600 / 0.185754 | PASS：本次编辑器受控负载响应成立 |

Editor结果不能补齐Player，也不是GPU profiler全战斗基准。Audit3和Editor启动时间接近，外部系统并非专用空闲性能实验室；不据细小差异比较引擎/插件性能。校准shader自身产生编译警告，已保留，Player负载不响应的详细GPU管线归因未完成。不能将Player返回的正数直接当可信性能结论。

官方：[Frame Timing启用](https://docs.unity3d.com/cn/6000.0/Manual/frame-timing-manager-enable.html)、[PlayerSettings](https://docs.unity3d.com/cn/6000.0/ScriptReference/PlayerSettings-enableFrameTimingStats.html)。以本机6000.6.5f1实际行为为准。

## 257分辨率与连续循环

4块×257²=264196个高度网格采样点/轮，不等于实际GPU三角形数。5进程×8轮=40轮160块，全部内容哈希与冻结世界一致。下表为预热后6轮的墙钟总耗时，包含Scene加载、四块生成/整形、NavMesh注册移除、卸载、UnusedAssets与GC；不称为纯MapMagic算法耗时或CPU Main Thread帧时间。

| 运行 | n | 完整循环均值s | 最小s | 最大s |
|---|---:|---:|---:|---:|
| Audit2 | 6 | 0.194052 | 0.189884 | 0.200061 |
| Memory1 | 6 | 0.201167 | 0.184926 | 0.239103 |
| Memory2 | 6 | 0.194834 | 0.186308 | 0.205504 |
| Audit3 | 6 | 0.215174 | 0.200418 | 0.242678 |
| EditorPlay1 | 6 | 0.284793 | 0.272240 | 0.303287 |

CPU逐帧、GPU Player、Draw Calls、逐调用GC、精确Native归属及最终性能预算本轮无可信完整数据：NOT_RUN。对象/保留内存样本在 [内存报告](MEMORY_ANALYSIS.md)，原始采样未丢弃首次测量或失败校准；本轮不沿用第二轮的性能PASS。
