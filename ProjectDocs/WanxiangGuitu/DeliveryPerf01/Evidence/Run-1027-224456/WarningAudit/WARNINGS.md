# 91条发行警告逐条审计

风险分布：{'信息': 36, '低': 37, '中': 18}。全部仍OPEN，未修改API或重存场景；信息级为同调用点的排序枚举附加诊断，不抹去对应API风险。完整原文、SHA、源码行/列、处置与读取核对见JSON/CSV。

|ID|代码/位置|API|风险|Player路径与处置|
|---|---|---|---|---|
|W001|CS0618 Assets/CombatPrototype/AdventureFlow.Exits.cs:6|FindObjectsSortMode|信息|InteractionResolver→出口查询/修复/撤离，限定场景与稳定出口ID；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W002|CS0618 Assets/CombatPrototype/AdventureFlow.Exits.cs:6|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|InteractionResolver→出口查询/修复/撤离，限定场景与稳定出口ID；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W003|CS0618 Assets/CombatPrototype/AdventureRandom.cs:34|FindObjectsSortMode|信息|按owner/session确定随机流，查询归属不能意外改变作用域；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W004|CS0618 Assets/CombatPrototype/AdventureRandom.cs:34|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|按owner/session确定随机流，查询归属不能意外改变作用域；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W005|CS0618 Assets/CombatPrototype/AdventureResource.cs:27|Object.FindFirstObjectByType<T>()|中|资源附近显示/主角查询，命中和掉落仍由原业务产生；旧First依赖InstanceID；不能机械换Any。先验证单例唯一性与owner/scene，保留多session/恢复/隐藏对象边界后再授权小补丁。|
|W006|CS0618 Assets/CombatPrototype/AdventureFlow.Exits.cs:25|FindObjectsSortMode|信息|InteractionResolver→出口查询/修复/撤离，限定场景与稳定出口ID；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W007|CS0618 Assets/CombatPrototype/AdventureFlow.Exits.cs:25|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|InteractionResolver→出口查询/修复/撤离，限定场景与稳定出口ID；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W008|CS0618 Assets/CombatPrototype/AdventureCombat.cs:137|FindObjectsSortMode|信息|真实攻击/弹体命中/范围命中目标枚举；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W009|CS0618 Assets/CombatPrototype/AdventureCombat.cs:137|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|真实攻击/弹体命中/范围命中目标枚举；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W010|CS0618 Assets/CombatPrototype/CampInventoryView.cs:11|Object.FindFirstObjectByType<T>()|中|营地旧管理界面的session查询（新UI接管后需核对调用条件）；旧First依赖InstanceID；不能机械换Any。先验证单例唯一性与owner/scene，保留多session/恢复/隐藏对象边界后再授权小补丁。|
|W011|CS0618 Assets/CombatPrototype/PlayerInventory.cs:148|Object.FindFirstObjectByType<T>()|中|近邻/通知/交互和旧缓存字段清理；旧First依赖InstanceID；不能机械换Any。先验证单例唯一性与owner/scene，保留多session/恢复/隐藏对象边界后再授权小补丁。|
|W012|CS0618 Assets/CombatPrototype/CombatFeedback.cs:56|FindObjectsSortMode|信息|攻击/受击/战斗表现对象发现；不应影响奖励流；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W013|CS0618 Assets/CombatPrototype/CombatFeedback.cs:56|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|攻击/受击/战斗表现对象发现；不应影响奖励流；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W014|CS0618 Assets/CombatPrototype/CombatEnemy.cs:122|Object.FindFirstObjectByType<T>()|中|敌人死亡掉落与session/世界归属；旧First依赖InstanceID；不能机械换Any。先验证单例唯一性与owner/scene，保留多session/恢复/隐藏对象边界后再授权小补丁。|
|W015|CS0618 Assets/CombatPrototype/CombatInventoryView.cs:29|Object.FindFirstObjectByType<T>()|中|旧背包/商店界面调用链；仅实际激活分支产生开销；旧First依赖InstanceID；不能机械换Any。先验证单例唯一性与owner/scene，保留多session/恢复/隐藏对象边界后再授权小补丁。|
|W016|CS0618 Assets/CombatPrototype/CraftingRecipeDefinition.cs:24|FindObjectsSortMode|信息|配方定义资源发现/查找，不应因顺序改变配方身份；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W017|CS0618 Assets/CombatPrototype/CraftingRecipeDefinition.cs:24|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|配方定义资源发现/查找，不应因顺序改变配方身份；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W018|CS0618 Assets/CombatPrototype/AdventureFlow.cs:42|FindObjectsSortMode|信息|出征/恢复/冻结/结算时的世界对象收集；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W019|CS0618 Assets/CombatPrototype/AdventureFlow.cs:42|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|出征/恢复/冻结/结算时的世界对象收集；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W020|CS0618 Assets/CombatPrototype/CraftingTargets.cs:38|FindObjectsSortMode|信息|只读制造目标/剩余资源与路线查询；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W021|CS0618 Assets/CombatPrototype/CraftingTargets.cs:38|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|只读制造目标/剩余资源与路线查询；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W022|CS0618 Assets/CombatPrototype/CombatSession.cs:114|FindObjectsSortMode|信息|场景session初始化与世界对象注册；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W023|CS0618 Assets/CombatPrototype/CombatSession.cs:114|Object.FindObjectsByType<T>(FindObjectsInactive, FindObjectsSortMode)|中|场景session初始化与世界对象注册；必须保留Include/Exclude、scene过滤和显式稳定ID排序；漏掉inactive参数可能遗留旧世界或漏模板。|
|W024|CS0618 Assets/CombatPrototype/CombatSession.cs:120|FindObjectsSortMode|信息|场景session初始化与世界对象注册；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W025|CS0618 Assets/CombatPrototype/CombatSession.cs:120|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|场景session初始化与世界对象注册；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W026|CS0618 Assets/CombatPrototype/EncounterGuard.cs:20|FindObjectsSortMode|信息|据点警报与敌人群发现，需保留场景/encounter边界；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W027|CS0618 Assets/CombatPrototype/EncounterGuard.cs:20|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|据点警报与敌人群发现，需保留场景/encounter边界；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W028|CS0618 Assets/CombatPrototype/ExtractionPoint.cs:11|Object.FindFirstObjectByType<T>()|中|出口与当前session交互归属；旧First依赖InstanceID；不能机械换Any。先验证单例唯一性与owner/scene，保留多session/恢复/隐藏对象边界后再授权小补丁。|
|W029|CS0618 Assets/CombatPrototype/CraftingTargets.cs:69|FindObjectsSortMode|信息|只读制造目标/剩余资源与路线查询；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W030|CS0618 Assets/CombatPrototype/CraftingTargets.cs:69|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|只读制造目标/剩余资源与路线查询；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W031|CS0618 Assets/CombatPrototype/EnemyProjectile.cs:61|FindObjectsSortMode|信息|敌人弹体命中与碰撞目标收集；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W032|CS0618 Assets/CombatPrototype/EnemyProjectile.cs:61|Object.FindObjectsByType<T>(FindObjectsInactive, FindObjectsSortMode)|中|敌人弹体命中与碰撞目标收集；必须保留Include/Exclude、scene过滤和显式稳定ID排序；漏掉inactive参数可能遗留旧世界或漏模板。|
|W033|CS0618 Assets/CombatPrototype/CraftingTargets.cs:72|FindObjectsSortMode|信息|只读制造目标/剩余资源与路线查询；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W034|CS0618 Assets/CombatPrototype/CraftingTargets.cs:72|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|只读制造目标/剩余资源与路线查询；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W035|CS0618 Assets/CombatPrototype/CraftingTargets.cs:75|FindObjectsSortMode|信息|只读制造目标/剩余资源与路线查询；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W036|CS0618 Assets/CombatPrototype/CraftingTargets.cs:75|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|只读制造目标/剩余资源与路线查询；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W037|CS0618 Assets/CombatPrototype/CraftingTargets.cs:81|FindObjectsSortMode|信息|只读制造目标/剩余资源与路线查询；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W038|CS0618 Assets/CombatPrototype/CraftingTargets.cs:81|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|只读制造目标/剩余资源与路线查询；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W039|CS0618 Assets/CombatPrototype/CraftingTargets.cs:87|FindObjectsSortMode|信息|只读制造目标/剩余资源与路线查询；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W040|CS0618 Assets/CombatPrototype/CraftingTargets.cs:87|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|只读制造目标/剩余资源与路线查询；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W041|CS0618 Assets/CombatPrototype/CraftingTargets.cs:97|FindObjectsSortMode|信息|只读制造目标/剩余资源与路线查询；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W042|CS0618 Assets/CombatPrototype/CraftingTargets.cs:97|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|只读制造目标/剩余资源与路线查询；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W043|CS0618 Assets/CombatPrototype/CombatInventoryView.cs:107|Object.FindFirstObjectByType<T>()|中|旧背包/商店界面调用链；仅实际激活分支产生开销；旧First依赖InstanceID；不能机械换Any。先验证单例唯一性与owner/scene，保留多session/恢复/隐藏对象边界后再授权小补丁。|
|W044|CS0618 Assets/CombatPrototype/ForestRewards.cs:14|FindObjectsSortMode|信息|地点剩余收益/事件/资源查询，结果必须只读；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W045|CS0618 Assets/CombatPrototype/ForestRewards.cs:14|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|地点剩余收益/事件/资源查询，结果必须只读；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W046|CS0618 Assets/CombatPrototype/HeroEquipment.cs:47|Object.FindFirstObjectByType<T>()|中|装备预览/迁移旧装备接口的session归属；旧First依赖InstanceID；不能机械换Any。先验证单例唯一性与owner/scene，保留多session/恢复/隐藏对象边界后再授权小补丁。|
|W047|CS0618 Assets/CombatPrototype/GamePreferences.cs:11|Object.FindFirstObjectByType<T>()|中|设置应用时相机/HUD与当前存档位置的单例归属；旧First依赖InstanceID；不能机械换Any。先验证单例唯一性与owner/scene，保留多session/恢复/隐藏对象边界后再授权小补丁。|
|W048|CS0618 Assets/CombatPrototype/CombatSaveSystem.cs:120|FindObjectsSortMode|信息|保存/恢复的资源、敌人、事件与地面物稳定身份采集；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W049|CS0618 Assets/CombatPrototype/CombatSaveSystem.cs:120|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|保存/恢复的资源、敌人、事件与地面物稳定身份采集；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W050|CS0618 Assets/CombatPrototype/CombatSaveSystem.cs:138|FindObjectsSortMode|信息|保存/恢复的资源、敌人、事件与地面物稳定身份采集；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W051|CS0618 Assets/CombatPrototype/CombatSaveSystem.cs:138|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|保存/恢复的资源、敌人、事件与地面物稳定身份采集；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W052|CS0618 Assets/CombatPrototype/GamePreferences.cs:12|Object.FindFirstObjectByType<T>()|中|设置应用时相机/HUD与当前存档位置的单例归属；旧First依赖InstanceID；不能机械换Any。先验证单例唯一性与owner/scene，保留多session/恢复/隐藏对象边界后再授权小补丁。|
|W053|CS0618 Assets/CombatPrototype/GameEntry.cs:60|FindObjectsSortMode|信息|Boot/Title进入或返回时清理旧世界；必须包括应清理的inactive对象；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W054|CS0618 Assets/CombatPrototype/GameEntry.cs:60|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|Boot/Title进入或返回时清理旧世界；必须包括应清理的inactive对象；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W055|CS0618 Assets/CombatPrototype/InputSettingsPanel.cs:9|Object.FindFirstObjectByType<T>()|中|从真实设置位置载入/应用绑定；旧First依赖InstanceID；不能机械换Any。先验证单例唯一性与owner/scene，保留多session/恢复/隐藏对象边界后再授权小补丁。|
|W056|CS0618 Assets/CombatPrototype/InteractionResolver.cs:28|FindObjectsSortMode|信息|每次情境交互解析；显示和执行使用同一解析身份；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W057|CS0618 Assets/CombatPrototype/InteractionResolver.cs:28|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|每次情境交互解析；显示和执行使用同一解析身份；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W058|CS0618 Assets/CombatPrototype/InteractionResolver.cs:32|FindObjectsSortMode|信息|每次情境交互解析；显示和执行使用同一解析身份；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W059|CS0618 Assets/CombatPrototype/InteractionResolver.cs:32|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|每次情境交互解析；显示和执行使用同一解析身份；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W060|CS0618 Assets/CombatPrototype/CombatSaveSystem.cs:179|FindObjectsSortMode|信息|保存/恢复的资源、敌人、事件与地面物稳定身份采集；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W061|CS0618 Assets/CombatPrototype/CombatSaveSystem.cs:179|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|保存/恢复的资源、敌人、事件与地面物稳定身份采集；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W062|CS0618 Assets/CombatPrototype/ForestRegionRuntime.cs:20|FindObjectsSortMode|信息|森林模板、实体、出口、恢复和导航检查的枚举；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W063|CS0618 Assets/CombatPrototype/ForestRegionRuntime.cs:20|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|森林模板、实体、出口、恢复和导航检查的枚举；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W064|CS0618 Assets/CombatPrototype/ForestRegionRuntime.cs:21|FindObjectsSortMode|信息|森林模板、实体、出口、恢复和导航检查的枚举；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W065|CS0618 Assets/CombatPrototype/ForestRegionRuntime.cs:21|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|森林模板、实体、出口、恢复和导航检查的枚举；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W066|CS0618 Assets/CombatPrototype/ForestRegionRuntime.cs:22|FindObjectsSortMode|信息|森林模板、实体、出口、恢复和导航检查的枚举；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W067|CS0618 Assets/CombatPrototype/ForestRegionRuntime.cs:22|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|森林模板、实体、出口、恢复和导航检查的枚举；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W068|CS0618 Assets/CombatPrototype/CombatSaveSystem.cs:211|FindObjectsSortMode|信息|保存/恢复的资源、敌人、事件与地面物稳定身份采集；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W069|CS0618 Assets/CombatPrototype/CombatSaveSystem.cs:211|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|保存/恢复的资源、敌人、事件与地面物稳定身份采集；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W070|CS0618 Assets/CombatPrototype/OnboardingFocus.cs:23|FindObjectsSortMode|信息|教程目标与资源/出口只读可达性查询；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W071|CS0618 Assets/CombatPrototype/OnboardingFocus.cs:23|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|教程目标与资源/出口只读可达性查询；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W072|CS0618 Assets/CombatPrototype/OnboardingFocus.cs:24|FindObjectsSortMode|信息|教程目标与资源/出口只读可达性查询；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W073|CS0618 Assets/CombatPrototype/OnboardingFocus.cs:24|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|教程目标与资源/出口只读可达性查询；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W074|CS0618 Assets/CombatPrototype/WorldEventPoint.cs:40|Object.FindFirstObjectByType<T>()|中|事件/宝箱/祭坛与当前主角、session归属；旧First依赖InstanceID；不能机械换Any。先验证单例唯一性与owner/scene，保留多session/恢复/隐藏对象边界后再授权小补丁。|
|W075|CS0618 Assets/CombatPrototype/WorldEventPoint.cs:44|Object.FindFirstObjectByType<T>()|中|事件/宝箱/祭坛与当前主角、session归属；旧First依赖InstanceID；不能机械换Any。先验证单例唯一性与owner/scene，保留多session/恢复/隐藏对象边界后再授权小补丁。|
|W076|CS0618 Assets/CombatPrototype/ForestRegionRuntime.cs:58|FindObjectsSortMode|信息|森林模板、实体、出口、恢复和导航检查的枚举；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W077|CS0618 Assets/CombatPrototype/ForestRegionRuntime.cs:58|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|森林模板、实体、出口、恢复和导航检查的枚举；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W078|CS0618 Assets/CombatPrototype/PlayerInput.cs:40|Object.FindFirstObjectByType<T>()|中|输入采样重连/场景变更后的主角定位，禁止串到其他session；旧First依赖InstanceID；不能机械换Any。先验证单例唯一性与owner/scene，保留多session/恢复/隐藏对象边界后再授权小补丁。|
|W079|CS0618 Assets/CombatPrototype/ScenePresentation.cs:13|FindObjectsSortMode|信息|场景表现资源收集/清理，不得改变碰撞/导航；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W080|CS0618 Assets/CombatPrototype/ScenePresentation.cs:13|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|场景表现资源收集/清理，不得改变碰撞/导航；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W081|CS0618 Assets/CombatPrototype/RouteScoring.cs:13|FindObjectsSortMode|信息|只读路线风险/收益/实体状态计算；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W082|CS0618 Assets/CombatPrototype/RouteScoring.cs:13|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|只读路线风险/收益/实体状态计算；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W083|CS0618 Assets/CombatPrototype/RouteScoring.cs:15|FindObjectsSortMode|信息|只读路线风险/收益/实体状态计算；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W084|CS0618 Assets/CombatPrototype/RouteScoring.cs:15|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|只读路线风险/收益/实体状态计算；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W085|CS0618 Assets/CombatPrototype/RouteScoring.cs:27|FindObjectsSortMode|信息|只读路线风险/收益/实体状态计算；这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。|
|W086|CS0618 Assets/CombatPrototype/RouteScoring.cs:27|Object.FindObjectsByType<T>(FindObjectsSortMode)|低|只读路线风险/收益/实体状态计算；当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。|
|W087|CS0414 Assets/CombatPrototype/PlayerInventory.cs:26|PlayerInventory.nearestEvent|低|近邻/通知/交互和旧缓存字段清理；当前是private、未SerializeField，只有声明/null或0赋值，没有读取。nearest/nearestEvent由InteractionResolver替代；nextAttack由AdventureCombat.attackAt负责。非有效保护状态、非当前性能瓶颈；删除后仍需E/H/攻击冷却/恢复回归。|
|W088|CS0414 Assets/CombatPrototype/PlayerInventory.cs:25|PlayerInventory.nearest|低|近邻/通知/交互和旧缓存字段清理；当前是private、未SerializeField，只有声明/null或0赋值，没有读取。nearest/nearestEvent由InteractionResolver替代；nextAttack由AdventureCombat.attackAt负责。非有效保护状态、非当前性能瓶颈；删除后仍需E/H/攻击冷却/恢复回归。|
|W089|CS0414 Assets/CombatPrototype/ThirdPersonHero.cs:15|ThirdPersonHero.nextAttack|低|见精确源码位置；不以警告数量推导已执行频率；当前是private、未SerializeField，只有声明/null或0赋值，没有读取。nearest/nearestEvent由InteractionResolver替代；nextAttack由AdventureCombat.attackAt负责。非有效保护状态、非当前性能瓶颈；删除后仍需E/H/攻击冷却/恢复回归。|
|W090|SCENE_VERSION Assets/CombatPrototype/Boot.unity:|GameObject serialized version 1 < minimum 6|中|BootEntry/GameEntry根对象反序列化；当前兼容读取不代表未来导入器永久安全；GameObject块缺少serializedVersion，按旧默认1读取；不要将Transform的version2误当成本诊断。原文件不改，冷导入与实际标题样本为最小复现；当前没有证据证明产品启动已因此损坏。|
|W091|SCENE_VERSION Assets/CombatPrototype/Title.unity:|GameObject serialized version 1 < minimum 6|中|BootEntry/GameEntry根对象反序列化；当前兼容读取不代表未来导入器永久安全；GameObject块缺少serializedVersion，按旧默认1读取；不要将Transform的version2误当成本诊断。原文件不改，冷导入与实际标题样本为最小复现；当前没有证据证明产品启动已因此损坏。|
