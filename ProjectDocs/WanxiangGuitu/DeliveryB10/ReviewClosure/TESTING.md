# 本轮只读审计复跑

沿用本地工具，不启动第二套业务测试框架。Python只读工程/已发布证据，**不访问玩家存档或启动游戏**。PowerShell环境脚本复用UI01现有实现。

```powershell
$auditRoot = 'D:/WanxiangValidationRuns/B10ReviewClosure/自选全新目录'
python -B ProjectDocs/WanxiangGuitu/DeliveryB10/ReviewClosure/Audit.py `
  --project D:/unity/WanxiangGuitu --output "$auditRoot/Audit"
& ./ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Inspect-InteractiveEnvironment.ps1 `
  -OutputDirectory "$auditRoot/Environment"
```

输出必须新建且不在工程内，拒绝LocalLow；环境发现不构成原生输入验收。exit0仅表示当前源码/证据合同断言满足，绝非游戏运行全部通过。Audit.py把上轮运行数据标为historical且所有runtime分层均NOT_RUN。

若用户之后主动修改两份保护文件导致基线SHA不同，保留用户新内容，重新记录获准基线，不为让审计通过而还原文件。若后续产品有已批准变动，不把与6cad的差异自动认定为产品缺陷，应按新固定SHA重新审计与运行受影响回归。

本轮实际根`D:/WanxiangValidationRuns/B10ReviewClosure/20261026-234056-137e8c52`。Before为文档更正前exit1，After相同脚本更正后exit0。Evidence中保留原始JSON字节与退出回执，没有旧游戏运行结果冒充新测试。

规则、正常AI、发行构建/新进程继续仍复用上级[TESTING.md](../TESTING.md)的隔离命令；本轮没修改游戏因此未再跑All。获得明确产品缺陷再选择受影响测试，不为了凑数无差别重跑或重做UNKNOWN实验。新阶段实验矩阵不是当前执行命令。
