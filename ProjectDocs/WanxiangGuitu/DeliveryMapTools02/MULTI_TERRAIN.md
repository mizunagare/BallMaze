# 多地形块验证

独立工程I:/WGCombat/MAPTOOLS02-A/Project，没有复制Library。Unity6000.6.5f1、URP17.6.0。生成批次使用免费核心真实Noise200→HeightOutput200，Pin触发生成，不重复调用StartGenerate。

## 实际矩阵

2×2地形块，每块64m，总覆盖128×128m。9137、20261、424242三个种子；每种子在129和257两种高度分辨率各重复3次：18个完整四块布局、72块实际生成。全部保留在Evidence/Generate2/generation.csv。

原生MM高度边缘与自制整形后的边缘分别检查，18组两阶段最大接缝高度差均0m；同种子同分辨率3次高度字节哈希一致，不同种子各产生3个不同高度哈希。最终四块257高度网格共264196采样顶点，不等于GPU实际LOD顶点/三角数。

## 功能归属

|功能|实现来源|
|---|---|
|Noise、HeightOutput、分块生成/工作线程、原生高度焊接|MapMagic免费Matrix核心|
|固定有限2×2区域与图参数|自有驱动调用免费核心公共API|
|湖盆、山脊、道路整平、遗迹地基|自有Shape后处理，不是Splines/Biomes|
|水面/水域阻挡、路面Mesh、植被与模块|自有程序化资源/布置，不是Objects模块|
|Terrain.SetNeighbors重新绑定、NavMesh与Scene检查点|自有加载适配与Unity原生API|

湖盆中心(60,85)，可视水域半径14m、水面1.55m；深水有27×27m的粗略BoxCollider并标记不可导航。山脊为高度场，具真实TerrainCollider；道路沿z32布置，地面整平后叠加向上路面网格，没有靠关闭碰撞伪造道路。

SetNeighbors不是已验证会自动持久化的引用。首轮“保存后自动存在邻接”断言失败，已保留；当前将保存的四块顺序作为拓扑数据，在加载OnEnable明确重绑定。Scene重开与Player加载均检查邻接与高度。

## 运行与恢复边界

Scene先保存固化TerrainData、Prefab、Collider和NavMesh，非开发Player直接加载，再用相同seed/resolution真实生成四块并施加同一自有整形，核对内容哈希。实验合成检查点记录地图身份、种子、分辨率、地形/布置哈希及实际导航位置；新进程读取后验证相同内容并使用正常NavMeshAgent初始化。

这是地图工具独立实验的跨进程检查点，**不是产品v9存档/Run恢复验证**。没有导入ForestLayout、RunState、经济、奖励或玩家存档。

接缝高度为0不等于最终视觉接缝质量已经通过；真实截图可见部分分块边缘的明暗/线条差异，未确定渲染原因，保留视觉评审边界，不以高度断言覆盖人工观感。
