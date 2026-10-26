# 阶段2失败与尝试（持续追加）

以下原始根均在工程外，后续发布脱敏副本与索引；不删除中间日志或修改退出码。

- `Stage2Baseline/20261026-235614-405d028b`：现有10方法+准备=11PASS，当前运行。
- `Stage2MetricBefore/20261027-000710-dd53ca97`：新规则先FAIL，准确扣血观测能力缺失；随后增加瞬时只读计数，未改HP/伤害。
- `Stage2Directed1/20261027-001258-dd5f5ef8`：准备+4规则=5PASS；100seed/3构筑属性/20实际种子受控通行。后续更精确记录控制器参数，不拿该次旧输入冒充最终All。
- MatrixPilot1：`OwnedMove`正确拒绝把父级Project文件当子级矩阵根内文件移动；没有启动Unity。改为仅允许已核对父owner下两个固定目录、六个已知文件的互逆交接，不放宽原OwnedMove。
- MatrixPilot2：长剑Safety/Gather三进程PASS；旧观测格式缺少部分后续指标，作为试跑保留。
- MatrixPilot3：记录器增加出口字段时`run?.runId==data.run`在两边均null时为true，随后读取run.exitId引发测试代码NRE。失败记录器再次抛错导致未退订循环；未伪称产品空引用或正常退出。
  - 原worker只选UnityWndClass/测试fixture，拒绝UnityContainerWndClass，关闭请求NOT_RUN。
  - 新增独立opt-in editor-close，只操作PID/Exe/非输入WGTest桌面/已知owner Project/中断回执绑定的Editor主窗口，发WM_CLOSE，不输入/激活/强杀。实际窗口结束，但当次`Process.GetProcessById`对象不能读ExitCode，回执NOT_RUN。后来改用事先持有的native handle读取退出码；该新正向Editor退出观察路径未重跑，不补填PASS。
  - Normal原始进程exit0不表示试验成功；该轮缺少完成回执，Resume FAIL，FinalResume NOT_RUN。新增Stage2完成/输入/阶段回执检查，显式中断不能算成功。
  - 修复记录器null判断；失败先退订，记录器自身报错也打印完整异常后正常以失败退出，不再阻断清理。原两万余条错误日志保留，不过滤制造通过。
- MatrixPilot4：修复后弓Gather/Gather三进程PASS，实际费用/入仓/制造/装备属性与新Run恢复；仍是定向试跑。
- `Stage2LogGateBefore`：无日志时JSON为FAIL但工具exit0；修复为空证据实际exit1，并覆盖嵌套矩阵日志。After三项合成探针断言通过，负例原始FAIL/exit1不改成游戏PASS。
- `Stage2Directed2`：故障夹具文本替换误把`int attempts`重复插入，C#编译FAIL，4依赖项NOT_RUN；未执行项目不标PASS。
- `Stage2Directed3/20261027-003934-fedcf32e`：新重试探针先取未创建的region，测试NRE/exit1；其他5步骤PASS，包括实际主角尺寸/保留敌人碰撞的20seed与原WGDeliveryA。修复为在挂hook前明确初始化同一森林服务；没有改产品生成器。
- `Stage2RetryAfter`：实际复现历史请求1440702505第三候选node:24不可达而合法fallback到1；请求1的第三候选3成功；全部失败回营。原失败seed没有被宣称修复。原WGDeliveryA重试夹具改用已经物理验证的固定请求1，保留原断言，不再随机假定任意第三候选必成功。

上轮B10的549产品空引用/73 Search异常、历史65/2/20/1及UNKNOWN/青色帧证据继续在各原目录保留。本文件不重新分类旧历史，也不把受控/回调/截图当原生或人工试玩。
