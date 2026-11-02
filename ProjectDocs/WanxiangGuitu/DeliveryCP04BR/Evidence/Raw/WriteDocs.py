from pathlib import Path
p=Path('H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04BR');r=Path('I:/WGCombat/CP04BR-1102-A')
(p/'.gitattributes').write_text('Evidence/** -text\nTests/** -text\n*.ps1 -text\n*.py -text\n')
(p/'.gitignore').write_text('__pycache__/\n*.pyc\n')
(p/'REPORT.md').write_text('''# CP04-BR 独立验收收尾

本批完成工具、调查、协议和独立运行；**整体仍 BLOCKED，不宣称产品最终验收通过**。未修改产品，不合并 main。

产品基准 `72db192a527bd256e2ba18cd7ab334d8334051da`；冻结修复与分支起点 `cc9b73679458b0b868d875890a16b4c5238fb878`。交付分支 `verify/cp04-staff-acceptance-br`，本文件所属最终提交即固定审查版本（完整 SHA 由提交后回执提供，避免自引用）。Unity 6000.6.5f1，URP/Core 17.6.0、Input System 1.20.0、uGUI 2.6.0，未升级。

| 分项 | 状态 | 实际结论 |
|---|---|---|
| 构建输入等同性 | UNRESOLVED | 已逐字段及阶段定位；UnityConnect 原生启用原因与完整行为等同性未证明 |
| GC Alloc 完整测量 | NOT_RUN | Editor 基线/修复逐 Solve 有效；非开发 Player 字节接口校准失败，不填零 |
| CPU 测量 | PASS（有限范围） | Editor 配对和修复版 Player 实测；基线 Player 配对及准确查询数量未完成，无性能预算通过结论 |
| Editor 功能 | PASS | 本轮 293 PASS，exit 0，无超时 |
| 非开发验收 Player 功能 | PASS | 本轮 293 PASS，exit 0，无超时；受控 API，不是原生输入 |
| 原生输入 | NOT_RUN | 已准备脚本与空白表，等待真实操作者 |
| 人工体验 | NOT_RUN | 已准备独立记录表，不能预填 |

七个分项：3 PASS（含范围限制）、3 NOT_RUN、1 UNRESOLVED。功能断言合计 586 PASS/0 FAIL；不包含工具失败，也不删除其历史。Editor 两组各 152 个采样作用域，不等同 304 项产品功能断言。

## 关键结果

冷打开、导入、编译五文件字节不变。BuildPipeline 内 URP 预筛选、运行时设置序列化、Input System 预加载和默认字段写回。连接开关从 false 变 true，并实际进入 Bee Services 配置；不能说“只是文本差异”。两次纯发行构建均成功、0 错误/96 警告；Shader 回调各 1050 次、变体观察值之和 2016，不是去重后最终 shader 数。纯发行程序集无 BRPlayer/BRProbe/CP03Cases、无 UnityEditor 引用。[构建审计](BUILD_INPUT_AUDIT.md)

Editor 原始 GC.Alloc 元数据通过正/零/释放引用校准。1.5m 夹具的中位数基线 2516 B、修复 4460 B；它不是零分配，也不是 Player 数据。非开发 Player GC.Alloc recorder 不可用且线程 API 正校准返回 0，明确拒绝其字节结论。[性能](PERFORMANCE.md)

固定修复版 Player 实际产生 13 次 Spawn、3590 次 Flight、一次接触解析和 33 点真实伤害，最大并发 5；完整功能组另有 293 条断言。基线 Player 有缺失脚本警告且没有性能回执，保留中断，未据此归因产品。[失败历史](FAILURE_HISTORY.md)

## 保护

2329 项产品/用户文件和 889 项旧 CP04-B 文档/证据全部哈希一致。CombatAim 与 cc9 冻结字节一致，SHA256 `9f5d9b7d8c1c39b7270839217562033b6425e2af2d357df51e1269558c4e346a`。用户场景、ProjectSettings、恢复目录均保留。仅隔离副本由 Unity 自动写回五文件，无手工恢复值制造一致性。主分支与历史修复/调查分支未改变。[保护证据](Evidence/Raw/protection-after.json)

历史 D3D12 UNKNOWN、Editor 青色帧等未关闭；历史 w2-s0-near / w2-s1-near 原始失败未改写。本批新功能断言不追溯修改旧 UNRESOLVED。下一步需要原生试玩环境、Player 逐调用可靠字节事件，以及 UnityConnect 原生构建行为的新因果证据。

[验收](ACCEPTANCE.md) · [复跑](TESTING.md) · [证据索引](Evidence/INDEX.md) · [原生协议](NATIVE_INPUT.md) · [人工表](HUMAN_PLAYTEST.md)
''',encoding='utf8')
(p/'BUILD_INPUT_AUDIT.md').write_text('''# 构建输入审计

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
''',encoding='utf8')
print('report/build docs written')
