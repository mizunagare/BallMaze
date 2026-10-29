# RUNLOOP-01-R1

开始时本地及远端 main：`d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179`。本轮只处理 RL01-RV-01/02；原 RUNLOOP-01 修复、营地及制造成果保留。产品冻结提交：`0defd1ef4be0edc10d00c38fa79a8675ed0b9d32`。最终交付提交以本报告固定 Git 版本及交付块为准；工具冻结及实际输入哈希见 Evidence/Bindings/source-bindings.json。

## 复审边界与修复

任务书和配套六文件分支模型已原文归档。模型重跑仍是 11 个离线条件，不是 Unity、JsonUtility、v9 校验器或 Windows 发布测试，单列于 Bindings/model-rerun.json。

修复前隔离 Unity 已实际复现两项发现。真实出征、资源 Hit 产生未拾取分页掉落、主动放弃产生 Pending，随后仅在负例夹具构造冲突：plan、outcome、来源数量、检查点资源生命、带入账与对应 checkpoint 数量。每个候选先经 AdventureValidation.Validate、分页写入及 InspectReadOnly 完整 v9 校验。它们是明确的人工冲突负例，不是正例奖励注入或真实玩家档案。仅改变 ID 不满足合法 v9 的初次夹具失败亦保留。

RL01-RV-01：提交前冻结完整 Profile、ActiveRun、Settlement 的 DTO 语义快照。提交失败后，只有确切预期 Committed 或完整旧 Pending 才分别确认/允许重试；任何其他内容、缺失或坏档进入待核对。比较使用现有 JsonUtility/AdventureData.Clone 往返，与分页读回的展开 DTO 对齐，不忽略收益或检查点字段，不添加 v9 字段或通用事务框架。原完整 Committed 成功核对分支保留。

RL01-RV-02：Restore/AdoptLegacy 不在开始时解除待核对。完整读取、运行时重建和必要迁移发布均成功后，由保存系统解除。运行时恢复失败且存在结果时恢复该标记；直接确认结算也受门禁限制。结算按钮的标签和调用统一使用 SettlementPrimaryLabel/ExecuteSettlementPrimaryAction，同一真实界面分派在故障解除后重读。测试直接调用此界面分派，属于受控 UI 命令，**不是原生点击或人工验收**。

旧版读取所需内部迁移写入有一个同步、私有、finally 清理的门禁例外；仓库操作仍被拒绝，迁移失败仍保持读取门禁。有限 v1～v8 夹具逐个验证迁移写入失败、保留精确原字节、同一命令重试、最终 v9 与可写状态，避免移动清标记代码造成迁移自锁。不声称穷尽旧档全部组合。

## 证据与口径

最终相同冻结夹具：Before06（旧产品）17 PASS / 15 FAIL；After04（修复产品）33 PASS / 0 FAIL，两个进程分别 exit 1 / 0、均无超时。旧版 Pending 恢复失败时主操作实际为“确认结算并保存”，Committed 为“返回营地 / 重试回营”；新版均保持“读取完整存档核对”。前后不同合成 Run 的 GUID 不同，不将其包装成同一 Run 跨产品版本恢复。

Migration03 为 8 个旧版本门禁用例全部通过，每例验证五个布尔合同。五个独立 Editor 进程共 47 条断言通过；RuntimeAudit 4 条、标题入口 5 条通过。原 RunloopFault、Uncertain Missing/Corrupt、Catalog 四进程、输入/伤害观测/Boss 回归本轮均 exit 0。正常 AI 三进程均 exit 0、无超时：实际采集木材 5、渡口只修复一次、真实撤离/提交/存取/制造、后继森林与两个新进程恢复。

当前有限验收条目为 **24 PASS / 0 FAIL**；另列 **6 NOT_RUN / 5 UNRESOLVED**，是验收条目数量，不是将各次重复运行的断言相加。首次失败及中间工具失败见 attempts 与 FAILURE_HISTORY，不混入“当前 0 FAIL”而消失。

非开发 Windows64 构建：BuildOptions.None，Succeeded，0 错误、94 警告，27.8872794 秒，进程 exit 0；完整消息保留。EXE SHA256 `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`，Assembly-CSharp SHA256 `884ad33c8864981469aa223520548786110f3565c3d41f223df5540980168c26`。只读 PE 检查无本轮/旧 RUN01 Editor 夹具或 UnityEditor 引用。三个修改产品文件在源码、最终测试副本和构建输入的 SHA256 全部相等；测试冻结 `63a838eef602500cfefdbe0ef46db38db9f48b4b`。构建使用的旧 R1Migration Editor 测试源码与最终反射兼容版有差异，后者由 Migration03 实测；两者均从发行程序集剔除，不声称全工程逐字节相等。

用户 5 个文件及既有 2040 个历史证据文件前后 SHA256 均不变。

[验收表](ACCEPTANCE.md)、[复跑说明](TESTING.md)、[证据索引](Evidence/INDEX.md)分别列出当前限定验收、实际尝试及保留开放项。故障候选、真实主备档/分页、发布前 Pending、恢复期望展开数据、各回调前后指纹均归档；完整原始输出保留，压缩日志记录原始和发布 SHA256。

自动保存、受控 InputSystem F5、失焦、暂停、退出回调验证实际文件及内存 Profile/Run 不被覆盖。调用退出回调不等于真实标题栏退出；EditorApplication.Exit 的进程退出也不等于发行 Player 原生操作。五进程循环与实际世界实体审计另列，正常 AI 与受控冻结敌人的夹具分开，不继承旧 PASS。

矩阵中的 validV9 表示故障前准备的候选通过校验；Missing/Corrupt 随后故意使主档缺失/损坏，不声称损坏文件本身合法。

## 保护与限制

隔离根 `I:/WGCombat/RL1-1030-A`；复用现有本机执行器和闲置副本。主工程用户 Editor 保持运行，不关闭、不抢占；不操作真实存档、不升级、不启用 CI、不强杀进程。用户场景、ProjectSettings、Recovery 只记录保护哈希，不纳入提交。实际构建输入含本机用户修改时，仅提交哈希并明确可复现边界，不擅自发布用户场景内容。

attempts 保留各次原结果；findings 仅标 FIXED/待独立复审；current_acceptance 不把历史负例机械计作当前缺陷；deferred 保留未执行层级。D3D12 UNKNOWN、Editor 青色帧、Search、JobTempAlloc、旧 C15 根因仍 UNRESOLVED；原生 U16、独立人工及性能未执行，仍 NOT_RUN。未扩大到全部 terminal/ack 回调排列或新玩法。提交推送后暂停，等待固定 SHA 复审。
