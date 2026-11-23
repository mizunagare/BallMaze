# UX-05 验收状态

> **R2当前裁定：PASS（本轮授权范围）。** 以下原实施/R1矩阵保留历史语境；本轮状态见本页末“R2最终复核”。最终混合/空/未知三条原生交互Run均退出0，旧失败与不完整Run原样保留。等待负责人复审。

**部分运行取证。** 完成定义尚未满足。通过判定只适用于表列证据和范围。

| 范围 | 状态 | 证据 |
|---|---|---|
| 标题显式迁移，原 v9 仍可读，v10 正常写 | PASS | MIGRATE-A04，原有 v9 主备夹具，Acceptance-02 |
| 普通启动重复读取 v10 | PASS（现有迁入档） | CLIENTPAIR-V10-A03、LOCK-HOLDER-A04，确认保留原迁移归档 |
| v9/v10 同便携根同时运行、各自写自己子目录 | PASS（Mono 探针） | CLIENTPAIR-V9-A05 和 CLIENTPAIR-V10-A05，两端同时进入各自游戏路径，实际 F5 保存后分别推进修订，v10 为最终 Acceptance-07 |
| 同一 v10 根双进程 | PASS（负例） | LOCK-HOLDER-A04 正常写，LOCK-CONTENDER-A04 观察到 Blocked 和继续按钮不可用。原始探针以 FAIL 退出，保留原判定，作为写访问拒绝的证据 |
| 完整归档哈希与旧版恢复 | PASS（含页和无页夹具） | A04 与 PAGED-RESTORE-A01，见 verified-paged-pending.json |
| 六字段、128/129 边界、被裁剪 Run 拦截、时间冻结、非法字段拒绝 | PASS（合同探针加实档边界） | CONTRACT-A02 覆盖 wire 与旧键。CAPACITY-A02 由 129 次真实目标和提交生成历史，冷进程 CAPACITY-REOPEN-A02 见 128 项、129 个结算键及七页。REPLAY-A01 以该实档回读后的旧 Run 重走产品规划入口，收到已结算拒绝 |
| 真实目标、Pending、替换前失败、替换后回读、重复提交、确认回营 | PASS（受控导航产品链探针） | OBJECTIVE-NEW-A04，三次真实宝箱交互、真实撤离倒计时和结算入口。受控导航未覆盖正常路径体验 |
| Committed 跨进程读回 | PASS（同一目标记录） | OBJECTIVE-READBACK-A04 和 OBJECTIVE-REPEAT-REOPEN-A02 |
| 双 UI 显示、筛选、分页、未知和改名表现 | 部分 PASS | OBJECTIVE-UI-A04 通过 uGUI 名称及筛选后主档不变，CAPACITY-REOPEN-A02 覆盖 uGUI 七页及翻页前后主档指纹，改名和 IMGUI 完整交互待验 |
| 外置页、旧 Pending 迁移、明确中断与恢复 | PASS（指定故障点） | MIGRATE-PAGED-PENDING-A01、MIGRATION-CUT-A03／RECOVER-A03。逐页字节、v9 SHA 和空未知历史已检查。BAD-SHA-A01 同时破坏测试 v9 主备校验，产品拒绝源档且未创建 v10。其他中断点与过期世代重放待测 |
| UX-03 七件武器的技能代表变体 | PASS（14 项 Mono Player 探针） | UX03-*，初次 sword-triple FAIL 保留，修复后新 Run 复测 |
| B1/B2 重点路径 | PASS（代表用例） | B1-B2-GATES-A01，金红保护、入库取回、收藏、错误物品拒绝和真实替换预览提交。其他变体待验 |
| D-20 新一局恢复默认 | PASS（代表用例） | OBJECTIVE-NEW-A04，进入新局前选择非默认槽，成功出征后读到 slot=0 |
| P1C 三地区 Challenge 闭环 | PASS（3 个 Release-08 副本 Player） | P1C-forest/ruins/cavern-A01。既有驱动记录真实行走、击杀、撤离和回营，独立核验各区 v10 历史及 committedRuns |
| D-23 无收益全矩阵 | NOT_RUN | 本批仅取得地区展示筛选和主档未变的证据 |
| Acceptance、NoDefine 完整构建 | PASS | unity-acceptance-07.log、unity-nodefine-07.log |
| Release 正式构建和发行门禁 | PASS | unity-release-08.log 与 release-08.release.json。NO-DEFINE-BOOT-A01、RELEASE-BOOT-A01 到达标题并正常退出，空隔离根未产生主档。早期失败保留 |

见 [Player 执行矩阵](PLAYER_RUN_MATRIX.csv)、[证据索引](EVIDENCE/INDEX.json) 和 [测试记录](TESTING.md)。

## 历史专项矩阵覆盖

