# 验收与源码审计

## 分层合同

| 层 | 含义 | 输出 |
|---|---|---|
| process | 真实进程结果；exit0 且未超时且启动器 PASS 才为 PASS | 原 `*.exit.json` / results.json |
| integrity | 文件存在、可解析、字段类型合法、唯一名称、冻结项目集合完整 | Semantic/acceptance.json |
| assertions | PASS / FAIL / UNRESOLVED / NOT_RUN，绝不改原 rows | assertions.csv、counts |
| overall | FAIL > INCOMPLETE > BLOCKED > PASS | acceptance.json、REPORT.md、工具退出码 |

明确失败（含启动器额外错误）→ FAIL/1；缺证、非法回执、未启动或超时且没有已知 FAIL → INCOMPLETE/3；有效强制断言存在 UNRESOLVED → BLOCKED/2；仅所有强制项 PASS 且进程成功 → PASS/0。UNRESOLVED 不是 FAIL，也不是 PASS。无实际 exitCode 不可推断进程成功。stdout 中的 Unity 子工具 ExitCode 不是 Player 退出回执。

[Receipt.py](../DeliveryCombatPresentation03/Receipt.py)同时检查顶层对象、layer/scope、非空数组、row 结构、name/detail/frame/time 类型、重复 JSON key、重复断言、未知状态、非有限值；显式绑定原 293 个断言名称，删项/加项均不能悄悄通过。JSON 及 CSV/Markdown 来自同一分类结果，回执 SHA 和合同 SHA 可追溯。输出目录必须新建，不能覆盖旧语义报告。

[Invoke-Runtime.ps1](../DeliveryCombatPresentation03/Invoke-Runtime.ps1)保留原启动/隔离/Step，新增分类后将 semantic-receipt 记为真实断言状态；根 REPORT 链接明确整体结果。[Editor 适配器](../DeliveryCombatPresentation03/Invoke-ReviewEditor.ps1)保留原 Editor 入口，对其实际 process receipt 分类，启动器额外错误传入分类器为 FAIL，不事后改 JSON 造成汇总不一致。

## 工具自测试

[SelfTest-R1.py](../DeliveryCombatPresentation03/SelfTest-R1.py)，[最终自测结果](Evidence/PostStyle/SelfTest/selftest.json)：50 PASS。每个 CLI 用例均验证退出码、JSON 整体状态、Markdown 状态及 CSV 存在；额外覆盖无启动/超时/非零退出/启动器失败和冻结项目缺失。

| 必需场景 | 预期整体 / exit |
|---|---|
| 全 PASS | PASS / 0 |
| PASS + FAIL | FAIL / 1 |
| PASS + UNRESOLVED | BLOCKED / 2 |
| PASS + FAIL + UNRESOLVED | FAIL / 1 |
| 缺文件 / 坏 JSON / 空 rows | INCOMPLETE / 3 |
| 未知 status / 重复名称 | INCOMPLETE / 3 |

工具负例的 FAIL/非零退出是预期拒绝结果，不删除。自测试 PASS 表示拒绝符合合同，不表示产品矩阵或人工体验 PASS。首次两个自测试实现错误以及输入绑定脚本错误保留于 [失败历史](FAILURE_HISTORY.md)。

## 精确源码检查

[Audit-Locked.py](../DeliveryCombatPresentation03/Audit-Locked.py)不再用 assert 或整行模糊过滤：冻结 c7efb644 作为 CP03 前输入，在 BeginAttack 2 行、Release 1 行、Melee 指定锚点后 1 行构造完整期望；每个 before 整行只允许 1 次，最终正文必须完全相等，MeleeTrace 恰好 1 次。[回执](Evidence/locked-contract-r1-attempt2.json)逐项列出位置/内容/数量。

13 个锁定文件逐个规范化字节相等（仅 UTF8 BOM 和换行）：CombatAim、CombatHealth、CombatEnemy、BossBrain、ForestBossBrain、ForestBossRules、ArmorMitigation、AdventureRandom、CombatSaveSystem、CombatSaveData、CatActorVisual、CombatSoundBank、OrbitCamera。FantasyActorVisual 的 LateUpdate→OnDestroy 整个区段逐字一致，唯一精确方法边界和哈希均记录。相对整改基准 72db192a 的全部 Assets/Packages/ProjectSettings Git diff 为空。

弹体采用 `(AttackId,ShotIndex)` 唯一键；拒绝重复、非法身份、缺失、未知追加及 NaN/Infinity，明确按 xyz 比较。历史 Before2 恰好 24 个配对样本，Final2 只允许已单列暂停箭 `(59,1)`，24 组实际 origin/direction 各坐标完全一致；追加箭不混算成配对。

负例覆盖同一行夹带玩法、重复/缺少 Trace、篡改参数、重复允许调用、额外逻辑、释放逻辑、采样时钟/边界、全部 13 锁定文件、弹体坐标/方向/缺失/额外/重复/非有限，以及审计 CLI exit1/FAIL 报告。[旧工具放行证据](Evidence/PostStyle/SelfTest/old-audit-bypass.txt)与新工具拒绝同类变体同时保留。

## 真实重跑

| 新集合 | 实际进程 / exit | 断言 | 整体 / 分类 exit |
|---|---|---|---|
| Editor | PASS / 0 | 291 PASS、2 UNRESOLVED | BLOCKED / 2 |
| EditorDiagnosis | PASS / 0 | 291 PASS、2 UNRESOLVED | BLOCKED / 2 |
| RuntimeFinal 非开发验收 Player | PASS / 0 | 291 PASS、2 UNRESOLVED | BLOCKED / 2 |

过程均未超时、无强制终止。旧矩阵未继承，新结果分别保存。[统一结果](Evidence/result-summary.json)。Editor、驱动观测、非开发验收 Player 都不是原生输入、正常 AI 冒险或人工试玩。没有发布“纯发行原生 UI 通过”结论。
