# RUNLOOP-01-R1 证据索引

- [机器可读状态与分层](status.json)：attempts/findings/current_acceptance/deferred 分离。
- [暂存内容与 LFS oid 核对](publication-check.json)：1525 个清单文件逐字节/oid 核对通过，119 个 LFS 文件；无用户文件暂存。
- [完整文件清单与双哈希](manifest.json)：发布文件 SHA256、原始 sourceSHA256；日志 gzip，原件仍在拥有者根。
- [源与输入绑定](Bindings/source-bindings.json)、[构建输入](Bindings/build-inputs.json)、[独立进程序列](Bindings/r1-sequence.jsonl)、[五进程](Bindings/verified-sequence.jsonl)。
- [审核模型重跑](Bindings/model-rerun.json)只有离线分支条件；配套来源原件见 ../ReviewModel，不计 Unity 数量。
- Before01/02/03/04/05：初始工具与夹具失败、合法负例原始结果均保留。Before04 为产品缺陷真实 Unity 复现，17 PASS/15 FAIL；不能与当前代码结果相混。
- Before06/After04：最终相同矩阵源码针对旧/新产品，独立根、实际执行源码和指纹；旧版没有新 presenter API，夹具使用其旧三分支行为；前版恢复入口丢失明确记录。
- After01/02/03：修复后独立尝试。After03 含发布前精确 Pending、负例候选、解析/运行时失败后相同界面命令二次读取、主备及 ground-loot 回调前后指纹。
- Migration01/02/03：v1～v8 有限迁移门禁及发布失败重试，不是旧版所有内容组合验收。
- RunloopFault-Run、RunloopUncertain-Missing/Corrupt：原回调发布一致性与恢复专项新运行。
- Verified/{Run,Running,Pending,Committed,Final}：五个独立进程，每阶段实际源、进程回执、主备、期望身份与检查结果；VerifiedShared 原合成连续档。
- RuntimeAudit：实际森林实体、资源生命、敌人生命、事件状态，不只 DTO。
- EntryRun、Catalog-*：真实标题/新档业务与完整读取/档案归档恢复；受控 Editor 命令，非原生点击。
- Regression：输入、观测、Boss 和三个正常 AI 进程，轨迹/恢复分开归档。
- Build/build-report-messages.json：非开发原 BuildOptions.None、完整消息；Build/release-inspection.json：哈希与 PE 边界，无测试驱动。
- Bindings/user-before/final、history-before/final、protection-check：用户五文件及历史文件保护核对，不发布用户场景内容。

没有本轮原生 UI、独立人工或性能数据；仍 NOT_RUN。旧引擎/关闭根因仍 UNRESOLVED，未通过本轮改名为 PASS。初始失败未归档执行源码的尝试只保留实际日志，不补造丢失快照；最终 Before06/After04 用相同冻结夹具补齐可复跑对照。
