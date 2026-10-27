# S2-R1 验收对照

执行输入 `583f19d905aa1b8d8b575f2441bf942b1e37b24f`；开始 `2ca1aac4bbf6fe6ca35a6604a2422dd79c889470`。结果是交付方本轮真实执行，不是独立复审结论。各层有重叠，**不相加为总游戏PASS**。

|要求|结果|证据/边界|
|---|---|---|
|S2-RV-01旧问题复现|PASS（复现成立）|OriginalReproduction四例；旧原件与任务ZIP哈希保留，非旧19条损坏证明|
|R01合法完整/构筑筛选|PASS|Offline/SummaryFinal；包括额外build-separation断言，首次FAIL保留|
|R02空Run自报PASS|PASS（明确拒绝）|同上R02-null-run，child exit1|
|R03假撤离/提交/ACK/后继、串档ACK|PASS（明确拒绝）|四flag与其他Run ACK；不能仅凭exit0|
|R04配置/配置hash/代码输入不符|PASS（明确拒绝）|三个独立负例，无自动补值|
|R05缺阶段/进程|PASS（明确拒绝）|stage/process分别缺失|
|R06非零/超时/中断|PASS（明确拒绝）|三故障、unknown与技术状态独立|
|R07已出征缺指标|PASS|started2/known1/unknown1/technical1，不写成有效出征1且整体撤离率100%|
|R08损坏JSON/错类型|PASS（明确拒绝）|包含bool冒充int、材料数组、Profile、attempt数组等|
|R09完整60+失败2|PASS|完整均值60，2秒单列partial；不写31秒|
|R10合法Death/Abandoned合同|PASS|完整观测测试PASS与业务结果分开，不要求都Extracted|
|R11重复case/attempt/Run或相同后继|PASS（明确拒绝）|重复身份具体诊断；正常三阶段同Run不误报|
|R12空计划/全未开始|PASS（拒绝终验PASS）|空计划exit1；全未开始exit2/NOT_RUN，rate=null|
|R13历史19只读重审|PASS（旧schema投影）|Historical19Audit3，214项主要值一致；不补造旧attempt/阶段hash|
|R14未结束/输入变化|PASS（明确拒绝）|缺结束回执、并发改变证据两例，不能临时摘要冒充终验|
|上述离线断言|35 PASS / 0 FAIL|子进程4 exit0、30预期exit1、1预期exit2；不是30次游戏失败|
|新attempt/三阶段正常流程|3 PASS / 0 FAIL|Stage2Protocol：真实采集/收费/撤离/结算/制造/不同后继森林与两次新进程，独立新协议审计PASS|
|真实HP事件存在及旧累计伤害规则|PASS|S2R1ObservationProbe、Stage2Rules.DamageMetric；改前缺事件exit1保留|
|同帧/首击/治疗/过量/零/无敌/重置/卸载/监听故障/暂停/RNG|PASS（受控规则）|s2r1-boundaries.txt，监听故障真实日志保留，时间为帧精度|
|18有限主配对|18目标实际击杀|长剑普通9、弓湖Boss9；每条件n1，非全平衡或撤离率|
|四武器各普通/Boss|8目标实际击杀|额外coverage，独立于18；26条同一产品/驱动程序集，唯一Run身份|
|普通敌跨进程伤害段|PASS|实际首扣血后暂停保存→新进程→2命中击杀，数据/经济身份核对|
|湖Boss跨进程伤害段|PASS|实际首扣血后暂停保存→新进程→9命中击杀，掉落与结算一次|
|伤害/技能/翻滚/死亡/首奖/重复奖励/恢复|PASS（受影响回归）|B07Combat六招命中/躲避/边界/中断/死亡；B07Interruptions/Economy/Rules四进程，不能当原生试玩|
|双武器冷却/随机/渡口/路线评分|PASS（受影响回归）|T06RegDualWeaponCheck、B3StreamRules、WGB1Check/Resume、RouteScoringRules/Resume|
|最终定向编排|31 PASS / 0 FAIL / 0 timeout|含1准备+30Unity步骤；不继承旧All154P或叠加26样本为新总数|
|非开发Windows构建|PASS，0错88警告|BuildOptions.None；BuildSummary、完整构建日志、exe/程序集SHA256；不声称运行时干净退出|
|正式驱动剔除/源与运行输入|PASS（静态产物审计）|102份runtime源和依赖一致；正式程序集无S2R1/Stage2/WG驱动；保护用户原字节|
|窄范围空引用/丢组件日志门禁|PASS|30日志0项；不是所有异常的全绿证明|
|v1～v9全量旧档矩阵重跑|NOT_RUN（本轮）|无存档字段/格式变化；本轮实际v9 Running/Pending/Committed和B07恢复回归通过，旧全量证据不继承|
|历史100规则/20实际seed|NOT_RUN（本轮）|生成/导航/碰撞及原通行驱动未改，仅引用历史范围；新战斗后撤的受影响三seed真实运行|
|最终Player原生UI/U16|NOT_RUN|没有安全独立原生交互会话；本轮没有把虚拟Editor输入冒充真实输入|
|四武器独立人工/理解|NOT_RUN|未安排独立玩家，截图/正常AI不替代|
|完整性能基准|NOT_RUN|模拟秒、构建45.8秒不冒充CPU/GPU/GC基准|
|D3D12 UNKNOWN、Editor青色帧|UNRESOLVED（历史）|无新因果证据，不重复关闭试验|
|Editor.Search根因|UNRESOLVED|本轮26条内部异常起始，完整栈保留，无未分类异常起始|
|JobTempAlloc因果栈|UNRESOLVED|本轮和历史构建日志均有；0退出不等于无异常，未归因产品事件|

## 不应忽略的失败

修复前汇总、分组漏筛、过严ACK校验、Play入口、无路后撤、同帧翻滚校准、尸体控制器校验、缺检查点恢复、旧All审计器不接受定向结束回执等均保留。详见[失败历史](FAILURE_HISTORY.md)。不存在将强制终止/超时改为正常退出PASS：本轮最终运行无超时/无遗留进程；此前缺检查点的拥有者Editor用明确的WM_CLOSE正常结束，仅为失败清理，未当原生U16或恢复成功。

最终可以提交S2-RV-01/02与观测子任务复审；阶段2整体/P0/发行验收仍开放，不能自动批准下一阶段。
