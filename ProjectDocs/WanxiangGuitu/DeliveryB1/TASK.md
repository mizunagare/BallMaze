# 《万象归途》A1 复审与交付 B1 任务书

日期：2026-10-23  
仓库：mizunagare/BallMaze  
复审分支：main  
复审基线：deaf0258b9335273546b4cfb20dda5d306780b82  
本次固定提交：f9631aac0d4f837825a33cd79ed3494ddbacc203  
产品修复提交：4eb69c6ce61213d1083f5a6e9a5bca890c924010

## 一、审查结论和边界

**结论：A1 三个定向问题通过本次源码与已提交证据复审，可以关闭这三项审查问题并进入交付 B1。**

在本次检查的启动隔离、重复选择、空目标迁移与恢复路径中，未发现需要继续阻塞 B1 的 P1/P2 问题。不要求再启动泛化存档重构或 A2 大批次。另有一项 P3 报告数量口径问题，可在 B1 开始时用独立文档提交纠正。

这是固定提交的静态审查与交付证据核对，不是审查者独立运行 Unity 后取得的 PASS，不是整库无缺陷证明，也不是完整 B06、发布或安全认证。未修改仓库，未访问真实玩家存档。

本次从 GitHub 重新读取 main，返回的 HEAD 与上述固定提交一致；本地工作区是否干净属于交付方报告，本审查不据远端推断本地状态。

### A1-01：启动隔离

核对的主要入口：
- Assets/CombatPrototype/ValidationStorage.cs
- Assets/CombatPrototype/CombatSaveSystem.Location.cs
- Assets/CombatPrototype/CombatSaveSystem.cs 的初始化、读写与退出审计接线
- ProjectDocs/WanxiangGuitu/DeliveryA1/Invoke-NormalAI.ps1
- ProjectDocs/WanxiangGuitu/DeliveryA/Tests/WGNormalAICheck.cs.txt

包装器在启动 Editor 前传入隔离参数；Run 在打开场景、进入 Play 前调用 ValidateLaunch。测试驱动等待默认初始化，断言 SavePath 位于启动根，不再在 Play 后执行第二次 InitializeStorage 切换路径。

ValidationStorage 对缺少/重复参数、非完全限定路径、LocalLow 与已检查的重解析位置有明确拒绝；Record 对隔离运行的存档入口做范围检查。正常产品无隔离参数时仍保留默认存档行为，不能将正常玩家启动误改成必须使用测试目录。

提交的 storage-audit.jsonl 有 39 条记录，第一条为 playing=false 的 pre-play，随后是隔离根内的定位、初始化和读写；正常与恢复进程各有一次初始化及 before-exit 记录。负例记录同时检查预期拒绝标记、退出码、无存档回执及替身哨兵，不是任意 exit 1 都算通过。

上述证据是应用入口审计，不证明所有 OS 文件访问均被追踪。历史正常 AI 是否触及真实目录继续保持“未核实”。

### A1-02：重复选择新版存档

SaveLocationMigration 已将不可覆盖的迁移发布回执和可更新的选择回执分开。选择更新使用唯一临时文件、Flush(true) 和 File.Replace，并保留 previous。UI 传入检查时的新旧集合指纹；提交前再次校验变化，避免旧界面确认未经复查的新集合。

WGA1Check.Choice 与 WGA1ExtendedCheck 覆盖首次选择、旧集合变化后再选、旧 UI 指纹拒绝、写前失败保留旧确认、重试、写后中断及跨进程重试；v8/v9 四态矩阵比较游戏主备/分页/档案字节。

这关闭的是已报告的重复确认失败，不代表跨进程数据库事务或全部恶意文件系统竞态已经证明安全。

### A1-03：空目标发布与恢复

Resolve 在发布前重新检查目标文件、重解析点和目录内容，对仍为空的目标仅执行非递归删除再发布；竞争内容出现时停止，不递归删除用户文件。

AdventureFlow.StartFresh 在 ApplyCamp 成功后清除旧 Error 和提示状态；失败不预先宣称恢复。测试覆盖安全空目标、文件占位、异常目录、发布前竞争写入、修复后重试及重新出征。

## 二、P3：修正正常 AI 报告的木材阶段数量

本提交存在以下可直接核对的差异：

- DeliveryA1/REPORT.md 写了“木材3收益”及“木材3收益、提交入库、取木2制造”。
- Evidence/NormalAI/normal-results.txt 为 `ACTUAL_HARVEST_PICKUP_PASS wood=5`。
- 正常 AI 驱动随后执行 `TransferMaterial(MaterialKind.Wood, 2, false)`，取出 2 个木材制造。
- Evidence/NormalAI/expected-normal.txt 材料行是 `0,0,0,3,0,0`，对应后续恢复时的仓库状态。

