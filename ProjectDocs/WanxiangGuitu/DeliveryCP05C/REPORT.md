# CP05-C：训练场重开与临时掉落

开始基准：`7fc4f5dc3043bcbb69f63c2ebf267359741ccbbe`。分支 `fix/cp05-training-restart-loot`；最终完整 SHA 由本报告所在提交及远端核验确定。不合并 main。

已修复两个实际产品缺陷：重开使用事务式场景替换，失败保留旧实例并可重试；训练死亡使用场景私有临时掉落上下文，沿用真实死亡、装备生成、地面掉落与经验路径，不创建假 CombatSession/Wave，不写正式存档。

## 修复前证据与原因

- [BeforeTraining/probe](Evidence/BeforeTraining/probe.json)、[Editor原始日志](Evidence/BeforeTraining/Unity.log.gz)：真实长剑攻击致死后，普通装备分支访问不存在的 `CombatSession.Wave` 抛空引用；第一次重开后，固定名称的 Restart scene 第二次创建冲突。
- [BeforePlayer/probe](Evidence/BeforePlayer/probe.json)、[Player日志](Evidence/BeforePlayer/Player.log.gz)：同一基准的非开发测试 Player 独立复现，实际退出码1。各层11 PASS/9 FAIL，未改写为通过。
- 生命周期审查还发现新训练 UI 借用即将卸载场景的 EventSystem；现每个场景拥有一个，并有实际回归。

## 最小实现与正式路径保护

- `CP05Training.cs`：唯一作用域/递增场景名；新实例完整后才卸载旧场景；恢复旧对象、时间状态与上下文；只清理本次拥有的场景及材质；单一事件订阅，外部卸载销毁DDOL控制器。
- `TrainingLootContext.cs`：场景级临时三随机流、显式英雄归属、正式Run场景拒绝注册、禁用/销毁注销。只服务现有普通训练敌人，不新增Boss训练机制。临时掉落不会结算入仓，退出训练即清理。
- `CombatEnemy.cs`：保留死亡门槛和先设 `lootDropped`；仅普通装备生成分支选择训练上下文或原 Session 路径。概率、经验、材料范围、Boss逻辑和调用顺序保持。
- `AdventureItems.cs`：原 `Roll` 的随机抽取及进度luck原顺序不变，共用同一品质/type/affix工厂；训练显式无进度加成，不假设波次存在。
- `AdventureRandom.cs`：只为已登记训练场景返回私有流，防止死亡后升级选项等抽取消耗 Unity 全局状态。未登记owner和null仍执行原正文。

[设计与逐项合同](DESIGN.md)。没有直接重置旧角色生命或修改其库存，重开通过原Prefab工厂生成新实例。没有注入Damage、伪造奖励或改写存档。

## 实际验证

| 层 | 本轮结果 | 证据 |
|---|---|---|
| Editor训练 | 92 PASS / 0 FAIL | [AfterTraining4](Evidence/AfterTraining4/probe.json) |
| 非开发测试Player训练 | 92 PASS / 0 FAIL，实际exit0 | [AfterPlayer](Evidence/AfterPlayer/probe.json)、[进程](Evidence/AfterPlayer/runtime.json) |
| Editor正式森林 | 43 PASS / 0 FAIL | [AfterFormal](Evidence/AfterFormal/probe.json) |
| 非开发测试Player正式森林 | 43 PASS / 0 FAIL，实际exit0 | [AfterPlayerFormal](Evidence/AfterPlayerFormal/probe.json) |
| 配对数据核验 | 16 PASS / 0 FAIL，包含上述语义复核，不与功能数累加 | [paired-results](Evidence/paired-results.json) |
| 源审计自测 | 8 PASS，包括7个篡改负例 | [audit-selftests](Evidence/audit-selftests.json) |
| 产品/用户哈希 | 2,347项原文件核验；仅4个准许既有脚本变化，另新增上下文及meta | [protection-final](Evidence/protection-final.json) |
| 纯发行构建 | 成功，0错误/98条BuildReport警告；Development=false | [构建摘要](Evidence/PureBuild/release.summary.txt)、[实际Bee](Evidence/PureBuild/release.bee.json) |
| 纯发行启动/关闭 | READY后普通窗口关闭，实际exit0；未自动战斗 | [PureSmoke](Evidence/PureSmoke/runtime.json) |

训练检查覆盖连续3次、暂停、真实AI致玩家死亡后重开、真实名称冲突回滚/重试、6次实际敌人死亡、5次重复掉落请求、旧敌人/三件独占世界材质销毁、事件注销及重新进入。每次真实死亡有[轨迹](Evidence/AfterPlayer/deaths.jsonl.gz)，场景清理有[轨迹](Evidence/AfterPlayer/restarts.jsonl.gz)。已有合成v9存档在训练全过程字节不变，地面掉落不提前入袋。

正式配对每层480组规则（32种子×5进度输入×普通/寻宝/Boss品质分支），不是480次战斗；不保存或领取这些受控工厂对象。另从原样复制的真实产品检查点继续同一森林Run，以真实剑攻击杀敌。前后Run/region/seed/目标ID、三随机流、XP/等级、实际掉落语义逐字段一致；新地面GUID分别验证唯一。没有重新生成测试存档或人为指定掉落结果。

## 构建及限制

测试构建0错误/102警告；基准测试构建100警告；纯发行98警告。完整日志保留。纯包剔除CPC驱动，12类产品IL与最终测试包一致，无UnityEditor或测试原生桥引用：[assembly-audit](Evidence/assembly-audit.json)。116项同目录产品脚本与实际构建输入逐字节一致：[input-match](Evidence/product-runtime-input-match.json)；纯构建前后隔离输入无变化：[build-writes](Evidence/isolated-build-writes.json)。固定PRIVACY-A Profile及五项实际Bee服务false，未修改用户配置。

纯包本机：`I:/WGCombat/CP05C-1104-A/PureBuild/Release`。EXE SHA256 `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`；产品程序集 `f746791802ca599cac4096229cb6ed1f666804e1a6aa15e578c0c0b12895cdaf`。[全文件哈希](Evidence/release-files.json)。EXE壳哈希相同不等于产品相同，故同时记录程序集及完整文件清单。

Editor退出仍有JobTempAlloc诊断，根因UNRESOLVED。历史D3D12 UNKNOWN、Editor青色帧等不因本批通过而关闭。原生键鼠、人工观感/独立试玩与新增性能测量均NOT_RUN。测试按钮回调、真实武器业务API、后台普通关闭都不冒充原生操作。纯包只做启动/退出烟测，复杂功能来自独立非开发测试Player，二者分层。

所有首次失败、编译失败、夹具失败和审计工具失败见[FAILURE_HISTORY](FAILURE_HISTORY.md)，不继承历史PASS，不宣称独立复审通过。交付后停止等待审核。
