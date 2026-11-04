# CP06-A证据索引

基准397d53fe87ce5b6c490c86c63d59015de26a46af。原始根I:/WGCombat/CP06A-1104-A；1074项[manifest](manifest.json)分别记录原始/发布SHA，日志只在发布副本压缩脱敏，不改写原证据。包保留于隔离根，完整文件清单可核对。

## 基准与失败

[BeforeEditor](BeforeEditor/probe.json) · [修正等待后的基准](BeforeEditor2/probe.json) · [基准非开发Player](BeforePlayer/probe.json)。旧技能实际数据见各legacy.json。AfterEditor1/2/4原失败断言、jsonl、日志和执行脚本保留；[失败历史](../FAILURE_HISTORY.md)区分等待门槛、禁用目标夹具及真实地面碰撞。

[工具失败](tool-failures.json) · [文档工具失败](documentation-failure.json) · [原始保护](protected-before.json)。每次运行保存命令、原生退出回执及完整日志（.gz），不以编排器exit0取代语义断言。

## 八技能真实运行

[Editor157条](AfterEditorFinal/probe.json) · [Player157条](PlayerFinal/probe.json) · [Player进程](PlayerFinal/runtime.json) · [实际命令](PlayerFinal/Player.command.json) · [独立桌面](PlayerFinal/Player.desktop-process.json)。

|武器|技能1真实轨迹|技能2真实轨迹|实际Player画面|
|---|---|---|---|
|剑|[三拍连斩](PlayerFinal/skill-0-1.jsonl.gz)|[回旋剑阵](PlayerFinal/skill-0-2.jsonl.gz)|[连斩释放](PlayerFinal/skill-0-1-1-release.png)|
|枪|[蓄势穿刺](PlayerFinal/skill-1-1.jsonl.gz)|[扫锋拒敌](PlayerFinal/skill-1-2.jsonl.gz)|[蓄势释放](PlayerFinal/skill-1-1-1-release.png)|
|杖|[余烬符阵](PlayerFinal/skill-2-1.jsonl.gz)|[回响连珠](PlayerFinal/skill-2-2.jsonl.gz)|[符阵真实脉冲](PlayerFinal/skill-2-1-2-field-pulse.png)|
|弓|[追点连射](PlayerFinal/skill-3-1.jsonl.gz)|[蓄势贯矢](PlayerFinal/skill-3-2.jsonl.gz)|[贯矢释放](PlayerFinal/skill-3-2-1-release.png)|

每技能还有同名.png及分阶段图。actual-health-damage记录实际健康回调；melee-DAMAGE/OBSTRUCTED记录真实近战几何；[旧物理弹体](PlayerFinal/projectiles.jsonl.gz)有spawn/flight/contact/resolved，新贯矢有pierce-spawn/flight/contact/blocked，符阵有field-created/contact/pulse。不是选中即命中。

[三目标实际贯穿](PlayerFinal/charged-piercing.jsonl.gz) · [释放前固定阵列](PlayerFinal/pierce-fixture.json) · [配置](skill-config.json) · [39张非黑帧内容核验](render-content-check.json)。原低位相机和世界Z轴阵列FAIL留在AfterEditor1/4，不能改写为成功；正向三目标没有射后移动对象。

## 附加、保存与旧回归

[Editor附加14](ExtraEditorFinal/probe.json) · [Player附加14](ExtraPlayer/probe.json)：普攻衔接、实际翻滚/uGUI选择/AI致死、缺相机及真实动画绑定。

[Editor保存](SaveEditorFinal/probe.json) · [Editor新进程继续](ResumeEditorFinal/probe.json) · [Player保存](SavePlayer/probe.json) · [Player新进程继续](ResumePlayer/probe.json)。SeedPackage为真实v9写档产物；expected.json只比较身份，不改保存字段或发奖励。

[CP05 Editor92](CP05RegressionEditor/probe.json) · [CP05 Player92](CP05RegressionPlayer/probe.json) · [正式森林Editor43](RegressionFormalEditor/probe.json) · [正式森林Player43](RegressionFormalPlayer/probe.json)。每层480组工厂规则在formal-rules.json；实际死亡及掉落身份在formal-death.json，不把规则对象算作实际收益。新GUID各自唯一，语义/身份/三随机流/XP/背包配对一致。

[20项配对汇总](analysis.json) · [2349项保护](protection-final.json) · [119产品源码/构建输入一致](product-input-match.json)。旧AdventureCombat只允许10处精确接入，原物理/时序/品质正文及其他冻结文件不变。

## 构建与发行

[基准摘要](BeforeBuild/release.summary.txt) · [测试包摘要](TestBuild/release.summary.txt) · [测试Bee](TestBuild/release.bee.json) · [纯包摘要](PureBuild/release.summary.txt) · [固定Profile](PureBuild/release.release.json) · [实际纯包Bee](PureBuild/release.bee.json)。

[18类IL/驱动剔除](assembly-audit.json) · [EXE/程序集身份](release-identity.json) · [包全文件SHA](release-files.json) · [测试输入](test-build-inputs.json) · [纯构建前](pure-build-inputs.json) · [构建后](pure-post-build-inputs.json) · [隔离写回](isolated-build-writes.json)。

[纯包启动/退出](PureSmoke/runtime.json) · [普通关闭](PureSmoke/close.json) · [纯包日志](PureSmoke/Player.log.gz)。只烟测，不是物理键鼠/人工战斗验收。最终布局在Player和ExtraEditorFinal使用；Editor核心旧布局脚本快照单列保留，没有冒充最终Player。

所有原生键鼠、人工观感/音质/手感/最终平衡、完整自主AI冒险和新Profiler指标NOT_RUN。历史Search、JobTempAlloc等引擎根因UNRESOLVED，完整原日志保留。受控截图、虚拟输入和API不可替代人工验收。

[Git索引与实际编译源码绑定](git-source-binding.json)：119项，仅既有CRLF规范化，原字节/索引SHA分别保留。
