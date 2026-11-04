# CP06-MAP-TOOLS-02：免费核心扩展验证

基准8111f1b3c868b67d03605b66ef24cf7eb5313cf4，独立分支research/cp06-map-tools-02。main保持72db192a527bd256e2ba18cd7ab334d8334051da。实际独立根I:/WGCombat/MAPTOOLS02-A，Project未复制Library；所有Unity启动均有3GB可提交内存门槛，顺序分批执行，没有强杀。

## 实际范围与结论

MapMagic免费核心真实生成连续2×2高度场：3个seed、129/257分辨率、各3次重复，共18组/72块。原生与自有整形两阶段接缝高度差均0，重复内容哈希一致。免费核心承担Noise、HeightOutput及分块生成；湖盆、山脊、道路、植被散布、封闭遗迹、导航、邻接重绑定与检查点均为自有适配，绝不称作免费Objects/Splines模块。

本轮保存并重新打开Scene/TerrainData，实际烘焙Collider导航；3个原型NavMeshAgent使用0.65m半径/2.5m高度，跨块行走、绕过深水、穿越遗迹门口，保存逐帧轨迹。它们不是产品战斗AI。

非开发Player从已保存的Scene直接加载，运行时再生成同seed四块并比对；实际卸载/重载、对象清理、新进程读取均执行。合成检查点相同，实际Player PID分别5500、4492；地图身份、seed、地形、布置哈希与真实导航位置一致。检查点属于工具实验，**不是产品v9存档验证**。

建议继续把免费核心当作自然高度场底板，围绕它建设清楚的自有地图适配层。尚不建议以本批替代正式产品集成验收：内存保留、构建退出警告、视觉边界差异仍开放，性能预算和人工评审未执行。DA仍仅研究室内模块化方向，无包、无实测、无采购。

## 分层结果

|层|PASS|FAIL|NOT_RUN|
|---|---:|---:|---:|
|Generate2：完整生成矩阵|60|0|0|
|EditorPlay6：修正后运行|36|0|2|
|PlayerWrite3：非开发写入|36|0|2|
|PlayerRead3：新进程读取|40|0|2|

加上构建、来源、保护、检查点绑定和6张Player PNG独立检查，当前矩阵为**185 PASS / 0 FAIL / 10 NOT_RUN / 4 UNRESOLVED**。只统计当前矩阵；历史失败在FAILURE_HISTORY和原始目录独立保留，不混入当前通过率，也不被覆盖。[逐项验收](ACCEPTANCE.md)、[机器明细](Evidence/acceptance.json)

## 来源核对

|来源层|实际观察|
|---|---|
|官方下载包|214148132字节，SHA256 6ebe30529ea5a98bac346b7423461e18c66e3c73eb54b31df67fd55646f6b8a5|
|Unity本地PackageInfo包头|id165180，MapMagic2，version2.1.20，version_id1425896，upload_id961788|
|源码常量|MapMagicObject.version为2.1.19|
|原包meta|1079项带旧Bundle来源/2.1.17标签；这些已在原包存在，不是本轮插入|
|导入目录|I:/WGCombat/MAPTOOLS02-A/Project/Assets/MapMagic|
|模块|Generators目录仅Matrix；未导入付费Objects/Splines/Biomes|
|来源/许可|用户已领取的[官方免费产品](https://assetstore.unity.com/packages/tools/terrain/mapmagic-2-165180)，商店标示Extension Asset及[标准Asset Store EULA](https://unity.com/legal/as-terms)|

三种版本标签的差异已核实，厂商维护原因未确定，不擅自改常量，也不由旧Bundle元数据推导付费模块授权。199项供应商源码/asmdef/asmref与原始包哈希完全一致。只发布自有资源、代码和脱敏证据，不发布原包、供应商源码、DLL、Demo资源或Player二进制。

## 构建与性能

Build3 Windows64非开发构建成功，0错误1条增量警告；Build1的6条警告完整保留，旧5条UAC0005未因增量不再发出而关闭。最终Bee精确目标对应Build3，Development=false，五项Services均false；这不是所有外部数据路径绝对关闭的证明。

本地Player：I:/WGCombat/MAPTOOLS02-A/Build3/Player/MapTools02.exe。184个文件共110913865字节；EXE SHA256为001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a，业务程序集Assembly-CSharp.dll SHA256为eb66f8d169a35d1b82c728a6f24eeca63aeb452b6e1404f953fd3f6bfdee23a8。EXE是通用Unity引导器，不能单凭其哈希识别实验版本；完整二进制/数据清单在证据中。

四块257高度场264196采样顶点、121个Collider、3个Agent。180帧Profiler记录、GPU原始数据、GC正/零校准和卸载前后内存见[PERFORMANCE.md](PERFORMANCE.md)。GC/GPU未校准保持NOT_RUN；活动对象归零不意味着总内存回到冷基线，也不意味着无泄漏。

## 开放项与保护

4项UNRESOLVED：原生内存保留归因、构建退出JobTempAlloc、分块视觉明暗/线条、厂商版本标签维护原因。无原生键鼠、人工试玩、美术/编辑效率或最终性能预算PASS。原有产品开放项保持原状态。

2413项用户/产品保护文件未变且无新增，包括既有场景、Prefab、ProjectSettings及暂停中的工作；ForestLayout、ForestRegionRuntime、RunState、CombatAim、TargetAssist、正式存档均未改。新分支只增加DeliveryMapTools02文档目录，旧批报告与证据不变。

[多地形](MULTI_TERRAIN.md)、[植被](VEGETATION.md)、[模块](MODULE_PLACEMENT.md)、[DA研究](DUNGEON_ARCHITECT_STUDY.md)、[复跑](TESTING.md)、[失败历史](FAILURE_HISTORY.md)、[证据索引](Evidence/INDEX.md)。推送独立分支后暂停，等待复审，不导入产品或开始下一批。
