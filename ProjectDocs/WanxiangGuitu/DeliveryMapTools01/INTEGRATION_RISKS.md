# 接入风险与隔离边界

本轮只研究，不修改ForestLayout、ForestRegionRuntime、CombatAim、武器、AI、存档或正式Build Profile。C1开发工作区及第一次失败仍留在原分支/隔离根，没有并入研究分支。

|风险|当前判断|验证门槛|
|---|---|---|
|精确引擎版本|6000.6.5f1为固定目标，不能用“Unity6”泛称关闭风险|同版本Editor编译、URP17.6、Win64非开发构建及真实画面|
|Terrain与室内几何不同|MapMagic高度场不等于地下顶棚/墙/多层结构|独立室内模块组合，地图Collider与NavMesh必须同时成立|
|免费/收费模块混用|Objects等不是免费基础包范围|逐项核实包内模块和许可，不复制付费节点替代|
|全局随机流|插件可能使用自有/Unity随机，尚未检测|生成前后采集三流/Unity状态；独立流与生成时机有证据后再适配|
|身份与恢复|Seed本身不足以跨版本还原已开的箱子、Boss和掉落|固定插件版本/图SHA/参数/模板SHA；地图数据与实体ID由产品权威系统持久化，不用InstanceID|
|旧在途布局|生成工具升级不能在加载旧Run时生成新布局|旧revision原路径，新增内容只在新Run显式启用|
|导航完成时机|图连通不等于碰撞或NavMesh可达|地形应用/模块完成后再烘焙，验证完整路径、门状态、出生和出口|
|动态地形/流送|无限瓦片与当前有限快照不天然匹配|首版优先有限、固定瓦片/编辑器烘焙；不擅自设计无限世界存档|
|经济和事件|插件的Spawn Marker不能直接发奖|只提供语义位置；产品交互、来源账、唯一结算负责奖励|
|材质与美术|示例素材风格不等于黑猫世界风格|统一自有卡通材质、光照/雾与可读性；无新许可素材不引入|
|构建与原生DLL|Editor可用不代表非开发Player完整|检查UnityEditor依赖、平台DLL/着色器剔除、输出新鲜度与完整SHA|
|性能|宣传/源码推断不能替代采集|同硬件、种子、分辨率/瓦片数；无效0不做零分配|
|许可证/公开仓库|免费包也可能禁止独立再分发|插件留工程外，Git只收自有工具、说明、统计和许可允许的证据|

## Dungeon Architect 适配提案（未实施）

优先Snap Grid Flow制作固定尺寸房间/转角/大厅Prefab；主题引擎只装饰模块，约束图表达可选分支、门和奖励位置。生成器输出只读中间布局：moduleId、模板GUID/哈希、坐标/旋转、连接端口、语义标记、碰撞和导航收集列表。适配器再创建产品区域实例及稳定实体ID。不要让DA样例控制器、奖励示例、UI或存档进入正式游戏。

官方模块文档要求统一Chunk Size、门高与连接尺寸、Prefab边界；旋转模块需对应X/Z尺寸。[Modules](https://docs.dungeonarchitect.dev/unity/snap-grid-flow/sgf-modules/)

官方运行时导航文档要求静态地面/墙/门的Theme节点参与导航，NPC与动态物件不要挖出孔洞；该页面注明适用于Theme类Builder，不能假设所有Builder相同。[Runtime Navigation](https://docs.dungeonarchitect.dev/unity/advanced-dungeons/runtime-navigation/)

现有产品使用UnityEngine.AI底层烘焙；接入时应明确只由一个系统拥有NavMeshData及移除生命周期。无需为工具评估改动正式导航或额外升级依赖。DA的逻辑钥匙可达保证还需由本项目代理尺寸、坡度、Collider、实际路径与出口规则进行第二次物理验证。
# 本机验证新增风险（2026-11-04）

- URP运行时新建MM2必须显式配置Terrain材质。Player1中默认Shader缺失引发Material构造异常；传入已保存的URP Terrain/Lit材质后Player2通过。没有修改插件。
- Pin会启动生成；驱动再次StartGenerate曾导致MarkReady重复键异常。Generate2即使exit0与断言PASS，也按异常日志不接受；Generate3去除重复请求后无异常。
- 供应商UAC0005反射警告未修复；构建退出JobTempAlloc来源未定位。不要把增量构建未重复警告或Profiler0值解释为风险关闭。
- 目前只是3种子、单块129×129和轻载夹具；无限地形、流式卸载、并发Boss与正式Run恢复未验证。独立NavMesh成功不能证明现有游戏身份/奖励/地图迁移已接入。
