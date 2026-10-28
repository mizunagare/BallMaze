> INPUT-01已增量交付，产品/执行测试冻结f16bdcaee45553c9d53d525bdceecdd2e2238a1a；[报告](DeliveryInput01/REPORT.md)、[动作表](DeliveryInput01/INPUT_ACTIONS.md)、[验收](DeliveryInput01/ACCEPTANCE.md)、[复跑](DeliveryInput01/TESTING.md)、[证据](DeliveryInput01/Evidence/INDEX.md)。I01～I13有限自动化PASS；I14产物可生成/启动但URP包2条Error与91警告，质量UNRESOLVED；I15原生/人工NOT_RUN。保留所有旧状态和原始失败，交付后暂停待固定SHA复审，不自行认定通过或开启新批次。

# 当前执行：INPUT-01 键鼠重绑定与统一提示

2026-10-27收到[固定a5e77006复审与任务书](Reviews/S2R2_a5e77006_REVIEW_AND_INPUT01_TASK.md)：S2-R2在限定源码、离线实跑及证据抽查范围内通过，S2-R1-RV-01／02／03三个P2关闭；原S2-RV-01/02在约定分支完成闭环。不扩大为全工具或全部历史来源认证。

当前仅实施INPUT-01：统一动作ID、默认/别名兼容、冲突和捕获取消、草稿/应用/恢复默认、独立首选项持久化、实际消费者及键帽/帮助/教程同步；复用原业务和无人值守入口。进度仍为v9，不改数值/经济/地图，不再次加固MatrixEvidence。

原生UI/U16、独立人工、完整性能仍未验收；UNKNOWN、青色帧、Search、JobTempAlloc根因继续开放。下列S2-R2及更早内容为历史交付快照，保留原失败，不继承为本轮PASS。INPUT-01完成后等待固定SHA复审，不自动进入下一阶段。

# 万象归途：滚动开发计划

更新：2026-10-27。来源为用户完整滚动计划、6.4～6.9及阶段2具体基线2.1～2.9；本轮将验收正式纳入计划并审计当前代码。**计划不是已实现能力或验收证据。**

仓库mizunagare/BallMaze，main；Unity6000.6.5f1、URP17.6.0、InputSystem1.20.0、uGUI2.6.0；单自动档v9，v1～v9兼容合同保留。

## 当前阶段：S2-R2 纯离线校验补丁，待固定SHA复审

当前限定复审结论为**S2-R1部分通过**：保留产品观测/26场战斗/配对/恢复，三个P2工具分支返工。任务已[归档](Reviews/S2R1_b4a08e98_REVIEW_AND_S2R2_TASK.md)，不把此前自报工具PASS反写为已独立全面通过。

- S2-R2开始b4a08e98，工具/测试冻结d5d3fd7c98b78ccc4bd4a781c0dd5d9ad1529e7c；[报告](DeliveryStage2R2/REPORT.md)、[验收](DeliveryStage2R2/ACCEPTANCE.md)、[复跑](DeliveryStage2R2/TESTING.md)、[证据](DeliveryStage2R2/Evidence/INDEX.md)。
- 只修必需阶段对象结构、版本化冻结合同、注册/启动与可信终态/诊断统计资格。原35＋新增58分别通过；旧19＋26＋完整三阶段只读重审原值一致，未新增战斗。
- 不改Assets、产品观测、依赖、PS运行路径或存档；Unity/构建/旧31步/26场/100规则/20通行本轮NOT_RUN，不继承旧PASS。配套原ZIP后来取得并核验，原12条件已原样复跑，候选对相同输入12断言通过；最初阻断保留历史。
- 原生/独立人工/完整性能仍NOT_RUN；UNKNOWN/青色帧/Search/JobTempAlloc根因仍UNRESOLVED。交付后暂停，不开新地图或下一阶段。

## 历史快照：S2-R1工具修复与战斗观测交付


用户随后明确授权归档的[S2-R1任务书](Reviews/Stage2_2ca1aac4_REVIEW_AND_S2R1_TASK.md)，覆盖下方旧“仅计划审计”的执行边界。本轮开始2ca1aac4，产品/执行测试冻结583f19d905aa1b8d8b575f2441bf942b1e37b24f。

