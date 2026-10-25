# B08 复跑

复用既有入口，不新增CI或第二套编排：

```powershell
& ./ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1 `
 -SourceProject D:/unity/WanxiangGuitu -TestRoot D:/WanxiangValidationRuns/B08FinalAll `
 -Phase All -FullRegression -B08 `
 -ShaderCacheSource D:/WanxiangValidationRuns/B07R1ReleaseAll/20261025-145529-a973b767/Project
```

B08包含B07/B4既有回归，附加Tutorial正常AI三进程及其最终Player恢复。唯一新测试根、完整合成存档；启动前隔离，不在Play后切换真实目录。缓存项仅复用同引擎已结束项目的ShaderCache，可省略，不宣称着色器从零编译。规则与UI先定向再完整All。不要并发启动多个Unity导入；曾观察到CoreCLR/GC初始化失败，首次记录保留，环境有限重试，未知根因不归咎产品。

定向沿用DeliveryB4/Invoke-Directed.ps1，方法为B08Probe.Run、B08Rules.Run/Resume/FinalResume/CompleteResume、B08Recovery.Run/Resume、B08Visual.Run；NormalStrategies Tutorial。先决失败后跳过后继恢复，编译/CLR不可用时跳过同副本后续Unity。

B08Rules为受控真实业务，NPC停用且位置夹具明确；验证只读帮助、旧档启用标识、故障前后设置、真实移动/资源/拾取、取消、结算、取材/制造与新进程。B08Recovery单列真实死亡、放弃和跳过后完整业务/恢复。

B08Visual为40张受控显示：1280x720、1920x1080、2560x1440、3440x1440各100/150%，每组合营地、森林、帮助、真实保存失败与仓库。直接设置教程显示阶段仅作布局夹具，不冒充真实完成。NPC停用，稳定帧/青色退化阈值与R1一致；检查屏幕边界、四设施标签、一项主目标、关键保存消息以及Profile/Run/随机只读。

Tutorial正常AI使用正常NPC和领域机器人：实际CharacterController移动、共享E/H交互、普攻、受伤与物品业务；无Boss生命/库存/结算覆盖，不通过虚拟键盘冒充原生。既有B4/B07机器人仍沿用其原入口与明确合成初始物资。Tutorial不额外发物资，使用原始四白武器，实际收集木/石/矿、正常战斗，可用实际掉落制作药水。第一进程备料至免费出口；第二进程撤离结算、仓库取材制造、再出征；第三进程继续同一后继Run，教学不重播。

最终非开发Player只验证启动、后台WM_CLOSE、退出审计和同一Run/教程/账目恢复，不是原生标题栏/鼠标键盘验收。没有安全独立输入环境则NOT_RUN，不要求用户守候，不强杀或关闭用户程序。完整构建警告、失败尝试和所有日志单列保留。

B08CampPause.Run用受控初始冷却验证一秒真实时间后，技能/普攻/武器切换/翻滚/药水的剩余时间保持不变，同时CharacterController移动与真实E设施交互可用；不通过设置库存或教程完成字段伪造。修复前后使用同一测试源，旧产品副本先冻结，不在运行中的副本上改源码。

## 证据后处理

仅对已结束运行执行；目标必须全新，失败和历史目录不能覆盖：

```powershell
$py='C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$run='<本轮实际新根>'
$module='ProjectDocs/WanxiangGuitu/DeliveryB08'
$evidence="$module/Evidence/FinalAll"
& $py -B "$module/Publish-Evidence.py" --run $run --target $evidence
& $py -B ProjectDocs/WanxiangGuitu/DeliveryB4/Provenance.py --project D:/unity/WanxiangGuitu --run $run --target $evidence
& $py -B ProjectDocs/WanxiangGuitu/DeliveryB07/Seal-Evidence.py --project D:/unity/WanxiangGuitu --run $run --target $evidence --commit '<运行时已冻结输入SHA>'
& $py -B "$module/Audit-Release.py" --project D:/unity/WanxiangGuitu --run $run --target $evidence --baseline 638dd9b8159887bd02b6fc0c2e38d817623622cd
& $py -B "$module/Summarize-Evidence.py" --run $run --output "$evidence/review-summary.json"
& $py -B "$module/Finalize-Report.py" --run $run --module $module
& $py -B ProjectDocs/WanxiangGuitu/DeliveryB07/Verify-Evidence.py --root "$module/Evidence" --output "$module/Evidence/evidence-verification.json"
```

历史独立用Archive-History.py的显式根清单复跑发布。后处理只读诊断，不读真实存档，不运行游戏，不修改产品。发布工具拒绝save.json、before/after存档封装、ground-loot页、计划、二进制、Library和转储；合成结算仅发布字段摘要。PNG和冻结源码保留原字节，日志脱敏前后各有SHA256。最终Player的Verify-Player仅用于显式给定的合成快照，不能对默认玩家目录运行。

正常轨迹b08-normal-ai.csv有表头；b08-attacks.csv为time,nodeId,kind,weapon,distance,before,after,released列的真实普攻日志。正常AI可战斗/受伤/升级，但不覆盖生命、资源生命或结算结果。受控规则的直接Hit/位置夹具与正常AI普攻轨迹分开，不能混称。
