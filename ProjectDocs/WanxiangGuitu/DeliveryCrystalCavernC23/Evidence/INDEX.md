# C2.3 原始证据索引

本批原始根：`I:/WGCombat/C23-1106-A`。原发行包与所有失败原目录保留。仓库归档的文件有原始 SHA 和来源路径，不改写旧测试结果。

## 身份与保护

- [baseline.json](baseline.json)、[baseline-inputs.json](baseline-inputs.json)：开工版本及输入。
- [final-inputs.json](final-inputs.json)、[final-protection.json](final-protection.json)：最终产品输入、七个允许改动及其余输入/用户文件保护。
- [build-input-differences.json](build-input-differences.json)：隔离 Unity 五项自动写回，不代表完整语义等同性通过。
- [release-audit-PureBuild6.json](release-audit-PureBuild6.json)：最终纯发行全包、程序集、EXE、Profile、Bee、Resources.meta。
- [asset-catalog.json](asset-catalog.json)：新资源 ID、路径、来源和 SHA；实际加载由运行断言及截图补证。
- [final-results.json](final-results.json)：最终分层结果及原始失败。
- [runs.json](runs.json)、[manifest.json](manifest.json)：全部保留尝试及逐文件 SHA。
- [Logs.zip](Logs.zip)、[log-archive.json](log-archive.json)：完整原始日志及压缩前 SHA；[build-warning-index.json](build-warning-index.json) 只作导航，非过滤后的替代日志。

## 核心运行

| 范围 | Editor | 非开发观测 Player |
|---|---|---|
| 采集、开桥、宝箱、保存 | [Store](Raw/EditorStoreVerified/assertions.tsv) | [Store](Raw/PlayerStoreVerified/assertions.tsv) |
| 同 Run 地面物品逐项恢复、撤离 | [Resume](Raw/EditorResumeVerified/assertions.tsv) | [Resume](Raw/PlayerResumeVerified/assertions.tsv) |
| 新进程入仓、防重复提交 | [Warehouse](Raw/EditorWarehouseVerified/assertions.tsv) | [Warehouse](Raw/PlayerWarehouseVerified/assertions.tsv) |
| 新 Run 普通资源可再获得 | [Repeat](Raw/EditorRepeatVerified/assertions.tsv) | [Repeat](Raw/PlayerRepeatVerified/assertions.tsv) |
| 桥关闭保存及恢复 | [ClosedResume](Raw/EditorClosedResumeVerified/assertions.tsv) | [ClosedResume](Raw/PlayerClosedResumeVerified/assertions.tsv) |
| 南岸正常 AI 遭遇 | [Inner](Raw/EditorInnerVerified/assertions.tsv) | [Inner](Raw/PlayerInnerVerified/assertions.tsv) |
| 两条岸路双向移动 | [Routes](Raw/EditorRoutesVerified/assertions.tsv) | [Routes](Raw/PlayerRoutesAudited/assertions.tsv) |
| 七武器活体命中与晶柱遮挡 | [Live](Raw/EditorLiveVerified/assertions.tsv) | [Live](Raw/PlayerLiveVerified/assertions.tsv) |
| 导航失败回滚与重试 | [NavFailure](Raw/EditorNavFailure/assertions.tsv) | [NavFailure](Raw/PlayerNavFailure/assertions.tsv) |
| 旧能量区真实翻滚规避 | [Hazard](Raw/EditorHazardFinal/assertions.tsv) | [Hazard](Raw/PlayerHazardFinal/assertions.tsv) |
| 受控危险区死亡及卸载 | [Death](Raw/EditorDeathFinal/assertions.tsv) | [Death](Raw/PlayerDeathFinal/assertions.tsv) |

每个目录含 command、desktop-process、exit、process 和 complete 文件。continuous.tsv 为采样位置，ai.tsv 为实际敌人状态，combat.tsv 为产品观测事件，enemy-health.tsv/health.tsv 为实际生命事件，paths.tsv 为对应导航路径。没有该文件的旧尝试不补造数据。

完整 Player 连续链：[连续出征](Raw/PlayerContinuousAudited/assertions.tsv)、[逐段实际导航](Raw/PlayerContinuousAudited/paths.tsv)、[连续轨迹](Raw/PlayerContinuousAudited/continuous.tsv)、[新进程入仓](Raw/PlayerContinuousWarehouse/assertions.tsv)。纯发行包独立：[pure-runtime.json](Raw/PureBoot6/pure-runtime.json)、[entry-audit.jsonl](Raw/PureBoot6/entry-audit.jsonl)。不把后台退出或观测驱动当作原生输入。

旧档：Editor/Player 的 Legacy21Verified、Legacy22Verified、ForestVerified、RuinsVerified 目录均独立保留。首轮错误工具断言见 EditorLegacy22Final 和 PlayerLegacy22Final 的 failure.txt/断言及日志。两条 FAIL 不删除。

## 实机图

- [最终湖口肩后视角](Raw/PlayerStoreVerified/01-lake-entry.png)
- [北侧环湖实际行进](Raw/PlayerStoreVerified/02-outer-actual-path.png)
- [南侧环湖实际行进](Raw/PlayerInnerVerified/02-inner-actual-path.png)
- [对岸与关闭的桥](Raw/PlayerStoreVerified/03-bridge-closed.png)
- [机关开启后的回程桥](Raw/PlayerStoreVerified/04-bridge-open.png)
- 初始表现问题：Raw/PlayerLake1，第二版：Raw/PlayerStoreFinal。全部原尺寸保留，未裁剪遮蔽问题。

## 量测与未执行项

[hardware-and-measurement.json](hardware-and-measurement.json)、[runtime-measurements.json](runtime-measurements.json) 记录实际硬件和对象/内存快照。没有可靠 GC/GPU 校准，不填零、不判性能通过。人工体验、原生操作和最终平衡仍 NOT_RUN。历史 C1/R7、引擎和发行等同性开放项见 [报告](../REPORT.md)，未因本批自动化通过关闭。