- [S2-R1报告](DeliveryStage2R1/REPORT.md) / [验收](DeliveryStage2R1/ACCEPTANCE.md) / [复跑](DeliveryStage2R1/TESTING.md) / [证据](DeliveryStage2R1/Evidence/INDEX.md)。
- RV-01/02修复有原失败与35新离线断言；历史19只读重审及214主要值核对不补造旧schema。
- 最小只读HP事件、18有限同条件配对、额外四武器8场、普通敌和湖Boss的中途保存/新进程击杀、新attempt三进程完整冒险均已实际运行。定向编排31PASS、非开发0错88警告；不同层级不相加，不继承旧All为新PASS。
- 未改战斗数值、AI、来源账、结算、v9、随机/地图语义。旧100规则/20场景范围保留历史，本轮未无差别重跑；不认定全面平衡或玩家体验通过。
- 原生/独立人工/完整性能NOT_RUN；UNKNOWN/青色帧/Search及JobTempAlloc因果栈UNRESOLVED。用户场景与ProjectSettings保持原SHA256，不提交用户修改。
- 完成本轮交付后暂停等待独立固定SHA审核，不进入新地图或下一阶段。

## 历史快照：2ca1aac4计划整合与现状审计


本轮开工远端main/本地HEAD为 `eb69b5ed8f1d508a0d6fccbca2b6eeb0eb1a5572`。此前用户2.1～2.9授权对应的阶段2已交付，产品/测试冻结输入为07ee0e2612c69602b24670f5c8ede53a4396e5d7；[交付报告](DeliveryStage2/REPORT.md)及其154P/2预期F/3NR/2UR等均为**已提交历史证据**，不是这次文档审计的新运行结果或独立复审通过。

- [正式阶段2验收基线2.1～2.9](STAGE2_VALIDATION_SPEC.md)：目标、四策略、四武器/三构筑、成长与流转、100规则seed/20实际seed/12记录/人工矩阵、指标公式、退出条件、未执行记录与审批边界。
- [当前源码/验收逐项对应及差异清单](STAGE2_CURRENT_STATE_AUDIT.md)：A1～A6、B1～B5、C1～C6、D1～D7、E1～E7、F1/P1映射到实际代码、历史证据和“已有实现/需要修复/需要补测/尚缺实现”；G1～G8列最小后续提案。
- 现有四武器、三构筑机制、导航/地点收益、来源/结算/制造/恢复可复用；没有据本次审计确认必须新增成长系统。普通敌精确TTK观测、配对样本、原生/人工与性能缺口不能以新增玩法替代。
- 本轮只改计划/审计Markdown与输入/验证回执；不重写产品/测试、不开Unity/Player、不读存档、不将历史PASS继承为新PASS。产品与引擎问题未经验证不关闭。
- 最小修复/补测提案提交后暂停等待审核；只有具体项获得明确授权才实施。阶段2完整玩家体验仍未验收，绝不自动开始后续阶段。

## 继续保留：B10/B10-R1复审与玩家体验缺口

已交付待审核版本9560b5bb68636fd7783810a6dc4bdead8ed934a3；产品/上轮构建输入6cad42d535347e0d96ede0e40f3d6a889a846bab。最新main只是代码状态，不表示已通过独立审核。见[P0台账](DeliveryB10/ReviewClosure/REPORT.md)。此前P0只读复核曾更正入口说明，原报告和失败记录保留；本轮仅计划审计，不新增游戏系统。

P0八项：固定SHA独立复审、正式Player原生操作、人工理解/试玩、D3D12 UNKNOWN、Editor青色帧、Editor.Search异常、角色/场景表现、真实性能验收。状态使用OPEN/IN_PROGRESS/BLOCKED/RESOLVED/NOT_APPLICABLE，验证状态另用PASS/FAIL/NOT_RUN/UNRESOLVED，不能混用。

只修复可复现产品缺陷、必要的诊断/测试问题、直接相关的局部表现与文档。先保留修复前失败，再最小修复。未定位引擎问题保留UNRESOLVED，不为了全绿试探生命周期。原生操作没有独立环境、独立人员未试玩时如实NOT_RUN。

阶段退出必须有版本追溯、受影响回归、失败保留及明确未完成项；需要独立审核的部分由审核方决定，不由实施者自行关闭。**第一阶段缺口仍开放；阶段2的开工依据是用户后续明确授权，并非实施方自行判断第一阶段通过。**

## 后续候选阶段（待当前审核与具体批次授权）

|方向|玩家问题与最小工作依据|验收约束|
|---|---|---|
|战斗手感与构筑|检查输入/动作衔接、命中窗口、音效/镜头/预警、暂停/死亡；先审计现有四武器与依赖|真实战斗/逐帧证据，不以属性表或静态截图证明手感|
|阶段2策略/成长剩余项（当前阶段，非新批次）|现有机制复用，配对/原生/人工/精确战斗观测与性能证据缺口见G表|[正式基线](STAGE2_VALIDATION_SPEC.md)和[对应表](STAGE2_CURRENT_STATE_AUDIT.md)；未经明确授权不执行提案|
|成长制造与恢复|仓库/配方/损失边界、来源账、满包、Pending/Committed/恢复|不新增虚构统一币值；优先现有v9，不重复发奖或扣费|
|黑猫视觉|角色比例、材质、面尾/动作、营地地表与远景、UI与特效可读性|来源/许可/引用/运行证据，概念不替代资源；环境不能改变导航与业务|

