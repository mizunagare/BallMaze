# 《万象归途》S2-R1 固定提交复审与 S2-R2 最小校验补丁任务书

日期：2026-10-27  
仓库：`mizunagare/BallMaze`  
本次审核提交：`b4a08e98f6de5cd56d192deb9f027f988d03afd9`  
产品/测试冻结输入：`583f19d905aa1b8d8b575f2441bf942b1e37b24f`  
上一轮基线：`2ca1aac4bbf6fe6ca35a6604a2422dd79c889470`  
建议归档：`ProjectDocs/WanxiangGuitu/Reviews/S2R1_b4a08e98_REVIEW_AND_S2R2_TASK.md`。

## 0. 复审结论

**结论：S2-R1 部分通过。保留产品观测、受控战斗、配对和恢复成果；原汇总问题的直接复现路径已修复，但回执校验和统计资格仍有三个有独立复现的 P2 问题，不能将 S2-RV-01/02 全面关闭。下一轮仅做 S2-R2 离线校验补丁，不重做玩法，不新增战斗实验规模，不启动新地图。**

在本次已审查范围内，没有发现要求回滚 `CombatHealth` 观测改动或重做26条战斗实验的 P0/P1 产品缺陷。这里的三个 P2 是验证工具问题，不是已经证实游戏掉档、伤害计算错误或历史26条战斗数据受污染。

本任务延续上一轮已经要求的“错误类型不能通过、冻结输入和阶段一致、未启动/未知/技术失败分开”，不是提高战斗难度、增加平衡指标或要求无休止扩测。

### 0.1 本次实际做了什么

- 通过已连接 GitHub 读取远端 main、固定提交差异、Git 子树、产品代码、汇总器、测试驱动、报告、验收和选定证据。
- 阅读真实伤害事件、观测器、暂停检查点/新进程恢复、受控战斗驱动、边界测试及发布汇总路径。
- 将两份 Python 审计源码复制到独立环境，逐字节计算 Git blob，与远端返回的 blob SHA 对齐，然后执行12个独立合成场景。
- 先按冻结版执行同一组12场景，再确认最终版仅改变模块首行说明文字，并按最终版重新执行同一组12场景。两轮不是24个不同验收条件。
- 对已提交的26行战斗 CSV 独立计数、检查唯一身份、复算 `TTK = death - firstDamage` 以及三种子的配对差值；CSV 原始 CRLF 字节与远端 blob 一致。
- 本次没有修改仓库、没有推送、没有独立重跑 Unity、Windows Player、原生输入、人工试玩或性能。
- 交付方的35项离线回归、31项 Unity 定向验证、214项历史对照仍是交付方记录；本次没有把它们冒称为审核方重新执行。没有通读全部原始日志、逐张审核截图或独立完成 LFS 全对象下载核验。
- 用户本机未提交文件的原始哈希保护属于交付方证据；远端目录未变不能证明本机当前状态。

### 0.2 独立复现材料

配套包：`WanxiangGuitu_S2R1_Review_Evidence.zip`。

包内包含本次实际执行的最终源码、冻结版模块快照、源码身份核验、合成输入、stdout/stderr、汇总输出、26行已提交CSV及独立算术核对。

```bash
python reproduce.py --output <不存在的绝对路径>
```

该入口只复现本次被审版本的行为，不读取玩家存档，不启动 Unity，不联网。其观察结果中包括错误的 PASS；不能将“成功复现缺陷”当作产品通过。修复后的验证应在独立候选目录执行，不覆盖包内原始版本或已有结果。

## 1. 版本与输入核对

审核时远端 `main` 为本次交付 `b4a08e98f6de5cd56d192deb9f027f988d03afd9`。

从开始基线到冻结输入的产品差异只有 `Assets/CombatPrototype/CombatHealth.cs`，其余变更属于验证脚本、测试、任务书与相关文档。冻结输入与最终交付的以下已提交子树一致：

|目录|Git tree SHA|
|---|---|
|Assets|`a05cd503a3b3ca3f8aa0bc7d42d04c241848454f`|
|Packages|`ca46f9594c2ecab1788502c0b88092762f4c805d`|
|ProjectSettings|`70ef819d3b93250c44a0b58f3b4cf2ed2d740a6c`|

审计模块最终版与冻结版的 blob 不同，原因已经核对：**仅首行模块说明文字改变，执行代码相同**。本次最终离线复现使用最终交付版，不把它冒称为冻结版的全字节相同文件。