现有步骤与记录对应“采集持有5 → 入仓 → 取出2用于制造 → 仓库剩余3”，报告把采集/收益与后续余额混写的可能性很高。请以原始运行记录、结算数据和截图核对后，明确各阶段数量并修正说明。

不要改历史日志去匹配报告；不要为凑成3而修改掉落；不要把这一差异直接宣称为丢失2个材料。若某份证据来自不同运行，拆分运行身份后再说明，不拼成一条流程。

## 三、证据口径与保留限制

- latest-method-status.json 列出原19项加7项A1检查，26个方法最后结果均为成功；这是多次执行的最终状态汇总，不要改写为“最终提交一次性全跑26项，从未失败”。
- Red-assertions.txt 保留四个失败，其中隔离项是安全的结构入口回归，不是故意运行旧不安全初始化以接触真实档。
- 报告保留了较早一次 Editor 启动阶段退出 -1、原因未核实；后续通过不等于其原因已查明。
- 正常 AI 是固定实际种子418的自动操作，带正常伤害/速度/AI；不等于人工操作、全部武器平衡或完整森林重复可玩性验证。
- 无运行驱动正式版仅有启动/初始存档证据；工具终止不能当正常退出。下批增加一次正常退出后新进程继续的验证，不以此要求现在重做A1。
- 人工试玩、内核级全进程文件审计、真实断电和物理磁盘损坏仍未验证。
- 分页回收、磁盘配额和所有恶意并发/路径别名不在本次关闭范围，保留已知限制，不据此无限扩展当前批次。

## 四、下一批：只完成 B1 可修复渡口

以下是下一批实施建议与验收要求，不是已经存在的功能，也不是对 A1 范围的追溯加码。

### 4.1 玩家可体验的目标

出征进入森林，看到普通出口和待修复渡口；能在世界中采集所需材料，修复渡口，选择从该条件出口撤离，并完成唯一结算。条件不满足时，仍能改走普通出口。

它的意义是提供第二种真实路线选择，不是多加一个与普通祭坛完全相同的按钮。

### 4.2 复用现有实现

优先增量扩展既有 ExtractionConfig、ExtractionPoint、AdventureFlow.Exits、森林状态捕获/恢复及统一撤离结算入口。不要重新实现第二套结算、仓库、材料来源账或存档系统。

CurrentExit 目前有按出口ID锁定引导、未引导时选择最近出口的逻辑。加入条件出口时，显式处理“选中目标”“修复资格”“启动撤离资格”：不可修复/不可用的最近出口不能让其他合法出口失去交互，也不能静默选择远处出口或错误扣费。

### 4.3 渡口规则

1. 普通出口无需稀有材料、特定武器或 Boss 击杀，每个合法生成布局至少一处真实可达。
2. 渡口提供清晰的未修复/可修复/已修复状态。成本从配置读取，首版使用已有常见素材，不新增一大套资源系统；具体数量由 Codex 在现有生成产量和六格补给约束下选择并写入配置与测试记录。
3. 交互前显示材料名称、所需/持有/缺少数量和“修复仅对本次冒险有效”。使用随身材料，不得直接扣营地仓库。
4. 修复与撤离分开：首次明确修复成功并持久化后扣费一次；之后再启动原有撤离倒计时。修复不自动发奖、不永久入库、不自动结束本局。
5. 撤离引导被打断、取消、离开范围或退出继续，已成功持久化的修复状态保留，不再次扣费、不退款。死亡/放弃仍沿用既有消耗规则，不恢复已经用于修复的材料。
6. 同一 Run / 区域实例 / 出口稳定ID 下只修复一次。新的独立 Run 重新采用该局配置；不在 Profile 里意外永久解锁全部渡口。
7. 受伤/死亡与交互发生同帧时遵守既有终局优先级；结局锁定后不继续扣费或修改渡口。
8. 首版只需岸边渡口、破损与修复后能辨认的差异、清楚的交互提示和可达空间。不要求自由游泳、真实浮力船舶、过场动画或完整海底系统。

### 4.4 扣费与持久化边界

材料数量、broughtRemaining/earnedRemaining 来源账、已修复状态和必要操作身份必须进入同一份一致检查点。优先花本局来源，再花带入来源，沿用已有规则。

两种状态必须能够恢复：
- 尚未成功发布：仍是未修复、未消费，运行时与来源账一起恢复；可以重试。
- 已成功发布：修复与消费都存在；重启/重复点击不再扣费。

