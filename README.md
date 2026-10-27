> INPUT-01：标题“设置→操作/键位”或游戏内“帮助→操作/键位”可修改键鼠；草稿、取消、冲突、恢复默认和应用已接真实输入。固定执行输入f16bdcae的[报告](ProjectDocs/WanxiangGuitu/DeliveryInput01/REPORT.md)/[验收](ProjectDocs/WanxiangGuitu/DeliveryInput01/ACCEPTANCE.md)/[复跑](ProjectDocs/WanxiangGuitu/DeliveryInput01/TESTING.md)/[证据](ProjectDocs/WanxiangGuitu/DeliveryInput01/Evidence/INDEX.md)。自动化适用项通过；构建质量有URP包错误待定位，原生/人工/完整性能及历史引擎项仍开放，等待独立复审。

# 万象归途 / WanxiangGuitu

> 当前：S2-R2纯离线校验补丁待固定SHA复审，见[报告](ProjectDocs/WanxiangGuitu/DeliveryStage2R2/REPORT.md)、[验收](ProjectDocs/WanxiangGuitu/DeliveryStage2R2/ACCEPTANCE.md)、[证据](ProjectDocs/WanxiangGuitu/DeliveryStage2R2/Evidence/INDEX.md)。S2-R1部分通过，产品/战斗/恢复成果保留；本轮原35＋新增58分别通过，仅只读重审既有数据，没有新Unity/构建/战斗。原包12条件及候选对照已补齐；原生/人工/性能及历史根因保持开放，交付后暂停。

[B09 正式入口、自动存档与角色呈现](ProjectDocs/WanxiangGuitu/DeliveryB09/REPORT.md) · [验收](ProjectDocs/WanxiangGuitu/DeliveryB09/ACCEPTANCE.md) · [存档规则](ProjectDocs/WanxiangGuitu/DeliveryB09/SAVE_COMPATIBILITY.md)。正式 Player 从标题进入，提供继续、新游戏确认、读取当前自动档、设置和退出。当前只有一个自动档集合；新游戏确认后全部重置，完整旧集合归档，不与新档混合。复用现有骨骼 Legacy 剪辑，翻滚为程序化动作；没有新增动画资产依赖。此段为 B09 历史交付摘要，当前批次以文首状态为准。原生 UI、人工试玩及既有 UNKNOWN/青色帧根因仍各自开放。

[B08 新手引导与营地体验](ProjectDocs/WanxiangGuitu/DeliveryB08/REPORT.md) · [验收](ProjectDocs/WanxiangGuitu/DeliveryB08/ACCEPTANCE.md) · [复跑](ProjectDocs/WanxiangGuitu/DeliveryB08/TESTING.md)。新Profile自动开启基础教学，旧档不强制重播。营地关闭面板进入走动，靠近四个设施按E；右上只突出一个当前目标，教学详情可跳过或重看。真实采集并拾取木/石/矿，走免费出口撤离，确认结算后回营取材制造，再次出征完成教学。完整仓库、工作台和制造目标仍保留。原生UI与独立人工可理解性验收仍开放；此段保留 B08 历史交付范围。

[B07-R1 森林战斗可读性](ProjectDocs/WanxiangGuitu/DeliveryB07-R1/REPORT.md) · [本轮验收与限制](ProjectDocs/WanxiangGuitu/DeliveryB07-R1/ACCEPTANCE.md) · [证据索引](ProjectDocs/WanxiangGuitu/DeliveryB07-R1/Evidence/INDEX.md)。森林首领使用屏幕空间生命与短预警；圆、冲锋、散射和潮印按实际攻击定义显示。挡住主角的怪物身体与枝冠会半透明，镜头离开后恢复；仅改变显示，不改变战斗碰撞。完成本轮后暂停等待复审，不自动开始新批次。

[B07 森林双 Boss 与永久徽章](ProjectDocs/WanxiangGuitu/DeliveryB07/REPORT.md) · [验收与限制](ProjectDocs/WanxiangGuitu/DeliveryB07/ACCEPTANCE.md) · [复跑入口](ProjectDocs/WanxiangGuitu/DeliveryB07/TESTING.md)。新森林出征可挑战精英哨站东侧的古林角卫与湖泊北岸的湖心潮灵，均可绕过；徽章永久，战利品需拾取并按原撤离/死亡规则处理。旧在途不补怪，先回营再新出征。B07 交付后暂停等待复审，不自动开放后续地图。


[UI-01 玩家 HUD 与交互一致性报告](ProjectDocs/WanxiangGuitu/DeliveryUI01/REPORT.md) · [运行前后截图](ProjectDocs/WanxiangGuitu/DeliveryUI01/COMPARISON.md) · [本地复跑](ProjectDocs/WanxiangGuitu/DeliveryUI01/TESTING.md)。E 最近交互、H 出口专用，费用与执行共用同一目标；F1帮助/M路线，详情内F2调整新HUD大小。U16正式包完整原生操作/正常退出继续尚未完成，详见报告限制。

