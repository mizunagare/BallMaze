# B10 / B10-R1 证据索引

最终构建输入 `6cad42d535347e0d96ede0e40f3d6a889a846bab`，开始远端main `b474765dc9c28aaf7d2d267bc0362f828f1902b0`。正式Player、Editor、受控回调、正常AI和原生UI分别标记。完整存档、分页、缓存和可执行二进制不上传。

## 当前主视觉与前后对照

- [主要概念原图](../ArtBible/Concepts/Revisions/用户主要视觉参考_黑猫猫族世界.png)：用户提供，仅设计参考。原始9图、历次方向、输入/来源哈希见ArtBible，未冒称动画或模型成品。
- [AssetAcceptance/INDEX.json](AssetAcceptance/INDEX.json)：12模块34组同分辨率原始前后截图。before为固定b474导出，after标题/动作/管理来自最终6cad新All，敌人来自799bd556的EntryFinalGate；两个输入分开记录。受控Editor，**不是原生或人工试玩**。
- 每个模块有concept/before/after、额外分辨率与动作、asset-mapping/runtime-check/review。映射中的文件SHA与实际资源台账相互对应。
- [AssetAcceptanceHistory](AssetAcceptanceHistory/)：最新主概念之前的旧图和映射原样保留，不覆盖旧视觉问题。
- [ExactBefore](ExactBefore/)与[BeforeCastFailure](BeforeCastFailure/)：不可变基线导出清单和旧版近战不可见FAIL，保留空画面，不伪造通过。

## 失败与定向诊断

- [FailureAttempts/INDEX.json](FailureAttempts/INDEX.json)：三轮旧All、当前材质/标题定向结果及失败日志（脱敏）逐次独立。
- [IconAlpha](FailureAttempts/IconAlpha/)：四个缺面图标的原始before、修复后after和实际alpha覆盖结果。只检查格式/完整性，不等于人工可辨认。
- [TitleFaceObscured](FailureAttempts/TitleFaceObscured/)：原始树冠遮脸与清场后原图，review.json明确before为图像检查发现、after有新增四分辨率几何遮挡断言。
- [旧绑定与拾取检查](FailureAttempts/B10RemainingRegressionGates/TargetedDiagnostics/)：旧骨架Renderer后来disabled；当前猫部件使用ActorFade。实际拾取CanPick/容量/位置日志，与原经济断言保留。
- [营地暂停交互](FailureAttempts/B10R1EntryFinalGate/TargetedDiagnostics/)：真实冷却、受控CC位移.2m与E目标camp:equipment；教程阶段正确。
- [EntryBefore](EntryBefore/)与[EntryAfter](EntryAfter/)：最初入口FAIL和P0定向修复结果；不替代最终输入复跑。
- [PlayerAttempt3](PlayerAttempt3/)与[PlayerAttempt4](PlayerAttempt4/)：旧受控非开发Player失败/修正历史；不继承为本轮正式结果。
- [FinalStyleDirected](FinalStyleDirected/)、[DirectedCatUI6](DirectedCatUI6/)等是此前简化风格/图标阶段历史，不能冒充用户最新材质风格通过。

## 最终新All（已结束）

外部原始运行目录 `D:/WanxiangValidationRuns/B10R1ReadinessFinalAll/20261026-202935-daf97cfa`。独立JSON/CSV、21正常AI轨迹、结算与新进程审计、无驱动正式Title截图、受控验证Player回调/退出/恢复、完整构建警告/哈希和性能观测，已在结束后按原脱敏器发布。原始日志保留工程外；压缩发布日志记录原始/脱敏SHA，不吞异常。

## 仍开放

D3D12 UNKNOWN与Editor青色帧根因UNRESOLVED；原生U16/独立人工理解NOT_RUN。背景WM_CLOSE、受控退出按钮和原生标题栏分别对待。只要没有安全独立输入环境或新因果证据，不伪造通过、不重复无效关闭实验。

[BeforeReadiness](BeforeReadiness/)保存前一完整轮的进程PASS、完整正式截图/Player恢复和审计，但实际549产品空引用使其验收FAIL。新的readiness前后结果在FailureAttempts/ReadinessBefore与ReadinessAfter，不吞日志、不以最后PASS覆盖失败。


## 本次最终可核对入口

- [FinalAudit/closure-summary.json](FinalAudit/closure-summary.json)：146/2/3/2，0非预期失败、21正常AI、8正式标题、子Player15单列、117日志0引用错误、实际构建哈希/性能。
- [FinalAll/Diagnostics/results.json](FinalAll/Diagnostics/results.json)、[CSV](FinalAll/Diagnostics/results.csv)：逐命令、时间、实际退出码、超时和状态。
- [FinalAudit/source-build-provenance.json](FinalAudit/source-build-provenance.json)：109产品源码、1143输入及147实际执行驱动；原始差异不隐藏。
- [FinalAudit/user-input-proof.json](FinalAudit/user-input-proof.json)、[cat-resource-input-check.json](FinalAudit/cat-resource-input-check.json)：用户文件保护和276猫资源。
- [正式Player主菜单](FinalAll/Screens/B09-Title-Missing/title-player.png)：无驱动发行二进制。
- [验证Player营地](FinalAll/Screens/ControlledPlayer/Case-new/b10-player-game-ready.png)、[背包](FinalAll/Screens/ControlledPlayer/Case-read/b10-player-inventory-0.png)：独立非开发驱动版，不是原生输入。
- [退出/存储审计](FinalAll/Diagnostics/ControlledPlayer/)：entry-audit、storage-audit、实际自退出及read/continue/new/pending校验；不发布完整存档。
- [异常清单](FinalAudit/exception-inventory.json)、[警告行](FinalAudit/build-warning-lines.json)：本轮只剩73 Editor.Search异常起始行；BuildReport88警告与172“warning”行不是同一个统计。
- [AssetAcceptance](AssetAcceptance/)更新为6cad代码的34组对照，敌人取景仍明确来自799bd556；图库不是原生或人工验收。

[首轮结算样本](FinalAll/ExistingFramework/SettlementSummaries/)是Pending捕获，后继Commit/ACK与入仓恢复见21进程轨迹；不把Pending状态冒称已经提交。

[暂存证据校验](FinalAudit/staged-byte-check.json)与[补齐忽略日志前的FAIL](FinalAudit/staged-byte-check-before-log-add.json)分别保留；不是玩法测试。

## 第一阶段复审准备（独立结果）

[报告](../ReviewClosure/REPORT.md) · [结构化P0台账](../ReviewClosure/OPEN_ITEMS.json) · [复跑](../ReviewClosure/TESTING.md) · [修复前11PASS/1FAIL](../ReviewClosure/Evidence/before.json) · [修复后12PASS](../ReviewClosure/Evidence/after.json)。只读源码/证据检查，不是新运行或独立审核通过。
