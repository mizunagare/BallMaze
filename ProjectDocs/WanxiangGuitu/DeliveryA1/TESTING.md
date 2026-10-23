# A1 定向复跑

使用PowerShell 7、Unity 6000.6.5f1与Windows构建模块，不升级依赖。

```powershell
& 'D:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryA1/Invoke-A1.ps1' `
  -SourceProject 'D:/unity/WanxiangGuitu' `
  -WorkProject 'C:/UnityValidation/A1NewProject' `
  -ArtifactsRoot 'C:/UnityValidation/A1NewResults'
```

必须为全新工程外目录；禁止玩家LocalLow。脚本复用既有19方法和三个受控进程，再安装A1检查：Isolation/Choice/Empty/Recovery与Extended.Matrix。Matrix覆盖v8/v9营地、在途、Pending、Committed，含页面引用、重复选择、陈旧UI指纹、发布后中断；检查游戏文件字节不变和隔离junction哨兵。只创建本地测试junction，不指向真实用户数据。

正常AI须另用Invoke-NormalAI.ps1运行Normal和Resume，参数/完整命令见 ../DeliveryA/TESTING.md。负例Mode使用新的隔离日志根。不要直接执行省略启动参数的旧命令。所有首次初始化、读写与退出路径记录于storage-audit.jsonl；它是应用存档入口审计，不是内核级全进程文件监控。真实玩家目录不参与故障注入。

Red结果由审阅基线副本执行最初四项回归得到；保留原源码SHA/失败断言。Green/Final是本轮实际运行，不能从历史PASS推断。规则、受控Player、正常AI、人工试玩分别报告；人工试玩NOT_RUN。
