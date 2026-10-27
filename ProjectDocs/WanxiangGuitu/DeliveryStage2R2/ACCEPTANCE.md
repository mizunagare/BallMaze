# S2-R2 验收矩阵

工具/测试冻结`d5d3fd7c98b78ccc4bd4a781c0dd5d9ad1529e7c`。结果为本地交付验证，不是新的独立审核结论。S2-R1保留限定认可及部分通过，不回滚产品，不反写历史PASS。

|任务项|本轮结果|证据及限制|
|---|---|---|
|RV-01：阶段读取与结构分开|PASS|三阶段×null/数组/字符串/布尔值12负例均拒绝，精确文件名；空对象/缺字段/坏JSON/缺文件另12例；不静默continue|
|RV-02：完整绑定冻结合同|PASS|计划、真实输入、指标input的版本化语义一致；单改合同/预期/接受集合/必要阶段/目标kind均拒绝|
|RV-03：实际启动/可信终态/诊断资格|PASS|仅NOT_RUN及仅注册不算启动；冲突终态Known0、不补死亡；可信终态＋后继失败仍known，但工具FAIL及诊断true|
|R2-01|PASS|合法economy三阶段完整，不能只靠计划缩减|
|R2-02|PASS，2例|合法terminal Death/Abandoned只需Normal，不误要求后继|
|R2-03|PASS，12例|每个必需阶段四类错误根结构全部拒绝|
|R2-04|PASS，12例|每个必需阶段空对象、缺字段、坏JSON和缺文件分别拒绝|
|R2-05|PASS，2例|计划单独缩减及三处声明一起将economy缩减都不能通过|
|R2-06|PASS|contract/expectedOutcome/acceptedOutcomes/contractVersion/指标input/目标kind语义漂移；接受集合仍容纳真实结果也不能偷换expectedOutcome|
|R2-07|PASS|隐式/等价显式默认双向兼容；description说明文字不改变验收|
|R2-08|PASS|仅NOT_RUN：started0/departed0/notStarted1/rate=null|
|R2-09|PASS，2例|注册保留registered1；仅登记或登记后跳过均不是启动|
|R2-10|PASS|实际depart后指标缺失，started/departed保留，unknown/技术状态不丢失|
|R2-11|PASS|Run/Profile/区域错配或缺失、相互矛盾、后文件覆盖、独立结算错Run、显式null均不计可信结局；原声明保留|
|R2-12|PASS|可信Extracted＋后继进程失败：工具FAIL、known1/extracted1、诊断true、完整统计n0|
|R2-13|PASS|完整60秒＋部分2秒，完整均值60，2秒单列|
|R2-14及原35|35 PASS / 0 FAIL|重复/空/变化/未结束等原断言不变；合法fixture补唯一region字段，旧29P/6F不删|
|R2-15|10组/46案例重审PASS|19历史、26战斗、1案例真实三进程；不是46次新运行|
|真实旧Snapshot兼容|PASS|缺outcome时必须有实际匹配结算记录，不从指标猜；显式null不能作为缺省|
|原值/原CSV|PASS|828行级值＋50组级值一致；CSV原始SHA不变；源manifest前后不变|
|冻结新增矩阵|58 PASS / 0 FAIL|原35与新增58分别计数；负子进程非零是预期，不算游戏失败|
|配套ZIP原包读取/12例原样复跑|PASS（来源/复现）＋12候选断言PASS|476文件核验，原脚本原样执行；候选只读同一批输入，旧结果/包内源码不改|
|Assets/Packages/ProjectSettings/产品观测|不变|只读核验树与用户字节；没有修改CombatHealth/观测器/游戏字段|
|PS启动路径|不变|仅解释和读取现有sidecar/登记字段，没有改调度器或启动Unity|
|Unity/31步/26场战斗/构建|NOT_RUN|纯离线修改，无相关执行路径变更，不继承历史PASS|
|100规则seed/20场景通行|NOT_RUN|无生成/导航/碰撞变更，不无差别重跑|
|原生UI/U16|NOT_RUN|没有新原生交互验收|
|独立人工理解与四武器试玩|NOT_RUN|未执行，不以离线或旧截图替代|
|完整性能|NOT_RUN|不将Python耗时/活动模拟时钟冒充CPU/GPU/GC基准|
|UNKNOWN/青色帧/Search/JobTempAlloc根因|UNRESOLVED|无新调查或生命周期改动，状态不自动关闭|

修复前58矩阵16P/42F、原35新严格校验29P/6F及首轮历史兼容拒绝均保留。完整出处见[失败历史](FAILURE_HISTORY.md)与[索引](Evidence/INDEX.md)。当前可提交三项工具补丁复审，原包来源核验已补齐；不能自认阶段2整体或发行验收通过。
