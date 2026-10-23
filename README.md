# 万象归途 / WanxiangGuitu

[UI-01 玩家 HUD 与交互一致性报告](ProjectDocs/WanxiangGuitu/DeliveryUI01/REPORT.md) · [运行前后截图](ProjectDocs/WanxiangGuitu/DeliveryUI01/COMPARISON.md) · [本地复跑](ProjectDocs/WanxiangGuitu/DeliveryUI01/TESTING.md)。E 最近交互、H 出口专用，费用与执行共用同一目标；F1帮助/M路线，详情内F2调整新HUD大小。U16正式包完整原生操作/正常退出继续尚未完成，详见报告限制。

Unity 3D 单人 PvE 搜打撤与局内肉鸽构筑原型。仓库仍为 mizunagare/BallMaze；WanxiangGuitu 是技术标识，尚无另定英文发行名。

使用 Unity **6000.6.5f1**（URP 17.6.0、Input System 1.20.0、uGUI 2.6.0），不要自动升级依赖。本机工程现位于 `D:\unity\WanxiangGuitu`，在 Unity Hub 中添加该目录；旧 Hub 路径不会自动更新。

打开 `Assets/CombatPrototype/ForestRuins.unity` 并 Play，从营地选择森林探索或保留的波次测试。ForestRuins 是测试场景。已有在途档会继续原局；先正常撤离或确认放弃，再选新模式。WASD 移动、Shift 跑、左键普攻、F 技能、V 切武器、空格翻滚、E 交互拾取、H 在出口引导撤离、Q 药水、Tab/B 背包、C 角色、R 确认放弃。撤离不要求清场。

菜单 **万象归途 → 构建 → Windows 正式版** 生成 `Builds/WanxiangGuitu/WanxiangGuitu.exe`，非开发构建。F9 在所有独立构建中禁用；仅编辑器当次试玩可从开发工具菜单显式启用。F5/自动存档与下次启动继续原局保留。

Company Name 保持 `DefaultCompany`，存档格式保持 v9，兼容已有 v1～v8 链。旧 Windows 路径 `%USERPROFILE%/AppData/LocalLow/DefaultCompany/BallMaze/ForestRuins`，新版为同级 `万象归途/ForestRuins`。启动会校验并迁移整个集合（含备份、ground-loot 和迁移档案），旧目录保留；冲突不自动覆盖或拼接。详见 [迁移说明](ProjectDocs/WanxiangGuitu/DeliveryA/SAVE_LOCATION_MIGRATION.md)。

[交付 B1 可修复渡口](ProjectDocs/WanxiangGuitu/DeliveryB1/REPORT.md) · [B1 隔离复跑](ProjectDocs/WanxiangGuitu/DeliveryB1/TESTING.md) · [交付 A1 定向补丁](ProjectDocs/WanxiangGuitu/DeliveryA1/REPORT.md) · [交付 A 验证报告](ProjectDocs/WanxiangGuitu/DeliveryA/REPORT.md) · [开发路线](ProjectDocs/东方元素肉鸽/DEVELOPMENT_ROADMAP.md)

新出征的森林在伐木林地西侧有可修复渡口，随身木材2、石头1，优先花本局采集材料。靠近按 H 修复，成功保存后再按 H 引导撤离；E 按最近的物品、事件或出口互动。受击、离开和取消会打断引导，已修复状态本局保留，不重扣材料。入口和归途祭坛仍免费，旧在途布局保持原样，新出征才生成渡口。

旧滚球／迷宫示例已退出当前工程；当前游戏的森林、波次、装备、仓库、存档回归工具及素材许可证继续保留。历史文档、内部 ForestRuins ID 与 CombatPrototype 目录暂不改名。
