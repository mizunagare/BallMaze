# 隔离复跑

沿用Unity6000.6.5f1与固定依赖。不要运行在当前用户工程；使用工程外全新拥有者根和合成存档。

1. `DeliveryUI01/Invoke-Rules.ps1 -SourceProject <源码> -WorkProject I:/WGCombat/<唯一>/B/Project -ArtifactsRoot I:/WGCombat/<唯一>/B/Results -PrepareOnly`。记录main、所有源输入和用户文件哈希。
2. `Invoke-UX02.ps1 -Project <独立Project> -Output <全新输出> -Batch`注入Editor专用测试，运行UX02Checks.Run。规则使用受控布置/直接Damage和uGUI回调，不是正常AI或原生键鼠。
3. 同一独立StorageRoot依次运行`-Method UX02Checks.ExtraRun`、`UX02Checks.ExtraResume`，输出目录分开；每次立即复制共享根ux02.json到对应输出，保留独立进程89项/5项结果及期望文件。
4. `-Method UX02BatchEntry.Combat -Batch`仅补原COMBAT01在batch模式缺少的显式合成存档初始化，原188项断言不改。原直接Combat01Checks.Run在batch模式会等待初始化超时，该失败已保留。
5. 原`DeliveryCombat01/Invoke-Regression.ps1`继续运行Input01/观测/B07战斗与三阶段正常AI，独立非活动桌面由已有协调器创建，不激活桌面。不要直接运行旧Invoke-NormalAI到未经准备的副本：重复类和清理依赖会失败。结束后如需再运行规则/构建，将Deferred的三类Editor驱动副本复制回原隔离测试位置，保留外部Deferred历史，不改主工程。
6. 先复制`DeliveryBuild01/Tests/Build01Audit.cs.txt`到副本Editor目录，再用`-Method Build01Audit.Run -Batch`调用原正式构建方法（BuildOptions.None，Boot/Title/Forest），记录全量警告和哈希。测试不进入发行程序集。
7. `python -B collect.py --root <拥有者根> --out <全新归档目录>`。保留早期快照；不覆盖原始结果。日志只脱敏许可token字段，保留错误与调用栈；原始日志仍在本机，清单含原件和发布件SHA。

截图分层：ScreenCapture原件原样保留，可能受旧青色帧影响。`controlled-*.png`由实际运行场景通过URP RenderRequest取得，临时将overlay改为ScreenSpaceCamera后还原，仅为受控布局/模型证据。不是普通屏幕或原生输入验收。

资源不足/占用时保留进程并跳过依赖，不关闭用户程序、不降低门槛。启动器明确返回退出0/1，不能依赖上一脚本的LASTEXITCODE；实际子进程回执仍单列。旧T06 v6最终断言已不适用于当前v9，不能放宽为自动PASS；本批另用真实29配方/v9事务与已有v9规则核验。
