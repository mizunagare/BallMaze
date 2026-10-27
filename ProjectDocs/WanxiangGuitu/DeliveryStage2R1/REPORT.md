# S2-R1：回执一致性、统计总体与精确战斗观测

## 范围与版本

开始本地/远端main：`2ca1aac4bbf6fe6ca35a6604a2422dd79c889470`。产品/执行测试冻结：`583f19d905aa1b8d8b575f2441bf942b1e37b24f`。最终文档与证据SHA由交付消息及固定链接给出，不制造自引用提交。任务原文已[归档](../Reviews/Stage2_2ca1aac4_REVIEW_AND_S2R1_TASK.md)，SHA256在[开工回执](START_BASELINE.json)。远端初始读取通过已连接GitHub工具和本机既有代理的单命令参数复核；直连HTTPS的失败保留，不修改全局网络/快捷键设置。

本轮不是重做阶段2。产品只改 `CombatHealth.cs` 的只读真实HP转换事件；复用来源账、单自动档v9、唯一结算、三随机流、地图/导航、装备/制造和正常AI驱动。没有修改伤害、生命上限、冷却、AI、掉落概率、首奖或存档数据模型。原工程的用户未提交场景与设置保持原字节，且不提交；隔离场景字节相同，隔离ProjectSettings被Unity重序列化的差异仅为两个中文名称使用Unicode转义，含义未改，不能冒称隔离设置字节相同。

## S2-RV-01 / S2-RV-02

- 原ZIP的原汇总器blob23900d与4例复现均保留在[ReviewIntake](Evidence/ReviewIntake/intake.json)、[原结果](Evidence/OriginalReproduction/review-results.json)。正常控制成立，同时确实复现自报PASS/空Run、已出征缺指标漏总体、失败2秒混入60秒完整均值。这里的复现exit0代表旧缺陷被观察到，不是游戏通过或旧19条损坏。
- `DeliveryStage2/MatrixEvidence.py` 独立检查输入/哈希、Profile/Run/区域、实际阶段、进程退出、Pending/Committed/ACK及后继Run。ACK后活动Run可为空，但若填有其他Run则拒绝；经济类型要求整个链成立，明确终态类型才允许Death/Abandoned。没有自动补true或旧身份。
- `Invoke-Matrix`/`Invoke-NormalAI` 在首次进程前登记attempt与冻结配置、代码/驱动身份，实际检查点后形成阶段回执。工具状态、业务结局和测量完整性分开；已经启动/出征但缺指标仍计数。完整/撤离/死亡/放弃/部分窗口分别统计，三构筑分别筛选；未知不补死亡。空计划、全未启动、活进程/变化中的输入不终验PASS。
- 新35断言全部通过，R01～R14映射见[验收](ACCEPTANCE.md)。修复前29断言5P/24F及后续分组错误等失败全部保留；不将预期负例的子进程exit1当产品FAIL，也不抹掉失败断言。
- 冻结版R13：[19条只读投影](Evidence/Offline/Historical19Audit3/matrix-summary.json)19PASS、19已知Extracted、0未知；[214项主要值比较](Evidence/Offline/Historical19Comparison3.json)全一致。旧schema没有真实attemptId/阶段hash，不回填、不用于新协议放宽。

## 观测与有限实验

[完整合同](OBSERVATION_CONTRACT.md)明确三类时间：接敌/首次扣血、首次正扣血→真实死亡TTK、完整遭遇；Unity活动时钟为帧精度。首击击杀合法TTK0，不能推导无限DPS。玩家承伤按实际回调累计且标为多来源unattributed；治疗、重置、卸载、暂停和跨进程段均单独处理。监听器故障保留错误且不影响原伤害，观测写入故障不得提升为完整证据。

主矩阵按事前[MATRIX_INPUTS](MATRIX_INPUTS.json)仅18场：长剑普通近战敌9、弓对湖心潮灵9，三固定seed×三构筑；各条件n1，逐seed配对，不混作构筑总体因果比较。另8条仅用于四武器各一普通敌/一Boss覆盖。预试/校准/重试不混入18主矩阵，额外启动总数和失败在[失败历史](FAILURE_HISTORY.md)明确保留，不用重试挑出漂亮样本。

一次合法受控摆位在观测前完成，之后正常AI/碰撞/实际攻击与药水工作；不是完整徒步探索或原生键鼠。所有Boss保留原驱动先观察3次攻击。可选后撤增加完整NavMesh检查，仅避免测试命令走向水域无路径位置；不改导航、敌人或玩法数值，不换失败seed。主实验目标死亡/英雄死亡/180活动秒为终止条件，剩余Run正常放弃并提交/ACK；未捡地面掉落不计收益、不伪称成功撤离。

普通敌9例均真实首击死亡，未观察到构筑TTK差异。湖Boss差值仅按三个区组报告，样本不足以证明安全/讨伐的普遍优势；保留攻击前观察与全部窗口承伤，不把操作等待冒充输出效率。

