# 发行包与构建清单

原始 A/B 由 R3 干净工程构建。原件、R4 纯包副本及 R3 清单逐文件核对，各 193 个文件完整保留，包含构建回执和非发行备份。两个原始 exe 的 SHA256 均为 001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a。完整发行身份使用逐文件哈希。

原始 BuildReport 各 0 错误、104 警告，Windows64、Development=false。Release Profile 和 UnityConnectSettings SHA256 在两套正式回执一致。完整 Bee JSON 有 35 项不同，对已知 A/B 根路径做明确映射后只剩 ILPP 的独立管道名。五项服务均为 false。

两个纯包在本轮新进程实际启动到标题并退出 0，隔离合成档无字节变化。审计副本另有资源载入，与纯包只差两个引导 JSON 和一个侧车 DLL。产品程序集、序列化资源和 Scene 的哈希保持一致。

[完整文件 SHA256、环境及 Bee 对照](Evidence/Audit/release-manifest.json) · [纯包 A](Evidence/RunPureA/pure-runtime.json) · [纯包 B](Evidence/RunPureB/pure-runtime.json)
