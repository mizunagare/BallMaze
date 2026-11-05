# 发行包语义等同性

起点 8a4ce422f97174160662e8f9acb7982e9d68502b。原始 A/B 均保留在 I:/WGCombat/C1R3-1105-A 下，目录分别为 ProjectA-Build/Release 和 ProjectB-Build/Release。对照原始清单逐包重新计算 193 个文件的 SHA256，均无变化。R5 纯启动副本也与各自原包逐文件相同。两个 exe 共用 SHA256 001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a。[清单与副本校验](Evidence/Audit/release-protection.json)

| 五项不同的发行运行时文件 | 差异解释 |
| --- | --- |
| resources.assets | 同内容的 Unity Performance Testing TextAsset 成对换位，涉及两项对象表记录及对齐字节。R4 精确重建。 |
| globalgamemanagers | ResourceManager 的两项关联 PathID 低位字节与上述换位配套。R4 精确重建。 |
| Managed/Assembly-CSharp.dll | 73 个不同字节位于 PE 时间戳、CLI MVID、CodeView 调试标识、路径及 PDB 校验等构建元数据。R3 单独核验的 40 类 IL 一致。 |
| Plugins/x86_64/lib_burst_generated.dll | 2 个不同字节均属于 PE COFF 时间戳。 |
| boot.config | build-guid 不同。 |

五项指五个运行时文件。完整审计目录另有两个构建回执和一份标记为不随游戏发行的 Burst 辅助文件存在哈希差异。R4 的资源引用重建及 316 个逻辑键的加载证据保留。五项差异字节有归因，完整运行时逐字节一致性仍 FAIL。未确定项集中在六个场内机位的像素差异和 GraphicsSettings 写回的独立因果影响。[全部差异路径及 SHA](Evidence/Audit/release-differences.json) · [R4 资源解析与运行证据](https://github.com/mizunagare/BallMaze/blob/8a4ce422f97174160662e8f9acb7982e9d68502b/ProjectDocs/WanxiangGuitu/DeliveryAncientRuinsR4/RESOURCES_ASSETS_DIFF.md) · [R4 程序集归因](https://github.com/mizunagare/BallMaze/blob/8a4ce422f97174160662e8f9acb7982e9d68502b/ProjectDocs/WanxiangGuitu/DeliveryAncientRuinsR4/Evidence/Audit/managed-byte-attribution.json)

两份原始包的 Bee 配置 Development=false，EnableUnityConnect、EnableCrashReporting、EnableInsights、EnableAnalytics、EnablePerformanceReporting 均为 false，无 R5 取证驱动。R5 的两次纯包启动实际到达标题并记录截图，随后通过独立桌面上的窗口关闭请求正常退出，两个进程退出码 0，合成存档文件无变化。原生菜单操作及人工体验没有执行。[纯 A](Evidence/PureBootA/pure-runtime.json) · [纯 B](Evidence/PureBootB/pure-runtime.json)

重新核对 2,413 项用户保护文件和 117 项 R4 历史证据，均无哈希差异。提交范围为 R5 独立文档、取证工具与证据。[保护核对](Evidence/Audit/protected-inputs.json)
