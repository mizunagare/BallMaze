# 证据索引

本轮唯一源根I:/WGCombat/C1-1105-A。原件不改；发布件仅压缩/隐私脱敏，源SHA256和发布SHA256见[manifest.json](manifest.json)。Windows通用exe哈希不能单独绑定游戏，须同时核对程序集和[完整构建文件](build-files.json)。未提交供应商包、供应商源码或Player二进制。

- [最终有效/历史语义结果、Run/seed身份](validation-summary-final.json)：35个真实案例，915 PASS（Editor规则33、受控Editor441、非开发测试Player441），0当前FAIL。旧875条汇总另保留，不覆盖。
- [产品冻结输入](frozen-inputs.json)、[最终保护检查](protection-before-push.json)：1368项输入、2413项用户/旧产品保护、199项供应商源码。
- [六次实际Bee服务与二进制身份](build-services-final.json)、[原始构建元数据复制哈希](receipt-copies.json)。四完整测试包0错108警告、纯包0错104警告、前三区0错110警告；所有配置None/非开发。
- [纯包程序集核验1](assembly-final-1.json)、[2](assembly-final-2.json)、[3](assembly-final-3.json)、[4](assembly-final-4.json)：所列38关键类型IL、产品测试驱动及Editor/MapMagic引用排除。
- [首次驱动排除](pure-excluded.json)、[纯包实际启动/退出](PureRuntime1/pure-runtime.json)、[原样合成营地](CampPreparePlayer1/camp-fixture.json)。纯包只证明标题/可继续/实际后台关闭退出，原生菜单输入与人工试玩NOT_RUN。
- [实际硬件](hardware.json)、[Player有效CPU/Draw](FullPlayer1/performance.json)、[Editor采样](FullEditorFinal1/performance.json)、[地图实际计数](FullPlayer1/scene-metrics.json)。GC/GPU校准无效/未完成，不写0分配或性能达标。
- [四处隔离设置差异](isolated-settings-differences.json)：不回写用户文件，完整输入等同性UNRESOLVED。
- [全部原始警告/异常行号索引](warning-index-final.csv)、[初始基线缺口](Before1/before.json)、[旧未完成源码哈希](prior-files.json)、[只读包来源](package-provenance.json)。旧目录/分支和本轮所有失败保持。
- [独立作者保存数据](Authoring2/authoring.json)、[保存Scene无生成器](AuthoringScene1/scene-clean.json)、[自有地形镜头净空](CameraSkirtBake1/camera-skirt.json)。免费核心高度生成与自有孔洞/模块明确区分。

## 当前有效逐进程

每项链接原始语义回执；同目录还包括process.json、实际command/desktop回执、源工具快照、Unity.log.gz或Player.log.gz及原始轨迹。脚本/API受控操作不当作物理键鼠或人工试玩。

