# PERF-01 失败与工具修正历史

全部首次尝试、原始帧、日志、退出回执和截图保留；本文件不替代原始suite/recovery结果。PLAYER02历史31 PASS/6 FAIL不重写，本轮结果另外统计。

## 校准

- V1/V2短Title探针只检查计时接口与记录器，不计60秒重复。初版可用计数器JSON中的`valid`是未赋值字段，会错误显示false；实际计数值与帧行另存。V3改为接口句柄`available`。旧文件与旧源码均保留。
- Mono `Process.WorkingSet64/PrivateMemorySize64`进程内查询返回0，不能解释为没有内存。V3保留为不可用-1，独立Windows精确PID sidecar记录实际内存。
- `GC.GetAllocatedBytesForCurrentThread`对已知64KiB分配仍报0；自分配量和不可用的Release GC Alloc recorder均NOT_RUN，不拿0证明无GC。
- FTM延迟/重复timestamp、GPU非正值不填补；缺失保持缺失，既不替换为CPU，也不删掉对应原始帧。

## 首轮完整队列

首轮`Invoke-PerfSuite`完整执行独立项后结束，原始suite-results/console/exit均保留于证据，另有Pass1冻结副本。

1. **后退出指纹工具失败**：Title R1 ON/OFF、Movement R1的Player有完整采样、PASS业务回执和真实OS退出0；但sidecar仍打开StorageRoot中的system CSV，既有PLAYER02指纹检查读取失败。本轮仍将这些样本的完整编排资格标FAIL，没有因Player退出0覆盖工具错误。
   - 修正：OS日志移到同一拥有者根的`Runtime/System/<case>`，独立于业务存档指纹集合，保留所有原始样本；sidecar停止和退出仍需独立回执。没有跳过或弱化原指纹检查。
   - 原工具版本存`ToolVersions/BeforeSidecarSeparation`；受影响窗口用原V3产物定向补跑。新例带ExecutedTools和SHA。早期例没有逐例工具快照，已明确这一证据限制。
2. **运行时采集驱动失败**：PrepareFerry与Gather三次，在与敌人战斗后升级选择暂停，既有Harvest内层循环没有处理新弹出的技能选择，30秒后报`resource attack not hitting`。原截图显示技能弹窗，不能归咎于资源碰撞、武器伤害或擅自改游戏数值。
   - 修正仅在PERF隔离副本的PLAYER02 fork：内层观察`IsChoosing`，通过原有虚拟Digit1输入选择技能；不直接调用技能/业务方法，不修改HP/库存/奖励/存档。原PLAYER02驱动文件未改。
   - V4单独编译，编译期间暂停性能测量；新PrepareFerry和Gather全部用V4。冻结的V3/V4 fork、构建报告及SHA均保留。
3. PrepareFerry首轮失败造成Loop×3、Resume×3依赖NOT_RUN；不注入修复状态或后继存档。定向补跑先由真实采集/扣费产生渡口档，之后才执行其依赖链。旧NOT_RUN仍留在suite中。
4. 首轮suite函数输出污染潜在路径值：内部脚本输出被PowerShell函数当作返回值。当前函数将诊断输出显式Out-Host，返回值只为路径；原执行版本保持于证据。首轮Prepare失败，没有借污染的值执行后继正例。

## 严格保留的边界

- 工具状态、业务状态、采样时段完整性和各指标有效性独立判断；不从编排器或OS exit 0推导全部PASS。
- 普通/精英首领窗口包含接近和耗尽观察，不能改名为120秒连续战斗。没有补敌、降低伤害或冻结世界以凑满负载。
- 没有性能预算；没有原生键鼠或独立人员。采样关闭对照也含基础写CSV/驱动和启用FTM的构建，不是无观测发行包。
- URP后处理shader不可用等运行时日志单独索引，不从91条中扣除，也不通过过滤原日志伪造干净运行。其影响/根因未经本批授权修复。
- D3D12 UNKNOWN、Editor青色帧、Editor.Search与JobTempAlloc根因保持UNRESOLVED；不复做无新线索实验。原生U16/人工仍NOT_RUN。

最终逐例状态和所有后续失败以REPORT及AnalysisFinal为准；有新失败应继续追加，不能覆盖本记录。
