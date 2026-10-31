# R1.2 验收表

| 条目 | 状态 | 证据 |
|---|---|---|
| 无默认 PASS/0/false | PASS | [60专项](Evidence/ProcessTests-Delivery/selftest.json)、签名检查 |
| 缺状态/exit/两者/原生回执拒绝 | PASS | [60专项](Evidence/ProcessTests-Delivery/selftest.json)，INCOMPLETE/3 |
| 非法状态/类型/矛盾/timeout0拒绝 | PASS | 同上，API/CLI 分别记录预期及实际退出 |
| 标量不能填补缺失文件字段 | PASS | 同上新增3项，原始内容保持不变 |
| 正式包装器实际来源与SHA | PASS | [Editor](Evidence/Editor/Semantic/acceptance.json)、[Runtime](Evidence/Runtime/Semantic/acceptance.json) |
| 有效真实退出证据+293PASS结构 | PASS（工具） | [8读核](Evidence/RealEvidenceChecks/results.json)，断言副本是合成，不是游戏293通过 |
| 有效真实退出证据+2UR | PASS（分类） | 同上，BLOCKED/2 |
| 保留旧50及R1.1的33 | PASS | [50](Evidence/Legacy50-Final/selftest.json)、[33](Evidence/Legacy33-Final/selftest.json)，原脚本/证据不改 |
| 真实 Editor/非开发 Player | UNRESOLVED | 各291PASS+2UR、进程0、整体BLOCKED |
| 一致性、哈希保护 | PASS | [38检查](Evidence/consistency.json)、[保护](Evidence/protected-after.json) |
| 历史法杖与引擎问题 | UNRESOLVED | 不改旧结论 |
| 原生 UI、人工、性能、新构建 | NOT_RUN | 本轮无对应实测声明 |

不把进程0、工具夹具或143项工具通过等同于游戏整体验收通过。
