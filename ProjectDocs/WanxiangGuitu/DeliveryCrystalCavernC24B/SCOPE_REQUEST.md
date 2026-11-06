# CP06-C2.4-B 开工审计：路线风险识别缺口

状态：用户已批准这两处共享文件的最小修改。批准边界：精确 C2.4 内容版本及 Boss 稳定身份；同一谓词区分未挑战绕行、挑战后实际路径暴露和死亡。不得改变权重、导航、桥门、撤离及旧地图规则。源码推导不是运行复现或 PASS。

已从设计基准 ed450ccfb6c64973a6e9348767742a18de598f25 创建 feature/cp06-crystal-cavern-boss。产品基准37b25bb641c72deefe4e7e48f19f270711f7fc01，远端main仍72db192a527bd256e2ba18cd7ab334d8334051da。开工无运行中的Unity，无本工作树修改。已在I:/WGCombat/C24-1106-A/Baseline保存无Library的输入副本，登记产品/用户文件哈希，不接触真实存档。

## 已确认的源码条件

1. Assets/CombatPrototype/ForestRegionRuntime.Navigation.cs:77，CopyRisk 的高风险类别谓词是：

```csharp
e.archetype == EnemyArchetype.Elite ||
e.GetComponent<ForestBossBrain>() != null ||
RuinsLayout.Is(Layout) && e.archetype == EnemyArchetype.Boss
```

2. Assets/CombatPrototype/RouteScoring.cs:92，pathElites 使用相同类别判断（map替代Layout）。
3. Assets/CombatPrototype/CraftingTargets.cs:67，pathElites为0时文本为“未见精英贴近路径”。它并不表示完全没有敌人；一般敌人数仍会增加pathEnemies。因此不能夸大为所有风险被清零，但Boss等级风险确实被遗漏。
4. 新设计必须保持Region=CrystalCavern，并使用EnemyArchetype.Boss保证控制免疫与独立AI。没有ForestBossBrain，RuinsLayout.Is为false。在路径确实靠近新Boss时，两处高风险类别谓词仍为false。这是源码逻辑推导，尚没有新增Boss运行样本。

## 为什么不能在现有授权文件里规避

把新Boss注册为Elite会混淆AI、控制免疫、掉落分派；附加ForestBossBrain或改成Ruins地图会误用历史奖励/招式/版本合同。只在HUD写一条Boss提示无法修复NavigationPath.nearElite与RouteEvaluation.pathElites内部不一致。禁止这些绕行改法。

## 申请的最小范围

额外允许修改：
- Assets/CombatPrototype/ForestRegionRuntime.Navigation.cs
- Assets/CombatPrototype/RouteScoring.cs

只在现有类别谓词中增加精确新版本下的晶脊守望者识别（新实体ID、Boss类型、新脑组件身份相互核对）。死亡不计风险；现有NearPath、缓存、导航距离、风险权重、推荐评分公式保持不变。未激活Boss的危险提示应明确为可选挑战风险，不能伪称正在攻击；具体启用条件须在新Boss状态接入时与设计的选择点语义一致。

不修改CraftingTargets、CombatAim、TargetAssist、镜头、武器、旧奖励工厂、随机流或v9字段。不泛化为所有未注册Boss类型，也不改旧地图类别。

## 获授权后的定向证明

- 同位置、同路径：新洞窟活Boss被两处一致识别，死亡后去除；远离路径不误计。
- 未挑战、挑战中、脱战返回三状态的危险标签和实际遭遇边界一致。
- 原森林/遗迹/普通敌/精英相同输入下，风险分项、导航距离和总评分与基准一致。
- 查询前后库存、存档、三条旧随机流及Unity随机状态不变。
- Editor和非开发Player分别执行；保留负例和首次失败。上述当前全部NOT_RUN。

既有注册审计同时发现：EnemyProjectile实际碰撞半径是0.16m，设计0.18m只是候选；优先复用0.16m，不改共享弹体碰撞参数。首奖/常规奖励可复用NewWeaponRegistry的确定性工厂，但遗迹专用白名单、pending识别及死亡完整快照需按已授权清单接入。目前未发现必须新增持久化字段的证据，不预先扩展v9。

按已收到的明确授权，继续原三步实现与验收；不会以本审计代替可玩原型交付，也不会宣称已经完成或推送最终产品。
