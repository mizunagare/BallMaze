# R1.3 证据索引

所有本轮输出源于 `I:/WGCombat/CP03-R1-1031-D`。原C/Editor、C/Runtime目录只读；原件路径和哈希见复核报告及保护清单。本轮没有启动新的Unity或Player。

- [发布清单与原始/发布SHA256](manifest.json)
- [修复前10FAIL与1控制PASS](Before/regressions.json)
- [旧50项](Legacy50-First/selftest.json)
- [旧33项](Legacy33-First/selftest.json)
- [旧60项](Legacy60-First/selftest.json)
- [新增35项来源关联负例与控制](Association-First/selftest.json)：每个用例目录保留command、actual-exit、stdout、stderr以及ApiReport/CliReport JSON、CSV与Markdown。
- [原始Editor/Player只读复核汇总](Reaudit/results.json)
- [Editor关联结果](Reaudit/Editor/Semantic/acceptance.json)；[CLI实际退出码](Reaudit/Editor/actual-exit.json)
- [非开发Player关联结果](Reaudit/Runtime/Semantic/acceptance.json)；[CLI实际退出码](Reaudit/Runtime/actual-exit.json)
- [独立一致性44项](consistency.json)
- [3476项保护清单](protected-before.json)、[3191项旧证据保护](extra-protected-before.json)、[保护复核](protected-after.json)
- [1147产品输入及3个二进制](input-binding.json)
- [严格锁定源码及24组发射证据审计](locked-contract.json)
- [包装器语法检查](powershell-parse.json)、[工具入口退出码](tool-runs.json)

`.log/.stdout/.stderr/.jsonl`发布副本按既有发布工具gzip；源字节哈希与发布字节哈希分别登记，原件未改。普通JSON/TXT及既有历史证据不会改写。合成工具测试不是新进程业务、原生键鼠或人工体验证据。两项法杖仍UNRESOLVED，整体BLOCKED/2。

- [Git/LFS发布字节与文档链接核验](publication-check.json)：2380项，4个LFS对象，2376个直接Git对象，零错误。
