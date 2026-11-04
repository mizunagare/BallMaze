# CP06-MAP-TOOLS：独立工具评估交付

2026-11-04。研究起点07e47664101b1e4476b675e2b2163ae2ca9f512f；分支research/cp06-map-tools。先前获取阻断记录在aea2f5275ada029386e03e856537c275d855fced保留。当前main仍72db192a527bd256e2ba18cd7ab334d8334051da，不合并、不修改产品。

## 结论

**当前不购买条件下首选MapMagic 2免费核心，作为自然地形底板工具；室内模块化遗迹首选研究候选Dungeon Architect。** Gaia暂不引入。该判断结合本机MM2烟测和官方功能范围；没有DA/Gaia安装包，不能宣称三款均已实测、某款画质/效率/性能胜出。[比较](MAP_TOOL_COMPARISON.md)、[建议](RECOMMENDATION.md)、[DA研究](DUNGEON_ARCHITECT_STUDY.md)

## 实际完成

- 找到用户下载的官方免费包，214148132字节，完整SHA256见[来源](Evidence/Validation/package-provenance.json)。商店2.1.20与源码常量2.1.19不一致，明确保留。
- 仅在I:/WGCombat/MAPTOOLS-1104-A内导入及运行。实际验证工程ValidationProject，Unity6000.6.5f1、URP17.6.0、D3D12。
- 真实MM2 Noise→Height节点生成128m、129×129地形，9137重复3次、20261重复2次、424242一次，重复高度字节相同，3种子有3种高度哈希。
- 25次TerrainCollider探测通过；Scene/TerrainData保存重开高度不变。
- 自有石柱Prefab+手工参数布局建立遗迹房间、转角通道和Boss厅夹具；自有程序化树木补充自然区。四个区域有真实NavMesh路径及Agent移动。通道是无顶盖转角白盒，地下封闭空间、门锁/模块语法尚未验证。不能计作MM2免费版具有DA式室内生成能力。
- 非开发Windows64 Player真实运行，同seed9137生成高度与Editor逐值一致。四张Player ScreenCapture实际存在并已看图；不是概念图、原生键鼠或人工审美测试。

## 分层结果

|层|PASS|FAIL|NOT_RUN|说明|
|---|---:|---:|---:|---|
|Editor生成Generate3|11|0|0|真实节点、碰撞、保存重开，无未捕获异常|
|Editor受控Play1|14|0|3|四区域Agent、运行时再生成、原始采样；GC/GPU缺口|
|非开发Player2|18|0|3|四区域Agent、4图、运行时再生成，无未捕获异常|

连同构建、Bee和保护3项，以及研究范围缺口，当前矩阵**46 PASS / 0 FAIL / 13 NOT_RUN / 1 UNRESOLVED / 1 BLOCKED**。这只统计当前矩阵，不抹除历史失败。整体因补测资源保护保持BLOCKED，不宣布全部插件/性能/人工验收通过。[逐项记录](Evidence/Validation/acceptance-final.json)

Build1：0错误5条UAC0005警告；Build2增量：0错误0条新BuildReport警告。旧警告未修复；两轮结束仍有JobTempAlloc警告，根因UNRESOLVED。Build2精确Bee目标五项Services全部false、Development=false，未依赖m_Enabled单字段。

Build2位于I:/WGCombat/MAPTOOLS-1104-A/Build2/Player/MapLab.exe，EXE SHA256为001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a；完整182文件/2400输入manifest在证据中。它含实验驱动，是插件验证Player，不能当成产品纯发行构建。

## 真实缺陷/限制

首次导入工具丢失跨程序集重载回调，超时进程68528保留，未强杀；正常关闭请求找不到受控主窗口。改用独立验证副本，旧输入与日志保留。复制Library时Unity自身日志记录处理残留ILPP runner，这不是无缓存导入性能样本；后续不得复制活跃Library。Generate1工具误用private StopGenerate编译失败；Generate2重复启动生成出现后台异常，即使exit0/断言PASS也不接受。Player1默认Shader被剔除导致材质异常且隐藏窗口截图失败；仅调整自有URP材质配置和私有桌面窗口显示后Player2通过，没有修改供应商源码。[全部历史](FAILURE_HISTORY.md)

性能只收集轻载整帧Main Thread和Draw Calls；有效逐生成GC、GPU、持续战斗、卸载资源增长、真人编辑效率/美术质量NOT_RUN。已保存原始无效GC/零Draw样本，不解释为优秀。[性能](PERFORMANCE.md)

## 保护与暂停

2413项用户/产品输入无修改、无新增，CombatAim、森林地图、ProjectSettings、存档及暂停中的C1工作保持原状。产品现有C#业务适配只是风险设计，未接入；旧产品通过/失败状态不因本批改变。仅提交文档目录中的自有工具、夹具、报告和脱敏证据，未上传插件包/供应商代码或真实存档。[保护](Evidence/Validation/protected-validation-after.json)

[验收](ACCEPTANCE.md)、[复跑](TESTING.md)、[图库](PROTOTYPE_GALLERY.md)、[证据索引](Evidence/INDEX.md)。推送独立研究分支后暂停，等待审核，不自动采购插件、导入产品或继续新地图。

完整预定协议并未全部执行；[协议覆盖差距](PROTOCOL_COVERAGE.md)逐项保留，不以较小代理/较少重复次数冒充全量通过。
