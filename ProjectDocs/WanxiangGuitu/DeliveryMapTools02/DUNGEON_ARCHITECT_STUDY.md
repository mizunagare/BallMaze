# Dungeon Architect：继续只读评估

本轮没有安装包，没有采购，没有导入，也没有DA本机运行PASS。以下为官方文档支持的能力与接入提案。

|评估项|官方资料与判断|本机边界|
|---|---|---|
|Unity6000.6.5f1|厂商称Unity版1.23.0支持Unity6，测试6.3LTS与6.5|精确6000.6.5f1 NOT_RUN；不能把6000.5与6000.6视为同版本|
|URP17.6|厂商说明示例用URP，核心不依赖特定管线|精确URP17.6着色器/构建NOT_RUN|
|模块拼接|Snap Grid Flow模块为Prefab，尺寸按Chunk Size倍数，旋转需匹配XZ|尺寸、Collider和玩家净空必须另测|
|地下封闭房间|自制模块可带墙、屋顶和内部结构，图连接不代替几何|本轮封闭遗迹是自制夹具，不是DA生成结果|
|门与端口|Connection关联Door/Wall，匹配连接显示门，未连端封墙|门厚/枢轴/朝向及NavMesh缝隙需配对验证|
|NavMesh|官方主题构建器导航说明要求静态Prefab参与导航，动态对象不参与|不自动推广到所有Snap模块；现有烘焙/代理合同未接入DA|
|C#规则|官方提供位置约束与模块类别约束接口|源码编译、确定性、异常回退及Player运行NOT_RUN|

来源：[厂商FAQ](https://dungeonarchitect.dev/faq/)、[模块](https://docs.dungeonarchitect.dev/unity/snap-grid-flow/sgf-modules/)、[连接与门](https://docs.dungeonarchitect.dev/unity/snap-grid-flow/sgf-connections/)、[导航](https://docs.dungeonarchitect.dev/unity/advanced-dungeons/runtime-navigation/)、[C#约束](https://docs.dungeonarchitect.dev/unity/snap-grid-flow/sgf-scripting/)。这些网页声明不是本机验证。

## 最小接入方向（未实施）

先在独立工程固化模块几何，导出模块ID、模板哈希、坐标、旋转、连接端口和生成版本。产品仍持有Run、敌人/宝箱身份、已生成奖励及恢复权威；插件不能接管Rewards/Placement/Events。门状态应同时驱动可视、Collider和导航，保存重载后重新绑定。

位置约束与房型约束可以控制地面层、上层和终点房型，但“抽象图连通”不足以证明屋顶、楼梯、门宽与实际Agent通行。本轮MapMagic实验已再次说明邻接需显式加载重绑定、物理阻挡需实际路径检查；不能把生成成功当成玩法完成。

结论：DA仍是室内模块化的优先研究候选，暂无采购/导入建议或性能结论。免费MapMagic核心负责高度场；封闭房间与门模块需要自有逻辑或以后获准的DA验证。保持现有产品工程不变。
