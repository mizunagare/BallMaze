# UX-05 一次性迁移窗口设计

负责人已裁决，不再处于待决状态。2026-11-18 冻结 D-19 A、D-20 A、D-23 A。文件名沿用原交付路径。若字段证据及后续授权均成立，从 v9 直接迁至一个获批目标版本，一次发布，无中间公开版本。暂按 v10 设计。CommittedAtUtc 采用 Pending 冻结的结算提交计划时间，等待字段和迁移实施授权。跨重启历史需求已经确认，v9 仅为旧档和无写入对照。 [专项字段设计](OBJECTIVE_HISTORY_DESIGN.md)

## 目标字段证据与取舍

| 研究项 | 现有来源与丢失点 | 候选与默认 |
|---|---|---|
| 目标完成回执 | RunState 保存当前 region、goal 和净余量。targetReached 属于测试挑战。终局 CaptureObjectives 在卸载前计算非序列化 LastObjective。已提交 SettlementRecord 保存结局及库存差分，无 cardId 或达成事实，并且提交后 activeRun 为空。重启无法从净余量恢复累计毛量，同一净量可对应不同达成结果。 | 若必须跨重启展示经确认的终局达成，研究带显式存在性的终局回执。v9 默认无记录，旧达成未知。 |
| 目标历史 | ProfileState.committedRuns 仅保留终局去重 ID，未保留地区、目标或达成事实。下次出发会清除最近 settlement。徽章、首领和特奖回执仅记录各自事件，不能完整关联目标。 | 若必须跨局回看，研究有界的已确认完成记录。v9 默认空且旧历史未知。优先由一份持久记录投影历史与回执，只有能够证明二者生命周期需要独立载体才考虑分别存储。 |