|文件|最终 Git blob|最终文件 SHA256|
|---|---|---|
|`DeliveryStage2/MatrixEvidence.py`|`ee2f3973e74ea54cb0eda37e007c2b1315624b09`|`cdf0cc9e94156d127ef5a310b427f71492a05d7ae321bb6dc56489ba59af56b8`|
|`DeliveryStage2/Summarize-Matrix.py`|`5bd06e6bc57f20508e75618610ede40a3582253d`|`299d01029a1b26c30bf62c734aff44cc9eda5fb3b10d3ceef695fb14b73fe311`|
|`Evidence/FrozenCombat/combat-results.csv`|`1b4489995867c0beb0dd125676aab53a6c1d5814`|`e3ea4b3358e5ea40af21f01e583e530764a4de80ec7b4c9410e81f4685ddef7d`|

下一轮从实际最新 main 继续；先比较后续变更，不 reset 回这些 SHA，不覆盖用户修改。

## 2. 本轮保留的成果和限定认可

### 2.1 原问题的直接路径已修复

本次独立实跑确认：

- 合法完整对照仍输出 PASS。
- 自报 PASS、Run 为空且四个完成布尔值为 false 的旧反例已被拒绝。
- 必需阶段文件真正不存在时会被拒绝。
- 已出征但指标文件缺失的案例保留在 started/unknown 总体，不再静默消失。
- 一条完整60秒加一条失败时只记录2秒的案例，完整耗时均值为60秒，2秒单列部分窗口，不再算成31秒。

这证明此次修改有效。第3节的问题是同一合同中尚未封住的分支，不表示以上修复不存在。

### 2.2 产品观测接线

`CombatHealth` 在真实扣血位置采样 before/after、活动时钟和死亡转换；治疗、重置、恢复、卸载分开通知。新增监听器异常单独记录，原有伤害/反馈异常传播未被整体吞掉。原伤害决策、防御、营地阻断、无敌帧以及累计伤害语义保留。

`S2R1Observation` 将首次实际扣血到死亡、接敌等待、整个遭遇分开记录。首击击杀可合法为TTK=0，同帧两次命中也可TTK=0，不能由此推断无限DPS。时钟是 Unity 活动时间的帧精度，不因 JSON 小数位很多而变成亚毫秒测量。

恢复实现使用暂停后的持久检查点和实验侧分段偏移，不直接以新进程的 Time.time 减旧进程的 Time.time；恢复核对 Run/目标/HP/随机状态/装备/来源账/地面ID/徽章等。现有受控规则覆盖同帧、回血、过量、零伤害、无敌、重置、卸载、暂停及观察者异常。

在上述已读代码和提交证据范围内，未发现需要本轮重写这一观测子系统的阻断问题。**属于限定源码/证据认可，不是审核方新取得的 Unity 运行 PASS。**

### 2.3 26条战斗记录独立核算

对已提交CSV的独立核对结果：26行、26个不同Run、26个不同attempt，其中18条主配对、8条额外覆盖；26行的TTK均等于其死亡时钟减首次实际扣血时钟。

普通敌9条主配对全部为1次实际命中击杀、TTK=0、承伤0。它们证明本次样本的首击行为，**不能证明三构筑在普通战斗中已经形成明显强弱差异**，也不需要为此临时加怪物血量或调装备。

湖Boss相对Safety的TTK差，独立重算与报告四舍五入值一致：

|seed|Gather − Safety（秒）|Boss − Safety（秒）|
|---|---:|---:|
|1|+0.198|+0.106|
|745672572|−0.743|−0.545|
|1132820888|−0.116|−1.151|

每个完全相同条件n=1；三个seed是三个区组，不是同条件重复三次。数据不能支持“Boss构筑在所有条件下都更快”或“已完成平衡”。原报告保留这一限制是正确的。

## 3. 尚未关闭的三个 P2 问题

共同源码：`ProjectDocs/WanxiangGuitu/DeliveryStage2/MatrixEvidence.py`，以下代码行号以最终提交为准。

### S2-R1-RV-01：必需阶段回执的错误 JSON 类型被跳过，最终仍 PASS

位置：第116～123行，重点第118行：

```python
stage = load('stage-result-' + mode + '.json', True)
if not isinstance(stage, dict):
    continue
```

`load` 对缺失文件和损坏JSON会记 issues，但对**合法JSON、错误结构**的 `null`、`[]`、字符串、布尔值不会自动报错。这里直接 continue，导致所有阶段字段校验被跳过，且没有给案例增加失败原因。