两个独立恢复探针在真实首次扣血后背包暂停、原SaveProgress保存并正常退出，新进程核对同Run/目标/HP/RNG/装备/地面ID/来源账/徽章后继续击杀。通过检查点证明暂停间隙不计活动时间，显式对齐进程时钟段，不拿两个进程Time.time直接相减。真实掉落、重复DropLootOnce与重复结算不增奖。

## 真实运行与边界

主要运行根：`D:/WanxiangValidationRuns/S2R1/FrozenValidation/20261027-102526-ad379719`。准备、回归、26条受控战斗、两个跨进程恢复与非开发构建均在该独立副本；全步骤实际退出/超时原件见证据。普通完整冒险另外复用现有三阶段协议，实际采集/拾取/修渡口/撤离/入仓/制造/后继森林/新进程继续，不能与受控战斗混计。

|本轮层级|实际结果|口径|
|---|---|---|
|离线发布汇总断言|35 PASS / 0 FAIL|30预期exit1、1预期exit2子进程；不当作游戏失败|
|旧19条只读重审|19 PASS、214主要值一致|显式legacy投影，不补旧attempt|
|新冻结定向编排|31 PASS / 0 FAIL / 0 timeout|1准备+30Unity步骤，不是完整旧All重跑|
|主配对 / 四武器覆盖|18/18击杀、额外8/8击杀|6配对区组，每条件n1；不与步骤相加|
|普通敌 / 湖Boss恢复|各2个独立进程PASS|分别2命中TTK约0.667秒、9命中TTK约19.270秒；独立探针，不混入18|
|真实完整正常AI冒险|3进程PASS，新协议汇总PASS|采集/渡口/撤离/结算/制造/不同后继森林，单独来源证明|
|发布构建|PASS，0错88警告，约45.83秒|BuildOptions.None；所有警告原文保留|
|输入与驱动剔除|PASS（静态）|102份产品源和包/版本输入匹配，正式程序集无R1/Stage2/WG驱动|
|运行引用错误窄门禁|PASS，30日志0空引用/丢引用/丢组件|不是干净退出或所有异常通过|

构建exe SHA256 `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`；发布Assembly-CSharp.dll SHA256 `03ab9307350740daf59fbe593005de02b25f16c23c722e8aae1ea36c4dfd4c2b`。Unity6000.6.5f1、URP17.6.0/Input1.20/uGUI2.6不变。具体开始/结束、退出码、超时、原始命令与日志路径见[编排表](Evidence/FrozenValidation/Diagnostics/results.json)。

湖Boss按Gather/Boss相对Safety的TTK差（秒）：seed1为+0.198/+0.106，745672572为−0.743/−0.545，1132820888为−0.116/−1.151；承伤差分别+27.60/+18.60、0/0、+6.20/+6.20。药水/时钟/命中数在[逐例与配对分项](Evidence/FrozenCombat/combat-summary.json)，每个差只来自一对，变化包含真实运行/操作时序，不能据此宣称统计显著或Boss构筑全面优胜。

最终日志有26条Search内部异常起始、1条故意注入的观察者故障、0条未分类异常起始。另有历史构建中也出现的JobTempAlloc诊断，无新因果栈，继续UNRESOLVED；不能因构建/进程exit0说关闭干净。BuildReport88警告与日志182条warning/JobTempAlloc标记行是不同口径，完整原文和上下文在[审计](Evidence/FrozenReleaseAudit2/release-audit.json)。

冻结根记录466条游戏存档定位/操作，均在显式测试根内；这是受审计游戏保存操作的证明，不是对Unity授权服务/系统文件的全面I/O声明。原工程两份用户文件SHA256与开工完全相同，独立核对见[最终结果](Evidence/FINAL_RESULTS.json)。

没有改地图生成、NavMesh/碰撞算法和原Stage2Physics驱动；对新受控战斗的可选后撤检查，以三个种子和四武器场景验证受影响路径。旧100规则/20实际seed范围仅引用历史，未无差别重跑、不继承为本轮PASS。

原生UI/U16、四武器独立人工理解、完整CPU/GPU/GC性能本轮均NOT_RUN。D3D12 UNKNOWN、Editor青色帧、Editor.Search根因仍UNRESOLVED。受控Editor截图仅证明此测试运行画面存在，不关闭美术/动态体验验收。没有试探性改生命周期或重复无新线索的关闭实验。

## 交付限制

新汇总和观测子任务可按固定SHA复审，阶段2整体、P0和发行验收不因此通过。所有失败、早期输入差异、预期故障、历史占用进程与未执行项保留。仓库只发布脱敏日志/诊断/截图/哈希，不上传真实或完整合成存档、ground-loot分页、构建、转储、Library或凭据。交付后暂停，不启动新地图或下一阶段，也不声称已经后台触发独立复审。
