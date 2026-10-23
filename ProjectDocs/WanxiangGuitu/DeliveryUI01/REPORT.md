# UI-01：交互一致性与玩家 HUD

仓库 `mizunagare/BallMaze`，分支 `main`。开始基线：`3574d7b62a2b06b396681b39f50be7ecf76a5fc4`；开始时本地与远端一致、工作区干净。未 reset、改写历史或覆盖用户改动。最终报告与证据所在提交以本文件的 GitHub 固定提交 URL 为准。

产品代码验证提交：`9d4a79a81b1bfd435440b1a955fc84433332d463`（此前 `b01658b`、`78d6ee5`）。随后只提交测试、证据与说明。Unity 6000.6.5f1 / URP 17.6.0 / Input System 1.20.0 / uGUI 2.6.0 保持不变，无 CI。**本批尚有 U16 的无驱动正式版正常退出/继续与原生操作验证未完成，不能宣布全部验收通过。**

## 改动与入口

打开 `Assets/CombatPrototype/ForestRuins.unity`，Play 后继续原档或从营地出征；森林仍是测试模式。运行时自动创建一个 uGUI PlayerHUD，无需重建场景。

- **B1-UI-R01 已修复**：InteractionResolver 产生唯一交互 offer，包含目标 ID、动作、图标、费用、持有量、原因和可执行状态。HUD 展示并钉住此 offer；真实 E/H 执行已展示对象，重新验证同一目标/Run/距离/动作/费用，过期拒绝并刷新，不悄悄改成付费动作。E 最近交互、H 出口专用；相同合并，不同主次分列；引导中仍显示可拾取 E 与 H 取消。键盘同帧只执行一次。旧程序接口保留给现有领域调用。
- 生命/等级/经验紧凑显示；主副武器、技能、翻滚、药水、补给统一图标、键帽、数字与真实冷却遮罩。缺图标短名回退。Esc 释放鼠标后可点已有操作按钮。
- F1 帮助、M 路线；详情中 F2 切换 100/125/150%。详情暂停游戏并管理焦点；默认关闭的 F3 诊断仅编辑器/开发构建可用，正式版拒绝。未新增耐力、法力、任务或小地图。
- 一处上下文提示读取真实撤离进度/取消原因。无目标不留空面板；拾取合并，存档失败与结果待核对独立优先显示，普通消息不能覆盖。
- 结算先看收获/损失，入场装备与来源详情折叠；Pending/Committed 分别显示待确认/已保存，原确认按钮、满仓待领取和唯一提交路径保持。

停用对应旧绘制：CombatHud 玩家常驻条、AdventureCombat 武器说明、PlayerInventory 探索提示/通知、AdventureFlow.UI 在途长文、ExtractionPoint/WorldEventPoint 标签、ForestRegionRuntime 常驻路线。完整背包、营地、工作台、技能选择、Boss 提示、伤害数字与资源血条保留。不叠加新旧玩家 HUD。

B1 扣费、来源账、出口修复回执、分页、唯一结算与死亡保护没有重设计。存档仍为 v9，无新迁移/清档；展示错误标志不写入存档。旧免费出口和旧在途布局语义保持。新增掉落交互 ID 仅用于当前对象寿命，不替换存档实体 ID。

## 实际验证

| 范围 | 结果 | 本次证据与边界 |
| --- | --- | --- |
| 干净隔离重新导入/30 项回归 | PASS | [完整汇总](Evidence/CleanVerified/results.json)，30/30，失败0、超时0；含装备/容器/双武器/冷却/工作台、v1～v9/分页/结算、A1、B1、UI规则与构建 |
| 非开发 Windows 构建 | PASS | [构建摘要](Evidence/BuildSummary.txt)：0 errors / 52 warnings，BuildOptions.None；Editor 测试不进入玩家包 |
| 本次正常 AI 完整路线及新进程恢复 | PASS | [运行结果](Evidence/NormalLatest/normal-results.txt)、[轨迹](Evidence/NormalLatest/normal-ai.csv)、[恢复](Evidence/NormalLatest/process-result-Resume.json)；保留实际攻击/采集，不冻结敌人，不在出征后传送 |
| 启动前隔离负例 | PASS | 缺失/相对/LocalLow 参数均预期 exit1、无存储审计、合成哨兵未变，见三个 LatestReject 目录 |
| 受控截图与布局 | PASS | [92 帧记录](Evidence/ScreensFinal/visual-layout.jsonl)、exit0；NPC 关闭、故障合成，不冒充正常 AI |
| 正式构建实际启动与 HUD 可见 | PASS | [真实窗口](Evidence/ReleaseUI/01-hud.png)，合成隔离档，无运行验证驱动 |
| 正式构建原生 HUD 操作、正常退出及新进程继续（U16） | NOT_RUN | F1 被本机 Snipaste 全局截获，截图确认层阻挡后续操作；Esc/Return/Alt+F4 未取得正常退出证据。最后仅终止本次游戏进程清理，非正常退出 PASS，见 [原生记录](Evidence/ReleaseUI/native-result.txt) |
| 人工试玩/首次可理解性 | NOT_RUN | 自动化观察不冒充人工试玩 |