独立复现：基于合法三阶段经济闭环，仅将 `stage-result-Resume.json` 分别改成 `null`、`[]`、`"complete"`、`false`；其余输入、进程和回执保持不变。

四个负例实际均为：

```text
exitCode = 0
status = PASS
finalAcceptanceEligible = true
```

对照：删除同一文件时会正确FAIL。因此这是“文件存在但结构错误”的漏检，不是不存在的阶段被上游正常执行补证。

整改：所有必需回执必须通过根对象类型与结构验证；错误类型必须记录具体文件/字段、给出非零退出，并禁止完成资格。不要只特判数组；null、标量、空对象和缺字段分别处理。原始证据不自动转换成 `{}`、不自动补字段。

证据：`results/final_commit/04-stage-*/`；控制组为`01-control`，缺失对照为`03-stage-missing-rejected`。

### S2-R1-RV-02：验收合同字段没有与冻结输入一致性绑定

位置：第4行CORE、第54～60行配置比较、第111行阶段循环及第125～128行合同选择。

当前输入比对只覆盖`id/build/strategy/seed/weapon/target`。`requiredModes`、`contract`、`expectedOutcome`、`acceptedOutcomes`等决定验收范围的字段来自计划，但未统一与实际冻结案例输入进行语义核验。

独立复现：保持原`stage2-input.json`、指标内input和其配置hash完全不变；仅把审核计划中的经济闭环案例改成`requiredModes=["Normal"]`，删除Resume和FinalResume共四份进程/阶段回执。其余生命周期事务仍保留。

实际输出仍为`exit0 / PASS / finalAcceptanceEligible=true`。

这意味着计划侧可以单独缩减“必须提交什么证明”，而工具不报告计划与实际输入的合同漂移。后继Run的一条事务文字不能替代两个独立进程的完成证明。

整改：定义版本化、归一化的案例合同，比较所有影响验收的字段，并明确默认值。经济闭环的实际三阶段证据不得单靠计划字段缩减；终态受控战斗可以合法只需Normal，**不能为了修该问题把所有terminal案例强制成三阶段**。

隐式默认值与语义等价的显式默认值应兼容；改变合同、可接受结局或必要阶段必须被识别。新数据使用真实冻结身份；旧数据只走明确的legacy投影，不回填虚构hash/attempt。

证据：`results/final_commit/09-plan-input-contract-mismatch/`。该反例是冻结合同一致性检查，不是认定本轮真实计划被人为改写。

### S2-R1-RV-03：未启动和有身份冲突的终态仍可能进入错误的统计总体

**分支A：明确NOT_RUN仍算started。**位置第40、51行。

`started`把任何相关results行都当作已启动，未检查这些行是否只是NOT_RUN。只保留三条`Normal/Resume/FinalResume=NOT_RUN`，不提供任何实际启动、指标或出征证据，结果仍是：

```text
started = 1
departed = 0
notStarted = 0
status = FAIL
```

应保留计划尝试但不能虚构启动。当前`Invoke-Matrix.ps1`本身存在“项目被占用→Note NOT_RUN→跳过后续阶段”的真实路径，因此该输入不是与现有编排无关的假设。

注册attempt和实际启动必须区分；注册时写的时间不能自动证明子进程已经运行。实际depart可以反证已启动；单独NOT_RUN行不能。

**分支B：已经判定身份冲突的终态仍算已知撤离。**位置第91～110、164～168行。

独立复现：只把`settlement-pending`中的Run/Profile/region改成另一个身份，保留`outcome=Extracted`。工具正确将案例标FAIL并列出身份冲突，但汇总仍为：

```text
knownTerminal = 1
extracted = 1
extractionSuccessRate = 1.0
statisticsDiagnosticOnly = false
```

这不是“本Run已经可信地撤离，只是后续进程失败”，而是终态证据本身无法归属于本Run。不能把这个证据继续纳入本Run的已知结局分母和撤离分子。

整改：以终态身份和一致性验证的结果决定knownTerminal资格；原始声明结局与可信结局分开保留。冲突不能自动变成死亡，也不能让后出现的文件无条件覆盖冲突。统计诊断标识必须反映影响统计的行级问题，而不仅看globalIssues。

注意：如果终态身份已确认、只是后继进程技术失败，已知业务结局仍可以保留。这与“身份冲突所以结局未确认”不同，不能用“所有FAIL都排除”粗暴修复。

