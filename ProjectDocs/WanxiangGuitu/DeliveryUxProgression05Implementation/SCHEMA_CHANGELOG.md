# UX-05 v10 Schema 变更

- 信封 adventure writer 为 v10，reader 区分并验真 v9/v10，未知或未来版本拒绝。v9 读路径不自动升级。
- ProfileState 包含 objectiveHistory 数组和 objectiveHistoryLegacyUnknown 覆盖标志。已存在的 SettlementRecord.plan 使用相同 ProfileState 结构。迁入时两处为空列表且旧覆盖未知，新档为空且覆盖标志 false。
- ObjectiveHistoryEntry 的六个序列化字段为 runId、objectiveId、regionId、completedAtUtc、committedAtUtc、displayNameSnapshot。UTC 格式固定为 round-trip o 且以 Z 结尾。缺失、超限及非法字段拒绝。
- SettlementId 按 runId + :terminal 派生，CompletionType 由稳定 ID 的历史映射派生。DefinitionVersion 不入档。未创建额外永久去重表。
- CommittedAtUtc 是冻结的计划时间。真正持久化通过主档校验、精确候选 SHA 及业务读回确认。
- 128 条容量以提交顺序裁剪，展示按两个 UTC 降序及三元键 ordinal 升序。现行 committedRuns 不裁剪。
