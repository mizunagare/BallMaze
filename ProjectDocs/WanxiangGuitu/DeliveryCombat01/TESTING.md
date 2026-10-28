# COMBAT-01 复跑

固定版本复跑，先核对远端完整SHA，保存用户文件与全部产品输入哈希。仅使用工程外新的显式拥有者根，例如 `I:/WGCombat/<唯一标识>`，不访问LocalLow玩家数据。

复用 `DeliveryUI01/Invoke-Rules.ps1 -PrepareOnly` 创建副本。`Invoke-Checks.ps1 -Project <拥有者根/B/Project> -Output <新的结果目录>` 复用既有协调器和独立非活动桌面worker；不激活用户桌面，不发送物理Esc，不强杀超时进程。

`Tests/Combat01Checks.cs.txt` 只注入副本的Editor目录。它使用真实Strike/UseSkill/Health/Physics/Projectile代码，受控布置目标、关闭AI与自动保存，不是原生输入或正常AI胜利。每轮保留执行源、日志、HealthObservation时间/帧、结果及进程回执。旧版负例用开工源码副本，新版用明确记录的产品输入；不能拿负例exit1当作工具误报。

非开发构建沿用 `DeliveryBuild01/Invoke-Diagnostic.ps1` 的Release/Acceptance两种隔离配置，Acceptance仅在隔离副本注入既有PLAYER-02驱动。构建输入变动时必须重新构建，并保留之前候选，不将旧产物当最终产物。

正常AI与保存恢复沿用 `DeliveryUI01/Invoke-NormalAI.ps1`；最终验收Player沿用 `DeliveryPlayer02/Invoke-P02Case.ps1` 的Setup/Main/Pending/Committed/Manufacture/Successor和audit_story.py。必须逐阶段核对真实业务回执、来源账、冷却与新进程身份，不以编排器exit0代替。

原生U16、独立人工、完整性能预算没有执行能力时保持NOT_RUN。GC字节计数不可用不能写零；对象数量和自有材质数量只证明本次负载中的生命周期，不证明全局零分配。

## 交付归档离线复核

`python -B verify_evidence.py Evidence/Run-1028-093640`逐一校验1143原件、无损解压日志、4项产品变更、5项保护文件及33个旧失败条件的新结果。不会运行游戏或操作存档。

`Invoke-Checks.ps1`支持显式`-WorkerPath`；默认值是本轮拥有者worker路径，换机器须先复用现有NativeProbe源码构建新拥有者worker并显式传参，不依赖旧路径可用。`-DesktopName`只接受本轮拥有者回执中的非活动WGTest名字，用于复用测试桌面，不能传入用户桌面或激活桌面。`-StorageRoot`仅用于受控Run/Resume共享的合成存档，日志输出仍用新的Output，失败目录不覆盖。

最终验收Player使用既有BUILD01入口`-Variant Acceptance -AcceptanceProfile Combat01`，仅追加实际升级UI的Digit1输入处理，所有产品输入与发行版匹配。旧Player02 profile仍保持原行为。依次执行既有P02Case的六个模式，并用audit_story.py只读核账。首轮旧驱动失败保留在Story，最终运行在新Story2，不复用旧PASS。

若Editor停在启动阶段没有用例回执，不继续修改该占用项目，也不强杀。Baseline3与SaveRun超时保留；相关专用验证NOT_RUN，独立安全Player验证继续。完整状态见ACCEPTANCE，不能以188断言PASS代替整批退出结论。
