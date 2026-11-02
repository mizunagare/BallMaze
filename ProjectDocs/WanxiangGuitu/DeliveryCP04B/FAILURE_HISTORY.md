# 历史与每次尝试保留

1. 原main/CP04-A的w2-s0-near、w2-s1-near为零伤害UR，不改原文件。本轮BeforeMatrix旧产品再次出现右/左1.5m零伤害；修复后以真实Collision+Damage断言替代原两UR，新293项通过，不能改写旧结果。
2. 最早Performance线程分配返回raw0但未校准；后续已知65536字节仍0，判NOT_RUN。BeforePerformance/AfterPerformancePaired采用Idle枪口，未覆盖关键负投影；完整保留，最终使用BeforePerfFrozen/AfterPerfFrozen及PlayerPerf的实际释放快照。
3. 工具摘要命令曾多写一层python路径，exit1、未启动分析；tool-failure-01保留。
4. 首次Player运行器因PowerShell大小写无关的root变量产生逐层嵌套目录，主批为7套，均在同一owned根、来源独立且真实完成；原脚本和嵌套结果不搬移、不覆盖。修复后另跑Wall/Boundary两套，确认平铺目录及真实语义。主批7+控制2=9个Player。
5. 只读包源码检索曾把Windows通配符原样传给rg，搜索失败；tool-failure-03保留，未据此编造配置写回根因。
6. Build后发现5项隔离配置差异，原两侧文本/SHA/diff保留；整体BLOCKED，未改源产品或用户文件，不用“进程0”消除这一缺口。
7. Search内部异常、JobTempAlloc等原始日志完整保留，不归为本次产品命中问题，也不关闭历史UNKNOWN/C15/青色帧等事项。原生输入、人工体验始终NOT_RUN。

原始18次Editor/9次Player均真实exit0、无超时。174项新数据检查PASS并不能覆盖上述缺项。最终分类退出2是BLOCKED，不是全部通过。