证据：`results/final_commit/07-all-explicitly-not-run/`及`08-conflicting-terminal-counted/`。

## 4. 独立离线结果汇总

|场景|被审版本实际结果|本次判断|
|---|---|---|
|合法完整三阶段|PASS|正常对照成立|
|旧空Run/假完成组合|FAIL|旧直接反例已修复|
|必需阶段文件缺失|FAIL|缺失检查有效|
|阶段JSON为null/数组/字符串/布尔值，4例|全部PASS|S2-R1-RV-01成立|
|已出征但缺指标|保留started2、known1、unknown1|旧丢失尝试问题已修复|
|完整60秒＋失败2秒|完整均值60、2秒单列|旧窗口混算问题已修复|
|所有步骤明确NOT_RUN、无实际启动|started1/notStarted0|S2-R1-RV-03A成立|
|终态属于其他Run/Profile/region|整批FAIL，但已知撤离率100%、非诊断标记|S2-R1-RV-03B成立|
|计划单独缩减为Normal、删后两阶段回执|PASS|S2-R1-RV-02成立|

合计12个不同场景。结果不是“12项产品PASS”；包含应失败却通过和统计分类错误。

原19条、现有26条与真实完整正常AI三进程的原始成果全部保留。以上合成输入不证明这些历史运行已经出现同类损坏；下一轮应使用修复版只读重审，不改历史原件。

## 5. 下一轮唯一任务：S2-R2（纯离线校验闭环）

建议交付目录：`ProjectDocs/WanxiangGuitu/DeliveryStage2R2/`。

### 5.1 允许修改范围

- `DeliveryStage2/MatrixEvidence.py`、`Summarize-Matrix.py`及相关离线测试。
- 必要的案例合同默认值/版本、attempt登记与已启动证据说明；确需调整现有PowerShell回执字段时，只做与这三项问题直接有关的最小修改。
- 新报告、验收、复跑说明、失败历史与当前路线台账。

**默认不修改Assets、Packages、ProjectSettings，不改CombatHealth，不重写观测器，不新增TTK方案，不扩配对规模。**

### 5.2 实施顺序

先复现并保存本任务书的旧行为；补失败回归；修三个问题；跑现有35项及新增离线矩阵；只读重审已有真实证据；解释差异后交付。

不是再提交一份“计划修复什么”的文档后停工，也不将已完成的战斗功能再做一遍。

### 5.3 具体实现约束

必需文件“读取成功”和“满足结构”必须是两个检查；任何结构错误都应带路径进入结果，不静默continue。不要为了终验全绿把失效证据重建成通过回执。

验收合同先归一化再比较：明确哪些字段属于稳定验收语义、哪些只是描述性元数据。默认economy合同应具有先前定义的三阶段恢复要求；合法terminal合同按实际目标选择必要阶段。不能用降低requiredModes来绕开经济恢复，也不能把历史缺字段猜成新schema。

统计至少能区分计划/注册、实际启动、实际出征、可信终态、终态冲突/未知与技术失败。可以在现有结构内增加少量字段，不另建调度平台或数据库。未知、错误和完整窗口分别输出；诊断性数字的限定必须留在相邻字段和报告中。

## 6. S2-R2 最低离线验收矩阵

以下是本轮的固定、有限范围；无需追加新玩法或更多真实战斗样本。

|编号|场景|必须结果|
|---|---|---|
|R2-01|合法economy三阶段|PASS，身份/终态/后继与必需阶段均有效|
|R2-02|合法terminal，仅Normal，真实Death或Abandoned|按该合同PASS；不误强制后继Run|
|R2-03|Normal/Resume/FinalResume各自为null、数组、字符串、布尔值|12个结构负例均拒绝，具体文件路径可查|
|R2-04|必需回执为空对象、缺字段、损坏JSON或缺文件|拒绝；不自动补数据|
|R2-05|只改计划requiredModes并删除后续证明|拒绝冻结合同不一致，不能PASS|
|R2-06|只改contract/expectedOutcome/acceptedOutcomes|分别识别真正语义漂移；不能偷换验收规则|
|R2-07|隐式默认和等价显式默认|正常兼容；与缩减语义严格区分|
|R2-08|全部相关步骤NOT_RUN、无实际启动|started0/departed0/notStarted=计划数；rate=null；整批不得PASS|
|R2-09|只有attempt登记/注册时间，启动前被阻断|登记保留，但不写成真实已启动/出征|
|R2-10|实际depart后缺最终指标|started/departed保留，结局未知和技术状态正确；不丢分母|
|R2-11|pending终态Run/Profile/region不匹配，或终态证据相互矛盾|明确冲突，不加入可信撤离分子/已知终态分母；不补死亡|
|R2-12|终态已可信确认，但后继进程失败|工具FAIL；已确认业务结局不被一刀切删除，完整窗口资格单独判断|
|R2-13|完整60秒＋部分2秒|完整均值60；2秒单列，不混算|
|R2-14|重复/空计划/输入变化/未结束等已有35项覆盖|继续满足原合同，失败历史保留|
|R2-15|历史19条、新26条各组、完整正常AI三进程只读重审|完整合法输入主要数值保持；新发现冲突逐项报告，不修改历史原件|

