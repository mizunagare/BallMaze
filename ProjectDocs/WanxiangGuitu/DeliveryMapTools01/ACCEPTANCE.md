# 当前验收矩阵

当前汇总：**46 PASS / 0 FAIL / 13 NOT_RUN / 1 UNRESOLVED / 1 BLOCKED**；整体BLOCKED。对应范围见[逐条机器记录](Evidence/Validation/acceptance-final.json)。原获取阻断24条旧汇总保留在Evidence/acceptance.json，不能与本轮重复相加，也未把它改写为成功。

|要求|结果|实际边界/证据|
|---|---|---|
|Unity6000.6.5f1、URP|PASS（MM2烟测）|Generate3、EditorPlay1、Player2；必须配置URP地形材质|
|Windows非开发Player|PASS（MM2实验）|Build2、Player2；含测试驱动，不是产品发行Player|
|固定seed重复与差异|PASS|3种子6次Editor+同seed跨Editor/Player高度一致|
|Collider、NavMesh、实际移动|PASS|25探测、四区域路径及真实Agent|
|Scene/TerrainData保存重开|PASS|Generate3高度哈希一致|
|自定义Prefab|PASS（自有夹具）|Column.prefab真实实例化、保存、Player可见；不是免费Objects模块|
|房间、转角通道、Boss厅|PASS（白盒夹具通行）|自有模块和参数布置，不是DA/MM2室内自动生成|
|完整地下封闭空间、模块语法、门锁|NOT_RUN|转角夹具无顶盖；不能伪称地下城工具链已完成|
|自然地形/树木|PASS（技术夹具）|MM2地形+自有树木摆放；非免费Objects自动散布|
|现有产品C#适配|NOT_RUN|仅风险/接口设计，未改正式地图/Run/身份|
|Gaia、DA实际运行|NOT_RUN|无安装包，不购买；官方资料研究不作本机PASS|
|编辑效率/美术评价|NOT_RUN|无真人计时/独立审美评估|
|有效GC、GPU、加载卸载/持续战斗预算|NOT_RUN|没有可靠校准或采样，不填0|
|构建JobTempAlloc|UNRESOLVED|原日志保留；未认定供应商或Unity根因|
|产品与用户文件保护|PASS|2413项无差异/无新增；main未改|
|原生键鼠与人工体验|NOT_RUN|私有桌面自动化截图/Agent不能替代|

历史失败单列：Import1超时；Generate1编译FAIL；Generate2后台异常虽exit0仍不接受；Player1 exit1及截图失败。Build1五警告保留，Build2增量0条不代表已修复旧警告。没有通过修改插件、断言或真实存档制造PASS。

完整预定协议并未全部执行；[协议覆盖差距](PROTOCOL_COVERAGE.md)逐项保留，不以较小代理/较少重复次数冒充全量通过。
