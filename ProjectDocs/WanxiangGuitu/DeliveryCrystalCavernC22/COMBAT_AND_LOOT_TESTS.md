# 战斗与物资复跑

工具位于 [Tools](Tools/)。使用 Unity 6000.6.5f1、Windows64、隔离根 `I:/WGCombat/C22-1106-A`。工具依赖本机 DeliveryUI01 的私有桌面启动器和 NativeProbe。保留首次失败及实际进程回执，每次运行必须创建新的子目录。验证工程仅包含来自固定输入的 Assets、Packages 和 ProjectSettings。不得在用户工程内放置驱动。

1. 把对应版本复制到隔离 `Project` 和 `EditorProject`。需要重制地图资源时，在 Project 上调用 `Invoke-Editor.ps1 -Method CrystalCavernAuthoring.BakeExpanded -Quit`。
2. 在无驱动的 Project 调用 `Invoke-Editor.ps1 -Method WanxiangBuild.ValidateBuild -Output I:/WGCombat/C22-1106-A/PureBuild2`。对纯包调用 `Audit-Release.ps1` 和 `Invoke-Pure.ps1`。后者只使用合成存档，验证标题出现和受控后台关闭。
3. Editor 专用副本中把 `Driver.cs.txt` 复制为 `Assets/C22ValidationDriver.cs`。调用 `Invoke-Editor.ps1 -ValidationCopy -NonBatch -Method CavernValidationEditor.Begin -Output <新的路径> -Mode <模式>`。
4. 调用 `Prepare-Player.ps1 -Observation C22DriverRetry7`，在纯包的独立副本安装观测程序集。随后 `Invoke-Player.ps1 -Output <新的路径> -Mode <模式>`。正式构建输入和纯包都没有驱动。C2.1 对照可用 `-Legacy` 生成旧版独立观测副本。
5. 新进程测试使用 `-Seed <上一轮隔离目录>`，逐文件核对 SHA 后才使用复制品。恢复模式不从真实玩家存档初始化。

| 模式 | 观察点 |
| --- | --- |
| live | 七武器 × 普攻、默认技能。记录目标 ID、武器实际几何或投射物轨迹、接触与生命事件。目标为活体，受控固定姿态，AI 行为由另一个测试覆盖。 |
| materials → material-resume → warehouse | 两类矿脉耗尽、真实掉落和拾取、新进程恢复、免费出口、结算回执、重复提交、入仓、新进程核对与重复确认。 |
| hazard | 恢复/预警阶段进入不掉血，实测翻滚无敌帧拒绝放电。 |
| chamber → chamber-resume | 关闭时实体门与无路径，打开时双向 NavMesh、玩家实际通行、普通掉落、已开机关与宝箱恢复。 |
| elite → elite-resume | 实际受击与暴露前后伤害、暂停、规避、正常击杀、重复死亡处理和新进程恢复。 |
| combo | 侧道实际移动、危险与精英窗口协调、实际敌人导航。 |
| legacy-cavern / forest / ruins | 固定旧洞窟合成存档，以及森林、遗迹入口与保存。 |

每个运行目录保存断言、原始日志、启动与退出回执。证据采集工具只读验证输出。控制器 API、Editor 和非开发 Player 分层记录。
