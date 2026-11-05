# CP06-C1-R7 GraphicsSettings 最终核查

基准 3ba94741f91f554b5aa69f0c130f01b17e4f8618。读取 R5 原始 YAML、6000.6.5f1 匹配符号的 Editor 构造及序列化代码、两个冻结发行包、非开发 Player 原生对象和 D3D12 提交记录。本轮未启动 Editor 写入工程配置，原始发行包未重建。[R5 写回证据](https://github.com/mizunagare/BallMaze/blob/f21f807fb39f38653d7d3a5d9a3e3371936fedbe/ProjectDocs/WanxiangGuitu/DeliveryAncientRuinsR5/NATIVE_SETTINGS_AUDIT.md) · [Editor 默认值指令](Evidence/Audit/editor-default-excerpts.txt) · [字段偏移](Evidence/editor-field-transfer.txt)

| 字段 | 旧 YAML | 匹配 Editor 的原生初始化值与写回值 | 实际非开发 Player A/B |
| --- | --- | --- | --- |
| m_GraphicsStateCollection | 缺字段 | 空引用 | 实例 ID 0 |
| m_CollectionStartupAction | 缺字段 | 0 | 0，None |
| m_TraceSavePath | 缺字段 | TracedCollection | TracedCollection |
| m_TraceSendToEditor | 缺字段 | 1 | 1，未触发启动跟踪 |
| m_AdditionalWarmupCollections | 缺字段 | 空 | 数量 0 |
| m_WarmupAsync | 缺字段 | 1 | 1，未触发启动预热 |
| m_EnableCacheMissTracing | 缺字段 | 0 | 0 |
| m_WarmupProgressivelyLimit | 缺字段 | -1 | -1 |
| m_CacheMissCollectionPath | 缺字段 | CacheMissCollection | CacheMissCollection |
| m_DefaultLightBaker | 缺字段 | 0，EditorOnlyGraphicsSettings 构造与 Reset 均写 0 | Editor 烘焙设置，未取得独立 Player 字段 |
| m_ShaderBuildSettings | 缺字段 | ShaderBuildSettings 构造初始化空覆盖、空定义、空编译设置及计数 0 | 构建侧设置，未取得独立 Player 字段。实际产物及绘制见下 |

两包序列化的 GraphicsSettings 对象各 864 字节，内容哈希相同。八次隔离 Player 进程均在原生 RegisterGraphicsStateCollection 回调读到相同九项值，未观察到启动跟踪或预热调用。对照基于本机匹配的 Unity.dll 和 UnityPlayer.dll 符号。本机文档说明 None 不执行自动启动操作，默认 LightBaker 用于光照贴图和探针生成。[发行载荷](Evidence/graphics-payload.json) · [运行原始轨迹](Evidence/INDEX.md) · [Unity Graphics Settings](https://docs.unity3d.com/6000.6/Documentation/Manual/class-GraphicsSettings.html)

七处原生相机在两包均使用 PC_RPAsset、UniversalRenderer、ForwardPlus。各机位两包四份结构化快照逐项同哈希，含相机、材质、Shader 关键字、纹理、光照与雾。标题方向光没有投影，营地和遗迹方向光为 Soft。原生相机没有附加后处理组件。后处理控制实测和实际 GPU 提交均有独立证据。R6 六处场内阴影开关证据保留。[场景快照](Evidence/Audit/scene-metadata.json) · [Shader 实测](SHADER_VARIANT_AUDIT.md) · [后处理](POST_PROCESSING_AUDIT.md) · [R6 阴影对照](https://github.com/mizunagare/BallMaze/blob/3ba94741f91f554b5aa69f0c130f01b17e4f8618/ProjectDocs/WanxiangGuitu/DeliveryAncientRuinsR6/CROSS_BUILD_RENDER_COMPARISON.md)

旧 YAML 缺字段、Editor 写出初始化值和两包实际渲染行为已分别核实。两包经历同样的写回，缺少一个跳过写回但其他条件不变的发行对照，独立因果影响仍为 UNRESOLVED。
