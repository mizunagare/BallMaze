# 构建输入审计

结论 **UNRESOLVED**，已定位写回阶段，不等于已证明发行输入等同性。

## 字段与影响

| 文件 | 精确变化 | 已确认范围 / 风险 |
|---|---|---|
| PC_RPAsset.asset | AdditionalLight 4→0，AdditionalLightShadows 0→2，ForwardPlus 1→2，SSAO 1→2，SSR 1→0；RenderingLayers/AlphaOutput/DBufferMRT3/三档 SoftShadows/ScreenSpaceIrradiance/BicubicLightmapSampling 变1；补 ShadowSmallMeshScreenPercentages、PointSamplingUpsampling、Light2D 字段 | URP ShaderBuildPreprocessor 重算并 SaveAssetIfDirty；会影响 shader 预筛选，不能当无意义格式化 |
| UniversalRenderPipelineGlobalSettings.asset | m_RuntimeSettings.m_List 空→16 个 rid | Core OnBeforeSerialize 在 isBuildingPlayer 时筛选并填 runtime list；确实进入运行时配置 |
| GraphicsSettings.asset | 补 GraphicsStateCollection、CollectionStartupAction、Trace/Warmup/CacheMiss、DefaultLightBaker、ShaderBuildSettings | 当前版本默认字段写出；尚未独立证明所有字段对发行无影响 |
| ProjectSettings.asset | productName/metroApplicationDescription Unicode转义；preloadedAssets 增 InputSystem_Actions GUID 052faaac586de48259a63d0c4782560b | 名称转义语义相同；Input System build provider 真实预加载后移除内存引用，磁盘快照可保留该引用；不能将整个文件归为文本变化 |
| UnityConnectSettings.asset | m_Enabled 0→1 | 内存先变、稍后磁盘写出；真实消费于 Services.EnableUnityConnect，精确 native 启用动因未定位 |

全部字段、行级 diff、原字节与 SHA：[field-differences.json](Evidence/Raw/field-differences.json)、[diff](Evidence/Raw/field-differences.diff)。上表缩写不代替原始逐行数据。

## 阶段证据

外部 50ms 只读 watcher 与 managed/asset import/build/shader callbacks 交叉记录：

- FixedOpen2：全新 Library 冷打开、导入、编译、执行入口和退出前五文件均原 SHA，exit0。
- FixedBuildAudit：execute-before-BuildPipeline 均原 SHA；随后第一次 tracked-assets-postimport（早于 int.MinValue build callback）先出现 URP asset 写回与 connect 内存 true。后续 postimport 五文件磁盘全部变化，早于首个 shader callback。
- Input System 构建 provider 调用 SetPreloadedAssets；URP 的 IPreprocessShaders 实现构造时调用 GatherShaderFeatures，解释为何变化早于普通 IPreprocessBuildWithReport。
- FixedWarmPureBuild 不恢复旧值，复用已写回副本：四文件磁盘稳定，ProjectSettings 仍有预加载事务写回。不得用此替代首次输入一致性证明。

[阶段全表](Evidence/Raw/build-phase-analysis.json)、[对照](Evidence/Raw/build-comparison.json)、[本地包源码行号/SHA](Evidence/Raw/package-source-audit.json)、[Input System](Evidence/Raw/input-preload-source-audit.json)。Unity/包版本见每个 snapshot；未升级任何依赖。

## UnityConnect

构建前 enabled=False，online=True、loggedIn=False、projectValid=False、workingOffline=False、preferencesEnabled=False；BuildPipeline 内 enabled=True，其他状态不变。只读扫描 UnityEditor DLL 的托管引用只找到消费者，没有调用 setter 的托管因果链。[扫描](Evidence/Raw/connect-managed-il.json)

BeeBuildPostprocessor.PlayerBuildConfigFor 调用 native-backed get_enabled，将其写入 Services.EnableUnityConnect。实际 Bee 输入为 true（PerformanceReporting false、Analytics false、CrashReporting true、Insights true）。[IL](Evidence/Raw/connect-consumer-field.json)、[实际输入](Evidence/Raw/bee-services.json)。没有证据证明用户登录、云服务操作或测试工具主动 setter；精确原生原因仍 UNRESOLVED。原生绑定参考 [Unity 6000.6 source](https://raw.githubusercontent.com/Unity-Technologies/UnityCsReference/6000.6/Modules/UnityConnect/UnityConnectSettings.bindings.cs)。

## 构建、shader、程序集与二进制

| 运行 | 类型 | errors/warnings | 秒 |
|---|---|---|---|
| FixedBuildAudit | 纯发行 None | 0 / 96 | 133.341 |
| FixedWarmPureBuild | 纯发行 None | 0 / 96 | 19.016 |
| FixedAcceptanceBuild | 非开发，验收 define | 0 / 195 | 28.391 |
| BaselineAcceptanceBuild | 非开发，验收 define | 0 / 362 | 64.199 |

所有 build.json 保留每条 BuildReport message，Unity.log 额外保留 JobTempAlloc/缺失脚本/shader stripping 警告，不过滤为通过。四次各1050 shader callback、variant观察和2016；该数不等于去重最终资源数量。冷/暖纯发行 exe 相同但 managed assembly SHA 不同；exe 是 Unity 启动壳，不能凭其相同证明数据相同。

[完整二进制清单](Evidence/Raw/binary-manifests.json)、[程序集/实际 Solve IL](Evidence/Raw/assembly-audit.json)。纯发行没有验收类型和 UnityEditor 引用；两验收程序集存在 BRPlayer/BRProbe/CP03Cases，明确隔离。尚未证明最终所有序列化构建数据等价，也未解释原生开关原因，继续 UNRESOLVED。
