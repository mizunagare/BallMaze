# GraphicsSettings 写回的运行影响

使用 Unity 6000.6.5f1、URP 17.6.0 和 R5 固定原始纯包。R5 已捕获 EditorBuildSettings 首次导入时的 BOM 规范化，及 GraphicsSettings 在 BuildPlayerStep → AssetDatabase::SaveAssets 时的原生写回。冻结的旧 YAML 没有这 11 个顶层字段。两份原始发行包中的 GraphicsSettings 对象（PathID 7，864 字节）内容 SHA256 完全相同。两包均保持冻结，本轮没有重建。[R5 原始配置和调用栈](https://github.com/mizunagare/BallMaze/blob/f21f807fb39f38653d7d3a5d9a3e3371936fedbe/ProjectDocs/WanxiangGuitu/DeliveryAncientRuinsR5/NATIVE_SETTINGS_AUDIT.md) · [发行对象与字段偏移](Evidence/graphics-payload.json)

| 字段 | 冻结 YAML | Unity 写回 | A/B 发行运行时 |
| --- | --- | --- | --- |
| m_GraphicsStateCollection | 省略 | 空引用 | 实例 ID 0 |
| m_CollectionStartupAction | 省略 | 0 | 0（None） |
| m_TraceSavePath | 省略 | TracedCollection | TracedCollection |
| m_TraceSendToEditor | 省略 | 1 | 1，启动路径未进入 trace |
| m_AdditionalWarmupCollections | 省略 | 空数组 | 数量 0 |
| m_WarmupAsync | 省略 | 1 | 1，启动路径未进入 warmup |
| m_EnableCacheMissTracing | 省略 | 0 | 0 |
| m_WarmupProgressivelyLimit | 省略 | -1 | -1 |
| m_CacheMissCollectionPath | 省略 | CacheMissCollection | CacheMissCollection |
| m_DefaultLightBaker | 省略 | 0 | 未直接读出独立 Player 字段。官方手册将该选项用于光照贴图与探针的烘焙选择。 |
| m_ShaderBuildSettings | 省略 | 覆盖、定义、编译设置均为空 | 未直接读出独立 Player 字段。构建输出的 Shader 对象和裁剪记录见下。 |

旧 YAML 的「省略」与内存中的空值分开记录。精确匹配的非开发 UnityPlayer PDB 及本机构造器指令确认 PSO 启动值默认 0、缓存未命中跟踪默认关闭、渐进限制默认 -1。其余 PSO 字段以写回和 Player 实测为准。官方手册确认 None 是默认启动模式，不自动加载 Graphics State Collection。LightBaker 与 ShaderBuildSettings 在缺字段时的内部 Editor 值没有独立读取。[Unity Graphics Settings](https://docs.unity3d.com/6000.6/Documentation/Manual/class-GraphicsSettings.html) · [匹配的 Player PDB 与函数位置](Evidence/player-symbols.json) · [默认与分支指令证据](Evidence/native-offset-evidence.txt)

两包各开一轮独立原生诊断。探针先校验 UnityPlayer.dll SHA，再校验原生对象虚表，观察启动注册回调和实际对象。两份回执均观察到注册函数入口，读数相同，跟踪期间均未进入启动 trace 或 warmup 函数。先前托管查询找不到同名静态 getter。首次 UnityPy 通用类型树严格解码因发行对象无内嵌树且结构更新而失败，完整错误保留。针对 PSO 的偏移解码与原生对象实测一致。[A 原生回执](Evidence/Frames-A-camp-native2/native-readback.jsonl.gz) · [B 原生回执](Evidence/Frames-B-camp-native2/native-readback.jsonl.gz)

## 渲染结果

- **Shader 与 Variant**。静态对照中 65 个 Shader 序列化对象逐项同哈希，R3 的 1,178 项 Shader/Pass/API 裁剪计数一致，七个机位记录的材质关键字与全局关键字一致。PSO 启动逻辑未启用预热和跟踪。逐 draw 实际选中的 GPU 变体没有采集。
- **URP、Lighting、Texture**。七个机位的有效 URP 资源、Camera、光照、雾、材质和纹理槽快照在 20 次采集中逐机位一致。A/B 对照的 272 个渲染相关序列化对象同哈希，含 61 个 Material、138 个 Texture2D、3 个 LightmapSettings 和 3 个 RenderSettings。
- **后处理**。诊断中七个游戏相机均无 UniversalAdditionalCameraData，Unity 安装中 URP 17.6.0 的 InitializeAdditionalCameraData 对此分支明确设置 postProcessEnabled=false。没有活动后处理可隔离为像素区域，后处理开关的独立画面对照为 NOT_RUN。雾、阴影和正常颜色处理仍计入完整帧。 [渲染对象清单](Evidence/render-object-hashes.json) · [场景对照](CROSS_BUILD_RENDER_COMPARISON.md) · [URP 分支定位](Evidence/urp-source-receipt.json)

上述证据支持两个现存发行包在本矩阵内使用相同渲染输入和状态。两包经历同一写回，本轮也没有阻止原生写回建立反事实。因此「写回是否改变一个从未写回的发行包」仍为 UNRESOLVED。
