# CP03-R1 原始证据索引

新合成根 `I:/WGCombat/CP03-R1-1031-A`；本目录仅发布该根的合成结果和工具负例。完整项目/Library/可执行文件没有入库。746 个发布工件见 [manifest](manifest.json)，其中每项列出原始与发布 SHA256。日志、stdout/stderr、jsonl 用 gzip 保存；公开日志仅凭据值遮盖，异常/调用栈/顺序不删，原始完整字节留在原 I 根。索引在发布后生成，不参与 manifest 自身哈希循环。

## 修复前与工具验证

- [旧 Invoke-Runtime](Invoke-Runtime.ps1.before.txt)、[旧 Audit-Locked](Audit-Locked.py.before.txt)、[旧分类谓词复现](before-classification.json)。
- [旧 Runtime2 只读重审](HistoricalReaudit/acceptance.json)：原文件未改，BLOCKED/2。
- [最终 50 项](PostStyle/SelfTest/selftest.json)，[CLI 全通过用例](PostStyle/SelfTest/all-pass/Report/acceptance.json)、[混合失败](PostStyle/SelfTest/mixed/Report/acceptance.json)、[开放项](PostStyle/SelfTest/pass-unresolved/Report/acceptance.json)、[缺文件](PostStyle/SelfTest/missing/Report/acceptance.json)、[坏 JSON](PostStyle/SelfTest/bad-json/Report/acceptance.json)、[空结果](PostStyle/SelfTest/empty/Report/acceptance.json)、[未知状态](PostStyle/SelfTest/unknown/Report/acceptance.json)、[重复名称](PostStyle/SelfTest/duplicate/Report/acceptance.json)。各目录含 stdout/stderr、CSV 和 Markdown。
- [旧审计错误放行](PostStyle/SelfTest/old-audit-bypass.txt)、[新审计 CLI 拒绝](PostStyle/SelfTest/negative-audit-cli.json)。old-bypass 下的 Assets 只是审计文本夹具，未进入 Unity 项目。
- [SelfTest1 首错](SelfTest1/tool-failure.txt)、[SelfTest2 首错](SelfTest2/tool-failure.txt)、[首次审计失败](locked-contract-r1.json)、[SelfTest3](SelfTest3/selftest.json)、[49 项版本](SelfTestFinal/selftest.json)、[50 项版本](SelfTestFinal2/selftest.json)均独立保留。
- [最终严格审计](locked-contract-delivery.json)、[PowerShell 解析](powershell-syntax.json)、[20 项报告一致性](result-summary.json)、[最终工具哈希](final-tools.json)。

## 本轮真实 Editor 与非开发 Player

- EditorFinal：[原命令](EditorFinal/CP03Editor.Run.command.json)、[真实退出](EditorFinal/CP03Editor.Run.exit.json)、[原进程结果](EditorFinal/results.json)、[原断言](EditorFinal/presentation.json)、[语义 JSON](EditorFinal/Semantic/acceptance.json)、[语义 Markdown](EditorFinal/Semantic/REPORT.md)、[根报告](EditorFinal/REPORT.md)、[完整日志](EditorFinal/Unity.log.gz)、[实际事件](EditorFinal/events.jsonl.gz)、[逐帧动作](EditorFinal/timeline.csv)。
- RuntimeFinal：[原命令](RuntimeFinal/CP03Runtime.command.json)、[真实退出](RuntimeFinal/CP03Runtime.exit.json)、[进程/语义行](RuntimeFinal/results.json)、[原断言](RuntimeFinal/presentation.json)、[语义 JSON](RuntimeFinal/Semantic/acceptance.json)、[语义 Markdown](RuntimeFinal/Semantic/REPORT.md)、[根报告](RuntimeFinal/REPORT.md)、[完整日志](RuntimeFinal/Player.log.gz)、[实际事件](RuntimeFinal/events.jsonl.gz)、[检查点原样复制](RuntimeFinal/fixture-copy.json)。
- [最初 Editor](Editor/Semantic/acceptance.json)、[最初 Runtime](Runtime/Semantic/acceptance.json)不被最终运行覆盖。
- [外层宿主观测记录](host-results-final.json)单列，非 Player 退出证明；进程必须查各 *.exit.json。Runtime 首次宿主1与分类器2差异保留，最终显式传播2。
- [日志异常与栈](log-findings.json)，含 Editor.Search 内部异常；不据进程0推断引擎干净。

## 法杖只读调查

- [EditorDiagnosis 原断言](EditorDiagnosis/presentation.json)、[真实退出](EditorDiagnosis/CP03Editor.Run.exit.json)、[语义回执](EditorDiagnosis/Semantic/acceptance.json)。
- [相机/枪口/Collider 三维原始数据](EditorDiagnosis/aim-diagnosis.jsonl.gz)、[Spawn/Flight/Damage 全事件](EditorDiagnosis/events.jsonl.gz)、[只读提取](aim-analysis.json)、[实际执行观测驱动](EditorDiagnosis/CP03Cases.executed.cs.txt)、[完整日志](EditorDiagnosis/Unity.log.gz)。

## 输入、硬件、保护

- [唯一根](owner.json)、[复制日志](project-copy.log.gz)、[初始工作树输入和 PE 哈希](input-binding.json)、[Git 原字节比较](input-binding-with-git.json)、[指针/换行差异保留](product-canonical-binding.json)、[工作树规范化](worktree-canonical-binding.json)、[5 设置来源](settings-provenance.json)、[最终 1,147 个冻结产品输入](frozen-build-product-binding.json)。
- [保护前](protected-before.json)、[保护后 1,802 项](protected-after.json)、[原用户 Git 状态](git-before.txt)、[空产品 diff](product-diff.txt)、[main 开工后复核](remote-main-precommit.txt)。
- [CPU](hardware-cpu.json)、[GPU 枚举](hardware-gpu.json)不是性能计时；全部 Profiler 指标 NOT_RUN。
- [绑定脚本首错](binding-attempt1.txt)、[编码首错](metadata-attempt1.txt)、[diff 首错](diffcheck-before.txt)、[diff 最终](diffcheck-final.txt)。

[历史 CP03 证据](../../DeliveryCombatPresentation03/Evidence/INDEX.md)未覆盖。受控 Editor/非开发验收 Player 不等于原生键鼠、正常 AI 或独立人工试玩；没有新构建/Profiler/完整平衡通过声明。

## 提交前字节核验补充

最后只移除新增工具/观测文本的 EOF 空行，重新自测 [50 PASS](PostStyle/SelfTest/selftest.json)；早期 SelfTestDelivery 原样保留。补充发布 [manifest](PostStyle/manifest.json)、[最终工具哈希](PostStyle/final-tools.json)、[首次提交中止记录](PostStyle/stage-attempt1.txt)。本目录 `.gitattributes` 保留 Evidence 原字节，避免 Git 自动换行转换改变 JSON/CSV SHA。原 746 项 manifest 不覆盖，PostStyle 用独立 manifest。

最终提交前 [字节/LFS/链接核验](DELIVERY_VERIFICATION.json)在原两份 manifest 之后生成；不是对旧 manifest 的覆盖。gzip 保留仓库既有 LFS 机制，校验 resolved 内容而非指针文本。
