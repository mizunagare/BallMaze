# WORLD-01 复跑

Unity 6000.6.5f1；使用已有本机 Prepare、Step/独立桌面 Worker、规则和正常 AI 驱动，不新建业务框架，不启用 CI。新根必须位于工程外 `I:/WGCombat/<unique>`，有 owner.json；先检查 Unity 占用、磁盘与用户保护哈希。禁止真实玩家档案。

```powershell
./ProjectDocs/WanxiangGuitu/DeliveryUI01/Invoke-Rules.ps1 `
  -SourceProject D:/unity/WanxiangGuitu `
  -WorkProject I:/WGCombat/<unique>/P/Project `
  -ArtifactsRoot I:/WGCombat/<unique>/Prepare -PrepareOnly
./ProjectDocs/WanxiangGuitu/DeliveryWorld01/Invoke-World01.ps1 `
  -Project I:/WGCombat/<unique>/P/Project -RunRoot I:/WGCombat/<unique>
```

Library 仅可从已确认闲置的旧验证副本复制；不得复制占用库或操作用户 Editor。Invoke-WorldCheck 是原 Invoke-Checks 的薄适配：相同 Step/Worker/超时/日志，增加 batch 启动、显式 shared storage 准备和本批 Editor 夹具注入。编译错误直接退出，不再等待 Safe Mode 人工操作。它不是正式 Player 或原生 UI。

本轮有效样本 418-A3、418-B、419-A/B、420-A/B。首次 418-A 编译失败和 A2 漏处理真实升级选择的 deadline 失败保留。新根首次没有 cycle-run.json 时主入口会自动执行 Run；已完成的目录不得覆盖。第一次样本五进程，其余三进程；每段保存原主备、期望身份及检查。失败停止该依赖链，后续独立样本继续；占用/超时则保留进程，不强杀或重用副本。

WorldAudit 输出实际布局、每实体路径、真实距离和评分，WorldCycle 复用 RUNLOOP-01 的真实业务入口，增加普通敌实际攻击、宝箱和运行时恢复核对。营地100×六材料是显式合成输入；不在正例终态编辑物资或结果。升级必须正常 SelectChoice；不能把 TimeScale 设回1绕过选择。非目标敌冻结/受控定位与正常AI区分。

正常AI及受影响旧规则由原 Invoke-Regression 执行。额外有界补测（顺序执行，无人工确认）：

```powershell
$entry='./ProjectDocs/WanxiangGuitu/DeliveryWorld01/Invoke-WorldCheck.ps1'
& $entry -Project <clone> -Output <root>/Boundary -StorageRoot <root>/Boundary-Store -Method Combat02Bench.Boundary
& $entry -Project <clone> -Output <root>/PoiRun -StorageRoot <root>/PoiShared -Method WorldPoi.Run
# 只有 PoiRun 真实成功后运行依赖阶段。
& $entry -Project <clone> -Output <root>/PoiResume -StorageRoot <root>/PoiShared -Method WorldPoi.Resume
# 需要完全复现本轮报告的命名时，用独立目录，绝不覆盖旧构建。
& $entry -Project <clone> -Output <root>/Build02 -StorageRoot <root>/Build02-Store -Method Build01Audit.Run
& $entry -Project <clone> -Output <root>/Build03 -StorageRoot <root>/Build03-Store -Method Build01Audit.Run
```

本轮 Build 首次在调用实际构建前缺目录失败，修工具后 Build02 成功；发现隔离设置重序列化，另用新 Build03/Build03-Store 做一次输入稳定复验。新根不需要人为制造旧故障；保存实际新结果，不继承本轮96或2条警告数量。需要再次复验时用新的输出目录调用 Build01Audit.Run，保存紧邻前后清单，完整归档警告。

Inspect-Build 只读核对 PE/哈希；Summarize 读取这次实际产物并做路径坐标几何复核，缺少前置结果会失败而不是填PASS。当前发布脚本使用本轮阶段名 Build02/03，复跑采用不同命名时应显式更新输入映射，不回填历史文件。

Collect.py 发布拥有者根白名单、压缩日志并记录原始/发布双SHA256，排除工程副本、Library、Packages、构建二进制、Worker运行时缓存。Verify-Publication.py 核对暂存字节或 LFS oid；所有故障合成备份/临时档仅在本批证据白名单强制暂存，不能清理旧玩家数据。

原生输入、独立人工、性能和发行Player游戏未执行应保持NOT_RUN。已知引擎/关闭异常不做无新线索实验；旧失败、内部deadline和工具失败单列。最终检查源范围、保护哈希、LFS，推送后重新读取远端完整SHA，暂停复审。