不凭本表自动开新地图、新经济、新武器体系、大型系统或后续元素区域。阶段2交付后再次暂停审核，不自动推进。

## 每轮共同合同

- 核对远端完整SHA、本地HEAD/工作区、用户场景/设置原始哈希。保留用户修改，不reset、不force push、不重写历史。
- 复用本地无人值守体系、唯一外部根与合成档；不接触真实档、不抢桌面、不关用户程序、不强杀超时进程。环境冲突记录并跳过不安全步骤。
- 不升级技术依赖、不启用CI、不将工程或存档另交外部服务处理；获准成果仍交既有GitHub仓库。
- 唯一结算、装备ID/来源账、随机流与确定内容恢复、旧森林布局、免费/收费出口与中断、Boss徽章/奖励、仓库制造事务、教程、v1～v9迁移备份、标题与新游戏确认全部保留。
- 先读真实代码，分为已有/缺陷/补验证/新增；只改当前授权验收项。所有新结果必须本轮运行，旧结果仅标历史。
- 源码检查、规则、Editor正常AI、最终Player、原生键鼠、独立人工试玩各自记状态；零退出码、文件/页面存在、概念/截图不等于功能或体验通过。
- 报告记录输入/输出SHA、行为差异、用例/路径/命令/退出码、兼容、警告、真实性能/缺失指标、首次失败和开放项。推送后重读远端核对完整SHA。
- 审核结果为通过/有条件通过/不通过/待验证，由独立审核方决定。循环为计划→实施→本地验证→提交→固定SHA审核→返工或通过→下一阶段具体授权，不跳过审核。

已有旧路线图保留历史；若与本文当前阶段冲突，以本轮用户明确授权和此处状态为准，不把后续建议当作开工授权。

## PLAYER-01 本批状态与证据（不改变历史结论）

开始main `3839d4f581415f20251737bba5cc1c5a4afa56ff`；仅验收诊断，无产品玩法、依赖或v9变化。[报告](DeliveryPlayer01/REPORT.md)、[验收](DeliveryPlayer01/ACCEPTANCE.md)、[复跑](DeliveryPlayer01/TESTING.md)、[证据](DeliveryPlayer01/Evidence/INDEX.md)。

本轮新正式构建0 Error/91 Warning/4 Log；六种正式Player标题/后台关闭/存档指纹观察通过，Editor输入/事务及Gather三进程支持回归另列。**正式Player完整冒险纵切总体NOT_RUN，P01-02/03/04/06/07未完成；P01-01和允许受控层的P01-05 PASS。** 不能从27个编排行PASS或Editor恢复推导玩家体验通过。

现有Gather/虚拟输入驱动依赖UnityEditor，未移植到正式Player；缺安全独立交互环境、可靠原生UI语义观测和独立人员。BUILD-01短路径规避限定接受，91警告仍在。原生U16/人工/完整性能NOT_RUN，D3D12 UNKNOWN、Editor青色帧、Editor.Search、JobTempAlloc根因UNRESOLVED保持开放。本批交付暂停，等待固定SHA独立复审，不授权新批次或新地图。


## PLAYER-02 本批状态（限定运行时验收，等待独立复审）

开工本地/远端main `428c41fa4f82e7a95c3163319384cad668b5ef6b`。本批不改产品、依赖或v9，保留用户场景/设置/Recovery覆盖层与原始哈希；实机输入含该覆盖层，不冒称纯Git场景验证。仅隔离Acceptance副本注入文档目录的运行时驱动；独立Release排除类型/参数/测试场景，均为非开发构建。

最终正式运行时验收Player六进程：设置/改键→真实采集拾取→收费渡口→Pending退出与读取→真实提交失败/重试→Committed恢复防重复→回营取材制造→再次森林出征→后继Run新进程恢复，限定自动化纵切PASS。最终八类标题/坏设置观察PASS且输入集合不变。P02六项PASS，31成功尝试与6失败尝试、工具初始失败均保留，不能改写成全部实验全绿。10项预检、26项现有Editor输入规则为本轮独立支持层。

发行构建0错误91警告（与PLAYER-01逐条相同）；最终临时验收构建0错误114警告，23条为驱动新增。1152项产品输入未变化。原生U16/独立人工/完整性能NOT_RUN；D3D12 UNKNOWN、Editor青色帧、Search、JobTempAlloc继续UNRESOLVED；发行包原生冒险、全面旧版本迁移/Boss矩阵未新执行。无新增地图或玩法。

