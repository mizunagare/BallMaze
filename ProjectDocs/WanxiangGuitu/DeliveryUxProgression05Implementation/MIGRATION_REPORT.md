# v9 → v10 一次迁移

普通标题检查只识别来源与现行目标。用户在读取页明确选择新版后，验真 v9 并保留完整旧集合。新版目标为 ForestRuins-v10，旧版客户端仍选 ForestRuins。导入对目标使用独占句柄并比较源档前后指纹。目标已存在时保留原样。

从独立归档读载荷，仅初始化空历史及旧覆盖未知。有效旧 Pending 保留计划与状态，迁移不评价目标、不发奖。外置页保持原格式，分离候选验真后原子发布新版目录，再读取实际目标。旧客户端继续使用原根。

A02 原始失败为内部暂存路径超过 Mono 可用范围。A03 与完整 Acceptance 的 A04 成功。最终 Acceptance-07 的 MIGRATE-PAIR-A05 再次验证显式迁移，CLIENTPAIR-V10-A05 验证新版继续读取和写入。窗口范围及故障残余见 [运行矩阵](PLAYER_RUN_MATRIX.csv) 和 [备份恢复报告](BACKUP_RECOVERY_REPORT.md)。
分别从已证明的实验 v9 夹具衍生主备 checksum 错误和未来版本两个负例。BAD-SHA-A01 与 FUTURE-SOURCE-A01 均在标题拒绝打开来源，检查未生成 v10。
