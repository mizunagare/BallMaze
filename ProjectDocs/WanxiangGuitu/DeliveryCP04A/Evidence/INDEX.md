# CP04-A 原始数据索引

所有新输出来自工程外 `I:/WGCombat/CP04-1031-A`。历史原件未修改。发布清单记录原始和发布SHA；日志/JSONL按既有工具gzip、仅凭据值脱敏，完整本机原件保留。

- [全部发布文件与双SHA清单](manifest.json)
- [原失败重现](Historical/presentation.json)；[几何JSONL](Historical/aim-diagnosis.jsonl.gz)；[Spawn/Flight/Damage](Historical/events.jsonl.gz)
- [原矩阵R1.3语义重审](Historical/Semantic/acceptance.json)；[分类器实际exit2](Historical/classifier-exit.json)
- [38项完整实际相机/骨骼/投影/射线/碰撞轨迹](Matrix/diagnosis.json)；[逐案例进度](Matrix/case-progress.jsonl.gz)
- [补充2项真实相机遮挡](CameraWall/diagnosis.json)；[补充摘要](camera-wall-summary.json)
- [分析和原始对应](Analysis/analysis.json)；[矩阵CSV](Analysis/matrix.csv)；[六项分析一致性](Analysis/verification.json)
- [24组真实发射配对](paired-24.json)
- [最终16项核验](final-verification.json)
- [2329项保护前清单](protected-before.json)；[保护结果](protected-after.json)；[1163冻结产品输入](product-input-binding.json)
- [5项旧证据保护SHA](historical-before.json)；[重点源码SHA](focus-source-hashes.json)；[辅助测试输入](isolated-helper-inputs.json)
- [首次分析工具编码失败](analysis-attempt1-error.json)；[包装器初次语法FAIL](wrapper-parse.json)；[修订后PASS](wrapper-parse-final.json)

真实进程来源与日志：

|运行|完整日志|Runner|NativeProbe退出|命令/宿主|实际子进程|
|---|---|---|---|---|---|
|Historical|[Unity.log](Historical/Unity.log.gz)|[results](Historical/results.json)|[exit](Historical/CP03Editor.Run.exit.json)|[command](Historical/CP03Editor.Run.command.json)|[desktop](Historical/CP03Editor.Run.desktop-process.json)|
|Matrix|[Unity.log](Matrix/Unity.log.gz)|[results](Matrix/results.json)|[exit](Matrix/CP04Editor.Run.exit.json)|[command](Matrix/CP04Editor.Run.command.json)|[desktop](Matrix/CP04Editor.Run.desktop-process.json)|
|CameraWall|[Unity.log](CameraWall/Unity.log.gz)|[results](CameraWall/results.json)|[exit](CameraWall/CP04Editor.CameraWall.exit.json)|[command](CameraWall/CP04Editor.CameraWall.command.json)|[desktop](CameraWall/CP04Editor.CameraWall.desktop-process.json)|

执行源码：每个运行目录的`*.executed.cs.txt`是实际执行副本；Matrix和CameraWall版本分别保留。根目录早期CP04*.cs.txt仅为初始候选，不充当执行版本。正式源码未插入观测代码，只有既有生产事件订阅。

JsonUtility对缺失predictedContact可能输出空字段对象，应以hasContact布尔为准；不能从默认坐标推断发生了碰撞。所有命中结论均交叉检查真实contact事件及Damage。

本索引不声明正式Player、原生输入、人工观感、性能或产品修复通过。

[Git/LFS字节与链接校验](publication-check.json)：124项，17个LFS对象，107个直接对象，无错误或断链。