Unity 3D 单人 PvE 搜打撤与局内肉鸽构筑原型。仓库仍为 mizunagare/BallMaze；WanxiangGuitu 是技术标识，尚无另定英文发行名。

使用 Unity **6000.6.5f1**（URP 17.6.0、Input System 1.20.0、uGUI 2.6.0），不要自动升级依赖。本机工程现位于 `D:\unity\WanxiangGuitu`，在 Unity Hub 中添加该目录；旧 Hub 路径不会自动更新。

普通 Editor Play 会先进入 Boot/标题菜单，再由玩家选择进入游戏；即使当前打开 ForestRuins，也不会直接绕过标题。进入营地后可选择森林探索或保留的波次测试。只有带启动前隔离参数的明确 Editor 自动化入口可使用测试路径。正式 Windows 包默认进入标题，不自动创建新档。ForestRuins 是测试场景。已有在途档会继续原局；先正常撤离或确认放弃，再选新模式。WASD 移动、Shift 跑、左键普攻、F 技能、V 切武器、空格翻滚、E 交互拾取、H 在出口引导撤离、Q 药水、Tab/B 背包、C 角色、R 确认放弃。撤离不要求清场。

菜单 **万象归途 → 构建 → Windows 正式版** 生成 `Builds/WanxiangGuitu/WanxiangGuitu.exe`，非开发构建。F9 在所有独立构建中禁用；仅编辑器当次试玩可从开发工具菜单显式启用。F5/自动存档与下次启动继续原局保留。

Company Name 保持 `DefaultCompany`，存档格式保持 v9，兼容已有 v1～v8 链。旧 Windows 路径 `%USERPROFILE%/AppData/LocalLow/DefaultCompany/BallMaze/ForestRuins`，新版为同级 `万象归途/ForestRuins`。标题的目录摘要只读检查；中断的新游戏事务先按日志安全恢复。确认继续时由原迁移器校验并迁移整个集合（含备份、ground-loot 和迁移档案），旧目录保留；冲突不自动覆盖或拼接。详见 [迁移说明](ProjectDocs/WanxiangGuitu/DeliveryA/SAVE_LOCATION_MIGRATION.md)。

[交付 B1 可修复渡口](ProjectDocs/WanxiangGuitu/DeliveryB1/REPORT.md) · [B1 隔离复跑](ProjectDocs/WanxiangGuitu/DeliveryB1/TESTING.md) · [交付 A1 定向补丁](ProjectDocs/WanxiangGuitu/DeliveryA1/REPORT.md) · [交付 A 验证报告](ProjectDocs/WanxiangGuitu/DeliveryA/REPORT.md) · [开发路线](ProjectDocs/东方元素肉鸽/DEVELOPMENT_ROADMAP.md)

新出征的森林在伐木林地西侧有可修复渡口，随身木材2、石头1，优先花本局采集材料。靠近按 H 修复，成功保存后再按 H 引导撤离；E 按最近的物品、事件或出口互动。受击、离开和取消会打断引导，已修复状态本局保留，不重扣材料。入口和归途祭坛仍免费，旧在途布局保持原样，新出征才生成渡口。

旧滚球／迷宫示例已退出当前工程；当前游戏的森林、波次、装备、仓库、存档回归工具及素材许可证继续保留。历史文档、内部 ForestRuins ID 与 CombatPrototype 目录暂不改名。

## B10-R1 黑猫猫族首版

当前源码接入原创黑猫主角、猫族设施代理/敌人/双Boss、立体材质和统一uGUI背包管理。普通Play与Windows正式版经Boot→标题菜单→玩家选择进入游戏，不自动创建新Run。真实单自动档、继续/读取、新游戏二次确认沿用原存档事务。

Unity仍为6000.6.5f1。已有猫族资源已经烘焙，不需先运行美术生成菜单。开发构建入口为“万象归途/构建/Windows 正式版”；自动化继续使用DeliveryUI01/Automation的启动前隔离入口。不要把编辑器受控截图或回调测试当作原生操作/人工试玩。

本轮为简化的原创刚性分件+既有骨骼动作，翻滚程序化；NPC静态复用真实设施，物资猫没有独立商店。部分环境细节/专用特效仍概念状态，新增草药等只是资源，不是已实现的新经济。主视觉与具体未完成项见[交付报告](ProjectDocs/WanxiangGuitu/DeliveryB10/REPORT.md)、[验收表](ProjectDocs/WanxiangGuitu/DeliveryB10/ACCEPTANCE.md)和[证据](ProjectDocs/WanxiangGuitu/DeliveryB10/Evidence/INDEX.md)。UI01原生/人工验收和既有根因调查保持开放。
