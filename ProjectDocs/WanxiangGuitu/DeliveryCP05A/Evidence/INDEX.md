# CP05-A 证据索引

- [源码审计](source-audit.json)：main72db，精确路径/SHA及关键调用行；AdventureProjectile定义于AdventureCombat.cs中，不是独立文件。
- [历史原始空间记录](historical-aim-diagnosis.jsonl)及[解释/源SHA](spatial-analysis.json)：来自既有CP04-A历史受控Editor记录，未经改写。原非ASCII名字存在编码损坏，未擅自修复。
- [CP04-B独立参考](cp04b-reference.json)：不合入本设计分支，也不声称main已有该修复。
- [保护文件前快照](protected-before.json)、[最终保护结果](protection.json)：无产品改动。
- [空间示意](spatial-topdown.svg)：历史数值的XZ投影，仅解释几何，不是Unity截图/新碰撞验证。

本轮没有启动Unity、创建原型、运行Player、物理输入或人工试玩。所有设计参数和未来矩阵均未验证。一次只读检索命令误用了PowerShell不支持的花括号文件列表，解析失败后用明确路径重跑；没有产品修改或丢失测试结果。
