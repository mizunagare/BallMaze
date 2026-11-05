# 预热后内存与对象引用

本轮共5个独立运行进程（4 Player、1 Editor）。每次先完整预热2轮，再测相同场景的6轮；每轮实际加载、AddNavMeshData、MapMagic四块257生成、确定性Shape、停止任务、销毁生成器/图/地形数据、移除NavMesh实例、卸载Scene、UnloadUnusedAssets、GC.Collect，再等待30帧。校准和图像/材质试验在预热前完成并清理。循环耗时包含加载/生成/卸载/GC，不伪称单独纯生成CPU。

## 测量定义

- Managed：Profiler.GetMonoUsedSizeLong / GetMonoHeapSizeLong；已保留原始值。
- Engine Allocated/Reserved：Unity Profiler 跟踪的总分配/保留，不是 OS 总内存，也不是扣除所有托管数据后的独占 Native Memory。
- 各对象：Resources.FindObjectsOfTypeAll + GetRuntimeMemorySizeLong，记录数量、原生大小及实体ID/名称/HideFlags。该大小不是全进程内存账本，可能存在共享资源，不能简单相加当独占显存。
- WorkingSet/PrivateMemory 的当前运行时 API 返回0，不具有效校准；均 NOT_RUN，未解释为零内存。精确 Native 分配来源/调用栈尚缺 Memory Profiler 快照：NOT_RUN。

以下只比较6轮测量中的首末卸载点，非冷启动：

| 运行 | Engine Allocated首→末 MiB | Reserved首→末 MiB | Mono Used首→末 MiB | Mono Heap MiB |
|---|---:|---:|---:|---:|
| Audit2 | 245.656→246.969 | 537.062→537.062 | 1.496→1.496 | 7.402 |
| Memory1 | 228.719→232.719 | 537.062→537.062 | 1.457→1.457 | 8.082 |
| Memory2 | 235.000→237.813 | 537.062→537.062 | 1.465→1.465 | 8.082 |
| Audit3 | 250.219→251.844 | 537.062→537.062 | 1.496→1.496 | 7.402 |
| EditorPlay1 | 511.266→511.328 | 1280.949→1280.949 | 33.500→33.508 | 82.859 |

## 对象边界

所有 Player 测量卸载点：TerrainData=0、Collider=0、NavMeshData=0、GameObject=4、Material=27、Texture=39、Mesh=4。材质/纹理/网格的实体ID、名称、HideFlags在同一进程六轮中稳定；不是仅数目相同而对象不断替换。生成和加载阶段对应对象数量真实增加，卸载后返回稳定集合。

Editor 的 Resources.FindObjectsOfTypeAll 包含持久化资产与编辑器对象：TerrainData=4、Collider=0、NavMeshData=0、GameObject=15、Material=101、Texture=948、Mesh=14。4个 TerrainData 是仍由编辑器/工程资源系统可见的自有 Tile 资产，不是4个活动 Terrain。独立 runtime cycle-unload 断言验证活动 Terrain=0。编辑器场景、资产浏览器和Player资源系统不同，不能将两者绝对数直接相减。

正引用控制：每次进程最后创建并持有1个专用 TerrainData，库存必须+1；Destroy、UnloadUnusedAssets、GC后必须恢复此前数量。5次控制均通过，说明对象库存能检测这一种真实保留。该控制不是逐调用GC校准，也不证明可以发现所有Native泄漏。

## 结论

PASS：本次已枚举场景对象不随卸载轮次增加，临时Terrain/NavMesh和材质试验未残留。Reserved 的大块扩容与对象数量不一致，不能仅凭 Reserved 未回到冷启动值判泄漏。

UNRESOLVED：Player Engine Allocated 仍有数MiB正漂移；对象ID稳定和Managed平稳不足以解释所有增长。缓存、分配器/渲染资源和测量观察器开销尚未分离，不能断言插件泄漏，也不能断言完全无泄漏。Editor约0.062MiB的首末漂移不代表Player情况。需要带Native调用栈的预热快照和更长、分阶段的资源归属对照后才能关闭。未修改插件、引擎或正式产品来强行回落数值。

[汇总](Evidence/runtime-summary.json)；各运行原始 memory.jsonl.gz、unloaded-summary.csv 在 [索引](Evidence/INDEX.md)。每条原始样本包含TerrainData、Collider、NavMeshData、GameObject、Material、Texture、Mesh的数量和内存，不以本表代替原数据。
