# S2-R1失败历史（持续追加，原始输出均保留）

- 离线原复现：`D:/WanxiangValidationRuns/S2R1/20261027-085949-review-intake/OriginalReproduction`，4例原脚本匹配blob23900d。1正常+3异常旧行为确实复现，不是产品PASS/旧19局损坏证明。原任务书最初缺失的阻断回执保留，用户补路径后已解除。
- `SummaryBefore`：新29断言5PASS/24FAIL；`SummaryAfter1`29PASS，`After2`31PASS，`After3`32PASS。负子进程的FAIL/exit1是预期，断言PASS不混同游戏PASS。R13只读旧19重审Historical19Audit1为19PASS，警告旧schema缺实际attemptID不回填。
- `ObservationBefore/20261027-093151-1cd96e56`：Unity实际缺事件probe FAIL/exit1；先失败再增加只读health-transition接线。
- `PilotOrd1/20261027-094723-7af75d9d`：准备、事件probe、旧伤害规则、普通敌seed1三构筑预试跑均PASS；三例均首击实际死亡TTK0，不是无限DPS。该预试运行早于parentMethod字段补齐，不能当最终冻结版主矩阵，原来源/数据保留。
- `PilotLake1/20261027-095325-5adc2223`：边界校验在batch模式未进入预期Play初始化，180秒内部deadline后exit1（不是测试通过）；湖Boss首例可选远程后撤点TryGround成功但无完整NavMesh路径，驱动抛错exit1，观测censored、0命中。Search内部异常另列，不是此驱动栈。修复测试入口为同类既有非batch私有桌面；可选4m后撤额外确认完整导航，否则停止输入，不改地图/怪物/攻击/躲避数值，不换失败seed。
- `RecoveryPilot/20261027-095837-2572e8f4`：普通敌真实首次扣血后暂停保存、第二进程继续至死亡/掉落/真实放弃结算均PASS；湖BossStart遇到同一旧后撤驱动问题FAIL。原编排未跳过LakeResume，缺检查点的Start前置异常未捕获，Editor留在等待。仅对该root/PID44576/独立WGTest桌面记录interruption后，使用既有editor-close发送WM_CLOSE正常结束：实际exit0、无超时/无强杀；这是失败清理，不是恢复验收PASS。该原始Resume进程exit0不改变缺少recovery-result的事实。已加R1 Start异常exit1与Start→Resume依赖，保留未完成记录；没有关闭用户程序或历史占用进程。

本轮未因这些边界试验调整任何玩法参数。后续每次复测均用新根/新attempt，原日志和失败不覆盖。

## 后续诊断与复测（均有独立目录）

- `GroupingBeforeFix`：32P/1F，R01-build-separation新增断言暴露新汇总实现漏了构筑筛选，Historical19Comparison同时发现分组均值不一致。补上分组条件后After4为33P。保留Audit1和第一次比较，不将它们改为通过；冻结版Audit3的19条/214主要值全一致。
- `SummaryAfter5`：33断言中28P/5F。进一步校验终局身份时错误要求ACK后仍存在活动Run/区域，与真实ACK会关闭Run的合同不符。改为Pending首局身份+Profile+阶段回执关联，ACK若提供非空Run/区域仍必须一致；新增错Run ACK和attempt数组类型回归。`SummaryFinal`35P/0F，30个负子进程exit1、全未启动exit2一个是预期，不是游戏失败。
- `LakeAfterGuard/20261027-100641-23b8f1a3`：三湖Boss预试完成；边界探针在Depart关闭背包的同帧立即翻滚，正确被Inventory.ClosedFrame保护拒绝，断言FAIL。将校准移到下一活动帧后验证，不改产品输入保护。LakeStart保存成功，Resume精确身份已对齐，但测试错误要求已死尸体控制器启用；改为只检查存活敌人，不能激活尸体。
- `BoundaryRecovery2/20261027-101700-1a9ec735`：6步骤PASS，普通敌和湖Boss均真实首次扣血→暂停保存→独立新进程→实际击杀→掉落/结算唯一；不是未运行项的替代。本轮最终冻结版又在FrozenValidation中各执行一次，早期源/辅助字段差异不抹除。
- `FrozenValidation/20261027-102526-ad379719`：最终输入583f19d9；31步骤PASS、0FAIL、0超时。18主配对均实际击杀，额外四武器8场均击杀；每条件n1，早期预试不并入主配对统计。覆盖实验是独立注册样本，不能与主矩阵叠加成更大同条件样本量。所有初次故障、预试和恢复重试仍在Failures下，无法定时完成的业务不靠后续PASS掩盖。
- `Stage2Protocol`：旧框架的一条真实完整冒险以新attempt/阶段协议跑3进程PASS。产品102份runtime源与冻结副本相同，原正常AI驱动及四Stage2 helper输入相同；此前准备副本中无关的R1诊断辅助字段不是这条冒险的观测器，不冒称整个Editor程序集与冻结主矩阵相同。
- `ReleaseAuditCompatibilityFailure`：旧B10→B07-R1审计器要求All专属`report.finalized`步骤，定向编排实际只有结束/空preserved进程回执，故exit1。没有伪造该步骤或放宽旧All断言。新增小型只读R1产物审计，检查定向编排真实结束、构建退出、输入/用户哈希和无驱动程序集，结果另存FrozenReleaseAudit2。首次堆栈和命令仍保留。为复用旧审计曾复制构建到本地Build/Release，非二次构建；最终审计直接读取原Rules/Release。

## 日志与未解决项

最终30份Unity日志：26条异常起始归于Editor.Search内部栈，1条为事前声明的S2R1_EXPECTED_OBSERVER_FAULT，0条未分类异常起始；既有窄范围空引用/丢组件门禁通过不等于日志无任何问题。监听器故障诊断完整保留，不能当产品正常无异常。

非开发BuildReport为0错88警告，原构建日志另有182条warning/JobTempAlloc标记行（不是另一个BuildReport计数）。JobTempAlloc在旧Stage2构建日志也存在，未取得因果栈，仍UNRESOLVED，不归因于本轮只读事件，也不以exit0判定干净退出。D3D12 UNKNOWN、青色帧、Search根因继续开放；原生/人工/完整性能NOT_RUN。没有新关闭实验或生命周期改动。
