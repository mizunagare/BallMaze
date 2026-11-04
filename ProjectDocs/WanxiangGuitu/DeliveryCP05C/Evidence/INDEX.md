# CP05-C证据索引

基准7fc4f5dc3043bcbb69f63c2ebf267359741ccbbe。新运行根 `I:/WGCombat/CP05C-1104-A`；所有原始文件保留。文本日志仅在发布副本压缩及脱敏，见[395项manifest](manifest.json)中的sourceSHA256/publishedSHA256；没有改写历史JSON。可执行包在工程外，不将大型Player二进制作为源码提交；完整文件哈希在[release-files](release-files.json)。

## 修复前

- [BeforeTraining](BeforeTraining/probe.json) / [日志](BeforeTraining/Unity.log.gz)：Editor真实旧例，11 PASS/9 FAIL，exit1。
- [BeforePlayer](BeforePlayer/probe.json) / [日志](BeforePlayer/Player.log.gz) / [进程](BeforePlayer/runtime.json)：非开发Player旧例，同样11/9，exit1。
- [BeforeFormal](BeforeFormal/probe.json)、[BeforeFormal2](BeforeFormal2/probe.json)、[BeforePlayerFormal](BeforePlayerFormal/probe.json)：原源码的真实森林及同一产品检查点继续；SeedPackage是真实保存产物，不是手写存档。
- [初始源审计失败](source-audit-before-after.json)、[工具失败分类](tool-failures.json)、AfterTraining1/2/3各独立日志、退出和断言保留，不覆盖。

## 修复后

- [Editor训练92项](AfterTraining4/probe.json) · [Editor进程包装](AfterTraining4Runner/results.json)
- [Player训练92项](AfterPlayer/probe.json) · [实际进程退出](AfterPlayer/runtime.json) · [命令](AfterPlayer/Player.command.json) · [独立桌面进程](AfterPlayer/Player.desktop-process.json)
- [真实死亡轨迹](AfterPlayer/deaths.jsonl.gz) · [重开/清理轨迹](AfterPlayer/restarts.jsonl.gz) · [Player实际画面](AfterPlayer/training.png) · [Editor画面](AfterTraining4/training.png)
- [Editor正式43项](AfterFormal/probe.json) · [Player正式43项](AfterPlayerFormal/probe.json)
- [Editor480行](AfterFormal/formal-rules.json) · [Player480行](AfterPlayerFormal/formal-rules.json) · [实际死亡及真实ID](AfterPlayerFormal/formal-death.json)
- [逐字段配对](paired-results.json) · [源审计8自测](audit-selftests.json) · [保护2347项](protection-final.json) · [原哈希](protected-before.json)

## 构建与输入

- [测试构建命令](AfterTestBuild/CP05Build.Run.command.json)、[退出](AfterTestBuild/CP05Build.Run.exit.json)、[完整日志](AfterTestBuild/Unity.log.gz)。其Release目录的实际发行元数据已在原运行根保留；本索引的纯包元数据如下。
- [纯构建实际命令](PureBuild/CP05Build.Run.command.json) · [实际退出](PureBuild/CP05Build.Run.exit.json) · [日志](PureBuild/Unity.log.gz)
- [纯包摘要](PureBuild/release.summary.txt) · [Profile回执](PureBuild/release.release.json) · [真实Bee](PureBuild/release.bee.json) · [release-identity](release-identity.json)
- [测试/纯包IL及驱动剔除](assembly-audit.json) · [116产品脚本输入匹配](product-runtime-input-match.json)
- [纯构建前输入](pure-build-inputs.json) · [构建后输入](pure-post-build-inputs.json) · [差异](isolated-build-writes.json)（0项） · [测试构建输入](test-build-inputs.json)
- [纯包启动/关闭](PureSmoke/runtime.json) · [普通关闭回执](PureSmoke/close.json) · [纯包日志](PureSmoke/Player.log.gz)

CP05Build的Prefab导出、编译及所有运行均在隔离副本，用户场景和ProjectSettings未写入。构建期间服务状态/实际Bee由现有Privacy保护核验，不以单个m_Enabled字段下结论。外部诊断路径、历史引擎问题仍沿原有边界保留。

截图属于受控API场景，不是原生键鼠或独立人工试玩。纯包只烟测，不声称完成物理点击或人工战斗。Editor退出JobTempAlloc仍UNRESOLVED，原生输入/人工/新增性能NOT_RUN。
