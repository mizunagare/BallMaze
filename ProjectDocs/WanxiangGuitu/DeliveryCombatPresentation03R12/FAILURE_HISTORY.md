# 保留的失败与尝试

- [修复前8场景](Evidence/Before/regressions.json)：6 个 guard FAIL，2 个旧正确拒绝对照。API缺exit、缺status、均缺和CLI缺status错误 PASS；非法状态/矛盾的旧 FAIL 不能当有效失败证据。[基线退出1](Evidence/Before/run-exit.json)保留。
- 本轮旧50、新33初轮及最终均独立通过，原源码不修改；使用适配副本只提供显式合成进程schema，不删除旧断言。
- [首轮57](Evidence/ProcessTests-First/selftest.json)、[明确CLI/API期望后的57](Evidence/ProcessTests-Final/selftest.json)、[最终60](Evidence/ProcessTests-Delivery/selftest.json)均保留。API字符串 timed_out 无对应布尔CLI语法，其CLI调用是明确的有效无标量控制，最终记录独立期望；不是把负例CLI成功隐藏。补充三项标量不能补文件字段后60全部通过，未降低产品预期。
- [真实来源8读核](Evidence/RealEvidenceChecks/results.json)中的293 PASS是新建、显式标记工具副本。没有改真实 presentation.json 或原两个进程文件；实际游戏仍291/2。
- 真实进程0、分类/宿主2是开放项阻断，不记整体PASS。日志异常上下文 [索引](Evidence/log-findings.json)保留，不以进程0证明引擎干净。
- 原 CP03/R1/R1.1 所有失败、源码快照、原JSON、日志和输入保持不变，[3,476项保护](Evidence/protected-after.json)。
- 法杖近距两项、UNKNOWN/C15/青色帧/Search/JobTempAlloc 根因保持 UNRESOLVED。原生U16、人工、性能 NOT_RUN；不执行无新线索关闭实验。
