# 失败与开放项

1. 固定 R1 的 5 个负例：无合同、回执错 layer、错 scope、合同追加字节、合同跨 layer，均错误 PASS/exit0。保留 [guard FAIL](Evidence/Before/regressions.json)、[真实基线退出](Evidence/Before/run-exit.json)。全部为合成工具夹具，未伪称 Unity 结果。
2. 本机两次 Git 读取失败：curl 28 和连接重置。首次发现脚本后续读文件使 shell exit0，不代表读取成功。[记录 1](Evidence/remote-attempt1.txt)、[记录 2](Evidence/remote-attempt2.txt)。改用 GitHub GET 成功；编码分支 URL 曾 400，[记录](Evidence/remote-api-url-attempt.txt)保留。未改网络/凭据配置。
3. 首次实现和首次文档调用各有 JS 字符串语法错误，命令执行前失败，无文件写入。[实现记录](Evidence/implementation-attempt1.txt)、[文档记录](Evidence/documentation-attempt1.txt)。修正编排引号后实施，不归为产品失败。
4. 初轮和最终旧 50 /新 33 项均独立保留。真实 Editor/Runtime 进程 exit0，分类/宿主 exit2 是保留两项 UR 的正确状态，不将其伪装为整体通过。
5. 本轮真实回执跨角色和无合同的 3 项只读负例均 INCOMPLETE/3，[原 SHA 不变](Evidence/RealCrossContext/results.json)。
6. 原 CP03/R1 的 JSON、失败、日志和输入全部保留，[2664 文件复核](Evidence/protected-after.json)。不将旧结果改写为本轮结果。
7. 法杖两项、UNKNOWN/C15/青色帧/Search/JobTempAlloc 仍 UNRESOLVED。原生 U16、人工体验、性能 NOT_RUN。不修改 CombatAim，不重复无新线索关闭实验。

本轮日志异常见 [完整索引](Evidence/log-findings.json)。公开日志只遮盖凭据值，异常/栈不删除；原日志留新隔离根，manifest 记录原/发布 SHA。没有以编排器 exit0 覆盖前置失败。
