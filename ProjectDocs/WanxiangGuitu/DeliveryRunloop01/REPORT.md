# RUNLOOP-01 报告

开工本地与远端main均为`4ae4ca8fa8d8d7ff64aaee388bfc653eb58f76e7`；交付SHA以本报告Git固定版本及交付消息为准。本轮先审计、再复现、最小修复和分层验证。没有新增经济、地图或大型系统。

## 复审归档与已有能力

用户提供的COMBAT03固定SHA复审结论已原文归档于REVIEW_AND_TASK.md：仅在交付方源码与证据范围有条件接受，不是审核方独立运行、武器平衡或人工手感通过。历史16P/5F/4N/5U不改写。

[真实状态图](RUNLOOP_STATE_MAP.md)逐项标注已有实现、条件、入口、物资边界、反馈和恢复。[来源矩阵](STATE_SOURCE_MATRIX.csv)区分地面、随身、计划、永久仓库、待领取及制造。AtCamp是ActiveRun为空的谓词，Committed未确认时也可为true；HasResult、Frozen和Ready共同限制操作，不将这些谓词误画成互斥持久化状态。

## 确认问题与最小修复

原Before实际exit1：提交文件已发布，回调抛错后SaveProgress返回false，磁盘revision4/Committed，内存revision3/Pending，显示“物资未转移”。真实原始fault-result及日志保留，未以重跑覆盖。

仅改AdventureFlow.cs、AdventureFlow.UI.cs、CombatSaveSystem.cs：

- Commit失败后只读核对修订、Profile和完整结算回执。同一已发布Committed才确认成功，更新内存修订，不重发奖励。
- 仍为旧Pending时保留原回滚/重试；无法核对或主档缺失/坏档/冲突时标记运行时SettlementNeedsRead，阻止盲目重提。
- 同一门禁阻止自动、手动与退出保存覆盖不确定结果。结算标题显示“结果待核对”，提供完整读取入口；成功读取／新档／旧版迁移清除临时标记。
- 标记不写入v9，不增加持久化状态。AdventureRules.Plan、来源账、奖励、死亡保护、概率、随机流、地图、制造支付数值均未改变。

After相同故障实际exit0：live/disk均Committed、revision4，Profile一致。Missing/Corrupt两个专项均核对：不误称已保存、重提和保存被拒绝、恢复精确原发布字节并正常读取后回到Committed，重复提交不新增修订或奖励。测试对拥有者根合成档做文件故障注入，不是编辑业务结果或真实玩家档。

## 实际运行

- Verified/Run→Running→Pending→Committed→Final为五个独立Editor进程；每阶段保留完整主档、备份、期望身份、实际执行源和进程回执。检查同Profile/阶段应有Run/区域/seed/layout/revision/随机流、实际装备ID、来源账、地面ID与仓库。
- 额外RuntimeAudit新进程直接检查恢复后的RuntimeForest布局/演员ID、实际敌人生命、资源生命与事件Used状态，4项通过，避免只验证保存元数据。
- Running/Extracting验证未满足渡口条件的展示原因与拒绝相同、不扣费；远离出口拒绝；引导保存失败回Running；真实取消、实际受伤中断；免费出口真实倒计时生成Pending。
- 两节点实际Hit生成地面，只拾取一份。拾取才计入背包/earned，地面第二份不进入Pending或仓库。普通链木材拾取5，提交后仓库100→105；带入木2留在随身，未混入永久收益。
- Pending新进程：发布前失败保持可重试；发布后回调失败核对成功；重复Commit不发布、不重复增加committedRuns。Committed新进程：确认、统一随身+仓库制造、注入失败完整回滚、真实成品、存取、同Profile新森林Run，再次新进程恢复。
- Death专项：实际伤害触发死亡结算，新得材料损失，仓库保持初值，不把地面或失败RunLoot存入仓库。Abandon由独立故障复现覆盖，未直接指定结算结果字段。
- Overflow专项15断言：合成初始仓库木材到既有上限，真实采集/撤离后超额仅进入待领取；未领取阻止出征，满仓领取拒绝，明确领取到背包才改变归属，重复请求无收益。
- Entry通过实际Title场景、GameEntry确认/取消、新档事务、Forest场景Boot到真实出征；是Editor业务请求，不是原生点击。B09Rules四进程覆盖缺失/有效/损坏/不兼容/不确定、只读旧档目录v1～v6、新档失败旧集合保留、归档中断与新进程恢复。不是全版本完整迁移的新验收。
- 复用原正常AI三阶段：实际采集木5、渡口修复一次、撤离结算、存取制造、再次森林出征和新进程继续；各exit0，无超时。输入、伤害观测、双Boss回归三个进程亦exit0。受控NPC冻结与正常AI严格分开，不冒充玩家操作。
- 非开发Windows64 BuildOptions.None：Unity6000.6.5f1，Succeeded，0错94警告，32.3457326秒，进程exit0。完整BuildReport消息、PE类型检查及哈希归档。发行程序集不包含本批验收类，不等于发行Player实际运行验收。

EXE SHA256：`001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`。

Assembly-CSharp SHA256：`431b7dc964998272fe16f191589c250542e2bce2908e05222212ed34a6c3bb09`。

## 保留、限制与交付口径

用户5文件和COMBAT02/R1/03历史1409文件前后哈希不变，原四exit1及aggregate没有写入。保护场景、ProjectSettings及Recovery未提交内容。使用工程外唯一根`I:/WGCombat/RUN01-1029-A`、合成档和闲置副本，没有真实档、升级、CI、抢桌面、关用户程序或强杀。

构建/导入副本与主工程部分设置资产不逐字节相同，build-inputs.json逐项照录；运行输入含受保护用户本机场景/设置，仅记录哈希，不擅自提交内容，不宣称固定Git单独重现这些本机差异。不同新鲜运行的GUID独立生成，不伪造成同一身份。

新增五项工具/发布初始失败保留：C#方法调用漏括号造成编译失败；关闭面板同帧交互屏蔽导致提示为空；JSON空字符串与内存null误判；发布校验误用GBK读取UTF-8；索引门禁发现合成tmp/bak被全局ignore排除并阻止提交。分别修工具语法、等待合法下一帧、规范化表示、显式UTF-8以及限定补充暂存本批证据，未改产品输入门禁、升级C#或弱化业务断言。依赖失败后停止，后续在新输出目录执行。

本批通过只代表受控核心循环/反馈一致。隔离验收Player、正式发行原生操作、U16、独立人工、性能，以及ack/terminal所有发布回调排列未全面执行，见NOT_RUN；D3D12 UNKNOWN、青色帧、Search、JobTempAlloc、旧C15继续UNRESOLVED。未重复关闭实验。报告不将编排器0或构建0等同所有验收通过。完成后暂停，等待固定SHA独立复审。
