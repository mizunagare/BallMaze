# COMBAT-02 复审与 COMBAT-02-R1 任务书

## 1. 固定 SHA 复审

仓库：`mizunagare/BallMaze`  
开始：`71877635f3b5891abeccaff4032045156ce8af85`  
最终：`fc11e2a3ee2d3a31254ce7625b7ff9da3a636b5a`  
已重新读取远端 `main`，完整 SHA 一致。

证据：
- [报告](https://github.com/mizunagare/BallMaze/blob/fc11e2a3ee2d3a31254ce7625b7ff9da3a636b5a/ProjectDocs/WanxiangGuitu/DeliveryCombat02/REPORT.md)
- [验收表](https://github.com/mizunagare/BallMaze/blob/fc11e2a3ee2d3a31254ce7625b7ff9da3a636b5a/ProjectDocs/WanxiangGuitu/DeliveryCombat02/ACCEPTANCE.md)
- [复跑说明](https://github.com/mizunagare/BallMaze/blob/fc11e2a3ee2d3a31254ce7625b7ff9da3a636b5a/ProjectDocs/WanxiangGuitu/DeliveryCombat02/TESTING.md)
- [武器数据](https://github.com/mizunagare/BallMaze/blob/fc11e2a3ee2d3a31254ce7625b7ff9da3a636b5a/ProjectDocs/WanxiangGuitu/DeliveryCombat02/WEAPON_DATA.md)
- [证据索引](https://github.com/mizunagare/BallMaze/blob/fc11e2a3ee2d3a31254ce7625b7ff9da3a636b5a/ProjectDocs/WanxiangGuitu/DeliveryCombat02/Evidence/INDEX.md)

## 2. 复审结论

**剑/枪差异化实现，在有限受控测量范围内有条件接受；COMBAT-02 整批仍为 FAIL。**

交付方总表为 `17 PASS / 1 历史预期 FAIL / 4 NOT_RUN / 7 UNRESOLVED`，另外首次恢复链有4个 exit1。它们是一个首因和三个依赖失败，不是四个独立产品缺陷，但不能忽略。

### 已接受的限定改动

- 枪普攻半径参数 3.8→3.1 米（仍叠加 ReachBonus），横向半宽 .85→.4，前向 dot 保留 .88。
- 枪普攻间隔乘 1.30、基础威力乘 1.25；白装由 33/.5s 调整为 41.25/.65s。
- 枪的前刺反馈与剑的弧光分离；近战提示不再用扩张整圆模拟枪刺。
- 保留技能、品质分支、长枪追加段、弓独立箭、法杖 AoE、经济、掉落、随机流和 v9 合同。
- 10cm边界测量显示枪/剑前向距离比约 1.54–1.62，支持长枪更远、侧向更窄的设计目标。
- 旧188项战斗规则在更新基础普攻预期为 `BasicPower` 后通过；原187/1失败历史保留。

### 数据限制

- 每武器/体型短战 n=2，只能支持首轮方向，不能证明平衡完成。
- 网格命中数39→23是固定采样覆盖，不是玩家命中率。
- 受控截图不能证明实际手感、声音反馈或玩家可读性。
- 非开发构建0错误、94警告，不等于发行 Player 战斗验收通过。
- 本次审查了报告、验收表、源码、武器数据、失败历史和恢复诊断；没有在 Windows 上独立运行 Unity。运行结果属于交付方证据。

### 阻断项 U07：首次恢复链失败

首次 `B07Rules.Run` 在40次导航请求（39个不同接受 seed）后，读取原出征的 Single 查找 Boss 失败。后续三个依赖进程因缺少 `b07-expected.txt` 失败。四个 exit1 原样保留。

另一个新 Run 加入只读 Dump 后，Run/Resume/Pending/Committed通过；但 Run ID 和 seed 不同，也未采集首次失败瞬间状态。因此不能据此关闭 U07。

原生 U16、独立人工试玩、最终发行 Player 战斗操作和完整性能预算仍 `NOT_RUN`。旧 C15、D3D12 UNKNOWN、Editor 青色帧、Search、JobTempAlloc、旧 Editor 启动阻塞仍 `UNRESOLVED`。

## 3. 下一批 COMBAT-02-R1：恢复首因只读诊断

开始基线：`fc11e2a3ee2d3a31254ce7625b7ff9da3a636b5a`。

本批不是新玩法开发。目标是捕获首次 `B07Rules.Run` Boss 查找失败的首因，区分产品恢复/生成问题与测试夹具、对象查找、场景实例或运行器问题。先诊断，不改产品恢复代码。

### R1-01 固定输入
- 开工先核对远端 `main` 完整 SHA；若已前进，停止并报告，不重置或覆盖工作区。
- 从原 `Recovery-Run` 证据恢复测试源版本、命令、地图/区域、Run ID、请求/接受 seed、revision、targetWave、生成版本和预期 Boss 身份。
- 标明哪些输入可精确重放，哪些缺失；不得伪造状态。若只能近似重放，明确标注。
- 使用新隔离拥有者根和合成存档；不访问真实存档、不抢占用户 Editor、不强杀进程。
- 原首次失败和三个依赖失败不能覆盖或改写。

### R1-02 失败点只读诊断
在隔离测试副本的失败点增加只读诊断，或使用独立诊断驱动。不得修改产品 `Assets` 中的恢复、导航或生成逻辑来帮助通过。

至少记录：
- PID、Unity版本、执行方法、场景名/句柄、阶段与初始化完成标志。
- `AdventureFlow` 的 Enabled/Tracking/AtCamp、ActiveRun ID、Region、regionInstanceId、requested/accepted seed、generationVersion、revision、targetWave。
- `RuntimeForest` 实例数、scene/scene handle、Boss Brain/Kind/稳定身份、active/enabled 状态及所属区域实例。
- `CombatSession.enemies` 与场景实际对象的 ID/引用对应，不能只输出名字。
- 40次请求的 requested seed、接受状态、fallback、生成尝试与失败列表。
- 查找前后场景卸载/重建、对象替换、异步初始化、fixture清理情况。
- 首次异常完整调用栈、时间戳、退出回执、测试源 SHA、产品输入 SHA。

若稳定复现，至少3个独立进程；若不稳定，报告真实次数与失败率，不降低断言或放宽超时来获得PASS。

### R1-03 分类与修复边界
- 若证据确认是测试夹具/运行器问题，允许只在隔离测试工具中做最小修复，产品输入哈希必须不变，修复后至少3个独立进程通过。
- 若证据指向产品恢复/生成状态不一致，停止并提交根因证据与最小修复方案，等待授权；本批不得修改产品行为。
- 若证据不足，继续 `UNRESOLVED`，不能因另一个Run通过或工具退出0而关闭。

### R1-04 交付
提交报告、验收表、复跑说明、证据索引、原始诊断、输入/产物哈希、用户文件保护哈希。保留旧4个exit1和原 `aggregate-status.json`。更新 `DEVELOPMENT_PLAN.md` 只增量记录，不覆盖历史。推送后核对远端完整 SHA，暂停等待独立复审。

## 4. 给 Codex 的执行指令

读取本文件。只诊断 COMBAT-02 首次 `B07Rules.Run` Boss 查找失败。默认不修改产品恢复/生成逻辑；只有证据确认是隔离测试夹具/运行器问题，才允许最小修复测试工具。若怀疑产品问题，停止并提交方案等待授权。

保护用户场景、ProjectSettings、未提交修改和真实存档；不升级依赖、不新增 CI、不关闭用户程序、不强杀进程。保留所有旧失败。推送后核对远端完整 SHA，交付报告与证据链接后暂停。