| 验收编号 | 本批证据状态 |
|---|---|
| OH01 | 三宝箱真实交互、撤离、Committed 及继续读取已验证，受控导航 |
| OH02 | 替换前真实失败和真实宝箱达标后放弃已验证，死亡及无目录目标变体 NOT_RUN |
| OH03 | 重复提交同一终局已验证，跨 Run 同目标由 OBJECTIVE-REPEAT-A02 和 OBJECTIVE-REPEAT-REOPEN-A02 实测 |
| OH04 | 冷进程原历史读回 PASS |
| OH05 | 同根两局真实目标跨重启均可读取。跨更多地区及长线场景 NOT_RUN |
| OH06 | uGUI 地区和类型筛选通过代表用例，P1C 三地区分别生成正确地区记录。混合地区与分页组合查询 NOT_RUN |
| OH07 | CAPACITY-A02 实际提交达成 128/129 边界，裁剪首个提交项，仍保留 129 个结算键。回拨时钟待验 |
| OH08 | 分页前隔离进程中断与迁移恢复通过。其余切点 NOT_RUN |
| OH09 | v9 营地及含页旧 Pending 可迁入，历史为空且覆盖未知。其余 v9 状态矩阵待验 |
| OH10 | 同候选 Pending 读回、恢复双 UTC、发布后精确确认通过。PENDING-STOP/RESUME-A01 在真正独立进程恢复并提交同一快照。旧 Pending 迁入和冷进程保留也已验证 |
| OH11 | 已迁入 v10 的跨进程继续读取通过，未生成新迁移归档 |
| OH12 | 无分页及含分页两类旧档归档在独立旧根读回成功 |
| OH13 | 真实第 128 次提交保留前 127 项，Mono DTO 拒绝缺失字段和非法 UTC。其他非法存档形状待验 |
| OH14 | CAPACITY-A02 第 129 次真实提交仅裁最早记录，重复确认检查主档 SHA 和材料。未满档替换失败已通过，满档故障与回拨测试待验 |
| OH15 | 三元键和结算复用有 Mono 合同与同局实测。跨局同 ID 已实测，ABANDON-A01 拒绝实际出征中的换卡请求。伪造候选的 wire 校验矩阵待验 |
| OH16 | 确定性排序经静态核对，真实 Player 冷读遍历七页。双 UTC 并列、回拨场景待验 |
| OH17 | 历史标题和兼容映射已验证，双目录改名及退役全流程 NOT_RUN |
| OH18 | 重复提交与确认前后收益无重复的代表用例通过，领取及地区 DATA_GAP 综合场景待验 |
| OH19 | 双 UTC 在 Pending、失败恢复、提交和重启中复用，代表用例通过 |
| OH20 | REPLAY-A01 从真实 129 次结算后的档案读出裁剪的 Run。最近结算已替换，产品 Plan 拒绝重放，Profile 和主档 SHA 不变。旧父和旧备世代故障变体待验 |


## R1 缺口复验

| 范围 | 当前判定 | 依据 |
|---|---|---|
| P0 存档与并发 | PASS | 八类迁移故障和恢复、两个结算故障、同根并发以及 v9 对 v10 的拒绝。真实输入记录和独立复算均保留。 |
| P1 历史语义 | PASS | 同时间排序、冻结时间恢复、快照改名、剪裁后的真实实档重放拒绝、同局换卡与跨局重复目标。 |
| P2 uGUI | PASS | 混合地区、类型、时间、七页、旧名、空与未知历史。 |
| P2 IMGUI | NOT_RUN（有效交互） | 多种探针尝试保留原始 FAIL。新物理输入探针无法安全确认窗口焦点，未达到实际控件。 |
| P3 保护与回归 | PASS | 攻击、防御、掉落、材料、配方按受控同输入比较。UX-03 七武器 14 项及 B1/B2 代表路径。 |
| 最终构建 | PASS | Acceptance-A06、NoDefine-A03、Release-A03。NoDefine 和 Release 的原 EXE 隔离启动成功，最终产品 DLL 无 UX_ACCEPTANCE 字样或测试探针。 |

[逐项 R1 证据及缺口](R1_COMPLETION_REPORT.md)

## R2最终复核

| 验收项 | 当前判定 | 证据等级与入口 |
|---|---|---|
| IMGUI打开/全部/地区/类型/时间/七页/末条/上一页/旧名/关闭 | PASS | [P][C] MIXED-A06，20次历程操作、退出0；逐操作actions/outcomes、实际滚动位置及截图 |
| IMGUI关闭无穿透、恢复营地输入 | PASS | [P] 关闭后preparing=false、Camp；实际关闭背包后inventoryOpen=false、inputBlocked=false |
| 空历史 | PASS | [P] EMPTY-A03 双UI实际打开关闭、退出0；早期EMPTY-A01缺回执、EMPTY-A02工具拒绝原样保留 |
| 旧版未知历史 | PASS | [P] UNKNOWN-A03 双UI实际打开关闭、退出0；未知未显示为未完成；早期缺回执Run不改写 |
| 双UI同存档一致性 | PASS | [C] 17对查询状态，全部六字段、排序和分页边界一致；交互期间主档及Profile不变；退出另有既存保存，未改变历史/结算/收益 |
| 原生前台诊断 | PASS（最终三条Run） | [P] 55次验证、55次投递，全部48次历程操作有真实输入与消费状态证据；早期未投递/误关联意图不计入 |
| 产品差异范围 | PASS | [C] 1504份接手源码/配置仅AdventureFlow.UI.cs变化；未改Schema、历史、迁移、结算 |
| 最终三种构建 | PASS（构建/静态门禁） | [B][S] Acceptance/NoDefine/Release A02退出0；发行回执匹配；NoDefine/Release查验收标记0、无sidecar |
| 历史证据保护 | PASS | [C] 原147行分类不变、4142个旧文件哈希和大小匹配；总159行保留全部非PASS类别 |
| 本轮完成定义 | PASS | 三条最终Run交互、截图、退出回执和独立复算完整；受测范围限定1280×720、DPI96；人工体验不冒充通过 |

[R2详细报告](UX05-IMGUI-R2/REPORT.md) · [独立复算](UX05-IMGUI-R2/EVIDENCE/independent-review.json) · [最终汇总](FINAL_ACCEPTANCE_REPORT.md)
