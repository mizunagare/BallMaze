# 验收结果

当前矩阵：**185 PASS / 0 FAIL / 10 NOT_RUN / 4 UNRESOLVED**，整体UNRESOLVED，不是独立审核通过。[完整具名明细](Evidence/acceptance.json)

|任务|结果|证据与边界|
|---|---|---|
|多块连接|PASS|18组、每组4块；原生/整形后接缝高度0；加载显式绑定邻接|
|湖泊、山脊、道路|PASS（自有适配）|真实高度/路面、深水物理及NavMesh阻挡；不是免费Spline能力|
|自定义Prefab/森林组合|PASS（自有适配）|90树、8柱、拱门；场景变换哈希与跨进程一致|
|石柱/封闭遗迹|PASS（技术夹具）|墙与屋顶第一碰撞、0.65/2.5代理通过门口；非最终美术|
|Collider与遮挡|PASS|16探测中14首先命中Terrain，其余不计作Terrain通过；水、墙、屋顶首碰另列|
|NavMesh与敌人移动|PASS（原型）|3个真实NavMeshAgent，路径、Warp、逐帧移动CSV；非产品战斗AI|
|Scene保存/重新打开|PASS|地形、布置身份一致，邻接由加载器重绑定|
|非开发直接加载|PASS|Build3及PlayerWrite3/Read3，Development=false|
|卸载/重载及活动对象清理|PASS（有限范围）|Scene卸载后Terrain/Agent为0，重新进入内容一致|
|原生总内存回收|UNRESOLVED|未回到冷Boot水平，不推断泄漏或无泄漏|
|固定seed跨进程|PASS（实验检查点）|相同保存内容、不同实际PID5500/4492；不是v9恢复|
|包身份/来源/源码保护|PASS|本地SDK2.1.20、完整包SHA、199源码与原包一致|
|标签维护原因|UNRESOLVED|源码2.1.19/旧meta2.1.17由原包保留，原因未知|
|Profiler MainThread/Draw|PASS（采集）|180帧，非性能预算通过|
|GC/GPU|NOT_RUN|正分配校准返回0；GPU未取得独立有效校准|
|JobTempAlloc|UNRESOLVED|构建退出原日志保留，未确认根因|
|分块视觉接缝|UNRESOLVED|高度0不覆盖实际渲染边界差异|
|DA运行|NOT_RUN|只读官方资料研究，无安装包、不购买|
|原生操作/人工/最终美术|NOT_RUN|自动化帧和Agent不能替代|
|正式产品/v9/AI接入|NOT_RUN|本轮禁止修改，不以独立实验冒充|
|用户/产品保护|PASS|2413哈希未变、无新增；旧分支/证据保留|

历史FAIL、缺回执与工具错误见FAILURE_HISTORY。修复的是实验驱动、加载适配和新建原型资源，不修改供应商、产品逻辑或测试目标来制造成功。没有继承旧批PASS。
