# ObjectiveHistory 最终实施前审查

**DOCUMENT_PASS · IMPLEMENTATION_NOT_STARTED · 字段批准待定。** 2026-11-19。D-19、D-20、D-23 均 A。目标版本暂定 v10，单一历史最近 128 条。已按负责人建议采用方案 A，关闭 CommittedAtUtc 设计阻塞。字段候选与产品实施仍待批准。

## 字段结论

| 字段 | 审查状态 | 结论 |
|---|---|---|
| RunId | APPROVED_CANDIDATE | 保存历史与来源局的关联，复用原 ID 和校验。 |
| SettlementId | DERIVED_NO_STORAGE | 参与三元键，按 RunId + :terminal 派生，捕获时核对真实结算 ID。 |
| ObjectiveId | APPROVED_CANDIDATE | 保存稳定卡片 ID，目录改名或退役不改变身份。 |
| RegionId | APPROVED_CANDIDATE | 冻结该项所属地区以供筛选。 |
| CompletedAtUtc | APPROVED_CANDIDATE | 记录含成功撤离条件的完整目标达成时刻，在 Pending 固定。 |
| CommittedAtUtc | APPROVED_CANDIDATE | 结算提交计划时间。首次合格计划形成时采一次，随首个 Pending 冻结。重试、恢复和单独确认均复用原值。 |
| CompletionType | DERIVED_NO_STORAGE | 九个稳定 ObjectiveId 有确定的历史兼容映射，涵盖基础类型和挑战标签。退役 ID 保留映射。 |
| DisplayNameSnapshot | APPROVED_CANDIDATE | 固定达成时的显示名，保障历史改名保真。 |
| DefinitionVersion | NOT_REQUIRED | 本功能展示已确认的事实和快照。当前无重演旧定义的需求。 |
| v9 的旧目标身份、完成时间及历史正文 | DATA_GAP | 迁入空历史及旧覆盖未知标志。旧 Pending 不重算。 |
| 地区长期指标缺口 | DATA_GAP | 只保留既有资料来源。不得用 128 条完成样本推算地区累计。 |

APPROVED_CANDIDATE 表示具备进入负责人审批的条件。存储字段、两项容器默认、闭集与派生规则均在本次实施授权前复核。 [逐字段审批表](OBJECTIVE_HISTORY_FIELD_APPROVAL.csv) · [实施任务书](IMPLEMENTATION_TASKBOOK.md)

## 源码与一致性结论

- [S] 复核 AdventureFlow.Objectives、ObjectiveEvaluator、AdventureRules、ProfileState、SettlementRecord、SaveProgress、提交回读及 GroundLootStore。现行奖励计划先于首个 Pending 保存。Committed 候选先换入内存，页及临时封套准备后才替换主档。必须用磁盘确认及发布门保护历史视图。完整源码定位和七个中断状态见 [事务模型](OBJECTIVE_HISTORY_TRANSACTION_MODEL.md)。
- [S/D] committedRuns 在现行已确认档内保存终局事实，可抵抗已被裁剪的旧目标重试。最近 SettlementRecord 下次出征会被清除，独立扫描 128 条不构成长久屏障。既有 100,000 条结算上限和 8 MiB 封套保护沿用。旧备作为独立恢复世代，过期计划由父世代校验拒绝。当前无需额外永久去重字段。
- [D] v9 直接迁往唯一目标版，只初始化显式默认，保留主备、必要事务和外置分页闭包。失败提交不裁剪主历史。第 129 条确认提交仅淘汰最早提交项，奖励、徽章、击杀、材料、领取和结算事实按各自既有合同保留。
- [D] 已保留 OH01–OH18，新增 OH19 双时间采样与 OH20 裁剪后过期世代重放。共享断言不重复计数。全部用例 NOT_RUN，OH19 以首次 Pending 冻结的计划时间为准，OH16 使用双 UTC 降序后按三元键 ordinal 升序。 [Player 计划](PLAYER_ACCEPTANCE_PLAN.md)

## 验证及保护

基线分支 feature/ux-progression-04-b2，HEAD ae705b944b7d0fe851fbd395229dfc30ec636f5c，父 95caf234256613d4a6e4f89a8ab0dc09c397c6b2。sparse-checkout 已启用。重新读取根 AGENTS.md。核对链接、CSV 结构、字段状态、用例映射及 SHA-256 变更范围。本轮仅更新授权目录内的九份现行设计与审查文档。跟踪工作区和暂存区 diff 为零，授权目录外状态清单前后一致，Schema 清单字节不变。未访问真实存档。构建、Player 运行及产品测试均为 NOT_RUN。未暂存、提交、推送、合并或启动实施。

## 负责人复审

批准 [最终字段审批表](OBJECTIVE_HISTORY_FIELD_APPROVAL.csv)、v10 及产品实施范围。CommittedAtUtc 采用方案 A。派生 SettlementId 与 CompletionType，DefinitionVersion 不入档。
