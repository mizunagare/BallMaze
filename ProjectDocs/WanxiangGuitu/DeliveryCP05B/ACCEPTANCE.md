# 分层验收

整体验收 **INCOMPLETE**，不以脚本exit0替代分项。原始断言统计不合并多轮样本；最终Editor和Player各157 PASS、0 FAIL、1 NOT_RUN。已修复负例的历史FAIL仍保留。

|验收内容|状态|证据/边界|
|---|---|---|
|自由肩后、居中构图切换，不主动改yaw|PASS|B3/EditorFinal和PlayerFinal probe.json；仅API|
|相机墙体避障、淡化恢复、传送重新锚定|PASS|上述probe；CameraJumpBefore FAIL及After PASS|
|输入UI屏障/暂停辅助失效|PASS|受控PlayerInput状态和原屏障；不是物理输入|
|目标有效性、评分、滞回、主动转向换目标|PASS|最终probe和原始进度日志|
|真实枪口、墙首撞及Damage|PASS|projectile-trace和damage-trace，弓/杖实发|
|无法辅助时与原自由解一致|PASS|最终probe自由组；CombatAim字节冻结|
|剑/枪有限面向、无新增水平位移、释放方向稳定|PASS|melee-trace；独立实际转角断言|
|小时间步累计上限|PASS|YawBeforePlayer exit1 → YawAfterPlayer exit0；保留两份|
|两个原AI敌人实际移动|PASS|开场观测，另有移动目标枪攻击；不等于多敌长期人工战斗|
|Editor运行|PASS|EditorFinal 157/0/1，actual exit0|
|非开发Player业务运行|PASS|PlayerFinal 157/0/1，actual exit0|
|B1/B2/B3非开发纯包|PASS|各阶段文件清单、BuildReport摘要、完整警告|
|纯包启动/普通关闭|PASS|B1 Smoke4、B2/B3 SmokeRelease；非原生验收|
|验收驱动排除及产品IL一致|PASS|assembly-audit.json、assembly-b2.json|
|产品保护及运行输入对应|PASS|protection-final.json、source-parity.json|
|Bee五服务关闭|PASS|三个阶段bee.json；不宣称所有外发路径绝对关闭|
|Editor逐查询GC校准与采样|PASS|ScopedPerfEditor，仅隔离编辑模式fixture|
|Player逐调用GC|NOT_RUN|正分配65536计数返回0，无效结果不得当零|
|CPU整体预算、GPU及长期并发|NOT_RUN|仅查询CPU原始观测，无约定预算|
|Player可见画面正确|UNRESOLVED|71张黑帧原图、capture-audit.json；不以API断言关闭|
|持续Player战斗对照录屏|NOT_RUN|仅有黑帧序列；Editor短GIF不替代|
|原生键鼠/输入设备切换|NOT_RUN|无人实际操作者；未抢桌面|
|人工手感、可读性、音质、最终平衡|NOT_RUN|HUMAN_PLAYTEST空表|
|完整CP04历史24组及全相机矩阵|NOT_RUN|本批有新的明确子集，不宣称全覆盖|
|正式森林整局、结算及跨进程恢复|NOT_RUN|业务源码冻结；训练不创建Profile/Run|
|旧D3D12 UNKNOWN/青色帧/历史关闭根因|UNRESOLVED|原状态保留，无因果证据不关闭|

类别计数仅对应上表；具体功能断言见原始probe，不把NOT_RUN/UNRESOLVED转为PASS。不得从本批推导原生U16或人工试玩通过。
