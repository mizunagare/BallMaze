# B3 本地复跑

Unity6000.6.5f1 / URP17.6.0 / Input System1.20.0 / uGUI2.6.0 保持原版本；不启用 CI。必须使用工程外唯一测试根，禁止真实存档。

```powershell
& '<工程>/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1' `
 -SourceProject '<工程绝对路径>' -TestRoot '<全新工程外测试父目录>' -GameplayOnly
```

可选 ShaderCacheSource 仅复用闲置同版本隔离工程 ShaderCache，不复用程序集、保存结果或玩家档；本轮不是全新 shader 编译声明。沿用原编排器的超时诊断、不强杀、失败传播、隔离启动和结果格式，不新建框架。

默认选定方法增加 B3StreamRules.Run、B3Checks.Run、B3Checks.Resume；前一进程失败则依赖 Resume 不运行。B2/B1/A1、装备、容器、双武器、工作台、分页、旧档和UI规则继续选定。正常AI使用新增 -B3 驱动，保留 -B2/旧驱动；正常AI在最终保存和新进程恢复时核对随机状态。规则可禁用NPC，正常AI不冻结敌人；两者不算原生UI/人工理解。编排仍会运行非开发构建和92帧受控UI布局矩阵。

- B3StreamRules：固定种子/30个不同种子、地图合法差异、奖励/布点/事件/全局隔离、异常回滚全局状态、空状态旧语义、损坏/未知状态拒绝。
- B3Checks：真实装备和宝箱材料序列、全局噪声+独立地图生成、查询前后完整Run及全局状态、序列结果比较、实际遗迹开箱/重复拒绝/落地装备ID、旧v9无启用标志、写盘故障和新进程恢复。
- B2Rules：遗迹roll=1必出，其他地点概率边界、五地点实际落地、敌人重复掉落、目标和来源账。
- WGB1Check/Resume：收费原子性、修复回执、新进程。

GameplayOnly不重跑关闭异常矩阵或ProcDump，UNKNOWN仍UNRESOLVED，原生U16/人工理解仍NOT_RUN。两个预期故障探针保留FAIL，不视为业务通过；其他失败使入口exit1。未选的完整历史矩阵NOT_RUN，不继承旧PASS。

## 修复前重现

Evidence/Before 对应开始提交的产品代码，仅新增B3Checks和测试入口。它在从同一保存状态恢复、插入500次Unity全局抽样后，24次真实装备/材料序列不一致，断言GLOBAL_NOISE_COUPLED_REWARDS，exit1。若重现，使用固定基线的全新隔离副本并只加入该轮记录的测试源；不可reset当前工程或修改真实档。

## 发布

`python -B DeliveryB3/Publish-Evidence.py --run <完成的唯一运行根> --target <新的证据目录>` 复用B2及UI01白名单脱敏器，额外复制B3断言和合成随机状态。拒绝覆盖历史目录。不发布save、分页载荷、构建二进制、转储、Library或Temp。原始日志保留本机，发布版转换前后哈希随manifest记录。