对于“已经发布但后续回调/显示失败”的不确定结果，先读取实际已保存修订或操作回执再处理，不得无条件退款或再次扣费。复用现有保存与恢复机制，不为这个需求引入分布式事务或新数据库。

不要仅靠UI按钮禁用实现幂等；领域方法必须自行拒绝重复修复、超距修复、材料不足和终局后的操作。

### 4.5 存档兼容与生成

- 出口修复状态进入正式森林快照，以稳定ID关联。恢复时不换种子，不重建一个未修复状态覆盖已保存状态。
- 已有普通出口在旧档中缺少新增字段时，仍是原来的免费普通出口，不能默认为“未付费渡口”。
- 不强行给已保存的旧布局插入新出口；旧Run按原布局完成。新出征才能使用新的生成配置；若提供显式迁移，必须有对应版本和测试。
- 根据实际格式/语义变化决定是否升级存档或内容版本；不得只改常量宣称兼容，也不得无理由清空旧档。
- 普通出口、渡口交互范围和资源来源实际可达；逻辑图连通不代替角色碰撞通行。失败采用既有受控重试/备用策略，保存布局恢复失败不能偷换种子。

### 4.6 B1 验收矩阵

| 编号 | 用例 | 必须满足 |
| --- | --- | --- |
| B1-V01 | 缺材料、远距离、终局后请求修复 | 不能扣费、不能改变出口状态，有可理解反馈 |
| B1-V02 | 正常采集后修复 | 消耗来自随身库存；数量与两类来源账相符；修复状态实际保存 |
| B1-V03 | 连点按钮、重复调用、同帧重复请求 | 成功修复只扣一次，不依赖UI防抖 |
| B1-V04 | 本局/带入材料混合并死亡 | 优先本局消费；已消费的带入部分不因死亡恢复 |
| B1-V05 | 修复后引导、受伤/离开/手动取消 | 回到可撤离状态；修复仍有效，不重扣、不退款 |
| B1-V06 | 修复后退出、新进程继续 | 同Run/种子/出口ID；状态与来源账一致，可继续撤离 |
| B1-V07 | 持久化前失败、失败重试 | 未发布时材料与修复状态一致回滚，无吞料或免费修复 |
| B1-V08 | 持久化后中断、新进程重试 | 识别已发布结果，不再扣费、不重复结算 |
| B1-V09 | 取消与再次进入、成功撤离与新Run | 本局修复保留；新Run按新局规则初始化，无跨局串状态 |
| B1-V10 | 普通与条件出口同场、不同附近交互物 | 未修渡口不阻断普通出口；选中对象和实际执行对象一致 |
| B1-V11 | 旧v9普通出口与旧在途布局 | 继续旧Run，无新增扣费门槛，不重抽世界 |
| B1-V12 | 多种子出口和资源通行 | 至少10个指定种子冒烟；普通/条件出口真实可达，异常布局不保存为成功 |
| B1-V13 | 正常AI且有收益的渡口完整流程 | 不靠直接把修复标志置true或冻结全部敌人完成体验；采集→修复→引导→结算→回营→新进程核对 |
| B1-V14 | 无运行验证驱动的非开发构建 | 可用正常退出路径退出，再启动继续同Run或已提交结果；工具强杀另列，不冒充正常退出 |

冻结AI的通行探针、受控扣费故障用例、正常AI自动流程、人工试玩分别报告。人工未执行继续标NOT_RUN，不要求AI伪装人工。

B1阶段不直接宣布通过整个B06的100种子/20通行和三收益路线验收；完整B06门槛仍在B4汇总。已有影响到的生成/回归检查应按变更范围复跑。

## 五、后续顺序与范围

- B1：条件渡口与扣费幂等，本次唯一实施目标。
- B2：地点收益差异、配方缺口与目标追踪。
- B3：布局/遭遇/掉落/事件/表现随机流分离，保存恢复与可复现性。
- B4：采集撤离、遗迹寻宝、绕精英改走条件出口三条有实际收益的正常AI完整冒险；汇总B06规则/通行和体验验收。
- B07：B06通过后才做双Boss与徽章。

本批不并行制作火山、冰原、海底、天空、天气谜题、完整战斗重做、大型UI翻新、分页垃圾回收或工具链迁移。

## 六、可直接给 Codex 的启动指令

继续《万象归途》mizunagare/BallMaze。

A1已在f9631aac0d4f837825a33cd79ed3494ddbacc203通过本次限定范围的源码与证据复审，不代表审核者独立运行Unity或游戏已达到发行标准。

先核对当前本地和远端以及该提交之后的修改，不reset、不覆盖用户改动。先单独纠正A1正常AI报告中木材采集量与后续仓库余额的口径，保留原始证据；然后按本任务书完成B1可修复渡口。B2～B4只维护路线图，不同时开工。

