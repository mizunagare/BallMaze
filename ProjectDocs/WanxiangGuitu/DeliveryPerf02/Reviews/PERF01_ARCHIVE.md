# PERF-01 固定SHA复审归档

依据用户提供的[复审及PERF02任务原文](USER_TASK.md)，PERF01固定SHA为94dcc009ff971272fc46d8c5b323cbb3251619b5；本批开工实读本地/远端main均为该SHA。

结论：测量与91项警告审计在其声明范围内有条件接受。不代表性能预算通过、瓶颈定位或警告修复。审核方核对报告、统计、清单与源保护记录，没有在Windows重新执行Player或重算全部归档，不能称为审核方独立重跑。

保留24有效窗口+3Title对照、全部首轮失败/补跑/校准、GPU有效子集缺失、GC分配与显存不可用、纯生成无marker、用户覆盖层输入等边界；91警告中18/低37/信息36仍全部OPEN。原生U16/人工/完整预算NOT_RUN，D3D12 UNKNOWN、青色帧、Search、JobTempAlloc根因UNRESOLVED。本批只验证测量能力，不重写或覆盖原PERF01证据与结论。
