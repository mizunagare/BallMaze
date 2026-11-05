# 发行构建输入审计

基准 d50d2425227e65f8e9f95f1cd7919f28f3bf421a。复核 R3 保留的 Windows64 原始构建。A 从 1,370 个跟踪文件的干净副本先独立导入再构建，B 从另一份同字节副本首次打开即构建。两者使用 Unity 6000.6.5f1（3ff58d469c8a）、URP 17.6.0、Input System 1.20.0、uGUI 2.6.0、同一 Packages 锁和正式 Windows Release Profile。本轮重新核对原始收据与输出。

| 路径 | 实测写回阶段 | 原值与结果 | 调用归因及 Player 边界 |
| --- | --- | --- | --- |
| ProjectSettings/EditorBuildSettings.asset | A 独立打开导入期间，B 首次打开期间 | UTF-8 BOM 被移除，解码行及场景列表相同 | 日志显示 LibraryAssetImporter。精确原生写入方法 UNRESOLVED。A/B 无场景表差异证据 |
| Assets/Settings/PC_RPAsset.asset | 两次构建预处理，先于 Player 脚本编译地标 | AdditionalLight 4→0、AdditionalLightShadows 0→2、ForwardPlus 1→2 等，完整值见字段 diff | 已安装 URP 的 ShaderBuildPreprocessor 调用 UpdateShaderKeywordPrefiltering 和 SaveAssetIfDirty。新增默认字段的精确写点未逐一定位。两包 1,178 项命名 Shader/Pass/API 剥离计数相同 |
| Assets/Settings/UniversalRenderPipelineGlobalSettings.asset | 两次构建预处理序列化 | m_RuntimeSettings.m_List 从空变为 16 个 rid，两次相同 | 本机 6000.6.5f1 的 RenderPipelineGraphicsSettingsContainer.OnBeforeSerialize 在 BuildPipeline.isBuildingPlayer 时调用 PerformStripping。配置资产列入 BuildReport |
| ProjectSettings/GraphicsSettings.asset | 两次构建预处理附近 | 增加 Graphics State Collection、warmup、默认光照烘焙与 ShaderBuildSettings 默认项 | 精确原生写回函数 UNRESOLVED。两个最终包中除两条资源引用外，globalgamemanagers 字节相同 |
| ProjectSettings/ProjectSettings.asset | 两次构建预处理临时写入，结束后撤回临时字段 | preloadedAssets 临时从空变为 InputSystem_Actions（GUID 052faaac586de48259a63d0c4782560b），完成后恢复空。中文字段持久差异是 YAML Unicode 转义 | Input System 的 ProjectWideActionsBuildProvider 使用 BuildProviderHelpers 和 PlayerSettings.SetPreloadedAssets。预加载参与构建期动作资源打包，两包无预加载差异证据 |

记录时间为文件首次被轮询看到的 UTC。完整绝对路径、前后 SHA256、中间版本、编辑器命令及退出回执见输入索引。两个干净副本构建后相同五个文件发生相同写回，原始字节保持 FAIL。

[路径、时间和 SHA256](Evidence/Audit/build-inputs.json) · [逐字段前后值](Evidence/R3Receipts/serialized-fields.txt) · [本机程序集调用](Evidence/Audit/installed-engine-call-sites.json) · [安装包调用](Evidence/Audit/package-call-sites.json)
