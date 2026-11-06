# First attempts — retained, not final acceptance

- Audit shell attempt: PowerShell rejected a Bash-style brace path list. Read-only command was corrected; no product action occurred.
- Audit lookups for absent paths/tools returned errors. Archived C2.3 tooling was then read with git show; no historical files were replaced.
- Bake1: isolated Unity exited 0. This proves compilation/resource generation only, not runtime acceptance.
- EditorStage1: exit 1, game-ready wait failed. Title/new-confirm passed. Driver used batchmode, while CombatSaveSystem.Start explicitly exits for Application.isBatchMode. No product startup code changed to accommodate the test.
- EditorStage1NonBatch: rerun used the existing inactive-desktop, non-batch entry. Original failed log remains intact. Narrow challenge-save/route assertions completed; this is not the full C2.4 acceptance matrix.
- Editor.Search.SearchDatabase internal ArgumentOutOfRangeException and shutdown messages remain in the original logs; no causal claim about product behavior is made.

All later attempts must use new directories. Native input, human readability, final balance and uncalibrated performance remain NOT_RUN. Second phase/full normal-AI/reward recovery are not yet validated.

- Phase2PureBuild1 audit first attempt: Audit-Release.ps1 line 10 failed because resources-meta-before-build.json was absent. Build itself succeeded (actual exit 0, 0 errors, 111 warnings). Audit now records missing before-manifest as NOT_RUN/null; no fabricated pre-build hash and no original build changed.
`n- PlayerWindupA1/B1: raw timeline/health/assertions and process exits retained. Summary JSON malformed by interpolated format closing brace (transition -R/R). This is an evidence-tool FAIL; replaced generation with JsonUtility typed serialization. Original summaries remain unchanged. Pair acceptance pending corrected summary verification.

- RewardObserved1: compiler rejected internal CaptureLegacy access; retained compile log. RewardObserved2 uses read-only reflection. PlayerRewardBefore1: failed-write-original-file FAIL; compared against pre-fight file despite legitimate autosaves during attacks. New fixture snapshots current file at first before-publish hook, preserving first failure. No product change.

- LifecycleObserved3 / NormalObserved1: driver compilation CS0136 local-name conflicts; original compiler logs preserved. Renamed test locals only; frozen product unchanged.

- PlayerNormalBankRestore1: full Profile recovery PASS, repeat-commit-rejected FAIL. Existing committed settlement deliberately returns true idempotently (AdventureFlow.cs); test corrected to assert unchanged complete Profile and revision, not a false return. Original log retained.

## 2026-11-07 收尾追加（不修改以上原始阶段记录）

上文“尚未验证”描述的是当时状态；后续已经执行的范围以 REPORT 和原始新目录为准，旧记录不改成 PASS。

- WeaponsObserved1：CS0619，Unity 6000.6.5f1 禁止旧 GetInstanceID API。只把驱动观察身份换为 GetEntityId，WeaponsObserved2 编译及七武器真实命中运行完成。产品没有变化。
- route-three-A1：dormant-lake-nav-risk FAIL。错误把“新 Boss 不贡献风险”写成“整条湖岸所有精英风险为零”。route-three-A2 逐实体记录：既有 c22:channel:crystal-core 在原距离缓冲内，C24 Boss 为 false。修正的是测试对象归因，不删旧敌人、不改评分权重。
- CombatMatrixAudit1：94 PASS / 8 FAIL。6 组 Boss 配对与双刃、巨剑晶柱配对的严格三维坐标比较失败。Y 落地步进微差被真实记录，未扩大容差；功能断言和严格配对分开报告。不是将 13 次运行退出 0 写成全矩阵通过。
- 半血 A2/B2：继续 INCOMPLETE。同步归因和真实恢复结束顺序的观察能力不足，按用户指示不再重采，不以其他完整战斗覆盖。
- 远端首次 ls-remote：连接重置；HTTP/1.1 重试读取成功，main 为 72db192a527bd256e2ba18cd7ab334d8334051da。没有改凭据或 main。
- 构建输入核对：9 个新 C24 材质 `_Color` 由隔离 Unity 写回；BaseColor 不变。保存全部字节差异，不宣称完整构建语义等同性。
- 保留 111 条发行警告、JobTempAlloc、Editor.Search 等原始日志。未过滤、未修改引擎/供应商或用户配置。
- 暂存区全文件 whitespace 检查退出 2：原始 Evidence 使用 -text 保留 CRLF，Unity 序列化文件含生成的空字段尾空格。产品 C# 专项检查退出 0。未为格式检查重写原始证据或资源；原始检查日志 gzip 和 SHA 保留。
