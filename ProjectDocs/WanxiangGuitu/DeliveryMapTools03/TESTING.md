# 复跑说明

只在独立研究副本执行。最低可提交内存3GB，未满足不启动Unity；不关闭用户程序、不强杀超时、不复制使用中的Library。原有输出一律不覆盖。入口工具拒绝已有输出与被占用工程；NativeProbe使用独立inactive desktop，不是物理键鼠操作。

## 重建输入

1. Unity6000.6.5f1、URP17.6.0，合法官方MapMagic FREE包。原包SHA在VERSION_PROVENANCE；许可证不允许假定可以重新分发，仓库不包含其源码/包。
2. 独立工程复用上批 [LabInputs](../DeliveryMapTools02/LabInputs)，将该批自有MT02WorldState.cs.txt还原为Assets/MT02WorldState.cs，以及原自有场景资源和依赖。供应商包独立合法导入，不导入正式游戏。
3. 本目录Tests/*.cs.txt还原为Assets/MT03Runtime.cs、Assets/Editor/MT03Editor.cs；Calibration.shader.txt还原为Assets/MT03Calibration.shader。使用LabInputs对应meta保留GUID。MT03Generated场景/Profile同目录提供，引用上批自有资源。
4. 本轮Package manifest和锁文件在LabInputs；独立工程设置FrameTimingStats=true。不要复制这些设置覆盖用户ProjectSettings。现场脚本固定路径可先在新的独立环境中审阅并修改为自己的隔离根；需要已有NativeProbe宿主，路径/源码引用列在Tools脚本中。

## 本机命令（输出必须是新目录）

```powershell
./Tools/Invoke-Lab.ps1 -Method MT03Editor.Prepare -Output I:/WGCombat/MAPTOOLS03-A/PrepareNew
./Tools/Invoke-Lab.ps1 -Method MT03Editor.BuildEmpty -Output I:/WGCombat/MAPTOOLS03-A/EmptyNew -DiagnosticJobs
./Tools/Invoke-Lab.ps1 -Method MT03Editor.BuildTerrain -Output I:/WGCombat/MAPTOOLS03-A/TerrainNew -DiagnosticJobs
./Tools/Invoke-Lab.ps1 -Method MT03Editor.BuildAudit -Output I:/WGCombat/MAPTOOLS03-A/AuditBuildNew -DiagnosticJobs
./Tools/Invoke-Player.ps1 -Exe I:/WGCombat/MAPTOOLS03-A/AuditBuildNew/Player/MT03.exe -Output I:/WGCombat/MAPTOOLS03-A/AuditNew -Mode audit
./Tools/Invoke-Player.ps1 -Exe I:/WGCombat/MAPTOOLS03-A/AuditBuildNew/Player/MT03.exe -Output I:/WGCombat/MAPTOOLS03-A/MemoryNew1 -Mode memory
./Tools/Invoke-Player.ps1 -Exe I:/WGCombat/MAPTOOLS03-A/AuditBuildNew/Player/MT03.exe -Output I:/WGCombat/MAPTOOLS03-A/MemoryNew2 -Mode memory
./Tools/Invoke-Lab.ps1 -Method MT03Editor.Play -Output I:/WGCombat/MAPTOOLS03-A/EditorNew -NonBatch -Seconds 180
```

Play必须非batch，WaitForEndOfFrame截图需要可运行GameView；否则超时保留进程并记录，不杀进程。Player有显式包含World的Build Profile，不靠EditorBuildSettings默认列表。测试驱动自动退出不代表菜单原生退出或人工操作验收。

`Tools/Analyze.py`只读核对本轮命名的结果，缺必需文件、重复行、未知status或失败进程会报错；重跑其他输出时显式改RUNS，不把旧PASS继承。`Tools/Publish.py`仅发布独立证据和自有资源，压缩大jsonl/log，保留源与公开哈希。原始证据不改。编辑器Resources库存与Player不能套用同一个绝对阈值。

本轮实际命令、启动身份、退出回执、驱动快照和结果在各Evidence子目录。原始Player二进制留在本机Build*/Player，仓库提供可执行文件/程序集SHA清单，不伪称已上传完整可执行包。
