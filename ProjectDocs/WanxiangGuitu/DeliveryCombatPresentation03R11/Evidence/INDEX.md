# CP03-R1.1 证据索引

唯一新根 `I:/WGCombat/CP03-R1-1031-B`。794 个工件的原始/发布 SHA、大小及凭据遮盖说明见 [manifest](manifest.json)。仅合成数据；P/Project、缓存和二进制不发布。原始日志保留 I 根，公开 gzip 只遮盖凭据值，异常/栈/顺序保留。Git/LFS 内容分别核对，不能把 LFS 指针当日志字节。

## 基准与修复前

- [main API](remote-main-api.json)、[R1 ref API](remote-r1-api.json)、[唯一根](owner.json)。
- [旧 Receipt.py 原文](Receipt.py.before.txt)、[旧 Runtime 入口](Invoke-Runtime.ps1.before.txt)、[旧 Editor 入口](Invoke-ReviewEditor.ps1.before.txt)、[旧自测](SelfTest-R1.py.before.txt)。
- [5 项 guard FAIL](Before/regressions.json)、[基线退出1](Before/run-exit.json)。各 Before 子目录含原输入、被篡改合同、旧工具输出/命令结果；它们是合成工具负例，不是 Unity 执行。
- [网络首次摘要](remote-attempt1.txt)、[重试摘要](remote-attempt2.txt)、[API 路径错误记录](remote-api-url-attempt.txt)、[实现编排语法错误](implementation-attempt1.txt)、[文档编排语法错误](documentation-attempt1.txt)。

## 全部工具测试

- [旧 50 项最终](LegacySelfTestFinal/selftest.json)、[初轮](LegacySelfTest1/selftest.json)。
- [新 33 项最终](BindingSelfTestFinal/selftest.json)、[初轮](BindingSelfTest1/selftest.json)。
- 代表负例：[省合同](BindingSelfTestFinal/contract-omitted/Report/acceptance.json)、[省角色](BindingSelfTestFinal/profile-omitted/Report/acceptance.json)、[Runtime 合同给 Editor](BindingSelfTestFinal/runtime-contract-used-for-editor/Report/acceptance.json)、[Editor 合同给 Runtime](BindingSelfTestFinal/editor-contract-used-for-runtime/Report/acceptance.json)、[回执错 layer](BindingSelfTestFinal/editor-receipt-layer/Report/acceptance.json)、[回执错 scope](BindingSelfTestFinal/runtime-receipt-scope/Report/acceptance.json)、[合同追加字节](BindingSelfTestFinal/editor-contract-whitespace/Report/acceptance.json)、[配套改名](BindingSelfTestFinal/self-consistent-receipt-contract-name-tamper/Report/acceptance.json)、[配套减项](BindingSelfTestFinal/self-consistent-runtime-row-removal/Report/acceptance.json)。
- 每个 CLI 案例含 stdout/stderr、command/实际退出码、原夹具、JSON/CSV/Markdown。正向 293 PASS 是合成分类器夹具，不能当游戏通过。
- [最终 35 项一致性](consistency-final.json)、[初轮 33 项](consistency.json)、[原锁定审计](locked-contract.json)、[PS 语法](powershell-syntax.json)、[工具字节冻结](tools-freeze.json)。

## 新真实 Editor / 非开发 Player

- Editor：[命令](Editor/CP03Editor.Run.command.json)、[真实退出](Editor/CP03Editor.Run.exit.json)、[原始断言](Editor/presentation.json)、[原进程结果](Editor/results.json)、[绑定/整体](Editor/Semantic/acceptance.json)、[CSV](Editor/Semantic/assertions.csv)、[语义报告](Editor/Semantic/REPORT.md)、[根报告](Editor/REPORT.md)、[完整日志](Editor/Unity.log.gz)、[实际事件](Editor/events.jsonl.gz)。
- Runtime：[命令](Runtime/CP03Runtime.command.json)、[真实退出](Runtime/CP03Runtime.exit.json)、[原始断言](Runtime/presentation.json)、[进程/语义行](Runtime/results.json)、[绑定/整体](Runtime/Semantic/acceptance.json)、[CSV](Runtime/Semantic/assertions.csv)、[语义报告](Runtime/Semantic/REPORT.md)、[根报告](Runtime/REPORT.md)、[完整日志](Runtime/Player.log.gz)、[实际事件](Runtime/events.jsonl.gz)、[原样检查点复制](Runtime/fixture-copy.json)。
- [宿主退出观测](run-host-exits.json)与原生进程回执分开：进程均0、宿主/分类均2、无超时或强杀。两项旧法杖 UR 保留，整体 BLOCKED。
- [新真实回执误用](RealCrossContext/results.json)：Editor-as-Runtime、Runtime-as-Editor、Runtime 省合同三项均 INCOMPLETE/3，源 SHA 不变。是只读重审，不是三次新增游戏运行。
- [异常上下文](log-findings.json)保留，不以进程0认定干净引擎。

## 合同与保护

- 新冻结 [来源](../Contracts/PROVENANCE.json)、[Editor 原字节](../Contracts/Editor.json)、[Runtime 原字节](../Contracts/Runtime.json)。
- [保护前](protected-before.json)、[保护后](protected-after.json)、[用户 Git 状态](main-status-before.txt)、[空产品 diff](product-diff.txt)。
- [复制日志](project-copy.log.gz)、[复制退出](copy-exit.json)、[1,147 输入和旧非开发构建哈希](input-binding.json)。
- 不修改 [旧 R1 证据](../../DeliveryCombatPresentation03R1/Evidence/INDEX.md) 或 CP03 证据。原生 UI、人工、性能、新构建继续 NOT_RUN，历史引擎和两项法杖继续 UNRESOLVED。

## 最终发布门槛

[794 项 Git/LFS 字节与链接核对](PUBLICATION_VERIFIED.json)、[两个合同暂存 Git 原字节核对](FROZEN_CONTRACT_VERIFIED.json)在 manifest 之后生成，独立保存，不覆盖原始记录。原 794 项 manifest 不含索引和这两份最后核验回执。
