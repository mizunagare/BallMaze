# 植被组合与资源归属

实际场景使用90棵自有程序化树木：60棵圆冠树、30棵锥形针叶树，包含独立树干碰撞。树冠仅为可视几何，不用隐藏真实树干碰撞来获得通行。

Oak.prefab、Pine.prefab、PineMesh.asset、Wood/OakLeaf/PineLeaf材质均在本轮独立工程制作；未引入第三方模型、纹理或动画。URP Shader来自项目固定Unity/URP依赖。

布置使用独立System.Random(424242)，排除道路、湖泊安全区和遗迹地基，采样高度来自实际Terrain。它是自有散布，不是免费MapMagic Objects、Splines或Biomes。最终样本的变换哈希已保存到Scene，并在不同Player进程核对；没有宣称其他seed的植被多样性已充分采样。

MapMagic生成矩阵每例对比Unity全局Random状态，18例均保持一致；自有散布不调用Unity Random。产品三条旧随机流根本未载入实验工程，因而没有“产品流已经集成”的结论。

三个导航原型使用真实NavMeshAgent，半径0.65m、高度2.5m，覆盖道路跨块、深水绕行和遗迹门口。它们是带可视胶囊的导航敌人原型，**不是产品CombatEnemy的战斗AI测试**，没有注入Damage或掉落。

早期原型胶囊默认材质在URP Player中呈粉色；已保留原图，改为共享场景中明确的URP材质，不新增材质克隆。释放导航原型时销毁其GameObject，场景卸载后检查无活动Agent/Terrain残留。长期资源泄漏、最终美术质量和人工可读性不从本轮短样本推导。

实际资源位于LabInputs/Assets/MT02GeneratedV2，文件SHA由资源清单记录；供应商原包、源码和Demo素材不提交。
