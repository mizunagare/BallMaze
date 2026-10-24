# B4 本地复跑

Unity 固定为 6000.6.5f1，沿用已有工具；不安装、升级或启用 CI。所有根必须在工程外且全新，不使用真实玩家目录。占用时跳过；超时保留进程及诊断，不强杀。

最终完整运行入口：

```powershell
& '<工程>/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1' `
  -SourceProject '<工程>' -TestRoot '<工程外唯一测试父目录>' `
  -Phase All -FullRegression -B4 -ShaderCacheSource '<已完成的隔离副本>'
```

不得加 `-GameplayOnly` 后将结果称为完整 All。未提供 ProcDump 时转储单元为 NOT_RUN；不因此推导 UNKNOWN 已消失。后台私有非激活桌面的关闭矩阵只证明 WM_CLOSE 路径，不证明标题栏或原生 U16。

定向规则及正常 AI：

```powershell
& '<工程>/ProjectDocs/WanxiangGuitu/DeliveryB4/Invoke-Directed.ps1' `
  -SourceProject '<工程>' -TestRoot '<工程外唯一测试父目录>' `
  -WorkerFrom '<已有且已结束的本机All运行根>' `
  -Methods B4Checks.Topology,B4Physics.Run,B4StateRules.Run,B4PickupRules.Run `
  -NormalStrategies Gather,Treasure,Bypass
```

此包装器复用既有 Step/worker/隔离准备和 Invoke-Rules/Invoke-NormalAI，不替代 All。启动参数及依赖由脚本实际参数定义。正常 AI 三策略各包含 Normal、Resume、FinalResume 三个独立 Unity 进程；NPC AI 正常运行，玩家由领域驱动操作，不是原生键鼠验收。

WorkerFrom 必须含与 SourceProject 匹配的受检 owner.json 及 Worker/NativeProbe.dll；不会下载或编译另一套工具。没有可复用 worker 时先使用主入口 All。ShaderCacheSource 仅复用缓存，项目源码仍重新复制与校验，不复用旧测试结果。

规则驱动说明：

- Topology：30 seed 重复生成、27 种图签名（以实际输出为准）、湖岸是否需经过精英点的差异；只读查询不改变随机状态。
- Physics：最多 60 个请求，累计 30 个不同的实际合法 seed；逐条边、地点和出口实际 CharacterController 通行，资源与遭遇 NavMesh 完整路径。仅此受控测试关闭 NPC；不冒充正常 AI。请求 seed、实际 seed、失败原因和 fallback 分列。
- StateRules：旧 revision 1/2/3 原布局保存恢复、耗尽和未拾取装备查询、全局与本局随机状态不变。历史存档夹具由原 FullRegression 同时覆盖。
- PickupRules：已开箱内嵌掉落可拾取，额外墙体仍阻挡，不自动领取；修复前失败保留。

证据发布：`python -B Publish-Evidence.py --run <运行根> --target <新证据目录>`；复用已有脱敏发布器，禁止保存文件、转储、Library 和构建二进制入库。结算只发布去除 plan 的合成摘要。`Provenance.py` 对照源码与隔离输入、构建输入及实际驱动哈希。

原生 U16、人工理解、真实标题栏关闭与 D3D12 UNKNOWN 保持独立状态。没有新的安全交互环境或因果证据，不重复诊断，也不修改生命周期代码。
