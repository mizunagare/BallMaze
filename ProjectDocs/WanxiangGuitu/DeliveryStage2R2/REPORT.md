# S2-R2：阶段结构、冻结合同和可信统计资格

开始本地/远端main：`b4a08e98f6de5cd56d192deb9f027f988d03afd9`。工具/测试冻结：`233db6a2027c462ee8cf2dc8c08b78b6412bed4e`。最终证据/文档SHA由交付消息给出，避免提交自引用。产品不变；Assets、Packages、ProjectSettings的已提交树不变，用户两份未提交文件原SHA256不变。

任务书已完整[归档](../Reviews/S2R1_b4a08e98_REVIEW_AND_S2R2_TASK.md)。S2-R1的产品观测、26场受控战斗、配对和恢复成果按本次限定复审保留；**S2-R1部分通过，三个P2工具问题并未在上一批全面关闭**。旧报告保留当时状态，新结论写在本目录，不重写历史。

## 来源与修复前复现

配套 `WanxiangGuitu_S2R1_Review_Evidence.zip` 在已检查的I盘根、下载目录、桌面、Codex附件目录未找到；已询问完整路径，截至交付材料整理时未收到。本轮**没有声称运行该ZIP或读到其未提供正文**，原包复跑记BLOCKED/NOT_RUN。已直接核对任务书提供的两个被审Git源码blob及SHA256，并从实际b4a08e98保存修改前源码，用任务书明确条件独立建立合成用例；不是猜测包内材料。

新矩阵修复前58断言16P/42F，保留每例输入、stdout/stderr、命令、退出码及断言。42是正确新要求未被旧版满足的断言数，包含错误结构漏过、合同缩减、启动/终态资格和诊断路径；不是42次游戏失败，也不是审核方原包12例的新执行结果。原35项在修改前仍35P，说明既有直接路径没有消失。

## 三项修复

### S2-R1-RV-01

所有实际必需process/stage文件先解析，再独立要求根为对象。null、数组、字符串、布尔值与其他标量均记具体文件错误；空对象、缺字段、错误schemaVersion/类型、身份或阶段不符均不具有完成资格。process不合格不能跳过同阶段结构诊断。保留原JSON，不重建回执。

### S2-R1-RV-02

增加**验收合同归一化版本1**，不是玩家存档版本。稳定条件包括原CORE（id/build/strategy/seed/weapon/target）、记录时的kind/blockId，以及contractVersion/contract/expectedOutcome/acceptedOutcomes/requiredModes。计划、真实冻结输入、指标内input三方归一化比较，仍保留原配置字节hash核验。描述文字description/scope不改变验收合同；阶段顺序与接受结局按语义集合规范化。

- 缺省版本1；缺省economy/Extracted/只接受Extracted/三个独立阶段。显式等价默认值兼容。
- economy不能单凭计划甚至三处一起改成只需Normal；它的成功定义仍要求三阶段实际恢复与完整经济链。
- terminal缺省仅Normal，或按冻结合同声明更多必要阶段；必须含Normal。真实Death/Abandoned可以合法通过该终态观测合同，不误要求后继Run。
- requiredModes的实际检查优先读取已绑定的冻结输入，不让计划独自缩减证据。版本不支持、预期与接受集合不一致、合同漂移均失败。
- 不增加或回填历史attempt/hash。旧19条仅显式legacy投影；已有现代attempt/stage时，即使显式传legacy参数也拒绝降级，仍按现代冻结身份检查；schema2的原冻结身份继续原样核验。

### S2-R1-RV-03

注册与启动分开，`attempt.launchedUtc`在现有编排实际上是启动前登记字段，不能单独证明执行。仅NOT_RUN行、仅登记、登记后占用跳过均为started0/departed0；保留registered及登记来源。现有根目录sidecar登记也读取，不修改PowerShell或造新启动时间。实际进程退出/超时证据、非NOT_RUN执行步骤、已产生指标和实际depart提供各自运行痕迹；出征计数要求记录完整身份的depart，不凭指标中的一个Run字符串推断。

原始终态声明和可信终态分列。必须归属于独立depart身份，Run/Profile/区域错配、显式无效结局或相互矛盾均为Unknown/conflict，不进knownTerminal或extracted。后出现的正确文件不能覆盖既有冲突。若首次终态身份及结局已确认，仅后继进程失败，则仍保留已知业务结局，但工具FAIL、诊断标记true，不能进入完整合同窗口统计。行级问题也设置statisticsDiagnosticOnly，CSV同时带可信/冲突/技术/诊断字段。

实际旧Stage2 Snapshot没有outcome字段，结局由独立的`b4-first-settlement.json`实际Run及枚举提供。只读核验这一真实来源，不根据metrics.extracted猜结局、不把缺字段填回旧文件；显式null不是旧字段缺省，也不能被另一个正确文件抹掉。首轮兼容误拒及修正依据保留。

## 本轮实际执行

|层级|结果|限定|
|---|---|---|
|原35断言（补齐合法夹具后）|35 PASS / 0 FAIL|原期望值全保留；原不完整夹具后的29P/6F单独保留|
|新增有限矩阵|58 PASS / 0 FAIL|含12种三阶段根类型负例、缺字段/合同/default/启动/冲突/晚期失败；负子进程非零为预期|
|历史只读重审|10组、46原有案例通过|19历史＋26受控＋1完整三进程，不是新战斗样本|
|原值比较|828行级原值及50个组级值一致|身份、承伤、时长、材料、生命周期等不改写；新增统计资格字段单列|
|原26行战斗CSV|原字节SHA256一致|`e3ea4b3358e5ea40af21f01e583e530764a4de80ec7b4c9410e81f4685ddef7d`，未新增TTK指标|
|配套ZIP原样复跑|BLOCKED / NOT_RUN|缺本机路径；任务书条件已独立复现，不冒充原包执行|
|产品/Unity/Player/非开发构建|产品不变；运行NOT_RUN|纯离线补丁，不继承旧31步/26战斗/100规则/20通行或构建为新PASS|

工具与测试是本机Python执行，无Unity/网络依赖。没有修改Assets、PS回执执行路径、随机流、存档、来源账、结算、地图或数值；没有新增CI或依赖。历史源manifest审计前后完全相同，输出写入独立新目录。S2-R1的旧报告、失败和所有实际数据保留。

源码、命令、退出码、断言和差异见[验收](ACCEPTANCE.md)、[复跑](TESTING.md)、[失败历史](FAILURE_HISTORY.md)、[证据索引](Evidence/INDEX.md)。原生UI/U16、独立人工、完整性能保持NOT_RUN；UNKNOWN/青色帧/Search/JobTempAlloc根因保持UNRESOLVED。工具验证通过不自动关闭阶段2、P0或发行验收；交付后暂停，等待固定SHA复审。
