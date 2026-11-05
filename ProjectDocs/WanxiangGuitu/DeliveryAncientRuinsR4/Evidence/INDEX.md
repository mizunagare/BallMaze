# R4 证据索引

基准 d50d2425227e65f8e9f95f1cd7919f28f3bf421a。R4 隔离目录 I:/WGCombat/C1R4-1105-A。原始发行包留在 I:/WGCombat/C1R3-1105-A 下的 ProjectA-Build/Release 与 ProjectB-Build/Release。发布证据源和发布 SHA256 见 [清单](manifest.json)。

- [五项写回](../BUILD_INPUT_AUDIT.md) · [文件绝对路径、时间和原始 SHA](Audit/build-inputs.json)
- [A/B 对象、索引、运行时与精确重建](../RESOURCES_ASSETS_DIFF.md) · [加载 A](RunProbeA/resource-runtime.tsv) · [加载 B](RunProbeB/resource-runtime.tsv)
- [发行清单](Audit/release-manifest.json) · [纯 A](RunPureA/) · [纯 B](RunPureB/)
- [原始构建日志、阶段收据和差异](R3Receipts/) · [程序集元数据归因](Audit/managed-byte-attribution.json)
- [失败历史](../FAILURE_HISTORY.md) · [验收](../ACCEPTANCE.md)

复跑为原始 A/B 建立全新隔离副本。使用 UnityPy 1.25.0 执行 Tools/Audit-Resources.py 并生成资源键。纯包用 Invoke-Pure.ps1。审计副本只追加 C1R4ResourceProbe.dll 和两份 JSON 引导注册，编译以原包 mscorlib、netstandard、System、UnityEngine.CoreModule 和 TerrainModule 为引用。用 Invoke-Resource.ps1 执行只读资源载入。之后依次运行 Audit-Exact.py、Audit-ManagedMetadata.py 和 Audit-Release.py。工具只在新审计根写结果，原始构建与完整路径从清单定位。