正常 AI 实际种子418 / Generation4 / B06-B1。木材实际拾取后6，修复扣2剩4；石头拾取后7（含入场1），修复扣1，结算/本局来源区分；取木2制造后永久仓库材料数组为 `0,0,0,2,5,0`（MonsterHide / CrystalShard / BossCore / Wood / Stone / Ore），即木材2、石头5。**以 expected-normal.txt 与原始日志为准，不能套用 A1/B1 旧轮数量。** 本次仍有9只敌人时完成撤离；实现未要求清场。

## U01～U16 对照

| 项 | 状态 | 证据/限制 |
| --- | --- | --- |
| U01 空地 | PASS | empty 图；无空板/检查点/坐标/整段键位 |
| U02 显示与执行 | PASS | UI01Rules 真实虚拟键盘 E；旧目标过期拒绝，原 B1/事件回归 |
| U03 更近付费渡口 | PASS | 可见费用/目标，真实 E+H 同帧只扣一次 |
| U04 E/H 不同 | PASS | dual 图、真实 E 拾取与 H 引导；引导中 E 仍可拾取 |
| U05 材料/状态 | PASS | missing/ready/paid/uncertain 图与领域断言 |
| U06 保存故障/幂等 | PASS | 发布前回滚、发布后回调故障读回确认、B1 Run/Resume；错误未被拾取盖住 |
| U07 引导/中断/暂停 | PASS | 实际 Damage 取消、help 暂停、原 B1 距离/H取消/恢复；channel/hit 图 |
| U08 四武器/冷却 | PASS | 四类图标逐一验证、切换冷却保持、翻滚共用移动方向；双输入门控 |
| U09 覆盖/焦点 | PASS（受控） | 背包/详情/技能选择/保存阻断/结算状态，单实例恢复；原生鼠标全流程未完成 |
| U10 结算 | PASS | settlement/source-details/death/abandon/overflow/committed 图，B05/B1唯一结算回归 |
| U11 通知 | PASS | 拾取合并、普通消息分桶、错误持久优先；新出征清旧通知 |
| U12 分辨率 | PASS（受控） | 720p/1080p 各21状态；1440p/3440×1440 与缩放组合；真实渲染大小/可见组/边界检查 |
| U13 缩放/长名 | PASS（新HUD） | 100/125/150%，低分辨率大比例改左右提示布局；未重写旧管理页缩放 |
| U14 帮助/诊断 | PASS（受控）；原生部分NOT_RUN | 正式配置诊断拒绝、帮助/路线/鼠标焦点规则；本机F1外部冲突已记录 |
| U15 恢复/反复出征 | PASS | 正常AI跨进程、B1恢复、UI单实例，启动审计链 |
| U16 无驱动正式包完整操作 | NOT_RUN | 仅启动/HUD可见通过，余项见上；不继承旧批PASS |

## 截图与可追溯性

[同场景前后对比](COMPARISON.md) 使用审阅基线3574运行画面与最终9d4运行画面，种子418、渡口旁同视角；720p/1080p均提供。截图来自游戏实际渲染，非效果图。[图标清单与许可](ICONS.md)，新增13张自制PNG，复用已有素材及许可证。

[证据索引](Evidence/INDEX.md) 区分受控/正常AI/原生窗口。日志压缩保留原字节；不提交玩家存档、合成完整存档、Library、Temp、凭据或构建二进制。运行代码/资源与构建项目逐项一致见 [对应表](Evidence/runtime-source-correspondence.json)，全部相同；[旧版对应](Evidence/baseline-source-proof.json)、[构建哈希](Evidence/build-hashes.json)。目录定位审计是应用证据，不是内核级文件访问证明；以前是否触及真实玩家目录仍未核实。

## 失败尝试和限制

保留而不抹去失败：首次拾取合并规则失败（修正普通消息分桶）；Full 准备脚本重复junction导致未启动；Full2 的两条旧B1脚本同帧关包后E被关闭帧保护拒绝（只让测试等待真实下一帧，保留业务断言）；Verified 首次干净导入300秒超时（原因未确证，最终 fresh copy 600秒限时全30通过）；Screens 有空白HUD与同帧修复失败（加帧推进、可见组、实际分辨率和异步截图落盘检查，最终92全部重跑）。对应失败结果及原始日志在 Evidence，不能据后续通过删除失败历史。

52条构建警告主要是现有API过时提示；原始日志另有 Unity Editor Search 内部异常/退出分配器提示，不隐瞒，不在本轮升级引擎。呈现器受控120帧均值94.49μs，关闭Canvas但继续更新104.86μs；采样很短，**不能推断整体帧率改善**，GPU/长期性能NOT_RUN。原生截图可见既有角色武器显示异常，未在UI-01更换模型/战斗美术。

本轮仅UI-01；B2地点收益/目标、B3随机流、B4三路线仍只维护计划，B07未开始。尚需在不被全局快捷键截获的环境完成 U16 原生点击、正常退出与继续，并进行人工可读性试玩。推送不等于下一次复审通过或发布验收完成。
