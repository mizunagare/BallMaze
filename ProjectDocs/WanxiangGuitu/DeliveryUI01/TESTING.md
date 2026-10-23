# UI-01 本地复跑

Unity 6000.6.5f1；PowerShell 7。使用独立、新建绝对目录，禁止指向 LocalLow、真实玩家档或现有工作区；不要在结果根内放其他文件。先关闭对应项目 Editor。所有测试驱动放在隔离工程 Editor 目录；正式玩家包不含运行驱动。

```powershell
$src = 'D:/unity/WanxiangGuitu'
$test = 'C:/Users/guan/Documents/unitytest/UI01-Recheck'
& "$src/ProjectDocs/WanxiangGuitu/DeliveryUI01/Invoke-Rules.ps1" -SourceProject $src -WorkProject "$test/Project" -ArtifactsRoot "$test/Results" -HistoricalRegression -TimeoutSeconds 600
```

创建干净 Assets/Packages/ProjectSettings 副本，安装旧版回归与本批 Editor 测试、合成历史夹具及测试junction，运行30方法。汇总实际退出码、超时和启动错误到 results.json/csv，不按日志包含PASS就忽略进程失败。UI01Rules 使用受控NPC与虚拟键盘检查可见E/H和实际动作、过期目标、真实受伤取消、写盘故障、四武器图标/冷却、焦点、单实例及通知。历史B1测试保留断言，只在关包/出征后等待真实下一帧再调用E，符合关闭帧保护。

正常 AI 必须在**进程启动参数**提供隔离根；驱动先验证再Play，不可Play后改目录：

```powershell
& "$src/ProjectDocs/WanxiangGuitu/DeliveryUI01/Invoke-NormalAI.ps1" -SourceProject $src -IsolationRoot "$test/Normal" -Mode Normal
& "$src/ProjectDocs/WanxiangGuitu/DeliveryUI01/Invoke-NormalAI.ps1" -SourceProject $src -IsolationRoot "$test/Normal" -Mode Resume
& "$src/ProjectDocs/WanxiangGuitu/DeliveryUI01/Invoke-NormalAI.ps1" -SourceProject $src -IsolationRoot "$test/RejectMissing" -Mode RejectMissing
```

另用新目录运行 RejectRelative、RejectLocalLow。正常模式暂装原项目 Editor 驱动、结束清理；不会改战斗属性或冻结AI。每次核对 process-result、storage-audit 与实际断言/CSV，不能继承旧批PASS。合成哨兵不是玩家真实目录的访问监控。

受控截图使用已准备好的隔离 Project，结果根必须不存在：

```powershell
& "$src/ProjectDocs/WanxiangGuitu/DeliveryUI01/Invoke-Visual.ps1" -SourceProject $src -WorkProject "$test/Project" -IsolationRoot "$test/Screens" -Mode After
```

92张，720/1080完整21状态加高分辨率/超宽/缩放子矩阵；检查真实 Screen 大小、组可见、范围/重叠、截图落盘及实际帧推进。NPC关闭，保存故障仅作用于显式合成根。不要同时操作该Editor窗口。Before模式需要在3574审阅基线的独立副本执行，不可拿新版代码生成before；本次关键旧源码与基线LF归一比较一致。截图收据不代替人工视觉观察。

非开发构建使用现有 WanxiangBuild.ValidateBuild（隔离根环境与命令行参数同上）；产物 `Release/WanxiangGuitu.exe`。无运行驱动窗口测试应用 Computer Use 的 sky 原生输入，勿把直接修改修复标志或测试脚本按键算成无驱动试玩。启动参数必须有 `-wanxiang-storage-root <新隔离根>`；用 UI01PlayerFixture.Run 生成的**合成完整档**可供可重复启动，禁止复制真实玩家档。正常退出必须有退出码与应用退出审计，再启动核对同Profile/Run/区域/物品，而不是强制终止后宣称正常退出。

本次这一步受Snipaste全局F1拦截影响，只有真实启动/HUD画面，完整U16为NOT_RUN；没有关闭或修改用户Snipaste配置来绕过。正常AI有驱动的新进程恢复PASS不能替代U16。人工试玩NOT_RUN。

本轮结果与失败历史见 [REPORT](REPORT.md) 和 [证据索引](Evidence/INDEX.md)。不添加CI，不升级依赖。
