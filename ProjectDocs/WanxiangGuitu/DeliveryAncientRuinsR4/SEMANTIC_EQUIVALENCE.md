# 等同性结论

resources.assets 字节一致 FAIL。资源内容与引用目标按 Resources 键比较 PASS。两份序列化文件的全部不同字节已解释，运行时 316 个键的实测返回一致。

| 发行文件 | R4 差异归因 |
| --- | --- |
| resources.assets | 两个同内容 TextAsset 换位，2 条对象表记录及对齐，精确重建 |
| globalgamemanagers | ResourceManager 两个配套的 PathID 低位字节，精确重建 |
| Assembly-CSharp.dll | 73 字节全部落在 COFF 时间戳、CLI MVID、CodeView PDB 路径和标识、PDB 校验等构建元数据。R3 核查的 40 个类型 IL 一致 |
| lib_burst_generated.dll | 2 字节都在 PE COFF 时间戳 |
| boot.config | 两个不同 build-guid |

完整发行包逐字节等同仍 FAIL。冻结仓库输入到构建实际消费的全面语义等同性仍 UNRESOLVED，尤其 GraphicsSettings 的精确原生写入调用和跨场景渲染没有独立验证。遗迹玩法、原生输入、人工体验和最终平衡保持 NOT_RUN。

[程序集差异归因](Evidence/Audit/managed-byte-attribution.json) · [发行字节差异](Evidence/R3Receipts/runtime-byte-deltas.json) · [资源索引与实测](RESOURCES_ASSETS_DIFF.md)
