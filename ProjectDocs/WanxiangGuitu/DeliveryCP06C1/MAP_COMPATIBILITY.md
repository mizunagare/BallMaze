# C1 开工兼容映射（先于实现）

产品起点07e47664101b1e4476b675e2b2163ae2ca9f512f；main读取72db192a527bd256e2ba18cd7ab334d8334051da。不合并历史分支，在feature/cp06-new-maps增量实施；用户主工程场景/Settings/Recovery未提交改动保护，开工SHA在隔离根protected-before.json。

现有ForestLayout支持1～5、七地点与两森林Boss硬校验；ForestRegionRuntime拥有导航、actor/root和资源回收；Run→checkpoint→enemies/events/loot→原子v9/分片保存→Pending/Committed→回营结算已存在。互动由InteractionResolver唯一选中WorldEventPoint，不能另建绕过系统。

最小方案：复用区域快照容器，ForestLayout追加可空mapId，遗迹显式revision6/mapId=ancient-ruins，原1～5分支逐值保留。五地点、机关/门/隐藏箱/独立碑文事件、专属守护者使用独立命名空间。快照包含原地位置/敌人/已消费事件/地面奖励；不添加v9顶层字段、不替换旧在途布局。旧二进制不承诺识别新revision；备份后使用当前版本继续，旧版档仍走原校验/恢复。

营地出征准备添加遗迹选项，进入新Run；region=AncientRuins、contentRevision=C1-RUINS-1、generationVersion=9。出口使用原免费撤离；死亡/放弃/取消/Pending/Committed不重写。退出保存后原Run继续，不能读取时重新生成机关或奖励；新地图没有同Run往返森林传送。

必要共享修改及风险：ForestLayout新版本分支；ForestRegionRuntime专用Build路径；AdventureFlow的Depart和Preparation仅新地图分支；AdventureValidation严格绑定region/content/map；CombatEnemy.DropLootOnce新地图独立奖励分支（旧核心保持）；WorldEventPoint标题/可交互/执行委托（旧路径不变）；CraftingTargets对新地图收益诚实显示；地图外观层避免森林装饰误入遗迹。CombatSaveSystem既有字段足够，优先不改。

新奖励用Run/region/seed/entity/规则版本SHA派生，旧Rewards/Placement/Events和Unity随机不用于新地图奖励，已开启/死亡状态与实际战利品同次保存。复用现有六类材料、可选新武器独立工厂，不建立新制造/出售系统。明确新增供给，不称经济不变。

Boss单独状态机：接近/锁定前摇/实际范围震击/定向三发射击/第二阶段组合与恢复；真实物理和原伤害入口，无注入胜利。共享武器/CombatAim/TargetAssist/Camera/八技能/七武器数值/Privacy配置全部冻结。须配对源码、旧回归、Editor和非开发Player；原生/人工/预算无证据保持NOT_RUN。

C1先独立验证、纯发行构建、推送并暂停。C2/C3不开始正式实施。
