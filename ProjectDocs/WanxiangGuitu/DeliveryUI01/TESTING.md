## 当前原生测试阻塞与只读复跑

先执行 [Automation/README.md 的只读环境检查](Automation/README.md#独立交互环境只读检查)。它不登录、不切桌面、不启动游戏、不访问存档；成功仅说明发现步骤完成。没有已授权独占会话时立即将原生 U16 NOT_RUN，不退回用户桌面，不要求用户手动配合。最新结果见 [环境边界报告](ENVIRONMENT_BOUNDARY_REPORT.md)；本轮没有重新执行 All 或关闭实验。

## 当前无人值守入口

使用 [Automation/README.md](Automation/README.md) 的单命令入口，无需逐项点击或人工确认。规则、正常AI、受控UI与正式Player后台关闭/恢复分开报告；独立私有桌面不抢用户焦点，原生语义无法验证时 NOT_RUN。超时保留诊断与进程，不强杀冒充正常退出。全量历史回归用 -FullRegression，关闭矩阵可 -Phase PlayerMatrix 复用成功合成构建。

本次实际结果与失败策略见 [无人值守报告](UNATTENDED_REPORT.md)。下列分项命令为既有人工/单项流程，不再作为每批必须用户逐个操作的入口。

# UI-01 本地复跑

## 正式Player关闭诊断与原生收尾

本轮没有产品改动，复用原BuildOptions.None包并重新核对exe、Assembly-CSharp、UnityPlayer、Mono及源码资源哈希。不要为了得到新时间戳重复构建并声称复测。原30项/92帧结果保留，未重新运行的领域项目注明旧轮。

在独立工程Editor测试目录安装 `Tests/U16Fixture.cs.txt` 为 `U16Fixture.cs`（不要放入正式运行时目录）。启动Unity进程前同时设置 `UNITY_TEST_ROOT` 和 `-wanxiang-storage-root` 为新绝对隔离根，再 `-executeMethod U16Fixture.Run`。该夹具只在Editor准备合法空遭遇森林、带入木2石1并保存到渡口旁，写入SYNTHETIC标记；不构成正常AI验证，不在Player中执行动作。完整夹具目录仅留本机，禁止提交完整玩家档。

```powershell
$src = 'D:/unity/WanxiangGuitu'
$test = 'C:/Users/guan/Documents/unitytest/UI01-Close-Recheck'
$player = 'C:/Users/guan/Documents/unitytest/WanxiangUI01/FinalCurrent/Release/WanxiangGuitu.exe'
& "$src/ProjectDocs/WanxiangGuitu/DeliveryUI01/Invoke-PlayerClose.ps1" -PlayerExe $player -SyntheticFixtureRoot "$test/Fixture" -IsolationRoot "$test/NativeDefault" -Renderer Default
```

使用可见游戏按钮，不发送F1、不修改Snipaste。人工/Computer Use原生操作与受控脚本分别记录；不要用物理Esc作为自动化停止/取消/退出。用标题栏×正常关闭；启动器持有进程句柄，记录实际退出码与超时；超时不强杀，仍不能标正常退出PASS。请求操作者点击关闭的时间与应用实际quit审计时间分开，不伪造精确点击时间。

使用 `-Renderer D3D11` 是独立对照，不是修改产品默认设置，也不是已经确认的根因修复。每轮新根/相同初始夹具，只变一个因素。附加ProcDump的运行单列，不能与未附加运行当成严格单变量对照。便携ProcDump仅用于本次隔离进程，不用-i/-k，不上传完整内存转储。

```powershell
python "$src/ProjectDocs/WanxiangGuitu/DeliveryUI01/Tests/analyze-player-close.py" --root "$test/NativeDefault" --process process-<stamp>.json --log player-<stamp>.log --since <launch-startUtc> --before "$test/NativeDefault/before-<stamp>.json" --save "$test/NativeDefault/after-<stamp>.json" --output "$test/NativeDefault/analysis.json"
```

Python使用本机可用运行时；尖括号替换为实际文件名，不作为字面命令。exit0仍可能分析失败：出现UNKNOWN/Native Crash Reporting、无退出审计、封装校验失败或修订未递增都不能PASS。原生日志有空栈时写UNRESOLVED，不套用Editor异常或官方相似Issue作为根因。

继续同局用启动器 `-Resume` 与同一IsolationRoot，启动后保存恢复快照，分析器 `--previous <上次退出快照> --current <新进程恢复快照>` 比较身份、种子、回执、物品ID、库存和来源账。快照只读、完整文件留隔离根；提交校验哈希/修订与摘要，不提交完整存档。恢复比较应在新的原生操作前取样，避免把正常玩家消耗当成恢复错误。

窗口工具返回外部停止信号时停止该次窗口操作，记录停在哪一步；本轮已发生，未完成原生步骤保留NOT_RUN。原生协助操作不等于未参与人员的无提示可理解性试玩。最终状态见 [ACCEPTANCE](ACCEPTANCE.md)。

## 已有受控/正常AI复跑

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