必须保存候选源码hash、执行命令、退出码、stdout/stderr和断言结果。负例子进程按预期退出非零，可使对应断言PASS；不能把子进程非零统一计为游戏失败或吞掉。

旧35项中的夹具若因更准确的合同定义需要调整，逐条解释原夹具为何不代表合法场景，保留旧结果；不得只改期望值让问题变绿。

## 7. 历史数据兼容与复跑边界

新输出写入独立目录，保留源manifest/hash。历史schema与新schema明确分开；可以按真实旧字段生成只读投影，不能回填虚构attempt、启动时间或阶段hash。

只读重审对象包括：阶段2历史19条；S2-R1的18主配对和8覆盖的实际分组回执；S2-R1完整正常AI三进程的真实回执。不要把受控终态战斗强行当作撤离/制造经济闭环。

对发生变化的统计字段逐项解释：错误资格或诊断标记应改；原始承伤、TTK、材料数量、Run/attempt身份不应因为修汇总而被重写。原始阶段记录若不足以支持某个新主张，标legacy限制或未验证，不能猜测填充。

**仅修改离线审计和测试时，本轮Unity构建、31步定向验证、26场战斗、100规则seed和20实际通行均记本轮NOT_RUN/未重跑，注明与改动无关；不继承为本轮PASS，也不要求无差别重跑。**

若修改回执登记PowerShell，优先做不启动Unity的脚本级/合成进程回执测试；只有确实改变了游戏执行路径且离线证据不能覆盖时，说明具体影响并运行最小相关验证。不要把三个脚本问题扩大成整批游戏返工。

## 8. 交付文件与退出条件

最少交付：

```text
DeliveryStage2R2/
  REPORT.md
  ACCEPTANCE.md
  TESTING.md
  FAILURE_HISTORY.md
  Evidence/INDEX.md
  Evidence/...
```

同步更新当前计划/现状审计对本轮的引用；保留S2-R1历史报告，新增复审差异或新报告，不回写历史PASS为当时已经发现的问题。

退出条件：三个问题均有修复前复现与修复后拒绝/正确统计；合法economy/terminal不误杀；旧35项和本轮新增矩阵有效；历史只读重审及差异说明完整；没有修改游戏数值、存档、随机、地图、用户文件或依赖。

通过后只关闭验证工具这三项及相应S2-RV剩余问题。原生UI、独立人工试玩、完整性能和历史引擎根因仍分别留账；不因脚本全绿自动宣布阶段2整体完成。

本轮收尾不再自动追加新的配对试验、TTK指标或“再做一份方案”。下一次固定SHA审核通过后，再根据实际玩家/视觉缺口制定内容开发批次。

## 9. GitHub交付与协作

本地实施和测试，不开启云端Work、不启用CI、不升级Unity/包、不访问真实玩家档、不抢用户桌面、不强杀既有进程。

保护用户场景、ProjectSettings和其他未提交修改，不reset、不force push、不重写历史。按已授权流程提交推送现有main；若分支保护阻止，按允许的分支/PR路径交付，不绕过权限。

执行前重新核对main。产品未修改时明确“产品不变”；工具冻结SHA与最终文档/证据SHA分别列出。推送后核对远端完整SHA；不在同一提交内制造自引用SHA要求。

交付后暂停，将以下信息实际发回本审核对话。GitHub推送本身不会自动触发此处审核，未建立通知任务时不声称已后台通知。

