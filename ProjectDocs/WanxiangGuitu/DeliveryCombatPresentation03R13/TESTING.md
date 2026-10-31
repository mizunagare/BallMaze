# R1.3复跑

使用全新输出目录，禁止覆盖已有证据。Python3，无新增依赖。

```powershell
$py='C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$d='H:/unity/WanxiangGuitu-CP03-R1/ProjectDocs/WanxiangGuitu/DeliveryCombatPresentation03R13'
& $py "$d/Legacy/SelfTest50.py" --output 'I:/WGCombat/CP03-R1-NEW/Legacy50-First' --original-root 'I:/WGCombat/CP03-1031-A'
& $py "$d/Legacy/SelfTest33.py" --output 'I:/WGCombat/CP03-R1-NEW/Legacy33-First'
& $py "$d/Legacy/SelfTest60.py" --output 'I:/WGCombat/CP03-R1-NEW/Legacy60-First'
& $py "$d/SelfTest-R13.py" --output 'I:/WGCombat/CP03-R1-NEW/Association-First'
& $py "$d/Reaudit.py" 'I:/WGCombat/CP03-R1-1031-C' --output 'I:/WGCombat/CP03-R1-NEW/Reaudit'
```

四组工具入口exit0；每项负例CLI实际应exit3，完整控制exit0，开放项控制exit2。Reaudit包装工具exit0表示两份原件均按预期BLOCKED/2，其内两个Receipt.py实际退出码仍为2，详见actual-exit.json；不是产品整体PASS。

本轮实际目录为CP03-R1-1031-D。Reaudit.py与本轮读取命令一致；没有重跑Unity。未来确需新运行时，使用原两个Invoke包装器、独立隔离工程/合成存档，包装器已明确传递新增三个来源路径，不手填PASS/0。

一致性：Verify-R13.py ROOT --source ORIGINAL_R12_ROOT --output NEW_JSON。需ROOT含本轮保护、输入、锁定审计等清单，所有目标均只读；检查44项。本轮数据、CLI命令、actual-exit、stdout、stderr及分类报告详见Evidence。Legacy适配副本不替代旧脚本，旧50/33/60断言及原文件完整保留。
