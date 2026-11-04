# 正式路径保留与训练临时上下文

基准7fc4f5dc3043bcbb69f63c2ebf267359741ccbbe。四个冻结文件不改。修改范围为CP05Training、CombatEnemy、AdventureItems、AdventureRandom和新增TrainingLootContext；不修改任何存档结构、场景、Prefab、依赖或数值。

## 正式路径的保留合同

1. CombatEnemy原死亡门槛保留；真实lootDropped在处理开始即设定，重复请求仍立即返回。普通正式Actor没有训练场景登记，继续原掉落核心；其中概率、经验、材料范围、Boss逻辑及调用顺序不变。只有原来访问Session.Wave的普通装备分支增加显式训练选择。
2. AdventureItems.Roll的随机抽取及luck计算顺序不变；品质判定及New调用抽为同一helper。RollTraining显式使用无进度加成的品质策略，**没有CombatSession、没有Wave属性，也没有伪造Wave=1**。阈值/type/affix仍共用原实现。
3. AdventureRandom.State只增加已登记训练场景的提前返回；未登记owner继续完整原正文。null owner也保留原语义。场景登记拒绝CombatSession/AdventureFlow；训练英雄升级选项等稍后发生的抽取，也由所属场景取得私有三随机流，不跨yield交换全局状态。
4. 注册只存在临时scene；OnDisable/Destroy注销，旧实例重开后销毁。正式Profile/Run不增加字段。现有训练普通敌人及其附加实例使用该上下文；不新增Boss训练系统。

源审计逐位置验证核心正文/抽取顺序、完整未变前后缀及冻结哈希；不以宽泛删除字符串放行差异。基准真实正式森林已生成隔离检查点；480组品质与完整随机状态、真实武器死亡及唯一掉落作为配对基线。修复版读取原样复制的真实v9检查点，比较实际Run/region/seed、目标身份、掉落语义、XP、全随机状态。新GUID分别验证唯一，不要求新生成GUID跨进程相同。

## 重开事务

先为每次尝试分配唯一场景名，在关闭旧实例前尝试创建；新工厂及上下文验证完整后才卸载旧scene并释放旧材质。失败时恢复旧对象/上下文/时间状态，清理本次新对象，finally恢复可重试状态。只拥有自己创建的scene，名称冲突的外部scene不得被清理。

每个新场景创建自己的EventSystem，避免借用即将卸载的旧UI系统。控制器在Awake即取得单例身份，外部卸载当前训练scene时注销事件并销毁DDOL控制器。没有直接重置旧角色生命或库存；新角色仍通过原Prefab工厂正常初始化。

## 验证边界

测试只在隔离工程复制文档驱动。死亡由真实Strike/AI攻击产生，不调用Damage/RestoreHealth等注入接口。暂停调用真实库存UI，冲突故障使用真实SceneManager同名拒绝；采集旧Actor/材质引用和scene事件订阅。正式Run规则矩阵中的种子/参数是独立受控规则输入，生成的对象不入袋、不落地、不保存；完成后恢复原随机状态对象，再执行真实死亡配对。

原生键鼠与人工体验独立NOT_RUN；纯发行包移除驱动，并保留PRIVACY-A Profile及实际Bee五项关闭检查。历史失败不覆盖。
