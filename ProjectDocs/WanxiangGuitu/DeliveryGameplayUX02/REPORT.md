# GAMEPLAY-UX02 交付报告

制定基线 `ab6b350ba900894f74efe29a803631271ed6ce7a`；开工远端/实际源码基线 `5ecaced7a0886d34698632ff36bc44ed41e71e7f`，中间仅新增TASK与计划，已正常快进。最终完整SHA见包含本报告的提交与交付回复；不将冻结输入冒充最终SHA。本批等待独立审核，不自行认定通过。

## 审计与最小修复

[设计/事件图](DESIGN.md)及[54项资源、46调用点清单](resource-call-inventory.json)核对CombatFeedback、动画载体/猫族绑定、真实Damage、四武器、普通敌信号、两类Boss预警、相机与资源所有权。既有KayKit legacy Animation由SampleAnimation采样；猫族为随骨骼挂点的刚性部件，翻滚仍程序化。7种音效由CombatSoundBank合成，非外部录音；既有KayKit/Kenney资源许可CC0已在工程Licenses中，无新资源/依赖。

产品仅 `Assets/CombatPrototype/CombatFeedback.cs` **三行修改**：

1. 真实0.25致死承伤原显示“−0”；保留两位小数，正承伤不足0.01显示“<0.01”，不伪报零伤害。原始float承伤仍记录在Observed，显示不是伤害计算。
2. 禁用组件后，Find仍能找到它，旧Paused未拒绝，新Damage继续建立数字/特效。Paused加入isActiveAndEnabled；拖尾遵守相同可用门。Damage仍生效，恢复启用后真实命中正常反馈。

未改伤害、几何、范围、释放比例、冷却、AI、护甲、经验、掉落、经济、地图、随机流、v9或迁移。未重建动画、音效或VFX框架。

## 本轮实际结果（分层，不相加当作通过率）

| 集合 | PASS | FAIL | 含义 |
|---|---:|---:|---|
| Before7 | 111 | 4 | 正式修复前负例，2类根因 |
| After2 | 115 | 0 | 同条件、同夹具完整复测 |
| AfterExpanded | 119 | 0 | 增加真实未命中/实体遮挡反例 |
| MissingGlow | 119 | 0 | 隔离副本实际移走Glow资源，验证既有Shader fallback与自建材质销毁；原SHA已恢复 |
| Runtime | 119 | 0 | 非开发验收Player，真实运行时代码，公开战斗/Damage调用与受控夹具；非原生输入/正常AI/人工 |
| BossGeometry | PASS | 0 | 6534个共享命中几何样本、36组HUD矩形；数据规则，非实战体验 |

四武器各普攻/技能有真实Action ID、启动/释放/结束帧、Motion/PoseTime和实际Damage记录；普通、远程、精英、普通Boss、森林双Boss及玩家的承伤/致死状态有独立断言。取消未释放攻击没有Damage/假命中数字；实体墙阻挡的法杖弹体不伤及墙后目标。暂停冻结特效/数字/相机时钟，容量检查为24特效/32数字/10声道。Reset、禁用/恢复、生成AudioClip销毁及共享/自建材质所有权实际执行。

[事件对照](TIMELINES.csv)、[完整分层结果](SUMMARY.json)、[命令/退出记录](RUNS.csv)。Damage事件标识采用原JSONL文件路径+1基行号；关联攻击是固定夹具上下文，HealthObservation不提供攻击者，未虚构引擎攻击者ID。seed/Profile/Run/生成版本见SUMMARY身份表及各合成save.json原封装；未直接修改最终存档。

## 必须保留的失败与边界

所有首次准备、夹具初始化顺序、碰撞体误禁用、变量重名编译、batch无GameView推进、正常关闭/期限退出均在[失败历史](FAILURE_HISTORY.md)和原始目录，绝不被后续PASS覆盖。

Before6/After/AfterTrace的法杖1.5m侧置相机样本未命中仍保留。弹体观察实际返回CAMERA_SURFACE_BEHIND_MUZZLE，没有接触目标，也没有虚构Damage/Hit反馈。后续6m为**不同条件的命中对照**；没有把远距成功宣称修复或关闭近距体验风险，没有修改CombatAim。该行为是否需要后续产品调整待独立任务/人工评估。

普通Boss三招做源码核对，森林六招做共享数据/Show-Hide/无Collider核对；不宣称正常AI讨伐或所有实际Boss攻击组合通过。音效通道配置/限流/抢占、距离衰减和生命周期做技术核对，未测真实声学质量。缺失Glow的Editor降级已执行，但缺失Shader/全部音频设备/全部Prefab组合没有可靠样本仍NOT_RUN。完整场景卸载/重建压力矩阵、正常AI冒险、本批动态录屏/人工观感未执行，不继承旧PASS。

## 构建与运行边界

Unity 6000.6.5f1，Windows Standalone，原构建入口Options=None：

- 隔离验收构建：0错误、97警告；包含GUXCases/GUXPlayer，代码只置于隔离Assets/GUXAcceptanceOnly。
- 验收Player：Boot→Title→显式受控新游戏确认→真实运行时119断言；实际exit0、timedOut=false、forcedTermination=false。不是原生点击，也不是标题栏/退出保存验收；夹具SuspendEntry后退出。
- 纯发行构建：0错误、96警告。PE确认不含GUX/既有测试驱动类型、无UnityEditor引用。未宣称纯发行原生操作通过。

全部警告/日志、exe/UnityPlayer/Assembly-CSharp SHA256、完整构建输入与7份关键产品源码匹配见Evidence。逐帧磁盘日志有观测开销，本批未测其CPU/GC/GPU开销，完整性能NOT_RUN，不用零值代替。没有性能优化结论。

## 保护与开放项

用户ForestRuins、ProjectSettings与Recovery五项原SHA256不变，不提交覆盖层。测试根 `I:/WGCombat/GU02-1030-B`，旧失败A副本保留；副本使用Git场景/设置，用户输入仅工程外留存。Glow故障实验只移动隔离资产并原SHA恢复。未读取真实玩家存档、激活用户桌面、关闭用户程序或强杀进程；无依赖升级/CI。

原生U16、人工可读性、动作观感、音效质感、舒适度、趣味和最终打击感继续NOT_RUN。UNKNOWN、旧C15、青色帧、Search、JobTempAlloc根因继续UNRESOLVED；本轮Search/JobTempAlloc原上下文另索引，exit0不等于干净引擎退出。

[验收](ACCEPTANCE.md) · [复跑](TESTING.md) · [原始证据索引](Evidence/INDEX.md)。提交推送后暂停等待固定SHA独立复审。

Raw Runtime.layer/scope沿用旧启动器的“virtual”分类标签；本批未发送InputSystem虚拟键鼠事件。准确层级为公开Strike/UseSkill/Damage业务API的受控验收Player，不能用这些回执证明原生或虚拟键鼠输入送达。实际驱动源码与构建输入均原样保留。
