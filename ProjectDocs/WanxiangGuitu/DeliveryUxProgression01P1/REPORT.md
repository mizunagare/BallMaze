# UX-PROGRESSION-01 P1 · 交付报告

分支 `feature/ux-progression-01-p1`（基线 `design/ux-progression-01` @ `59190b7036307e69420d43e23e5610f2ddbab9fc`）。
范围：P1-01 ~ P1-05，纯只读信息层。**未进入 P2。**

## 1. 一句话结论

三地区的出征目标、进度、路线 Top3、结算"下一局三件事"与武器/技能信息层已全部落地，
在真实 `WanxiangGuitu.exe` 上 13 条 Run 全部完成（1465 PASS / 0 FAIL / 9 SKIP），
经济、掉落、随机流、护甲、经验、武器伤害、技能冷却与存档 schema 的 diff 均为 0。

## 2. 开工前的两项阻塞已闭合

| 阻塞 | 处理 | 落点 |
|---|---|---|
| **D-08**：`earnedRemaining[]` 被当成"累计所得"，且无 gross 信号 | 冻结四量 `GrossEarned / EarnedRemaining / CarriedIn / Spent`；进度用本局新获得并排除带入；消费后不回退；零 schema 投影取 `max(EarnedRemaining, 运行时单调计数)`，两项都 ≤ 真值 ⇒ 假阳性结构上不可能，代价是重进"发生过消费的局"低报且 `exact=false` | `DESIGN.md §3.1.1`、`ObjectiveEvaluator.cs`、`ACCEPTANCE.md` B0-04 / B0-12 / N-01 / N-02 |
| **九卡可达性**：遗迹没有矿脉，`ruins.gather` 原定 8 单位不可达 | 逐卡核实后修正两处真实错误：遗迹 Gather 8 → **6**（2 箱 ≥4 + 2 普通敌各 1）；森林寻宝删掉"或 1 件本局装备"的模糊双指标 | `DESIGN.md §3.2`、`OBJECTIVE_CARD_MATRIX.csv` 的 `revised_in_p1` |

反例都以真实 Player 断言落地，不是推理：
`p1-carried-is-zero: hud=0,carried=30,earned=0`、
`p1-spend-no-regress: spent=True,before=18,after=18,spentRecorded=5,earnedNow=13`、
跨进程对 `xproc-not-exact-after-spend` / `xproc-hud-value-not-above-persisted` 各 3 次 PASS。

## 3. 交付物

| 文件 | 内容 |
|---|---|
| `P1_IMPLEMENTATION_REPORT.md` | 实施记录：设计口径修订、D-08 推导、九卡可达性、实现清单、Run 表、限制与 SKIP、禁止项自查 |
| `ACCEPTANCE.md` | 34 条验收（B0 14 / B1 5 / 负例 10 / C 类 5）：29 PASS、5 NOT_RUN（按设计冻结） |
| `OBJECTIVE_CARD_MATRIX.csv` | 9 张卡 × 14 列：条件、阈值、`source_evidence`（file:line）、最低产量证明、可达性、本批修订、对应 Run |
| `PLAYER_RUN_MATRIX.csv` | 13 条 Run 的机器可读汇总（判定 / PID / 三层 SHA / PASS-FAIL-SKIP / 失败与 SKIP 明细） |
| `TESTING.md` | 复跑说明：构建、驱动注入、批量运行、汇总、保护比对 |
| `Evidence/INDEX.md` | 证据索引：目录结构、每条 Run 的覆盖点、历史失败批次、复现路径 |
| `Evidence/PROTECTION_HASHES.tsv` | 22 个受保护文件：基线 blob vs 本批 blob，全部 `YES` |
| `Evidence/Player/p1-*` | 13 条主 Run × 15 个原始文件（命令行、日志、逐条断言、事件流、逐帧样本、PID、三层 SHA） |
| `Evidence/Driver/*` | 驱动编译命令行、编译器 SHA、编译日志（0 error） |

## 4. 本批实际改动

- 新增 5 个产品文件：`ObjectiveCatalog.cs`、`ObjectiveEvaluator.cs`、`AdventureFlow.Objectives.cs`、`RouteCards.cs`、`SkillTradeoffs.cs`（+ 5 个 `.meta`）。
- 修改 7 个产品文件：`AdventureFlow.cs`（只加记账钩子与结算前抓快照）、`AdventureFlow.UI.cs`、`PlayerHudPresenter.cs`、`WeaponSkillPanel.cs`、`AdventureLoadout.cs`、`WeaponLoadoutView.cs`、`CatInventoryPresenter.cs`。
- 修订 3 份设计文档：`DeliveryUxProgression01/{DESIGN.md, DECISIONS.md, ACCEPTANCE_CRITERIA.md}`。
- 零 `ProjectSettings` / `Packages` / 用户场景改动（Unity 构建期自动改写已还原，见 `PROTECTION_HASHES.tsv` 的 `ProjectSettings.asset` / `manifest.json` / `packages-lock.json` = `YES`）。

## 5. 由真实证据暴露并修正的 1 处缺陷

第一轮 13 条 Run 全绿后，逐条读结算文本发现：条件已满足但死亡时，`未竟：扫箱 已达成 · 待撤离`
下面却写着 `下一步：森林 · 拔点（换一种目标）` —— 与角标"条件已满足但未成功撤离"和本批口径矛盾。
修正 `AdventureFlow.Objectives.Suggest`（3 行），重编并**全部 13 条 Run 重跑**，现输出
`下一步：再来一次 森林 · 扫箱（条件已满足，只差成功撤离）`。详见 `P1_IMPLEMENTATION_REPORT.md §4.1`。

这条不是"顺手美化"：它是本批语义（达成 = 条件满足 **且** 成功撤离）在 UI 上的自我矛盾，
不修就等于交付一个自己打自己的提示。

## 6. 诚实的边界

- **观察脚手架**：驱动在采集/撤离期间补满英雄血量、并用瞬移走到"离敌人最远的出口"。
  不搬动敌人、不改 AI/掉落/边界/经济。早期"把敌人推远"的脚手架因造成越界已被彻底移除，失败记录保留。
- **9 次 SKIP**：全部是 `p1-ruins-no-vein-notice` 在森林/洞窟的语义性跳过。
- **三张挑战卡**只验证了显示/进度/路线，"击败"未在一次 Run 预算内完成，达成语义由其它两条路径交叉覆盖。
- **未做**：像素级外观、人工游玩、性能、原生输入 U16；以及按设计冻结的 C-01 ~ C-05。
- **EXE SHA 不标识构建**：Unity 启动器壳固定不变，构建身份看 `Assembly-CSharp.dll`。

## 7. 下一步

按任务书要求**暂停，等待复审**。不自动进入 P2（目标奖励发放、永久回执、技能槽持久化）。