复用既有来源账、检查点、分页、撤离、终局、仓库、装备及A1启动隔离；修复和扣费必须是同一持久状态，重复调用/取消/保存失败/进程恢复不重复扣费。普通出口始终无稀有道具门槛。UI做真实可操作的条件提示和状态反馈，不只放占位按钮。

完成B1-V01～V14及受影响的历史回归，本地验证、不升级Unity和依赖、不启用CI、不使用真实玩家档做测试。正常AI必须沿用启动前隔离入口，缺安全参数先拒绝，不能Play后切目录。

允许分小提交连续实施，但交付完整可玩闭环。最终推送现有仓库并核对远端完整SHA；分支保护拒绝时用允许的分支/PR，不force push。提交代码、可复跑测试、报告和证据索引；不要提交真实存档、凭据、Library/Temp或无关改动。

报告开始基线/最终SHA、修改与规则、存档兼容、PASS/FAIL/NOT_RUN、正常AI与正式构建、已知限制。推送完成不等于新批次已通过复审。

## 七、固定提交来源索引

以下链接均锁定本次提交，后续更新不得反写本次审查事实。

- [A1报告](https://github.com/mizunagare/BallMaze/blob/f9631aac0d4f837825a33cd79ed3494ddbacc203/ProjectDocs/WanxiangGuitu/DeliveryA1/REPORT.md)
- [隔离参数与审计](https://github.com/mizunagare/BallMaze/blob/f9631aac0d4f837825a33cd79ed3494ddbacc203/Assets/CombatPrototype/ValidationStorage.cs)
- [迁移与重复选择实现](https://github.com/mizunagare/BallMaze/blob/f9631aac0d4f837825a33cd79ed3494ddbacc203/Assets/CombatPrototype/SaveLocationMigration.cs)
- [默认定位入口](https://github.com/mizunagare/BallMaze/blob/f9631aac0d4f837825a33cd79ed3494ddbacc203/Assets/CombatPrototype/CombatSaveSystem.Location.cs)
- [营地恢复](https://github.com/mizunagare/BallMaze/blob/f9631aac0d4f837825a33cd79ed3494ddbacc203/Assets/CombatPrototype/AdventureFlow.cs)
- [正常AI启动包装器](https://github.com/mizunagare/BallMaze/blob/f9631aac0d4f837825a33cd79ed3494ddbacc203/ProjectDocs/WanxiangGuitu/DeliveryA1/Invoke-NormalAI.ps1)
- [正常AI驱动](https://github.com/mizunagare/BallMaze/blob/f9631aac0d4f837825a33cd79ed3494ddbacc203/ProjectDocs/WanxiangGuitu/DeliveryA/Tests/WGNormalAICheck.cs.txt)
- [核心回归](https://github.com/mizunagare/BallMaze/blob/f9631aac0d4f837825a33cd79ed3494ddbacc203/ProjectDocs/WanxiangGuitu/DeliveryA1/Tests/WGA1Check.cs.txt)
- [矩阵与跨进程重试](https://github.com/mizunagare/BallMaze/blob/f9631aac0d4f837825a33cd79ed3494ddbacc203/ProjectDocs/WanxiangGuitu/DeliveryA1/Tests/WGA1ExtendedCheck.cs.txt)
- [26方法最后状态](https://github.com/mizunagare/BallMaze/blob/f9631aac0d4f837825a33cd79ed3494ddbacc203/ProjectDocs/WanxiangGuitu/DeliveryA1/Evidence/latest-method-status.json)
- [基线失败](https://github.com/mizunagare/BallMaze/blob/f9631aac0d4f837825a33cd79ed3494ddbacc203/ProjectDocs/WanxiangGuitu/DeliveryA1/Evidence/Red-assertions.txt)
- [应用存档回执](https://github.com/mizunagare/BallMaze/blob/f9631aac0d4f837825a33cd79ed3494ddbacc203/ProjectDocs/WanxiangGuitu/DeliveryA1/Evidence/NormalAI/storage-audit.jsonl)
- [正常AI逐步断言](https://github.com/mizunagare/BallMaze/blob/f9631aac0d4f837825a33cd79ed3494ddbacc203/ProjectDocs/WanxiangGuitu/DeliveryA1/Evidence/NormalAI/normal-results.txt)
- [恢复期望](https://github.com/mizunagare/BallMaze/blob/f9631aac0d4f837825a33cd79ed3494ddbacc203/ProjectDocs/WanxiangGuitu/DeliveryA1/Evidence/NormalAI/expected-normal.txt)
