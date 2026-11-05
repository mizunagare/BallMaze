# 失败历史

- 首次侧车编译缺少原包 netstandard 引用，产生 CS0012。补上同一原包的 netstandard.dll 后成功。
- 首次解析对资源键错误地要求逐记录唯一。原始索引 327 条、316 个唯一键。改用按键分组并在运行时调用 LoadAll，保留重复键及顺序。
- 第一次精确字节重建遗漏旧位置尾部四个字节变为零的对齐情况。保留偏移列表，扩大到 A/B 两个对象结束位置的并集并核对不覆盖其他对象后，重建通过。
- R3 的输入和输出字节差异、原有失败和引擎未解决项继续保留。R4 重核 354 对 R3 原始及发布文件。

[编译失败](Evidence/compile1.log.gz) · [重建初轮剩余字节](Evidence/Audit/remaining-first-attempt.json) · [R3 失败历史](../DeliveryAncientRuinsR3/FAILURE_HISTORY.md)
