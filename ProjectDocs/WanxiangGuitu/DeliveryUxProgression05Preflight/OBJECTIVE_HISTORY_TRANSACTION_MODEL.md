# ObjectiveHistory 持久化事务模型

[D] 设计审查，IMPLEMENTATION_NOT_STARTED。D-19/D-20/D-23 均 A。v10 暂定。提交时间采用方案 A，字段与实施授权待审批。已确认主 profile 是唯一可查询的 ObjectiveHistory。Pending 的 plan 是既有结算事务投影，无第二个历史事实源。

## 源码实际先后 [S]

1. ResolveTerminal 根据死亡或已请求结局进入 LockOutcome。CaptureObjectives 先取现行 Live 快照，匹配地区与目标卡，调用 Evaluate。achieved = met && settledSuccess，结果留在非序列化 LastObjective。条件满足本身不等同于目标完成。结算前补结死敌掉落、捕获世界及仓库快照、处理教程，再建结算 plan。 [终局入口](../../../Assets/CombatPrototype/AdventureFlow.cs#L45-L65) · [快照](../../../Assets/CombatPrototype/AdventureFlow.Objectives.cs#L12-L23) · [求值](../../../Assets/CombatPrototype/ObjectiveEvaluator.cs#L75-L92) · [终局达成](../../../Assets/CombatPrototype/ObjectiveEvaluator.cs#L246-L289) · [锁定](../../../Assets/CombatPrototype/AdventureFlow.cs#L182-L189)
2. AdventureRules.Plan 首先检查 committedRuns，克隆 profile 后以 RunId + :terminal 组装结算，将战利品、材料、配方和溢出待领写入 plan，追加已结算 Run。OutcomePending 主 profile 尚未采用 plan。Pending 先保存，恢复会还原原 plan 并冻结。 [计划](../../../Assets/CombatPrototype/AdventureRules.cs#L13-L39) · [恢复](../../../Assets/CombatPrototype/AdventureFlow.cs#L82-L101)
3. CommitSettlement 只使用既有 plan，先换入候选内存 profile，清活动 Run 并把记录设为 Committed，然后保存。SaveProgress 在分离副本校验并打包四个可能的分页世界，写并刷新临时封套后 Replace/Move。after-publish hook 或载入营地可能在持久化之后失败。失败路径只认精确子快照或精确父快照，否则设置 SettlementNeedsRead。v9 无 ObjectiveHistory。 [提交及回读](../../../Assets/CombatPrototype/AdventureFlow.cs#L191-L225) · [发布](../../../Assets/CombatPrototype/CombatSaveSystem.cs#L75-L105) · [校验与分页读回](../../../Assets/CombatPrototype/CombatSaveSystem.cs#L221-L237) · [分页闭包](../../../Assets/CombatPrototype/GroundLootStore.cs#L15-L49)
4. 确认回营单独保存 acknowledged 与教程状态。待领由待领 ID、剩余额与既有特殊回执控制，用营地事务写入。历史及裁剪不参与领取或放奖决策。 [确认](../../../Assets/CombatPrototype/AdventureFlow.cs#L221-L225) · [领取](../../../Assets/CombatPrototype/AdventureFlow.World.cs#L14-L32)

## v10 条件状态转换 [D]

目标完成 → Pending 固定快照 → 验证来源和奖励计划 → 确认 Pending 可恢复 → 原子发布 Committed → 读回确认后发布历史视图 → UI 查询。

目标完成取包含成功撤离的现行 achieved，以符合资格的终局首次确认时刻采集 CompletedAtUtc。捕获稳定三元键、名称、地区与两项冻结 UTC。CompletionType 由 ObjectiveId 通过历史兼容映射派生。历史候选和原奖励 plan 同一事务。当前 CommitSettlement 在发布前已交换内存 Profile，UI 须从最后已确认快照读取，或在未决时停用历史查询，避免内存先行泄漏。已提交子封套含主 profile、同一次交易奖励和 committedRuns。主封套引用的页先耐久，历史不做独立写入或分页。

| 中断位置 | 持久状态及恢复 |
|---|---|
| Pending 写入前 | 仍为上一完整检查点，无可靠候选、无新增历史或结算奖励。进程内重试可沿原冻结候选，进程丢失则恢复旧活动局。玩家从旧检查点再次达成真实终局可走新的正常捕获，恢复本身不为丢失的历史重算。 |
| Pending 写入后 | 主历史不变，已保存计划可恢复。使用固定目标快照及原 plan，校验 run、settlement、objective、profile 和父 revision。 |
| 奖励准备后 | 源码实际先准备奖励计划才写首个 Pending。若 Pending 尚未成功则仍处于旧检查点。若已写，确认或处理提交时仅使用该计划，领取路径不开放。 |
| Committed 写入期间 | 页或临时档不算发布。只认可核验完整精确父或子。父仍在则可重试同一候选，子已发则只认领。第三种状态冻写。候选列表在副本可算裁剪，权威旧历史保持不变直至确认。 |
| Committed 成功但进程退出 | 用新进程读实际主封套、版本、revision、checksum、全部可达页和业务键，验证历史、已结算集合与奖励一起生效。不运行 Plan、ObjectiveEvaluator 或再发奖。 |
| 回读成功 | 精确匹配子世代即发布只读历史。精确匹配父仍为 Pending。其他或页缺失归为不确定。回读规则对比实际语义与原始身份，不能只依赖 revision 或保存返回值。 |
| 重复确认 | Commit 的 Committed 分支既有幂等门保持。回营确认和奖励领取按自身合同处理，不追加历史、不裁剪、不改时间。 |

旧 v9 Pending 默认无历史候选，不重算。v9 已提交记录及孤立页都不能推测旧历史。版本迁移依赖完整归档和源/目标世代复验。 [单次迁移](MIGRATION_V10.md)

## 裁剪后的去重证据

[S] committedRuns 是每档持久终局事实清单。Plan 拒绝旧 RunId，成功提交的 profile 则增加 RunId。验证拒绝重复 ID，限制最多 100,000，且拒绝已结算 Run 成为活动局。Pending 必须用有效活动 Run、主 profile 不含本局、plan 含本局。Committed 必须无活动 Run、主档含本局。下一次出征清除最近 SettlementRecord，故它或可派生 SettlementId 单独无法提供长期去重。 [计划](../../../Assets/CombatPrototype/AdventureRules.cs#L13-L32) · [验证](../../../Assets/CombatPrototype/AdventureValidation.cs#L8-L15) · [活动局及终局验证](../../../Assets/CombatPrototype/AdventureValidation.cs#L31-L58) · [出征](../../../Assets/CombatPrototype/AdventureFlow.cs#L132-L155)

[D] 当前每局一张卡、一个终局。档内逻辑历史键为 (RunId, SettlementId, ObjectiveId)，SettlementId 按源事务核验后派生，三元 ordinal 比较。新增须同时通过既有 RunId 结算屏障。即使历史项裁剪，只要已确认世代保留 committedRuns，就不重放。当前证据足以复用既有字段，额外持久化需求为零。100,000 边界及 8 MiB 拒绝行为不变，不删除已结算键换容量。旧备回退到提交前属于恢复旧分支，不能从其自身证明后来世代曾提交，禁止合并或拿旧世代重放到现行档。双写者、过期主档或跨根混用需由持锁、父代比对和隔离规则阻断。若未来允许一局多目标或清理 committedRuns，先审是否须新增永久身份账，再确定最小差异。

## 双时间冻结与排序

[S] savedAtUtc 在临时封套及 Replace 前生成，普通保存也会更新。实际提交发生在主封套发布时。 [原始取时与发布](../../../Assets/CombatPrototype/CombatSaveSystem.cs#L84-L105)

[D] 采用方案 A。CompletedAtUtc 在现行完整目标达成时采样。CommittedAtUtc 表示**结算提交计划时间**。合格目标和结算计划首次准备完成后，在首个 Pending 写入前给同一候选采样一次 UTC，并同计划一起冻结。它描述计划形成的时点，实际主档发布由独立的读回确认判定。Pending 恢复、首写返回失败、重试、确认回营和 Committed 失败均不得调用时间源补写原候选。封套 savedAtUtc 和文件时间均不作为历史时间来源。

[D] 首次 Pending 写入结果不明时，先验证实际主档及其分页。精确匹配已保存 Pending 即复用。确认仍为旧检查点且同进程持有原候选时可重存原值。若跨进程只能恢复旧检查点，丢失的候选不创建历史或补时间。只有玩家重新完成真实终局，才会创建新的 Pending 候选。已保存 Pending 中缺失或非法的目标候选时间按 v10 结构错误处理。迁入时无候选的旧 v9 Pending 沿原计划继续结算。

[D] 读视图依次使用 CompletedAtUtc 降序、CommittedAtUtc 降序、三元键 ordinal 升序。两个 UTC 可相等，也可受时钟回拨影响。排序不依赖本地时区、时间单调性、哈希遍历或翻页动作。留存按已确认提交顺序，第 129 项确认后移除数组中最早提交的一项。该改动与新历史、committedRuns 和原计划收益一起进入同一 Committed 主封套。重复提交与领取仍走既有不同事务入口。 [字段审批表](OBJECTIVE_HISTORY_FIELD_APPROVAL.csv)
