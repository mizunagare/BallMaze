# R1原始证据索引

拥有根 `I:/WGCombat/ER1-1030-A`。P/Project、Library、用户Deferred和Release二进制排除发布；均为合成进度。日志/逐帧jsonl gzip，manifest包含源SHA和发布SHA。

## 修复前与失败历史

- [Before/Unity.log.gz](Before/Unity.log.gz)：SceneHandle工具编译失败。
- [Before2Store/r1.json](Before2Store/r1.json)：64PASS/16FAIL。
- [AfterStore/r1.json](AfterStore/r1.json)：初步产品修复76PASS/4夹具FAIL。
- [BeforeFinalStore/r1.json](BeforeFinalStore/r1.json)：修正Guard夹具后旧版68PASS/12FAIL。
- [After418Store/r1.json](After418Store/r1.json)、[After419Store/r1.json](After419Store/r1.json)：原几何条件80PASS与79PASS/1FAIL。
- [Lane419Store/initial-lanes.jsonl.gz](Lane419Store/initial-lanes.jsonl.gz)：只读物理诊断，石柱9.611793米阻挡原射线。
- [verification-processes.json](verification-processes.json)：首次流程保留After419的FAIL，未运行原420；后续旧回归独立继续，不能说该流程全绿。

每次Launch目录有实际命令、PID、退出码/超时、资源门槛、日志、当次驱动及ForestBossBrain.executed.cs。Store内events.jsonl.gz逐帧记录Boss状态、释放数、弹体数、威胁起止、AI/actor活动、HP及Run/区域/场景身份。

## 最终同条件聚焦

| 版本 | Store | 结果 |
|---|---|---|
| b040旧版 | [BeforeClear418Store/r1.json](BeforeClear418Store/r1.json) | 68PASS/12FAIL |
| b040旧版 | [BeforeClear419Store/r1.json](BeforeClear419Store/r1.json) | 68PASS/12FAIL |
| 一行修复 | [AfterClear418Store/r1.json](AfterClear418Store/r1.json) | 80PASS |
| 一行修复 | [AfterClear419Store/r1.json](AfterClear419Store/r1.json) | 80PASS |
| 一行修复 | [AfterClear420Store/r1.json](AfterClear420Store/r1.json) | 80PASS |

- [clear-lane-processes.json](clear-lane-processes.json)：3个最终进程实际exit0。
- 各Store/initial-lanes.jsonl.gz包含有上限的导航/物理候选，保留原挡路点和最终点；不改障碍。
- 各对应Launch/EncaiR1.cs.txt、r1-config及ForestBossBrain.executed.cs保留具体输入。新旧418/419驱动、配置和候选日志逐字节一致，见[input-binding.json](input-binding.json)。
- [RESULTS.csv](../RESULTS.csv)：两个旧版160条检查与三个新版240条逐项明细；不是5次人工试玩。

## 必要回归与构建

- [EncaiRepro-Run/repro.json](EncaiRepro-Run/repro.json)新19PASS、[EncaiGuard-Run/guard.json](EncaiGuard-Run/guard.json)新13PASS。
- B3StreamRules-Run、B07Economy-Run及[BossRulesStore/b07-rules.txt](BossRulesStore/b07-rules.txt)：随机、经济、六招与Running/Pending/Committed真实恢复；原始回执/预期实际快照同目录。
- [PureBuild/build-report-messages.json](PureBuild/build-report-messages.json)：首个非开发构建0E96W及完整消息。
- [PureBuildFinal/build-report-messages.json](PureBuildFinal/build-report-messages.json)：最终缓存构建0E2W；Boot/Title告警保留，不认为94条编译告警已修复。
- [PureBuildFinal/build-inputs.json](PureBuildFinal/build-inputs.json)、[PE/二进制哈希](PureBuildFinal/release-inspection.json)：Options=None、无R1验收/Editor驱动，exe/UnityPlayer/核心程序集SHA。
- [input-binding.json](input-binding.json)、[user-before.json](user-before.json)：唯一产品源与构建输入一致，5用户文件不变，原DeliveryEncounterAI01无差异。
- [manifest.json](manifest.json)和publication-check.json：发布字节/LFS oid及授权范围核验。

旧524PASS仅在[原固定提交报告](https://github.com/mizunagare/BallMaze/blob/b040b550a5725511a34867de4a2cb27dc56a2b95/ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01/REPORT.md)保留，不计入R1新PASS。完整冒险/发行Player操作、原生U16、人工与性能本批NOT_RUN；历史引擎根因UNRESOLVED。没有把Editor实际AI或显式Destroy故障夹具当成人工/胜利。
