# B1 本地复跑

PowerShell 7、Unity 6000.6.5f1。所有目录均为显式隔离测试目录，禁止指向玩家存档或 LocalLow。新测试必须使用不存在的目录。保留失败日志，不用最后一次成功覆盖历史失败。

## 隔离副本规则、通行、历史回归及正式构建

```powershell
& './ProjectDocs/WanxiangGuitu/DeliveryB1/Invoke-Rules.ps1' `
 -SourceProject 'D:/unity/WanxiangGuitu' `
 -WorkProject 'C:/UnityValidation/B1Project' `
 -ArtifactsRoot 'C:/UnityValidation/B1Rules' -HistoricalRegression
```

安装的检查位于副本 Editor 目录，不进入 Player。WGB1Check.Run/Resume 是两个进程；来源账/失败注入/传送及冻结 NPC 属于受控规则检查，不能冒充正常 AI。WGB1Routes 使用 CharacterController 碰撞探针、指定种子1～10，检查兴趣点、普通/条件出口互动位置、出生点及三类资源候选；NPC 为探针禁用。历史 WGRoutesCheck 的1～20种子另列。

## 发布后进程中断

在上述副本关闭后运行：

```powershell
& './ProjectDocs/WanxiangGuitu/DeliveryB1/Invoke-PublishCrash.ps1' `
 -WorkProject 'C:/UnityValidation/B1Project' `
 -ArtifactsRoot 'C:/UnityValidation/B1Crash'
```

仅测试驱动在 File.Replace 之后、Published/调用方确认之前，以 TerminateProcess 终止自己的隔离 Unity 进程，预期退出29且必须存在注入意图记录；不是正常退出。第二进程必须退出0、核对同一 Run/区域/回执/库存/来源账且重复修复不扣费。它不测试真实断电或物理磁盘损坏。

## 原工程正常 AI（先关闭该工程 Editor）

```powershell
& './ProjectDocs/WanxiangGuitu/DeliveryB1/Invoke-NormalAI.ps1' `
 -SourceProject 'D:/unity/WanxiangGuitu' `
 -IsolationRoot 'C:/UnityValidation/B1Normal' -Mode Normal
& './ProjectDocs/WanxiangGuitu/DeliveryB1/Invoke-NormalAI.ps1' `
 -SourceProject 'D:/unity/WanxiangGuitu' `
 -IsolationRoot 'C:/UnityValidation/B1Normal' -Mode Resume
```

沿用 A1 的启动前 `-wanxiang-storage-root`、ValidateLaunch 和应用入口审计。缺少/相对/LocalLow 参数分别用 RejectMissing/RejectRelative/RejectLocalLow，每项使用新的 IsolationRoot。预期明确拒绝标记、退出1、无存档入口回执、合成根外哨兵不变，不能仅凭任意退出1通过。

Normal 固定实际布局种子418，带入石1矿2及初始弓/剑，不改生命/伤害/速度，不冻结 AI，不在出征后传送。实际攻击、弓击杀、采木、V 切长剑采石、到渡口修复、切弓处理局部威胁、允许受击中止后重试、引导、提交入库、取木制造、再次出征及新进程恢复。它不是人工试玩；也不是 B4 三条路线验收。角色选择技能通过既有 API，移动通过 InputSystem；攻击、互动通过实际领域入口。

## 无运行驱动的正式 Player

```powershell
& './ProjectDocs/WanxiangGuitu/DeliveryB1/Invoke-ReleaseResume.ps1' `
 -Executable 'C:/UnityValidation/B1Rules/Release/WanxiangGuitu.exe' `
 -IsolationRoot 'C:/UnityValidation/B1ReleaseResume' `
 -FixtureDirectory 'C:/UnityValidation/B1Rules/b1-save'
```

FixtureDirectory 只能是上述检查生成的合成档。脚本复制完整集合，启动无运行驱动的非开发 Player 两次；使用操作系统 WM_CLOSE 请求关闭该脚本启动进程的自有窗口，要求退出0、quit回执、无超时，并核对同 Run、区域实例、种子、出口修复与材料来源账。超时终止只能记失败。没有往产品里加自动退出/测试行为，也不冒充人工点击或完整正式版玩法试玩。

## 证据

REPORT.md 与 Evidence/INDEX.md 记录本次实际运行；可复跑脚本的存在不等于已经执行。引擎 Search 索引异常、构建警告、失败尝试与后续通过分开记录。应用入口审计不能声称覆盖所有 OS 文件访问；历史正常 AI 是否触及真实玩家目录仍未核实。
