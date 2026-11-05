# CP06-MAP-TOOLS-03 证据索引

所有本机原始资料在 `I:/WGCombat/MAPTOOLS03-A`；正式产品工程没有导入插件。此目录为发布副本，源/发布双哈希及许可标识、原生堆字节载荷的处理均见 [manifest.json](manifest.json)。压缩文件解压后可直接读取 JSONL/日志，未修改源文件。构建警告、失败与分配栈均保留；被省略的原生堆 hex 不是根因归属证据，原始日志留在本机。

## 版本、保护与输入

- [owner](owner.json)、[保护结果（2413用户/产品文件、199供应商源码）](protection.json)、[保护前](protected-before.json)、[保护后](protected-after.json)。
- [提交前远端引用](prepush-refs.json)、[最终用户文件复核](final-protection-check.json)、[51个PNG指针对应26个本地LFS对象校验](lfs-staged-check.json)。远端推送后SHA核对在最终交付回复给出，不能预写成功。
- [上批90项自有场景资源比对](fixture-comparison.json)、[官方包重算](package.json)、[版本官方材料/API](VersionResearch/official-observations.json)、[公开维护文件版本摘取](VersionResearch/public-core-version.json)。
- [独立工程运行后输入库存](lab-input-manifest.json)：2545项。它是运行后清单，不冒充每次构建前冻结快照。
- [实际驱动快照一致性](tool-consistency.json)：每次构建/Editor的 ExecutedTools 保存启动前代码；BuildAudit3后增加的Editor.Play入口只影响Editor工具，已明示差异，不伪称所有输入字节相同。
- [最终Bee五项关闭](final-bee-services.json)、[CPU](cpu.json)、[显卡/驱动](gpu.json)。本研究构建含测试驱动，不当作纯发行游戏。
- 新自有场景/Profile/meta/依赖锁在 [LabInputs](../LabInputs)，运行代码在 [Tests](../Tests)，复跑工具在 [Tools](../Tools)；上批自有基础资源仍引用 [原目录](../../DeliveryMapTools02/LabInputs)。供应商原包、源码、演示美术及Player二进制不公开再分发。

## 最终与补充真实运行

| 运行 | 层次 | 结果 | 原始内存 | 进程 |
|---|---|---|---|---|
| Audit3 | 非开发Player，六阶段材质/接缝对照及8循环 | [60 PASS、3 NOT_RUN](Audit3/results.json) | [memory](Audit3/memory.jsonl.gz) / [CSV](Audit3/unloaded-summary.csv) | [退出](Audit3/process.json)、[命令](Audit3/Player.command.json)、[Native宿主](Audit3/Player.desktop-process.json) |
| EditorPlay1 | Editor受控Play，独立8循环 | [61 PASS、2 NOT_RUN](EditorPlay1/results.json) | [memory](EditorPlay1/memory.jsonl.gz) / [CSV](EditorPlay1/unloaded-summary.csv) | [退出](EditorPlay1/process.json)、[实际退出回执](EditorPlay1/Editor.exit.json) |
| Audit2 | 非开发Player，初版五阶段及8循环 | [56 PASS、3 NOT_RUN](Audit2/results.json) | [memory](Audit2/memory.jsonl.gz) / [CSV](Audit2/unloaded-summary.csv) | [退出](Audit2/process.json) |
| Memory1 | 独立Player，专用8循环 | [35 PASS、2 NOT_RUN](Memory1/results.json) | [memory](Memory1/memory.jsonl.gz) / [CSV](Memory1/unloaded-summary.csv) | [退出](Memory1/process.json) |
| Memory2 | 另一独立Player，专用8循环 | [35 PASS、2 NOT_RUN](Memory2/results.json) | [memory](Memory2/memory.jsonl.gz) / [CSV](Memory2/unloaded-summary.csv) | [退出](Memory2/process.json) |

[只读汇总](runtime-summary.json)。memory-only协议不测GPU，缺gpu-status不是自动通过；Editor资源库存含持久资产，活动Terrain卸载断言单列。没有以Process退出0推断整体PASS。

## 非开发 Player 固定机位原图

| 机位 | 修复前原图 | 材质来源控制原图 |
|---|---|---|
| 全景 | [baseline-v0](Audit3/baseline-v0.png) | [matte-v0](Audit3/matte-source-control-v0.png) |
| 湖岸/坡面 | [baseline-v1](Audit3/baseline-v1.png) | [matte-v1](Audit3/matte-source-control-v1.png) |
| 近地观察 | [baseline-v2](Audit3/baseline-v2.png) | [matte-v2](Audit3/matte-source-control-v2.png) |

原图1280×720，不裁切。其余邻接/实例化/法线/阴影控制原图在同一Audit3目录，不用关闭阴影画面充当修复。[高度与两向法线](Audit3/seam-state.jsonl)、[边界投影](Audit3/boundary-projection.jsonl)、[像素对照](image-comparison.json)。Editor截图与Player截图分目录，不混作人工观察结论。

## GC / GPU 校准

- Player：[GC原始正/零控制](Audit3/gc-calibration.json)、[可用计数器及单位](Audit3/available-counters.txt)、[GPU300帧原始样本](Audit3/gpu-calibration.csv)、[GPU校准结果](Audit3/gpu-status.txt)。GC及GPUPlayer仍NOT_RUN。
- Editor：[GC](EditorPlay1/gc-calibration.json)、[GPU300帧](EditorPlay1/gpu-calibration.csv)、[受控GPU结果](EditorPlay1/gpu-status.txt)。GPU仅此层通过负载响应；GC未通过。
- [PERFORMANCE](../PERFORMANCE.md)明确循环墙钟、逐帧CPU和逐调用分配的不同口径；没有沿用旧批性能结果。

## 构建与 JobTempAlloc

- [构建、进程、exe/程序集哈希总表](build-summary.json)。最终BuildAudit3成功：0错13警告；[实际BuildReport摘要](BuildAudit3/build.json)、[全部报告消息](BuildAudit3/build-messages.txt)、[原生完整栈日志发布副本](BuildAudit3/Unity.log.gz)。
- 修正后的 [Empty2摘要](BuildEmpty2/build.json)、[Terrain2摘要](BuildTerrain2/build.json)、[Audit2摘要](BuildAudit2/build.json)。
- [逐条原生分配栈/行号](job-stacks.json)。Empty2不含活动MapMagic或地形场景，仍有ShaderCompilation栈；不宣称插件从项目中卸载或引擎根因已修复。

## 失败历史

[FAILURE_HISTORY](../FAILURE_HISTORY.md)、[Prepare1原始编译失败](Prepare1/Unity.log.gz)、[Audit1旧入口异常](Audit1/Player.log)、[初次关闭被身份保护拒绝](Audit1/close-request.json)、[正常关闭请求](Audit1/close-request2.json)。错误场景Profile的首次三个构建与工具快照均保留。

[分析工具首次缺文件失败](analysis-attempt1.log)、[Editor库存错误模型断言](analysis-attempt2.log)、[修正分层后的只读核对](analysis-attempt3.log)。未修改历史JSON或放宽活动场景卸载要求。历史MAPTOOLS02文档与结果原位保留。
