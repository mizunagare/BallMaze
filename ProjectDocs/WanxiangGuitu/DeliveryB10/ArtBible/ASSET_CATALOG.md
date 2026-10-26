# 黑猫猫族首版资产台账（技术验收与未完成项）

原始9张及历次方向保留；最新用户黑猫猫族世界PNG为主视觉，STYLE_GUIDE v0.7为生产规范。概念不是实机，不将概念视觉复杂度等同实际资源完成度。完整文件大小/SHA256见ASSET_INVENTORY.json。

|Asset ID|名称|状态|实际入口/限制|
|---|---|---|---|
|WX-UI-001|标题 Logo|VERIFIED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatUI.cs, Assets/CombatPrototype/CatTitleStage.cs；技术导入/引用/真实非开发运行显示；不代表概念相似度、原生点击或人工认可; 文字标题与原创猫头像，非独立手绘Logo字形|
|WX-UI-002|主菜单背景面板|VERIFIED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatUI.cs, Assets/CombatPrototype/CatTitleStage.cs；技术导入/引用/真实非开发运行显示；不代表概念相似度、原生点击或人工认可|
|WX-UI-003|继续游戏按钮|VERIFIED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatUI.cs, Assets/CombatPrototype/CatTitleStage.cs；技术导入/引用/真实非开发运行显示；不代表概念相似度、原生点击或人工认可|
|WX-UI-004|新游戏按钮|VERIFIED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatUI.cs, Assets/CombatPrototype/CatTitleStage.cs；技术导入/引用/真实非开发运行显示；不代表概念相似度、原生点击或人工认可|
|WX-UI-005|读取存档按钮|VERIFIED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatUI.cs, Assets/CombatPrototype/CatTitleStage.cs；技术导入/引用/真实非开发运行显示；不代表概念相似度、原生点击或人工认可|
|WX-UI-006|设置按钮|VERIFIED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatUI.cs, Assets/CombatPrototype/CatTitleStage.cs；技术导入/引用/真实非开发运行显示；不代表概念相似度、原生点击或人工认可|
|WX-UI-007|退出按钮|VERIFIED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatUI.cs, Assets/CombatPrototype/CatTitleStage.cs；技术导入/引用/真实非开发运行显示；不代表概念相似度、原生点击或人工认可|
|WX-UI-008|存档状态展示卡片|VERIFIED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatUI.cs, Assets/CombatPrototype/CatTitleStage.cs；技术导入/引用/真实非开发运行显示；不代表概念相似度、原生点击或人工认可|
|WX-UI-009|新游戏确认对话框|VERIFIED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatUI.cs, Assets/CombatPrototype/CatTitleStage.cs；技术导入/引用/真实非开发运行显示；不代表概念相似度、原生点击或人工认可|
|WX-UI-010|标题界面过渡遮罩 / 淡入淡出|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatUI.cs, Assets/CombatPrototype/CatTitleStage.cs；既有加载硬遮罩与提示，非淡入淡出动画|
|WX-UI-101|玩家生命条|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-102|当前武器面板|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-103|当前技能图标面板|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-104|药水数量图标|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-105|当前目标面板|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-106|交互提示面板|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-107|撤离状态面板|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-108|Boss 血条|INTEGRATED|Assets/CombatPrototype/ForestBossHud.cs, Assets/CombatPrototype/ForestBossTelegraph.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-109|Boss 攻击预警提示|INTEGRATED|Assets/CombatPrototype/ForestBossHud.cs, Assets/CombatPrototype/ForestBossTelegraph.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-110|顶部状态通知条|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-201|背包主面板|VERIFIED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；技术导入/引用/真实非开发运行显示；不代表概念相似度、原生点击或人工认可|
|WX-UI-202|分类标签栏|VERIFIED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；技术导入/引用/真实非开发运行显示；不代表概念相似度、原生点击或人工认可|
|WX-UI-203|物品格子|VERIFIED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；技术导入/引用/真实非开发运行显示；不代表概念相似度、原生点击或人工认可|
|WX-UI-204|装备栏|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-205|详情栏|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-206|稀有度边框|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-207|仓库面板|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-208|工作台面板|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-209|配方卡片|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-210|材料缺口提示条|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-UI-211|教程帮助面板|INTEGRATED|Assets/CombatPrototype/TitleMenu.cs, Assets/CombatPrototype/CatInventoryPresenter.cs, Assets/CombatPrototype/PlayerHudPresenter.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-CHR-001|黑猫主角基础模型|VERIFIED|Assets/CombatPrototype/Resources/CatWorld/Actors/Hero.prefab, Assets/CombatPrototype/CatActorVisual.cs, Assets/CombatPrototype/CatCampVisual.cs；技术导入/引用/真实非开发运行显示；不代表概念相似度、原生点击或人工认可|
|WX-CHR-002|黑猫主角基础材质|VERIFIED|Assets/CombatPrototype/Resources/CatWorld/Materials/Fur.mat, Assets/CombatPrototype/Resources/CatWorld/Materials/Cream.mat, Assets/CombatPrototype/Resources/CatWorld/Materials/Cloth.mat, Assets/CombatPrototype/Resources/CatWorld/Materials/Canvas.mat, Assets/CombatPrototype/Resources/CatWorld/Materials/Leather.mat, Assets/CombatPrototype/Resources/CatWorld/Materials/Steel.mat, Assets/CombatPrototype/Resources/CatWorld/Materials/Red.mat；技术导入/引用/真实非开发运行显示；不代表概念相似度、原生点击或人工认可|
|WX-CHR-003|黑猫主角待机动作|INTEGRATED|Assets/CombatPrototype/FantasyActorVisual.cs, Assets/CombatPrototype/CatActorVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-CHR-004|黑猫主角行走动作|INTEGRATED|Assets/CombatPrototype/FantasyActorVisual.cs, Assets/CombatPrototype/CatActorVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-CHR-005|黑猫主角跑步动作|INTEGRATED|Assets/CombatPrototype/FantasyActorVisual.cs, Assets/CombatPrototype/CatActorVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-CHR-006|黑猫主角攻击动作（长剑）|INTEGRATED|Assets/CombatPrototype/FantasyActorVisual.cs, Assets/CombatPrototype/CatActorVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-CHR-007|黑猫主角攻击动作（长枪）|INTEGRATED|Assets/CombatPrototype/FantasyActorVisual.cs, Assets/CombatPrototype/CatActorVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-CHR-008|黑猫主角攻击动作（法杖）|INTEGRATED|Assets/CombatPrototype/FantasyActorVisual.cs, Assets/CombatPrototype/CatActorVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-CHR-009|黑猫主角攻击动作（弓箭）|INTEGRATED|Assets/CombatPrototype/FantasyActorVisual.cs, Assets/CombatPrototype/CatActorVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-CHR-010|黑猫主角翻滚动作|INTEGRATED|Assets/CombatPrototype/FantasyActorVisual.cs, Assets/CombatPrototype/CatActorVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-CHR-011|黑猫主角受击动作|INTEGRATED|Assets/CombatPrototype/FantasyActorVisual.cs, Assets/CombatPrototype/CatActorVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-CHR-012|黑猫主角死亡动作|INTEGRATED|Assets/CombatPrototype/FantasyActorVisual.cs, Assets/CombatPrototype/CatActorVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-CHR-013|黑猫主角头像 / 小头像|VERIFIED|Assets/CombatPrototype/Resources/CatWorld/Icons/portrait.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json；技术导入/引用/真实非开发运行显示；不代表概念相似度、原生点击或人工认可|
|WX-CHR-014|黑猫主角立绘 / 角色卡|CONCEPT_ONLY|；没有单独角色立绘；不以模型或概念图冒充立绘|
|WX-NPC-001|仓库管理员猫|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Actors/Keeper.prefab, Assets/CombatPrototype/CatActorVisual.cs, Assets/CombatPrototype/CatCampVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-NPC-002|工匠 / 铁匠猫|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Actors/Smith.prefab, Assets/CombatPrototype/CatActorVisual.cs, Assets/CombatPrototype/CatCampVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-NPC-003|向导 / 教学猫|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Actors/Guide.prefab, Assets/CombatPrototype/CatActorVisual.cs, Assets/CombatPrototype/CatCampVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-NPC-004|出征管理员猫|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Actors/Departure.prefab, Assets/CombatPrototype/CatActorVisual.cs, Assets/CombatPrototype/CatCampVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-NPC-005|商人 / 物资猫|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Actors/Supplies.prefab, Assets/CombatPrototype/CatActorVisual.cs, Assets/CombatPrototype/CatCampVisual.cs；物资猫共用已有仓库，静态代理；没有独立商店/交易AI|
|WX-ENM-001|野猫盗匪|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Actors/Bandit.prefab, Assets/CombatPrototype/CatActorVisual.cs, Assets/CombatPrototype/CatCampVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENM-002|山猫投掷手|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Actors/Scout.prefab, Assets/CombatPrototype/CatActorVisual.cs, Assets/CombatPrototype/CatCampVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENM-003|猫爪蘑菇灵|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Actors/Mushroom.prefab, Assets/CombatPrototype/CatActorVisual.cs, Assets/CombatPrototype/CatCampVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENM-004|林间猫灵|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Actors/WoodSpirit.prefab, Assets/CombatPrototype/CatActorVisual.cs, Assets/CombatPrototype/CatCampVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENM-005|野猪 / 替代森林兽（如保留）|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Actors/Bandit.prefab, Assets/CombatPrototype/CatActorVisual.cs, Assets/CombatPrototype/CatCampVisual.cs；采用猫科森林兽替代外观；没有新增野猪AI|
|WX-ENM-101|豹猫猎手|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Actors/Hunter.prefab, Assets/CombatPrototype/CatActorVisual.cs, Assets/CombatPrototype/CatCampVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENM-102|猞猁精英战士|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Actors/Lynx.prefab, Assets/CombatPrototype/CatActorVisual.cs, Assets/CombatPrototype/CatCampVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-BOSS-001|古林狞猫守卫（陆地 Boss）|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Actors/Warden.prefab, Assets/CombatPrototype/CatActorVisual.cs, Assets/CombatPrototype/CatCampVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-BOSS-002|湖心潮灵猫（湖中 Boss）|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Actors/Tide.prefab, Assets/CombatPrototype/CatActorVisual.cs, Assets/CombatPrototype/CatCampVisual.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-WPN-001|长剑（基础）|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/sword.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/sword.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-WPN-002|长枪（基础）|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/spear.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/spear.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-WPN-003|法杖（基础）|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/staff.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/staff.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-WPN-004|弓（基础）|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/bow.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/bow.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-EQP-001|护甲|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/armor.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/armor.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-EQP-002|裤子|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/trousers.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/trousers.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-EQP-003|手臂护具|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/arms.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/arms.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-EQP-004|鞋子|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/boots.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/boots.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-EQP-005|饰品|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/ring.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/ring.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-EQP-006|背包|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/bag.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/bag.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-EQP-007|胸挂|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/armor.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/armor.png；胸挂真实容器业务；外观图使用护甲示意，没有新专用胸挂模型|
|WX-ITM-001|药水|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/potion.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/potion.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ITM-002|卷轴|CREATED|Assets/CombatPrototype/Resources/CatWorld/Props/scroll.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/scroll.png；实际制作资源，当前经济无对应物品定义；不新增或假称可拾取、制造，未接入业务物品|
|WX-ITM-003|任务道具|CREATED|Assets/CombatPrototype/Resources/CatWorld/Props/quest.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/quest.png；实际制作资源，当前经济无对应物品定义；不新增或假称可拾取、制造，未接入业务物品|
|WX-MAT-001|木材|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/wood.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/wood.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-MAT-002|石块|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/stone.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/stone.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-MAT-003|矿石|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/ore.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/ore.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-MAT-004|晶体|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/crystal.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/crystal.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-MAT-005|草药|CREATED|Assets/CombatPrototype/Resources/CatWorld/Props/herb.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/herb.png；实际制作资源，当前经济无对应物品定义；不新增或假称可拾取、制造，未接入业务物品|
|WX-MAT-006|蘑菇|CREATED|Assets/CombatPrototype/Resources/CatWorld/Props/mushroom.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/mushroom.png；实际制作资源，当前经济无对应物品定义；不新增或假称可拾取、制造，未接入业务物品|
|WX-MAT-007|布料|CREATED|Assets/CombatPrototype/Resources/CatWorld/Props/cloth.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/cloth.png；实际制作资源，当前经济无对应物品定义；不新增或假称可拾取、制造，未接入业务物品|
|WX-MAT-008|皮革|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Props/hide.prefab, Assets/CombatPrototype/Resources/CatWorld/Icons/hide.png；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-CAMP-001|篝火|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-CAMP-002|帐篷|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-CAMP-003|仓库建筑 / 仓储区|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-CAMP-004|工作台|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-CAMP-005|出征准备点|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-CAMP-006|路牌与旗帜|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-CAMP-007|箱子木桶物资堆|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-CAMP-008|营地地面与地形装饰|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-CAMP-009|营地远景层|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-FOR-001|森林主路|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-FOR-002|支路 / 分岔|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-FOR-003|树木组|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-FOR-004|灌木与草丛|CONCEPT_ONLY|；未制作独立灌木/草丛组，不以树冠当草丛|
|WX-ENV-FOR-005|岩石组|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-FOR-006|资源点视觉节点|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-FOR-007|宝箱点|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-FOR-008|遗迹结构|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；只接入石刻/祭坛/事件视觉，未制作完整遗迹建筑群|
|WX-ENV-FOR-009|撤离点|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-FOR-010|可修复渡口|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-LAKE-001|湖面材质|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-LAKE-002|岸边区域装饰|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-LAKE-003|湖中 Boss 战斗区域|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ENV-RUIN-001|石柱|INTEGRATED|Assets/CombatPrototype/CombatWorldEvents.cs, Assets/CombatPrototype/CatEventVisual.cs；复用真实祭坛石柱，非全新遗迹建筑组|
|WX-ENV-RUIN-002|遗迹门框|CONCEPT_ONLY|；现有为石刻/祭坛，没有完整遗迹门框|
|WX-ENV-RUIN-003|地面台阶|CONCEPT_ONLY|；未制作专用遗迹台阶，不以平面路标替代|
|WX-ENV-RUIN-004|光效节点|INTEGRATED|Assets/CombatPrototype/CatWorldScenery.cs, Assets/CombatPrototype/CatCampVisual.cs, Assets/CombatPrototype/CampRuntime.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-001|背包图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/bag.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-002|仓库图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/warehouse.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-003|工作台图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/workbench.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-004|出征图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/camp.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-005|路线图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/route.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-006|教程 / 帮助图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/help.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-007|免费撤离图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/exit.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-008|可修复渡口图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/bridge.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-009|Boss 图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/boss.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-010|遗迹图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/route.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-101|木材图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/wood.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-102|石块图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/stone.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-103|矿石图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/ore.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-104|晶体图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/crystal.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-105|药水图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/potion.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-106|长剑图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/sword.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-107|长枪图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/spear.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-108|法杖图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/staff.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-109|弓图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/bow.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-ICO-110|宝箱图标|INTEGRATED|Assets/CombatPrototype/Resources/CatWorld/Icons/chest.png, Assets/CombatPrototype/Resources/CatWorld/Icons/Bounds.json, Assets/CombatPrototype/CatIconLayout.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-VFX-001|主角基础攻击特效|INTEGRATED|Assets/CombatPrototype/CombatFeedback.cs, Assets/CombatPrototype/ForestBossTelegraph.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-VFX-002|长剑斩击特效|INTEGRATED|Assets/CombatPrototype/CombatFeedback.cs, Assets/CombatPrototype/ForestBossTelegraph.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-VFX-003|长枪突刺特效|INTEGRATED|Assets/CombatPrototype/CombatFeedback.cs, Assets/CombatPrototype/ForestBossTelegraph.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-VFX-004|法杖法术特效|INTEGRATED|Assets/CombatPrototype/CombatFeedback.cs, Assets/CombatPrototype/ForestBossTelegraph.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-VFX-005|弓箭飞行特效|INTEGRATED|Assets/CombatPrototype/CombatFeedback.cs, Assets/CombatPrototype/ForestBossTelegraph.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-VFX-006|药水使用特效|CONCEPT_ONLY|；药水有真实业务和通知，未制作专用使用特效|
|WX-VFX-007|Boss 预警圈|INTEGRATED|Assets/CombatPrototype/CombatFeedback.cs, Assets/CombatPrototype/ForestBossTelegraph.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-VFX-008|陆地 Boss 震地特效|INTEGRATED|Assets/CombatPrototype/CombatFeedback.cs, Assets/CombatPrototype/ForestBossTelegraph.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-VFX-009|湖中 Boss 水波特效|INTEGRATED|Assets/CombatPrototype/CombatFeedback.cs, Assets/CombatPrototype/ForestBossTelegraph.cs；待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED|
|WX-VFX-010|撤离成功特效|CONCEPT_ONLY|；撤离有进度与结果UI，未制作专用成功特效|
