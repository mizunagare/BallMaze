# 证据索引

原始运行根I:/WGCombat/MAPTOOLS-1104-A。发布日志为脱敏副本；压缩保留全部日志行，原始文件未改写。没有插件包或受限供应商源码进入仓库。

- [获取尝试清单与双SHA256](acquisition-manifest.json)：Acquire1～4，sourceSHA256与publishedSHA256分列。
- [首次实际获取结果](Acquire2/acquisition.json)、[原始日志发布副本](Acquire2/Unity.log.gz)、[进程状态](Acquire2/process.json)。
- [用户登录后重试](Acquire3/acquisition.json)、[日志](Acquire3/Unity.log.gz)、[进程状态](Acquire3/process.json)。
- [等待账户valid后的有界请求](Acquire4/acquisition.json)、[状态变迁](Acquire4/states.jsonl.gz)、[日志](Acquire4/Unity.log.gz)、[实际退出](Acquire4/Editor.exit.json)、[进程状态](Acquire4/process.json)。
- [官方来源与观测元数据](official-sources.json)：网页声明，不是本机兼容测试。
- [初始保护清单](protected-before.json)、[早期复核](protected-after.json)、[获取结束复核](protected-after-acquisition.json)。
- ProjectInputs/：独立工程manifest、lock及Unity版本。不是正式产品构建输入。
- [当前分层记录](acceptance.json)：4 PASS、1 BLOCKED、19 NOT_RUN；不删除失败历史。

上述Acquire1～4和旧acceptance.json为先前阻断快照，保留不改写。用户自行下载后完成的实际继续验证见下方，不能重复合计两套汇总。原C1失败、产品历史证据与用户修改保持原位置。

## 用户下载后的真实验证

- [官方包来源/大小/SHA](Validation/package-provenance.json)，不包含安装包本体。
- [发布双哈希清单](Validation/manifest.json)：原始来源、发布文件、脱敏标记。
- [Import1超时](Validation/Import1/process.json)、[正常关闭未执行](Validation/Import1/owned-normal-close.json)、[原日志](Validation/Import1/Unity.log.gz)。
- [Generate1编译失败](Validation/Generate1/Unity.log.gz)、[Generate2后台异常](Validation/Generate2/Unity.log.gz)，旧exit0与10PASS不能掩盖异常。
- [Generate3实际结果](Validation/Generate3/editor.json)、[6次种子数据](Validation/Generate3/seed-results.csv)、[日志](Validation/Generate3/Unity.log)。
- [Editor受控Play](Validation/EditorPlay1/runtime.json)、[实际进程](Validation/EditorPlay1/process.json)与同目录原始PNG/CSV。
- [Build1结果](Validation/Build1/build.json)、[全部5警告](Validation/Build1/build-messages.txt)、[冻结输入](Validation/Build1/input-manifest.json)、executed-runtime-reconstructed.cs.txt为严格按哈希核对的源码重建副本。
- [Player1失败](Validation/Player1/runtime.json)、[实际日志](Validation/Player1/Player.log)。
- [Build2结果](Validation/Build2/build.json)、[实际Bee](Validation/Build2/bee-services.json)、[2400项输入](Validation/Build2/input-manifest.json)、[182输出哈希](Validation/Build2/binary-manifest.json)。Bee清单保留旧Build1缓存行，必须匹配Build2完整DestinationPath才有资格使用。
- [Player2分层结果](Validation/Player2/runtime.json)、[实际退出](Validation/Player2/process.json)、[D3D12日志](Validation/Player2/Player.log)、[窗口隔离](Validation/Player2/Player.desktop-process.json)及4张PNG原图。
- [Profiler原始采样汇总](Validation/performance-summary.json)；Editor与Player各180帧CSV保留，Player1零Draw与GC无效结果未删除。
- [用户保护](Validation/protected-validation-after.json)：2413项不变、无新增。
- [当前矩阵](Validation/acceptance-final.json)：46PASS、0FAIL、13NOT_RUN、1UNRESOLVED、1BLOCKED；历史FAIL在原目录及FAILURE_HISTORY中独立保留。

自有固化Scene/Prefab/Terrain/NavMesh/Profile和meta位于../LabInputs，自有驱动与复跑说明见../TESTING.md。图库来自真实Editor/Player，不包含供应商宣传图或AI图。未发布供应商源码、DLL、包或游戏二进制。

完整预定协议并未全部执行；[协议覆盖差距](../PROTOCOL_COVERAGE.md)逐项保留，不以较小代理/较少重复次数冒充全量通过。
