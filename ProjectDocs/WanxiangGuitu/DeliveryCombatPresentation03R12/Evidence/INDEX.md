# R1.2 原始证据索引

新根 `I:/WGCombat/CP03-R1-1031-C`；3,100 个发布工件见 [manifest](manifest.json)，列出原/发布 SHA、大小、仅凭据值遮盖。原日志在 I 根，gzip 保留所有异常/栈/顺序。P/Project、缓存和二进制不入库；gzip 使用已有 LFS。索引在发布后生成，不参与 manifest 自身哈希循环。

## 基准与修复前

- [main](remote-main.json)、[R1.1](remote-r11.json)、[唯一根](owner.json)。
- [旧 Receipt](Receipt.py.before.txt)、[旧 Runtime 入口](Invoke-Runtime.ps1.before.txt)、[旧 Editor 入口](Invoke-ReviewEditor.ps1.before.txt)。
- [修复前8场景：6 guard FAIL/2控制PASS](Before/regressions.json)、[基线实际退出1](Before/run-exit.json)。各子目录保留旧分类报告，全部为合成工具夹具。

## 全部工具自测试

- [原50最终](Legacy50-Final/selftest.json)、[首轮50](Legacy50-First/selftest.json)。
- [R1.1的33最终](Legacy33-Final/selftest.json)、[首轮33](Legacy33-First/selftest.json)。
- [专项最终60](ProcessTests-Delivery/selftest.json)、[首轮57](ProcessTests-First/selftest.json)、[明确CLI期望后的57](ProcessTests-Final/selftest.json)。
- 必需负例：[无exit](ProcessTests-Delivery/no-exit-code-no-receipts/ApiReport/acceptance.json)、[无status](ProcessTests-Delivery/no-status-no-receipts/ApiReport/acceptance.json)、[均无](ProcessTests-Delivery/no-both-no-receipts/ApiReport/acceptance.json)、[非法status](ProcessTests-Delivery/illegal-status/ApiReport/acceptance.json)、[status/code矛盾](ProcessTests-Delivery/pass-nonzero-contradiction/ApiReport/acceptance.json)、[timeout=true/code0](ProcessTests-Delivery/timeout-zero/ApiReport/acceptance.json)。
- 禁止标量补缺：[exit字段](ProcessTests-Delivery/manual-zero-cannot-fill-exit-field/ApiReport/acceptance.json)、[status字段](ProcessTests-Delivery/manual-pass-cannot-fill-status-field/ApiReport/acceptance.json)、[timedOut字段](ProcessTests-Delivery/manual-false-cannot-fill-timeout-field/ApiReport/acceptance.json)。
- 每个专项案例包含 ApiReport/CliReport 的 JSON/CSV/Markdown、stdout/stderr、合成schema标记；summary 记录两种接口的独立预期和实际退出码。无进程实际执行，不能把schema夹具当Native结果。
- [旧来源/适配副本哈希](legacy-source-binding.json)、[38一致性](consistency.json)、[锁定审计](locked-contract.json)、[PS语法](powershell-syntax.json)、[工具冻结](tools-freeze.json)。

## 本轮真实 Editor/非开发 Player

- Editor：[实际命令](Editor/CP03Editor.Run.command.json)、[原生退出](Editor/CP03Editor.Run.exit.json)、[运行器原字节快照](Editor/process-results.json)、[快照来源](Editor/process-origin.json)、[原始断言](Editor/presentation.json)、[资格/来源SHA/整体](Editor/Semantic/acceptance.json)、[CSV](Editor/Semantic/assertions.csv)、[语义报告](Editor/Semantic/REPORT.md)、[根报告](Editor/REPORT.md)、[完整日志](Editor/Unity.log.gz)、[实际事件](Editor/events.jsonl.gz)。
- Runtime：[实际命令](Runtime/CP03Runtime.command.json)、[原生退出](Runtime/CP03Runtime.exit.json)、[运行器原字节快照](Runtime/process-results.json)、[快照来源](Runtime/process-origin.json)、[原始断言](Runtime/presentation.json)、[资格/来源SHA/整体](Runtime/Semantic/acceptance.json)、[CSV](Runtime/Semantic/assertions.csv)、[语义报告](Runtime/Semantic/REPORT.md)、[根报告](Runtime/REPORT.md)、[完整日志](Runtime/Player.log.gz)、[实际事件](Runtime/events.jsonl.gz)、[原样检查点复制](Runtime/fixture-copy.json)。
- [宿主退出](run-host-exits.json)与原生文件分开：实际进程0，分类/宿主2。无超时、无强杀；不是进程消失或发送关闭请求的推断。
- [真实退出证据8项读核](RealEvidenceChecks/results.json)：[实际2UR](RealEvidenceChecks/Runtime-actual-open/acceptance.json)必须BLOCKED/2；[真实退出证据+合成293PASS](RealEvidenceChecks/Runtime-actual-exit-synthetic-293-pass/acceptance.json)为工具正向PASS/0，不是游戏293PASS；[只有标量无文件](RealEvidenceChecks/Runtime-scalars-only-no-proof/acceptance.json)为INCOMPLETE/3。
- 新建 `reader-tool-synthetic-293-pass.json` 只作分类夹具，有 SYNTHETIC 标记。原始presentation/快照/原生退出三文件SHA前后相同。8读核不是8次新增Unity运行。
- [异常上下文](log-findings.json)原样归档，不以0声明干净引擎。

## 输入及保护

- [保护前](protected-before.json)、[保护后3476项](protected-after.json)、[原用户Git状态](main-status-before.txt)、[空产品diff](product-diff.txt)。
- [复制日志](project-copy.log.gz)、[复制退出](copy-exit.json)、[1147冻结输入及旧构建二进制SHA](input-binding.json)。
- [R1](../../DeliveryCombatPresentation03R1/Evidence/INDEX.md)、[R1.1](../../DeliveryCombatPresentation03R11/Evidence/INDEX.md)及CP03原证据不改。法杖/引擎未解决项仍开放；原生、人类、性能、新构建NOT_RUN。

## 最终发布验证

[Git/LFS 字节和链接验证](PUBLICATION_VERIFIED.json)在原 manifest 后独立生成。3100项发布字节与暂存Git直接blob/LFS内容一致；该回执和索引不覆盖原始manifest。
