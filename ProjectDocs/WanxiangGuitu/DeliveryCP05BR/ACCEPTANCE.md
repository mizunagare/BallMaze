# 分项验收，不设单一总PASS

|项目|状态|证据/范围|
|---|---|---|
|历史黑帧保留|PASS|原CP05B无diff，保护快照及原始PNG保留|
|黑帧启动条件复现与整改|PASS|原B3包hidden 8黑/shown 71正常；默认新运行器不隐藏|
|非开发Player真实Frame|PASS|PlayerFinal/Gated真实渲染PNG和窗口/相机回调；不是Editor图|
|D3D12/D3D11对照|PASS|同诊断包不同启动API，D12隐藏负例保留FAIL，显示两API正常|
|视觉门禁分类/CLI退出码|PASS|RenderSelfTests 7项；缺证INCOMPLETE/3，明确失败FAIL/1|
|Editor实际Profiler|PASS|最终1116采样，472个query/control与Unity metadata全匹配|
|非开发Player逐调用GC|PASS|原生Mono allocation profiler正/零校准；2172/2215/2223有限记录|
|六类模式及真实双敌水平移动|PASS|最终analysis的workloadCoverage；早期仅落地不算移动|
|十活敌与有限连续弹体|PASS|至少4秒、实际Spawn/Flight/Collision；不等于长期多敌讨伐|
|物理查询及材质/数组审计|PASS|原始逐方法数据、材料计数及源码对应；没有产品优化|
|纯发行构建|PASS|0错误96条BuildReport警告，完整日志另保留退出诊断|
|固定Profile/Bee五服务关闭|PASS|原PRIVACY-A身份与实际Bee；不宣称所有外发路径绝对关闭|
|纯包无测试驱动/分配桥|PASS|Cecil类型/PInvoke检查及文件清单，实际测试包负例被拒绝|
|最终产品IL与保护|PASS|8类型IL一致；2347个源/用户文件未变；CombatAim冻结|
|纯包训练启动与普通关闭|PASS|PureSmoke READY、可见Unity窗口库存、实际exit0；不是原生交互|
|原B3 API功能回归重跑|PASS|LegacyShownD12 157 PASS/0 FAIL/1 NOT_RUN，保留该NOT_RUN|
|第二次重开训练|FAIL|Editor1真实按钮调用的场景重名；等待独立修复授权|
|训练敌人死亡掉落|FAIL|Editor2实际死亡后DropLootOnce空引用；等待授权|
|一般窗口工具|BLOCKED|工具初始化路径错误；未假装使用其截图，已有运行时替代Frame|
|Profiler buffer/Editor.Search/JobTempAlloc根因|UNRESOLVED|失败和原始日志保留，最终定向采样不关闭引擎问题|
|历史D3D12 UNKNOWN/青色帧/关闭根因|UNRESOLVED|本次隐藏窗口结论不推广到这些历史项|
|纯包独立外部屏幕采集、原生键鼠|NOT_RUN|纯包没有测试驱动；一般窗口工具不可用；不伪造物理输入|
|独立人工观感/音质/手感|NOT_RUN|空白试玩表，无真实操作者|
|整帧Main/Render Thread、GPU/性能预算|NOT_RUN|逐方法和局部区间不能替代整帧，未设阈值|
|长期森林/首领与真实玩家会话|NOT_RUN|有限训练样本，未访问真实存档|
|产品性能优化|NOT_RUN|只交提案，没有授权修改冻结源码|

技术整改及采样可以复核，但两项产品FAIL未关闭，因此不声明整体可发布。工具自测、实际运行、期望负例和人工验收分别统计，不将采样数当成功能PASS数。完成后暂停等待独立复审。
