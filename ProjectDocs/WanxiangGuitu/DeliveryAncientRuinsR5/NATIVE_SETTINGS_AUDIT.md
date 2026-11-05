# Unity 原生配置写回

在独立干净工程中使用 Unity 6000.6.5f1（3ff58d469c8a）和 URP 17.6.0。冷导入与正式构建分成两个 Unity 进程。启动前核对 1,370 项冻结输入。跟踪器记录实际目标路径上的 Windows 原子替换及调用栈。两个官方 PDB 的 MSF GUID 和 age 均与安装二进制的 CodeView 记录一致。下列时间为跟踪器记录的 UTC。[原生调用栈](Evidence/Audit/symbolized-writebacks.json) · [符号身份](Evidence/Audit/pdb-identity.json) · [Unity Windows 调试文档](https://docs.unity.com/en-us/engine/6000.6/manual/platform-specific/windows/develop/debugging/instructions) · [Frida API](https://frida.re/docs/javascript-api/)

| 文件 | 写回阶段与调用链 | 完整配置 |
| --- | --- | --- |
| ProjectSettings/EditorBuildSettings.asset | 08:39:52.738，首次 AssetDatabase Refresh，早于构建。StopAssetImportingV2Internal → RefreshInternalV2 → ImportOutOfDateAssets → ReSerializeAssetsWithoutImportIfNeeded → WriteRevertAssets → WriteSerializedAssetsV2 → 原子替换。 | [前 b12fcbab](Evidence/NativeProject-Import/Observed/ProjectSettings_EditorBuildSettings.asset-b12fcbabcb28b89b8bc5936caff0c69b4a1acacf1f51f44e8e0870642d352b84.txt) · [后 2005ba4a](Evidence/NativeProject-Import/Observed/ProjectSettings_EditorBuildSettings.asset-2005ba4a47db26bd00c3a4b43aac5d2ab15c47a34d6b5392c34e256c161e8a83.txt) |
| ProjectSettings/GraphicsSettings.asset | 08:40:24.833，构建预处理日志之后、Player 脚本重编译请求之前。BuildPipeline::BuildPlayerInternal → BuildPlayer → BuildPlayerStep → AssetDatabase::SaveAssets → WriteRevertAssets → WriteSerializedAssetsV2 → 原子替换。 | [前 674353be](Evidence/NativeProject-Build/Observed/ProjectSettings_GraphicsSettings.asset-674353be91a9a32dfa24e4db263f11105ee6c82ff20cc346bc150eb4903b33ff.txt) · [后 d1288ed7](Evidence/NativeProject-Build/Observed/ProjectSettings_GraphicsSettings.asset-d1288ed712c51a6803de0b43556ca13a1b418835de68e806846a8fc0c608e03a.txt) |

EditorBuildSettings 的变化限于 UTF-8 BOM。解码后完整 YAML、场景列表和顺序相同，两套发行包的标题均实际启动。GraphicsSettings 则新增真实序列化字段，既有字段值保持一致。新增项涉及 GraphicsStateCollection 与预热、跟踪字段，默认 LightBaker，以及空的 ShaderBuildSettings 覆盖、定义和编译器设置。两套原始纯包的写回后 GraphicsSettings 哈希相同。构建期可见的着色器裁剪统计和七个实测机位的已记录渲染状态相同。是否改变禁止写回时的发行行为仍为 UNRESOLVED，本轮没有改变 Unity 序列化行为建立该反事实。

跟踪用构建独立保留。Unity 报告 Succeeded、0 错误、104 警告，构建选项 None，进程退出码 0。退出日志仍有 JobTempAlloc 警告，保留原始记录。[导入阶段](Evidence/NativeProject-Import/log-landmarks.jsonl.gz) · [构建阶段及 BuildReport 步骤](Evidence/NativeProject-Build/log-landmarks.jsonl.gz) · [构建摘要](Evidence/Audit/traced-build.summary.txt) · [构建日志](Evidence/NativeProject-Build/Unity.log.gz)
