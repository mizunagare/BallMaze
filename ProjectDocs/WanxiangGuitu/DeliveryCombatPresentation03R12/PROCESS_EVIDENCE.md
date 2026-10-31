# 进程证据合同

## 删除的默认成功

`evaluate` 的 process_status、exit_code、timed_out、process_receipt、exit_receipt 均默认 None；CLI 不再默认 PASS 或 false。缺文件、缺状态、缺 exitCode、类型非法或互相矛盾，都不能取得进程资格，整体 INCOMPLETE/3。

手工 status/exitCode/timedOut 只作可选一致性断言，不能单独授权成功，也不能填补文件中缺失的字段。即使显式给 PASS/0/false，无文件仍 INCOMPLETE/3。有真实文件时可以不重复传手工标量，状态来自文件的必需字段，属于读取证据，不是使用默认值。

## 正式来源

正式 Editor/Runtime 包装器先把实际运行器 `results.json` 原字节复制成 `process-results.json`，并保存 `process-origin.json` 的源/副本 SHA 与捕获时间；再把该快照和同次 NativeProbe 的 `CP03Editor.Run.exit.json` 或 `CP03Runtime.exit.json` 交给分类器。

原 `results.json` 仍是原有可追加语义行的编排汇总，不用它后续的不同字节冒充捕获时字节。快照和 NativeProbe 回执不改。原 `presentation.json` 原样读取，不改断言、帧或结果。

检查：同一运行目录、固定 profile 对应的阶段名称/作用域/可执行文件、唯一阶段、日志前缀与退出文件配对；status、exitCode、timedOut 的类型；PASS=0、FAIL≠0、未超时；运行时间顺序与原生退出时间落在阶段内；NativeProbe 非强制终止、合法 hostPid、两份退出码一致。hostPid 是观察器进程身份，不冒称 Unity 子进程 PID。

exitCode 只接受 JSON/Python 整数（不接受 bool/浮点/字符串），范围为 Windows 有符号32位到无符号32位范围；两份原码必须相同，不猜测转换。timedOut 必须 bool，null/字符串/数字不当作 false。NOT_RUN、超时或未知终态均不作为正常成功。

报告记录两份来源绝对路径、同次读取字节 SHA、阶段/作用域、开始结束/退出时间、观察器 PID、forcedTermination、手工 claims 和错误原因。原始文件内容不修改；SHA 与解析来自同次读取。

## 聚合

- 进程证据缺失/非法/不一致：INCOMPLETE/3，优先阻断整体资格；原 FAIL/UNRESOLVED 仍保留在 rawAssertionStatus、rows 和 CSV，绝不改 PASS。
- 有效证据确认失败或断言明确 FAIL：FAIL/1。
- 进程证据有效、冻结绑定有效、原两项 UNRESOLVED：BLOCKED/2。
- 只有全部强制条件通过：PASS/0。

冻结合同 SHA/layer/scope/名称集合仍按 R1.1 严格校验。进程退出0只是一个必要条件，不代表业务或引擎干净。

## 测试边界

离线负例中的进程 JSON 是明确标记的合成 schema 夹具，未执行进程。原 50/33 项的适配副本只增加这种显式证据输入，不删断言；原源码和历史结果保留。

[真实来源读核](Evidence/RealEvidenceChecks/results.json)另用本轮真实运行器/NativeProbe 文件。293 PASS 正向输入是另存的 `reader-tool-synthetic-293-pass.json`，有 SYNTHETIC 标记，仅验证分类器；真实游戏始终是原 `presentation.json` 的 291 PASS+2 UR。没有通过修改真实回执或游戏预期制造全通过。