源码依据见 [ProfileState、RunState、SettlementRecord](../../../Assets/CombatPrototype/AdventureState.cs#L3-L67)、[终局快照](../../../Assets/CombatPrototype/AdventureFlow.Objectives.cs#L12-L23)、[快照与达成求值](../../../Assets/CombatPrototype/ObjectiveEvaluator.cs#L75-L92)、[已提交状态校验](../../../Assets/CombatPrototype/AdventureValidation.cs#L53-L55)、[出发与结算](../../../Assets/CombatPrototype/AdventureFlow.cs#L132-L225) 和 [提交去重](../../../Assets/CombatPrototype/AdventureRules.cs#L13-L39)。达成还要求成功结算，见 [ObjectiveEvaluator.cs](../../../Assets/CombatPrototype/ObjectiveEvaluator.cs#L246-L289)。证据证明现有数据不足以重建完整历史。是否需要持久保存取决于审批后的展示范围，新增字段仍须逐字段审批。

## 候选字段逐项结论

[D] 当局和当次结算仍使用原快照。2026-11-19 已确认跨重启与跨局历史不能由该快照满足。采用单一历史事实源提案，无独立持久回执。本表用于必要性对照，具体字段、默认及版本以 [专项设计](OBJECTIVE_HISTORY_DESIGN.md) 为准。地区缺口保持 DATA_GAP。

| 审查问题 | 目标完成回执 | 目标历史 |
|---|---|---|
| 1. 已有等价数据 | 无。LastObjective 为进程内状态，SettlementRecord.outcome 仅说明结局。 | 无。committedRuns 是已结算去重集合，独立首领或特奖回执仅证明各自事件。 |
| 2. 可否推导 | 当前局可用 region/goal 和现场证据计算。成功撤离与相同净库存可以来自不同累计拾取过程，重启后既有字段无法无损重建。 | 下一次出发会清掉最近 settlement。即使仍有 runId，无法补齐历次目标、达成和地区。不可按徽章或材料差分回填。 |
| 3. 是否必须持久化 | 当次结算展示可用内存。只在必须重启后确认同一终局时需要持久证据。 | 只在必须跨局保留并展示完成记录时需要持久集合。完整旧生涯无法补采。 |
| 4. 重复记录 | 优先共用一份达成记录。仅回执需求可限定最近终局。同时有历史需求则从历史按结算键投影已提交回执。 | 需要历史时用 plan 中候选集合随提交转成权威 profile。plan 是事务镜像。避免另外维护一套永久回执、统计结果或重复的键集合。 |
| 5. 候选写入 | LockOutcome 以现有目标判定捕获已确认的达成，Pending 只固定候选。与终局提交同一发布后才能展示为已提交。 | Plan 计算带上限的候选集合，以已提交 profile 为读面。裁剪规则和覆盖起点随字段批准，优先保留最近终局供回执投影。 |
| 6. 重复发奖 | 仅随既有终局提交。按档内 RunId + SettlementId + ObjectiveId 去重，并复用既有结算防重放。迁移和查看均不调用 Plan、CommitSettlement 或发奖入口。 | 同一三元键只留一项。不同 Run 的同一目标独立记录。同一 Run 的第二个 ObjectiveId 在现行单卡片合同下须拒绝。即使历史裁剪，committedRuns 仍作为既有去重权威。回营确认与读取不会追加。 |
| 7. 中断恢复 | 已有 Pending 沿候选原样恢复，Committed 严格比对并确认。结果不明先锁写、回读实际主档。 | 对比主 profile、plan、run/settlement 键和实际奖励。匹配子世代只补确认，匹配父世代方能重试。其他组合冻结。 |
| 8. 缺失默认 | v9 显式无记录，旧达成未知。目标版本声明为有效记录却缺键或字段非法时拒绝。 | v9 默认空列表且覆盖起点表明旧历史未知。目标版同样要求显式结构与边界，不能用默认掩盖损坏。 |
| 9. v9 影响 | v9 reader 语义、哈希及既有 Pending 保留。迁移不据旧 Pending 重算达成。 | v9 不回填记录，不清除 committedRuns。正常结算、历史边界和 rollback 独立验证。 |
| 10. 零 Schema 方式 | 沿用当局及当次结算快照，重启无证据时显示未记录。 | 提供当前会话投影或显示未记录，跨局持久历史不在该路线交付。 |

[D] 单项身份键为 RunId + SettlementId + ObjectiveId。SettlementId 按终局合同派生并同原记录核对，存储 UTC 和必要历史显示快照。主 profile 与有效 plan 按字段清单初始化，不重算或倒填任何历史。128 条裁剪只改历史列表。地区 DATA_GAP 禁止从该列表反推。 [逐字段审批表](OBJECTIVE_HISTORY_FIELD_APPROVAL.csv) · [事务模型](OBJECTIVE_HISTORY_TRANSACTION_MODEL.md)

[S] CombatSaveData 继承 CombatCheckpoint，根、营地、在途与计划营地都可能有分页，目标记录不属于世界快照。AdventureData.World 精简旧仓库字段，Clone 通过 JsonUtility 复制声明类型。方案需验证显式存在、字段白名单和 plan 深复制。不能靠默认构造、投影或删掉未知 JSON 字段证明兼容。见 [存档架构](SAVE_ARCHITECTURE.md)、[字段清单](SCHEMA_INVENTORY.csv) 与 [CombatSaveData.cs](../../../Assets/CombatPrototype/CombatSaveData.cs#L4-L41)。

## D-23 地区展示指标

| 显示指标 | 原始字段 | 计算方式与覆盖范围 | 是否需要新增字段 |
|---|---|---|---|
| 地区探索次数 | ProfileState.committedRuns、ProfileState.regions、activeRun.region/mode | runId 为 GUID，committedRuns 无地区或模式。regions 的 forest:hunts-complete 为里程碑。当前局只可说明当前状态，无法累计生涯入场。 | DATA_GAP，保留未知，本任务禁止新增 |
| 成功撤离次数 | ProfileState.committedRuns、SettlementRecord.outcome、activeRun.region | 仅最近结算保留 outcome。已提交后 activeRun 为空，历史终局 ID 无地区或结果，无法筛出各区 Extracted 总数。 | DATA_GAP，保留未知，本任务禁止新增 |
| 首领挑战记录 | ProfileState.bossHunts 的 bossId/kills/receipts、badges、regions。specialRewards 的首领奖励回执 | 按森林 bossId 展示已记载击杀次数和徽章，用双首领标记展示里程碑。其他地区的既有首领奖励 ID 仅证明对应首领里程碑。 | 既有击杀和里程碑无需新增。全区挑战尝试、失败和未记载重复击杀为 DATA_GAP |
| 收藏进度 | ProfileState.badges、regions。specialRewards 的 specialRewardId/claimed | 森林展示已获得的两枚首领徽章及双首领里程碑。按目录对遗迹 Artifact/Guardian、洞窟 First 的奖励 ID 去重计已领取项，分母为相应目录项数，已获得待领取单列。 | 该口径无需新增。通用永久装备收藏为 DATA_GAP，B2 进程内收藏不作历史依据 |
| 历史最佳成绩 | ProfileState.committedRuns、bossHunts、badges、regions。最近结算及现行检查点 | 没有按地区保留的历局可比较成绩或最大值。累计击杀和最近成绩不能推导历史最佳，成绩定义也需确认。 | DATA_GAP，保留未知，本任务禁止新增 |

地区键以现行目录 ForestRuins、AncientRuins、CrystalCavern 为准，未知键不归入森林。数据缺口禁止补零、猜测或擅自新增字段。源码见 [局 ID 与生命周期](../../../Assets/CombatPrototype/AdventureFlow.cs#L132-L152)、[森林讨伐和标记](../../../Assets/CombatPrototype/ForestBossRules.cs#L46-L64)、[特奖目录](../../../Assets/CombatPrototype/RuinsSpecialRewards.cs#L7-L30)、[领取与摘要](../../../Assets/CombatPrototype/RuinsSpecialRewards.cs#L96-L106)、[B2 会话收藏](../../../Assets/CombatPrototype/B2Collection.cs#L27)。

地区展示只读。禁止地区等级、永久攻击或防御、掉落倍率、每五次撤离送材料、地区专属配方解锁及任何隐性收益。熟练度、声望或精通沿用 D-06 同一约束。跨局技能构筑保存为 NOT_IN_SCOPE。品质格位、装备尺寸变化及 D-24 攻击力变化排除。

## 单窗口实施顺序

1. **读 v9。** 经获批迁移入口选源，先持规范化根的写者锁。清单浏览和同版读取只走只读路径。检查活动迁址、新档或迁移事务、旧客户端和普通写者。遇到未明事务冻结，完成独立核对后再选源。
2. **验原始校验。** 固定原始封套字节与指纹，验证 payload UTF-8 SHA-256、version/revision/profile、v9 校验及全部页。标记损坏候选，不把不支持、I/O 受阻或权限问题当作损坏。
3. **备份。** 主档、滚动备档、所有保留世代可达页、关联文件、校验信息、必要事务状态和版本清单写入不可覆盖的独立归档，使用源规则验证可恢复性。
4. **迁前检查。** 核对唯一目标版本、获批字段和默认、空间、同卷发布能力及锁覆盖。无法验证依赖闭包、已挂起事务或未知字段策略时停止。零 Schema 路线在此合同之外，无迁移文件、无自动写回。
5. **纯转换。** 只处理分离的 DTO，保留业务语义。对主 profile 和已存在 plan 应用获批缺失默认，不重建现场。新终局记录按后续正常结算生成。
6. **暂存。** 保全既有页，先耐久化候选引用的页。唯一、排他的同卷临时文件写入目标封套并 Flush(true)，原始父/预期子集合指纹先耐久记录。
7. **复验。** 从暂存文件用目标 reader 全量读回。核对页、原始校验、允许差分、版本与 revision，以及库存、奖励、状态和所有引用一致。
8. **原子发布。** 持锁复核父世代及主备指纹，原子替换主档。保留完整旧档和有效备份。已确认成功的迁移只出现一次目标版本发布与一次 revision 递增。
9. **恢复。** 发布前保留父档，可从验证过的归档与父指纹重试。发布后持锁回读，按已确认子、已确认父或未知三类处理。未知冻结并保留证据，不覆盖唯一可恢复世代。
10. **重复读取。** 新版完整校验目标快照，重复同版读取和重复迁移请求不变更档案、回执数量、备份和业务状态。普通保存另测。
11. **跨进程验证。** 首先用新进程重开同一隔离根，核对锁释放、主备页、确认和回执。再以独立克隆验证复现、仅从完整归档恢复 v9，以及不配合写锁的旧版无共享写根。

事务规则及错误分类见 [备份恢复](BACKUP_RECOVERY.md)，跨进程证据见 [Player 验收计划](PLAYER_ACCEPTANCE_PLAN.md)。

## 迁移与结算合同

1. 继续支持 v9 读取。只有确认必要且无法无损推导的目标记录才能进入候选窗口，逐字段记录来源、默认、上限、验证和旧档缺失语义。缺失初始化为明确的无记录或空集合并保留旧覆盖未知标志。保留原 profile、物品、坐标、随机流、结算状态、原计划与旧语义。目标版本声明中的非法结构必须拒绝。
2. 转换分离快照，对既有 Pending 计划应用同样的缺失默认。迁移只复制旧事实，不执行目标重算、抽样、终局提交或发奖。旧 Pending 后续照原计划结算，不补历史。
3. 后续若批准写入新记录，按档内 RunId + SettlementId + ObjectiveId 校验去重。身份、显示快照和 CompletedAtUtc 随 Pending 固定。CommittedAtUtc 在首次合格计划形成时采样一次，与首个 Pending 一起保存。恢复与重试复用原值。CompletionType 按稳定 ObjectiveId 映射，不添字段。历史在确认 Committed 时与原计划收益和 committedRuns 同一事务生效，已提交才作可信展示。重开、确认回营、重试和裁剪后均不得重发奖或重复写回执。证据不足时保留未知。
4. 按 [备份与恢复](BACKUP_RECOVERY.md) 先验证并冻结迁移前原始集合，候选页先耐久化，独占写者校验父世代后单次发布，再完整回读。发布结果不明时先回读判定，重试保持幂等。新版可读旧档，新版进度无法保证无损降级。

隔离 Player 验收另行授权。历史第二阶段见 [MIGRATION_V11.md](MIGRATION_V11.md)。