|案例|层|断言|语义|进程|
|---|---|---:|---|---|
|RulesFull10|Editor rules|33|[PASS](RulesFull10/rules.json)|[原始退出](RulesFull10/process.json)|
|FullEditorFinal1|controlled Editor|50|[PASS](FullEditorFinal1/probe.json)|[原始退出](FullEditorFinal1/process.json)|
|FullPlayer1|isolated nondevelopment Player|50|[PASS](FullPlayer1/probe.json)|[原始退出](FullPlayer1/process.json)|
|ResumeEditor1|controlled Editor|33|[PASS](ResumeEditor1/probe.json)|[原始退出](ResumeEditor1/process.json)|
|ResumePlayer1|isolated nondevelopment Player|33|[PASS](ResumePlayer1/probe.json)|[原始退出](ResumePlayer1/process.json)|
|FrontierResumeEditor1|controlled Editor|11|[PASS](FrontierResumeEditor1/probe.json)|[原始退出](FrontierResumeEditor1/process.json)|
|FrontierResumePlayer1|isolated nondevelopment Player|11|[PASS](FrontierResumePlayer1/probe.json)|[原始退出](FrontierResumePlayer1/process.json)|
|EliteEditor3|controlled Editor|20|[PASS](EliteEditor3/probe.json)|[原始退出](EliteEditor3/process.json)|
|ElitePlayer2|isolated nondevelopment Player|20|[PASS](ElitePlayer2/probe.json)|[原始退出](ElitePlayer2/process.json)|
|BossEditor2|controlled Editor|28|[PASS](BossEditor2/probe.json)|[原始退出](BossEditor2/process.json)|
|BossPlayer1|isolated nondevelopment Player|28|[PASS](BossPlayer1/probe.json)|[原始退出](BossPlayer1/process.json)|
|DeathEditor3|controlled Editor|17|[PASS](DeathEditor3/probe.json)|[原始退出](DeathEditor3/process.json)|
|DeathPlayer2|isolated nondevelopment Player|17|[PASS](DeathPlayer2/probe.json)|[原始退出](DeathPlayer2/process.json)|
|FaultEditor2|controlled Editor|14|[PASS](FaultEditor2/probe.json)|[原始退出](FaultEditor2/process.json)|
|FaultPlayer1|isolated nondevelopment Player|14|[PASS](FaultPlayer1/probe.json)|[原始退出](FaultPlayer1/process.json)|
|BossResumeEditor1|controlled Editor|33|[PASS](BossResumeEditor1/probe.json)|[原始退出](BossResumeEditor1/process.json)|
|BossResumePlayer1|isolated nondevelopment Player|33|[PASS](BossResumePlayer1/probe.json)|[原始退出](BossResumePlayer1/process.json)|
|CampPrepareEditor1|controlled Editor|24|[PASS](CampPrepareEditor1/probe.json)|[原始退出](CampPrepareEditor1/process.json)|
|CampPreparePlayer1|isolated nondevelopment Player|24|[PASS](CampPreparePlayer1/probe.json)|[原始退出](CampPreparePlayer1/process.json)|
|WeaponEditorSword2|controlled Editor|24|[PASS](WeaponEditorSword2/probe.json)|[原始退出](WeaponEditorSword2/process.json)|
|WeaponPlayerSword2|isolated nondevelopment Player|24|[PASS](WeaponPlayerSword2/probe.json)|[原始退出](WeaponPlayerSword2/process.json)|
|WeaponEditorSpear2|controlled Editor|24|[PASS](WeaponEditorSpear2/probe.json)|[原始退出](WeaponEditorSpear2/process.json)|
|WeaponPlayerSpear2|isolated nondevelopment Player|24|[PASS](WeaponPlayerSpear2/probe.json)|[原始退出](WeaponPlayerSpear2/process.json)|
|WeaponEditorStaff2|controlled Editor|25|[PASS](WeaponEditorStaff2/probe.json)|[原始退出](WeaponEditorStaff2/process.json)|
|WeaponPlayerStaff2|isolated nondevelopment Player|25|[PASS](WeaponPlayerStaff2/probe.json)|[原始退出](WeaponPlayerStaff2/process.json)|
|WeaponEditorBow2|controlled Editor|25|[PASS](WeaponEditorBow2/probe.json)|[原始退出](WeaponEditorBow2/process.json)|
|WeaponPlayerBow2|isolated nondevelopment Player|25|[PASS](WeaponPlayerBow2/probe.json)|[原始退出](WeaponPlayerBow2/process.json)|
|WeaponEditorTwin3|controlled Editor|31|[PASS](WeaponEditorTwin3/probe.json)|[原始退出](WeaponEditorTwin3/process.json)|
|WeaponPlayerTwin3|isolated nondevelopment Player|31|[PASS](WeaponPlayerTwin3/probe.json)|[原始退出](WeaponPlayerTwin3/process.json)|
|WeaponEditorGreat3|controlled Editor|31|[PASS](WeaponEditorGreat3/probe.json)|[原始退出](WeaponEditorGreat3/process.json)|
|WeaponPlayerGreat3|isolated nondevelopment Player|31|[PASS](WeaponPlayerGreat3/probe.json)|[原始退出](WeaponPlayerGreat3/process.json)|
|WeaponEditorScythe3|controlled Editor|31|[PASS](WeaponEditorScythe3/probe.json)|[原始退出](WeaponEditorScythe3/process.json)|
|WeaponPlayerScythe3|isolated nondevelopment Player|31|[PASS](WeaponPlayerScythe3/probe.json)|[原始退出](WeaponPlayerScythe3/process.json)|
|AssistEditor1|controlled Editor|20|[PASS](AssistEditor1/probe.json)|[原始退出](AssistEditor1/process.json)|
|AssistPlayer1|isolated nondevelopment Player|20|[PASS](AssistPlayer1/probe.json)|[原始退出](AssistPlayer1/process.json)|


## 实机截图（均明确受控来源）

- [非开发Player广场/机关门](FullPlayer1/plaza-door.png)、[地下密室](FullPlayer1/underground-hidden.png)、[守护者大厅](FullPlayer1/guardian-hall.png)。正常Orbit跟随，无后期裁切隐藏问题；不当成人工画面验收。
- [Player实际Boss战后](BossPlayer1/combat-Sword.png)、[Boss真实攻击轨迹](BossPlayer1/boss-trace.jsonl.gz)、[辅助真实释放](AssistPlayer1/assist-release.json)、[辅助实机](AssistPlayer1/assist.png)。战斗夹具使用可复现相机，不冒充普通玩家镜头手感。
- 七武器各目录combat-<类型>.png、corridor-<类型>.png、hall-<类型>.png；输入、原始Spawn/Flight/Collision与真实生命轨迹位于各runtime-trace.jsonl.gz。选择目标不等于命中。

## 历史与限制

[FAILURE_HISTORY](../FAILURE_HISTORY.md)链接所有首次失败和实际退出。65条旧probe/rules FAIL之外，初始3项缺口、编译、安全模式超时、作者工具和文档/编排错误另列。CameraColumnFixed1早期宽阈值不作为最终跟随证据；FullEditorFinal1/FullPlayer1新增arm一致性均0。FullEditor1仍是stage3，不能用于五区通过。

旧B3/B07受控规则结果在LegacyStreams1/b3-stream-results.txt和LegacyEconomy1/b07-economy.txt；B07夹具含合成填包/直接Damage，不计C1真实战斗。原始package、Player包和未脱敏日志保留本机；Git只含获准源码、自有资源、测试文本与证据。推送后完整SHA以交付回复及本机remote-after-push回执为准，推送不等于复审通过。
