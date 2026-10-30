# 复跑说明

开工源码main `804b4abbd36928618cd3629fc2e286787bfc44d6`；实际本轮根 `I:/WGCombat/AIM01-1030-A`。所有路径必须替换为**新的**I:/WGCombat子根；不要覆盖本轮原证据。Unity6000.6.5f1，显式启动前 `-wanxiang-storage-root`，合成存档；既有资源门槛3GB/独立私有测试桌面（不激活桌面），不关闭用户程序、不强杀超时进程。

## 隔离副本

复用 `DeliveryUI01/Invoke-Rules.ps1 -PrepareOnly` 创建新副本，目录形状为根/F/Project。只在副本中把用户修改场景/设置移至该拥有根的Deferred目录，改用开工Git blob；Recovery亦移出副本。用户原工程只读这些文件并核对SHA，不提交用户差异。设置owner.json，复用既有NativeProbe构建/启动器，不另写测试编排系统。本轮缓存副本失败后使用新鲜Library，不复制历史PASS。

复制授权产品源码到副本；测试模板只复制至副本 `Assets/CombatPrototype/Editor/B06LocalChecks`。`Invoke-Check.ps1` 复用既有编排器Step，检查进程冲突/资源/退出/日志/异常回执；每次Output必须新目录。命令示例（从仓库根PowerShell执行）：

```powershell
& ./ProjectDocs/WanxiangGuitu/DeliveryCombatAim01/Invoke-Check.ps1 -Project "$owned/F/Project" -Output "$owned/Paired" -Method Aim01Before.Run
& ./ProjectDocs/WanxiangGuitu/DeliveryCombatAim01/Invoke-Check.ps1 -Project "$owned/F/Project" -Output "$owned/Rules" -Method Aim01Rules.Run
& ./ProjectDocs/WanxiangGuitu/DeliveryCombatAim01/Invoke-Check.ps1 -Project "$owned/F/Project" -Output "$owned/Timing" -Method UX04CombatTiming.Run
& ./ProjectDocs/WanxiangGuitu/DeliveryCombatAim01/Invoke-Check.ps1 -Project "$owned/F/Project" -Output "$owned/Area" -Method Combat03Area.Run
```

事务三进程依次用UX04Matrix.Target、CraftOnly、Resume，三个不同Output、同一StorageRoot `$owned/CraftShared`。只重用原事务断言；新的Collider交集矩阵单独列，不把根点旧预期偷偷改成所有结果不变。UI测试需要图形，不能 `-nographics`。每项还必须读取对应before/rules/combat01/area/matrix JSON：空结果/OS0本身不够。

## 两类非开发构建

先无任何Player02AcceptanceOnly运行时文件，复制既有 `DeliveryBuild01/Tests/Build01Audit.cs.txt` 为副本Editor/.../Build01Audit.cs，用同wrapper -Method Build01Audit.Run -StorageRoot `$owned/ReleaseFinal/Results`，得到BuildOptions.None正式产物。保存完整消息和input哈希，再运行 Inspect-Build.ps1 对所有Managed模块检查驱动类型/UnityEditor引用。

再调用 `python -X utf8 -B Prepare-Runtime.py $owned D:/unity/WanxiangGuitu AimFinal`：只在该拥有根副本注入PLAYER02 partial与小用例；有项目占用时拒绝。建立Runtime/owner.json，kind=`PLAYER-02 isolated runtime acceptance`、source为仓库，复用PLAYER02 worker/中继。用同构建方法输出 `$owned/Runtime/T/AimFinal/Results`。严禁把注入文件加入产品Assets或纯发行构建。

Runtime/FinalStory/aim01-config.json先为 `{"stage":"Core"}`，随后为 `{"stage":"Resume"}`，分别运行**原有**：

```powershell
& ./ProjectDocs/WanxiangGuitu/DeliveryPlayer02/Invoke-P02Case.ps1 -ParentRoot "$owned/Runtime" -StorageRoot "$owned/Runtime/FinalStory" -BuildRoot "$owned/Runtime/T/AimFinal" -Mode Observe -WorkerPath "$owned/Runtime/Host/Worker/NativeProbe.dll"
```

每次Attempts独立目录，原runner冻结StorageAfter、命令/退出/超时/日志/hash和新鲜语义回执。Mode Observe仅为复用启动器参数；有明确aim01-config时驱动分派Core/Resume，不是旧Observe标题检查。虚拟输入不是原生/人工。临时低掩体单列受控物理用例，采集/拾取/保存全部走真实运行时，不写最终存档或奖励字段。

## 收集和复核

`Collect.py <拥有根> <仓库>` 只发布合成证据，排除工程/缓存/发行二进制/用户Deferred/Host，日志gzip并凭据脱敏；manifest同时保存本地原始与发布SHA。检查六源码文件在源/副本/两构建input哈希相同，五用户文件前后相同；旧交付差异为零。所有失败独立保留。发布前核对Git/LFS、定向差异并只stage授权文件，正常push后ls-remote完整SHA；不force/reset。交付后暂停。