[报告](DeliveryPlayer02/REPORT.md) · [验收](DeliveryPlayer02/ACCEPTANCE.md) · [复跑](DeliveryPlayer02/TESTING.md) · [失败历史](DeliveryPlayer02/FAILURE_HISTORY.md) · [证据](DeliveryPlayer02/Evidence/INDEX.md)。交付后暂停，等待固定SHA独立复审，不授权下一阶段。

## PLAYER-02 复审归档与 PERF-01（测量/风险分类，等待独立复审）

用户对固定`6f2abca5f89fc80fc5d298623eda12f557654b78`的PLAYER02复审已[原文归档](DeliveryPerf01/Reviews/PLAYER02_REVIEW_PERF01_TASK.md)：仅隔离非开发验收Player自动化纵切，在交付方证据范围内有条件接受；审核方没有独立Windows重建/运行。原生输入、人工、性能、引擎开放项和31/6历史不因该结论自动关闭。

PERF01开工实读远端/本地同为该SHA，只增加文档目录的临时采样/审计工具与BUILD01包装器可选Perf01配置，不改Assets/Packages/ProjectSettings或v9。8类固定场景各3次独立Player窗口，另3次Title额外计时开关对照，真实采集/战斗/扣费/结算/制造/新出征与3次后继恢复；运行输入含用户覆盖层，完整哈希留证但不提交正文。首轮15 PASS/7 FAIL/6 NOT_RUN与定向补跑13 PASS分开保留，不继承旧PASS或抹掉失败。

CPU主/渲染/GPU有效子集、内存、GC集合、加载和离群数据形成可复跑基线；每帧GC分配/可用显存/纯生成耗时NOT_RUN，GPU完整覆盖未取得。采样器/CSV/驱动也产生开销和GC，不将临时观测包称为无观测发行包，不从小样本认定已完成性能预算或因果定位。新Release0错91警告，逐条风险为中18/低37/信息36，仍全部OPEN；导入期JobTempAlloc等另索引，不默认授权API迁移或警告清零。

[报告](DeliveryPerf01/REPORT.md) · [验收](DeliveryPerf01/ACCEPTANCE.md) · [口径](DeliveryPerf01/METRICS_POLICY.md) · [复跑](DeliveryPerf01/TESTING.md) · [失败](DeliveryPerf01/FAILURE_HISTORY.md) · [原始证据](DeliveryPerf01/Evidence/INDEX.md)。用户1152项产品输入字节保持，原生U16/人工NOT_RUN，D3D12 UNKNOWN/青色帧/Search/JobTempAlloc UNRESOLVED。本批提交后暂停等待固定SHA复审，不自动开始性能优化或新批次。

## PERF-01复审归档与PERF-02（测量能力边界，等待独立复审）

用户对固定94dcc009ff971272fc46d8c5b323cbb3251619b5的PERF01复审有条件接受仅其声明的测量/警告审计范围，不代表性能达标、瓶颈或91警告修复；审核方未独立Windows重跑。原文及限定结论归档在DeliveryPerf02/Reviews，不覆写历史失败和开放项。

PERF02开工远端/本地同该SHA；只ProjectDocs工具/证据和此计划增量，产品1152项未变。I盘新短路径、3份新Library非开发临时验收包；Missing/Title同输入，10秒预热/60秒窗口，ABC/BCA/CAB共9窗口，另5次能力/定向诊断进程，全实际结束。A无额外逐帧采样器，内部帧指标NOT_RUN；B最小FTM固定缓冲，C完整采样器和sidecar。没有把工具包当无观测发行包，或从差值推导产品分配率。

已知主/后台分配下字节API仍0，目标GC Alloc Recorder无效，UNAVAILABLE而非零分配PASS。GPU Frame Time有纳秒正值子集，FrameTime.GPU未获可靠正值，完整GPU覆盖UNRESOLVED。C按实际D3D11设备LUID匹配DXGI进程段用量/预算；PDH/WMI有定向有效实例，原始无效/退出附近样本和错误全保留；不是整卡剩余显存，A/B唯一LUID及sidecar完整自成本未测量。最多3类警告语义只读复核，91仍OPEN，未迁移API或重存场景。

[报告](DeliveryPerf02/REPORT.md) · [验收](DeliveryPerf02/ACCEPTANCE.md) · [口径](DeliveryPerf02/METRICS_POLICY.md) · [复跑](DeliveryPerf02/TESTING.md) · [失败](DeliveryPerf02/FAILURE_HISTORY.md) · [证据](DeliveryPerf02/Evidence/INDEX.md)。无硬件预算、原生U16/人工NOT_RUN；UNKNOWN/青色帧/Search/JobTempAlloc根因继续UNRESOLVED。交付后暂停，等固定SHA独立复审，不自动优化产品、清零警告或开始新批次。
