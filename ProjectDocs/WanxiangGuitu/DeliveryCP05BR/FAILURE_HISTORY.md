# 原始失败与边界

所有尝试位于I:/WGCombat/CP05BR-1103-A独立目录；原文件未覆盖，仓库日志gzip镜像及脱敏前后SHA见manifest。

|尝试|实际结果|处理|
|---|---|---|
|computer-use初始化两次/reset一次|kernel assets路径错误|BLOCKED；未再试探用户桌面，记录替代观测方法|
|原B2/B3 Player黑帧|10/10、71/71|原CP05B不修改、不删图|
|本轮LegacyHiddenD12|8/8黑，但API可运行|保留负例，不能由exit0认定画面正常|
|新诊断PlayerHiddenD12|7/7黑、相机回调0|视觉回执仍FAIL/1；正是需要保留的控制样本|
|Editor1|第二次真实重开场景名重复，测量未完成|产品FAIL/测量INCOMPLETE；240秒目标超期后普通owned窗口关闭。实际exit0只代表清理，不改成测量PASS|
|Editor2|真实敌人死亡掉落空引用；Profiler丢帧/内存压力；Editor runner最终deadline/exit1|全部保留。后续清理请求到达时该桌面已退出，cleanup NOT_RUN，不虚构成功|
|Editor采样器自观察|早期profileEditor=true会包含Editor采集工具自身的开销|后续仅profile Play loop、关闭额外分配栈、限制raw帧容量；超限必须报错而非截断为PASS。最终472作用域无丢失/无差异|
|早期Editor3/Stress和Player短样本|逐方法GC有效，但第二敌人主要垂直落地/连续弹体持续时间不足|不继承为完整负载通过。增加水平位移检验、夹具初始摆放及至少4秒密集场景；旧结果不覆盖|
|纯/测试构建退出诊断|JobTempAlloc剩余分配警告|UNRESOLVED；不是因BuildReport成功就关闭|
|Editor.Search|原始SearchDatabase内部异常|继续UNRESOLVED，不归因于产品且不删日志|
|测试包冒充纯包的程序集负例|类型CP05BRProbe与原生分配桥PInvoke被发现，实际CLI exit1/FAIL|保留该预期负例；纯包另做独立正控|
|首次证据发布|已知硬件/窗口工具元数据由Windows默认GBK生成，UTF8假设导致UnicodeDecodeError/exit1；表格读取也缺少显式编码|原元数据不改，PartialEvidence归档；只对两份已知metadata严格GBK解码、转UTF8镜像，manifest记录编码及原/发布SHA，不使用忽略错误|

原35/50等历史项目、法杖近距原失败、旧D3D12 UNKNOWN、青色帧、原生U16与人工状态不在本批被改写。新的有效GC方法不能改写旧线程计数器的NOT_RUN。没有降低伤害/碰撞断言或修改玩法以隐藏错误。
