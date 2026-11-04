# 原始失败与尝试

所有旧分支/旧CP05报告未修改。新增证据是独立目录，原始运行根 `I:/WGCombat/CP05C-1104-A` 不覆盖。

| 尝试 | 真实结果 | 原因/后续 |
|---|---|---|
| BeforeTraining | 11 PASS/9 FAIL，exit1 | 基准真实Sword死亡空引用、重开重名、上下文缺失、Unity RNG耦合；原始失败保留 |
| BeforePlayer | 11 PASS/9 FAIL，exit1 | 非开发Player独立复现同类缺陷 |
| source-audit-before-after | FAIL | Git源含UTF8 BOM，读盘已剥BOM造成前缀假差异；统一解码，仍逐字全文比较，无宽泛白名单 |
| 首次复制工具 | FileNotFoundError | Editor目标目录少了CombatPrototype；未覆盖数据；随后用正确路径重新复制。原控制台错误记录于tool-failures.json |
| AfterTraining1 | 编译失败，实际exit1 | Unity SceneHandle隐式int CS0619；私有registry改用Scene键。精确自有SafeMode Quit收尾，未强杀；第一次普通close未找到主窗口也保留NOT_RUN |
| AfterTraining2 | 90 PASS/2 FAIL，exit1 | 第二敌被前一个夹具禁用，没有Update处理；修复夹具仅重新启用真实目标，不删除唯一性断言 |
| AfterTraining3 | 90 PASS/2 FAIL，exit1 | canary文本CRLF/LF不一致；实际原始存档哈希完全相同，只规范ledger换行，未修改存档 |
| AfterTraining4 | 92 PASS，exit0 | 从原始合成检查点重新复制，全部新鲜运行 |
| AfterFormal | 43 PASS，exit0 | 同真实Run继续、480规则、真实剑死亡配对 |
| AfterPlayer/AfterPlayerFormal | 92/43 PASS，均exit0 | 独立非开发Player实际执行 |
| PureBuild/PureSmoke | 成功/exit0 | 纯包独立构建及普通关闭；退出JobTempAlloc日志仍UNRESOLVED |

[工具失败](Evidence/tool-failures.json)、[首次源审计失败](Evidence/source-audit-before-after.json)、各尝试独立probe/Unity日志/进程回执均在[索引](Evidence/INDEX.md)。历史法杖、黑帧、C15等旧证据未覆盖或重新定性。发布副本仅压缩/脱敏日志，sourceSHA及发布SHA分别保留。

文档链接检查初次FAIL：索引链接把“0项”误放进URL，改正后全部本地链接存在。该工具失败不涉及产品或运行结果。
