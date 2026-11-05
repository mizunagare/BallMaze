# CP06-MAP-TOOLS-03：独立技术验证

基线 `31dbbd23f646e494d49f938c727116e1bba3963f`；分支 `research/cp06-map-tools-03`。2026-11-05，本轮仅在关闭后复用的独立工程 `I:/WGCombat/MAPTOOLS02-A/Project` 中验证，输出在 `I:/WGCombat/MAPTOOLS03-A`。没有复制正在使用的 Library，没有购买工具、修改正式地图或合并 main。远端 main 开工值为 `72db192a527bd256e2ba18cd7ab334d8334051da`。

## 四项遗留问题的结论

| 上轮问题 | 本轮结论 | 边界 |
|---|---|---|
| 视觉块边界/亮线 | PASS：固定历史场景的高亮条带已解释，并有隔离材质对照 | Alpha 光滑度来源为主因；不是高度裂缝。法线最大偏差仍 1.40653°；不宣称任意地图/角度均通过美术验收 |
| 冷启动后总内存未回落 | UNRESOLVED：已排除本组已枚举场景对象逐轮累积，但 Player 跟踪分配仍增长 | 不据 Reserved Memory 或冷启动比较认定泄漏，也不据对象计数稳定认定完全无泄漏 |
| 构建退出 JobTempAlloc | UNRESOLVED：分配栈已缩至原生 Shader Variant 编译链 | 无 Terrain/无活动 MapMagic 的空场景构建也复现；未确定原生退出释放根因 |
| 2.1.20/2.1.19/2.1.17 | UNRESOLVED：下载元数据、常量和旧 meta 来源均可追溯 | 官方公开维护分支为 3.0.0，不能替代稳定包的供应商解释 |

详见 [接缝分析](SEAM_ANALYSIS.md)、[内存分析](MEMORY_ANALYSIS.md)、[原生分配分析](JOBTEMPALLOC_ANALYSIS.md)、[版本来源](VERSION_PROVENANCE.md)。没有把未定位项改成 PASS。

## 真实运行与失败历史

最终独立非开发 Player Audit3：60 PASS / 0 FAIL / 3 NOT_RUN；EditorPlay1：61 PASS / 0 FAIL / 2 NOT_RUN。额外有效 Player Audit2、Memory1、Memory2 分别保留。五次真实运行合计 247 PASS / 0 FAIL / 12 NOT_RUN，属于重复运行行数，不是 247 个独立功能；另有验收清单中的 3 个 UNRESOLVED。过程退出 0 只说明运行完成，不代表整批通过。

四个非开发 Player 进程共 32 个四块生成/卸载循环，Editor 8 个循环。每进程前 2 轮预热、后 6 轮测量；共 160 个 257×257 地形块生成，所有内容哈希一致。没有将旧测试继承为本轮 PASS，也没有重跑或宣称本轮覆盖上批全部敌人通行用例。

Prepare1 编译失败、第一次三项场景列表错误构建、Audit1 旧入口异常和分析工具两项失败均保留。原始尝试未覆盖；详见 [失败历史](FAILURE_HISTORY.md)。

## 构建与校准

最终 BuildAudit3：Unity 6000.6.5f1 / URP 17.6.0 / Windows64 / Development=false，构建成功，0 错误、13 警告；警告完整归档，含自制校准 Shader 编译警告。它是含诊断驱动的独立研究 Player，不是正式发行游戏。最终 Bee 五个服务开关为 false，不能推导所有外部发送路径绝对关闭。构建源工具快照、可执行文件和 Assembly-CSharp 哈希见证据索引；完整lab-input-manifest为运行后库存，不冒充每次构建前冻结快照。

GC 当前线程 API 的正分配控制返回 0，GC.Alloc 事件未测出正控制：NOT_RUN。Player GPU 能返回正数和时钟频率，但受控负载未增加计时：NOT_RUN；Editor 同协议通过负载/恢复校准，仅限 Editor。没有声称零 GC 或 Player 性能优秀，没有自行制定性能预算。

## 保护与交付边界

2,413 项正式工程保护文件、199 项供应商源码、90 项上批自有场景/资源均核对无变化。仓库本批只新增此文档目录；产品 Assets、用户 ProjectSettings、真实存档、main 及旧证据不变。原始包和供应商受限源码不上传。原始日志留在隔离目录，公开日志仅去除许可标识和原生堆字节转储，所有警告、分配及调用栈保留，双哈希在 manifest。

[验收表](ACCEPTANCE.md) · [复跑说明](TESTING.md) · [证据索引](Evidence/INDEX.md)。推送研究分支后暂停，等待固定 SHA 复审；不开始正式地图集成。
