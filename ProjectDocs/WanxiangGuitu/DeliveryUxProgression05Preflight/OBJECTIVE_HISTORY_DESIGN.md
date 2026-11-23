# UX-05 跨重启目标完成历史

**需求已确认，IMPLEMENTATION_NOT_STARTED。** 2026-11-19 确认跨局和跨重启历史。D-19、D-20、D-23 维持 A／APPROVED。核心功能、单一事实源、128 条和三元去重键已确认。目标版本暂按 v10 设计。逐字段方案及实施待批准。CommittedAtUtc 采用方案 A，表示 Pending 冻结的结算提交计划时间。实施入口为 [实施任务书](IMPLEMENTATION_TASKBOOK.md)。

## 完成的定义与证据

[S] ObjectiveCatalog 已有九个稳定卡片 ID，以地区和 ExpeditionGoal 匹配。CaptureObjectives 在 LockOutcome 锁定终局时计算 LastObjective。ObjectiveEvaluator 的 achieved 同时要求条件达成和成功结局。AdventureRules.Success 也包含 TestChallengeComplete，而测试挑战与无尽波次没有本方案定义的地区卡片完成合同。[ObjectiveCatalog](../../../Assets/CombatPrototype/ObjectiveCatalog.cs#L33-L93) · [CaptureObjectives](../../../Assets/CombatPrototype/AdventureFlow.Objectives.cs#L12-L23) · [Evaluate](../../../Assets/CombatPrototype/ObjectiveEvaluator.cs#L246-L289) · [Rules](../../../Assets/CombatPrototype/AdventureRules.cs#L13-L39)

[D] 本方案仅记录由 ForestExploration 局产生的有效目录卡片。需要卡片与实际 Run 的地区/类型匹配、现行求值确认 achieved、终局为 Extracted，且该 Run 的 Committed 成功持久化。Death、Abandoned、测试挑战、空或不匹配 ID、证据不足、仅击杀、仅开箱、仅领取均不生成历史。退出未结算的冒险时不提前记账。当前局重启可能遗失内存毛量。以源码支持的可靠当前证据为准，可证达成仍可记录，无法确认时保留未知，不把 exact 当作完成条件或改变目标判定。 [目标账本](../../../Assets/CombatPrototype/ObjectiveEvaluator.cs#L14-L42) · [终局提交](../../../Assets/CombatPrototype/AdventureFlow.cs#L182-L225)

### 写入和恢复顺序

1. LockOutcome 用现行求值固定候选及时间。固定 ObjectiveId、来源 Run、结算键、UTC 和必要显示快照，仅在 AdventureRules.Plan 的独立计划 profile 中追加。按三元键与本局卡片校验。Pending 写入同一封套中的 plan 是候选，页面始终读已发布主 profile。
2. CommitSettlement 使用既有 plan，一次发布 Committed、主 profile、奖励变化与 committedRuns。只有保存结果确认后，历史视图才能见到新项。不能直接绑定提交期间的临时内存 profile。领取奖励、回营确认、读历史与重试都没有独立追加路径。
3. 发布前失败保持 Pending 原计划，重试使用同一身份和时间。已知发布后失败以磁盘完整读回比对 profile、plan、结算键、revision 和页后认领。未知冻结写入。恢复 Pending 不重算旧候选。已提交但回营装载失败仍识别已提交主档，不再记账或发奖。 [保存边界](../../../Assets/CombatPrototype/CombatSaveSystem.cs#L75-L105) · [状态验证](../../../Assets/CombatPrototype/AdventureValidation.cs#L52-L58)
4. 当前 plan 的历史更新只能是同一旧列表或追加本局并按上限淘汰首项，旧记录内容不可变。提交时历史与 plan 一致。既有 acknowledged 后工作流保留其合法资料变化，不依赖主 profile 与旧 plan 在所有字段上的永久相等。

## 数据模型比较

| 维度 | A · 单一有界 ObjectiveHistory | B · 独立终局回执与长期历史 |
|---|---|---|
| 数据冗余 | 回执按三元键从主列表投影。计划仅是既有事务镜像 | 两处都要表达达成身份、时间和结果 |
| 去重 | 每档每局一条，沿用 committedRuns 的永久去重职责 | 两套唯一性外还要验证映射和生存期 |
| 容量 | 固定上限，封套中同时预算 profile 和 plan | 回执寿命独立，但重复载荷与边界更多 |
| 查询 | 一个集合供筛选和近期结算读取 | 近期查询更直接，跨视图须检查一致性 |
| 迁移复杂度 | 同一默认写入主档及存在的 plan | 多个可选存在位及匹配默认 |
| 中断恢复 | 沿既有 Pending→Committed 一次发布和回读 | 同封套仍要校验两个对象是否一并生效 |
| 未来扩展 | 只读元数据目录可扩展，历史形态仍紧凑 | 适合有独立审计寿命或独立终局消费者的需求 |
| 旧档兼容 | v9 空历史加覆盖标识，无推测回填 | v9 两边都未知，需防止部分默认造成假回执 |

[D] 已确认采用 A。已提交主 profile 是唯一历史事实源。近期结算按三元键查询同一集合，无独立持久回执。

## 逐字段审批清单

[字段审批表](OBJECTIVE_HISTORY_FIELD_APPROVAL.csv) 为九个逻辑字段的权威审查表。当前存储候选包括 RunId、ObjectiveId、RegionId、CompletedAtUtc、CommittedAtUtc 与 DisplayNameSnapshot。SettlementId 由 RunId + :terminal 派生并核对源记录。DefinitionVersion 当前无必要。CompletionType 从下节稳定映射派生，无独立字段。现行有效终局只有 Extracted，结局由历史成员资格派生。

容器默认是 ProfileState.objectiveHistory=[]，主 profile 与有效 plan 一致初始化。objectiveHistoryLegacyUnknown 在 v9 迁入显式为 true，新档为 false。历史项无缺失默认，v9 不构造任何历史。目标版显式字段缺失、类型错误或超限须拒绝。两个容器字段随清单审批。

档内按 RunId + SettlementId + ObjectiveId ordinal 去重，仍须通过 committedRuns 的结算屏障。同一三元键不重复追加。不同 Run 的同一目标分别记录。同一 Run 的第二个目标与现有单卡合同冲突，拒绝发布。裁剪后不得靠历史名单判断旧终局能否重试。当前已确认世代的 committedRuns 提供持久判据，无需另建去重表。 [事务模型](OBJECTIVE_HISTORY_TRANSACTION_MODEL.md)

## CompletionType 的稳定派生

[S] 现行 ObjectiveCatalog 有九个稳定 ID 和对应的 ExpeditionGoal。Boss 与 Special 是本设计的历史展示分类，部分 Challenge 卡允许精英或首领任一达成，因此仅靠 ID 后缀、当前 goal 或可变 UI 名称无法完整分类。 [目录](../../../Assets/CombatPrototype/ObjectiveCatalog.cs#L42-L93)

[D] CompletionType 为 DERIVED_NO_STORAGE。以稳定 ObjectiveId 做 ordinal 查表，冻结下列历史兼容映射，与当前卡片 UI 名称和可变规则解耦。

| CompletionType | ObjectiveId |
|---|---|
| Gather | forest.gather、ruins.gather、cavern.gather |
| Treasure | forest.treasure、cavern.treasure |
| Challenge | forest.challenge |
| TreasureSpecial | ruins.treasure |
| ChallengeBoss | ruins.challenge、cavern.challenge |

新增目标在允许生成历史前须登记该映射。已写入历史的 ID 即使退出当前目录也保留历史映射。同一历史身份不可重分类，重新定义类别时使用新 ID。读取未知但结构合法的 ID 时仍显示已存名称和地区，类型标未知，不猜测首领或专项类别。全历史及地区筛选可查询，已知类型筛选不命中该项。支持目录的漏配由验收拒绝发布。DefinitionVersion 无需入档。

## 留存、排序与边界

- 128 条已确认记录占满时，仅新的合格三元键提交可形成第 129 项候选。计划列表尾追加，再按提交顺序从头移除一项，与新结算原子发布。未确认前主列表保持原 128 条。重复、失败、取消、读取和筛选均不裁剪。目标档输入超过 128 条时拒绝，不静默修复。
- 仅改 ObjectiveHistory。裁剪不修改 committedRuns、地区累计、首领与特奖回执、库存、领取状态或任何其他累计数据。超出封套容量则拒绝该次发布并保持原档，禁止扩大裁剪范围。预算覆盖主 profile 及 plan。
- 保留顺序使用提交顺序。展示固定按 CompletedAtUtc 降序、CommittedAtUtc 降序、稳定三元键 ordinal 升序。先筛选，再排序和按每页 20 条分页。时钟回拨不改变留存次序。CommittedAtUtc 在合格计划首次形成后、首个 Pending 写入前采样一次。只读视图在确认发布后展示。不得沿用数组位置作为并列键。

## 冒险历程

- 营地进入「冒险历程」，默认显示全部。地区和目标类型可组合，支持首领／特殊挑战视图，排序、分页与并列规则按上节。
- 每条显示完成时的名称、地区、完成时间（本地显示并标示时区）、来源 Run（可查看完整 ID）、成功撤离、目标类型及首领／特殊挑战标签。冻结标签映射：遗迹守护者和洞窟守望者为首领目标，遗迹机关链为特殊挑战，森林「拔点」是精英或首领均可满足的通用挑战，因此不标示为首领击杀。其余普通卡不标。退役卡片继续使用历史映射。
- 新档无记录时显示「尚无已记录的完成目标」。迁入空历史显示「旧版目标历史未知」，有记录后仍提示升级前历史不可用。筛选无匹配单独提示。列表提示最多保留 128 条，未知、已裁剪和筛选无结果均不表达为目标未完成。目录改名或退役时仍展示冻结名称和已知分类。未知地区名可使用稳定键及未知说明。历史视图不触发保存、奖励或地区统计。

## 单次迁移与备份

[D] 目标版本提案为 **v10**，一次从 v9 直接发布，v11 保持历史。先独占与严格验证 v9 原始封套、checksum 及外置页，再归档主档、滚动备、主备和保留世代全部可达掉落分页、关联文件、必要事务、版本与原始哈希清单。只初始化上述默认并保持原业务状态，按目标规则重读暂存件，校验父指纹后原子替换。崩溃前后分辨真实父/子集合，重试幂等。旧版恢复使用完整迁前快照及隔离根，解冻前由旧版验证。 [一次性迁移](MIGRATION_V10.md) · [备份与恢复](BACKUP_RECOVERY.md) · [Player 验收](PLAYER_ACCEPTANCE_PLAN.md)

[S] v9 的 committedRuns 只有身份。SettlementRecord 只有最近结局和计划，出征可清除它，目标求值依赖消费前的运行时累计证据。由库存、奖励、徽章推导会误记。迁移不倒填任何历史。地区长期线仍只投影既有记录。不得从有界 ObjectiveHistory 推算或补齐探索次数、成功撤离总数、首领挑战总记录、收藏进度或最佳成绩的 DATA_GAP。 [存档架构](SAVE_ARCHITECTURE.md)