```text
批次：S2-R2
开始基线：<完整SHA>
工具/测试冻结：<完整SHA>
最终交付：<完整SHA>
远端复核：<结果>
S2-R1-RV-01：<结构错误拒绝结果>
S2-R1-RV-02：<合同绑定/默认兼容结果>
S2-R1-RV-03：<未启动/可信终态/诊断统计结果>
离线回归：<旧35项/新增矩阵，分别记数>
历史19＋26＋完整三阶段只读重审：<实际范围、差异与legacy限制>
产品/Unity/构建：<不变/NOT_RUN或实际最小运行>
用户文件保护：<结果>
原生/人工/性能及历史根因：<原状态>
报告/验收/复跑/证据：<固定SHA链接>
已暂停，不进入新地图或下一阶段。
```

## 10. 固定来源索引

所有事实均指固定提交，不把后续main改动反写成本次审查内容。

- [S2-R1报告](https://github.com/mizunagare/BallMaze/blob/b4a08e98f6de5cd56d192deb9f027f988d03afd9/ProjectDocs/WanxiangGuitu/DeliveryStage2R1/REPORT.md)
- [S2-R1验收](https://github.com/mizunagare/BallMaze/blob/b4a08e98f6de5cd56d192deb9f027f988d03afd9/ProjectDocs/WanxiangGuitu/DeliveryStage2R1/ACCEPTANCE.md)
- [证据索引](https://github.com/mizunagare/BallMaze/blob/b4a08e98f6de5cd56d192deb9f027f988d03afd9/ProjectDocs/WanxiangGuitu/DeliveryStage2R1/Evidence/INDEX.md)
- [最终结果/保护记录](https://github.com/mizunagare/BallMaze/blob/b4a08e98f6de5cd56d192deb9f027f988d03afd9/ProjectDocs/WanxiangGuitu/DeliveryStage2R1/Evidence/FINAL_RESULTS.json)
- [矩阵审计模块](https://github.com/mizunagare/BallMaze/blob/b4a08e98f6de5cd56d192deb9f027f988d03afd9/ProjectDocs/WanxiangGuitu/DeliveryStage2/MatrixEvidence.py)
- [阶段回执错误类型分支](https://github.com/mizunagare/BallMaze/blob/b4a08e98f6de5cd56d192deb9f027f988d03afd9/ProjectDocs/WanxiangGuitu/DeliveryStage2/MatrixEvidence.py#L111-L123)
- [汇总CLI](https://github.com/mizunagare/BallMaze/blob/b4a08e98f6de5cd56d192deb9f027f988d03afd9/ProjectDocs/WanxiangGuitu/DeliveryStage2/Summarize-Matrix.py)
- [提交方35项离线回归源码](https://github.com/mizunagare/BallMaze/blob/583f19d905aa1b8d8b575f2441bf942b1e37b24f/ProjectDocs/WanxiangGuitu/DeliveryStage2R1/Tests/Test-Summary.py)
- [矩阵启动与NOT_RUN路径](https://github.com/mizunagare/BallMaze/blob/583f19d905aa1b8d8b575f2441bf942b1e37b24f/ProjectDocs/WanxiangGuitu/DeliveryStage2/Invoke-Matrix.ps1)
- [产品健康观测](https://github.com/mizunagare/BallMaze/blob/583f19d905aa1b8d8b575f2441bf942b1e37b24f/Assets/CombatPrototype/CombatHealth.cs)
- [战斗观测器](https://github.com/mizunagare/BallMaze/blob/583f19d905aa1b8d8b575f2441bf942b1e37b24f/ProjectDocs/WanxiangGuitu/DeliveryStage2R1/Tests/S2R1Observation.cs.txt)
- [跨进程恢复驱动](https://github.com/mizunagare/BallMaze/blob/583f19d905aa1b8d8b575f2441bf942b1e37b24f/ProjectDocs/WanxiangGuitu/DeliveryStage2R1/Tests/S2R1Recovery.cs.txt)
- [边界规则](https://github.com/mizunagare/BallMaze/blob/583f19d905aa1b8d8b575f2441bf942b1e37b24f/ProjectDocs/WanxiangGuitu/DeliveryStage2R1/Tests/S2R1BoundaryRules.cs.txt)
- [26条战斗CSV](https://github.com/mizunagare/BallMaze/blob/b4a08e98f6de5cd56d192deb9f027f988d03afd9/ProjectDocs/WanxiangGuitu/DeliveryStage2R1/Evidence/FrozenCombat/combat-results.csv)

---

文档结束：包含固定版本、限定认可、三个确定性问题、12场景复现、S2-R2允许范围、最低矩阵、重审与复跑边界、交付协议和来源。当前仅供Codex实施与提交，审核方未修改GitHub。
