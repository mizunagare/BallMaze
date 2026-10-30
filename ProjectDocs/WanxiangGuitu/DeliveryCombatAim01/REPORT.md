# COMBAT-AIM-01 交付（待固定 SHA 独立复审）

开工本地/远端 main：`804b4abbd36928618cd3629fc2e286787bfc44d6`。本批为实际产品修复，不宣称独立复审通过。最终完整 SHA 由提交后 `git ls-remote origin refs/heads/main` 核对并在交付消息返回；本提交不自引用不存在的提交哈希。

## 三批限定复审归档

任务书的审核结论按原范围登记，不改写为本代理独立审核：WORLD-01（eb11dd3d）源码/重点证据有条件接受，未执行分支保留；GAMEPLAY-UX04（77c4c8c3）目标完成、滚动、抓取/整理/双击及范围显示修复接受，低矮目标与原生指针手感不随之关闭；BALANCE-AI-01（804b4abb）首版经验/所查AI规则接受，高防御底伤、整体威胁与长Run压力仍开放。审核侧没有运行Unity/Player/人工，离线汇总复算不是游戏实测。完整原文归档于TASK_AND_REVIEW及Reviews，不回滚三批、不重做已有功能。

## 实际修改

- `CombatAim.cs`：仅接受角色实际绑定、同场景、有效的 OrbitCamera；相机中心射线确定意图，实际弓弦/杖首晶体发射点确定扫掠路径。相机不等于枪口，角色到枪口有墙时回退到合法起点，先碰实际遮挡。无有效相机拒绝远程攻击，不使用无关 Camera.main。
- `AdventureCombat.cs`：在相机 LateUpdate 后释放一次带版本/帧身份的共享三维解，HUD 使用同一解；远程身体 yaw 随相机，近战移动/转向规则保留。普通箭仍无重力，不自动锁敌。多箭/侧球围绕同一方向，保留伤害、速度、寿命、扇形角与品质数量。
- 初始重叠和极近目标也使用实际 Collider；墙内起始的弹体不得通过爆炸越墙。每颗箭仍独立扫掠、接触和结算伤害。暂停冻结、切武器保留已释放弹体，死亡/重置/卸载清理；UI、失焦、翻滚等取消未释放动作而不退冷却。
- 长枪从根点判断改为真实 Collider 与原球/锥/半宽交集，尺寸不扩大。偏心及多 Collider 可命中，真正体积外拒绝。有限迭代未收敛保守拒绝；不支持的非凸 Mesh/Terrain 不伪造可伤害接触，真实森林资源 Box 与敌人 CharacterController 已覆盖。
- HUD 增加中心准星、预测接触点和短遮挡提示；额外近战截线仅诊断视图启用。预测不等于命中确认。修正运行截图发现的准星文字裁切。
- `CraftingTargets.Name` 复用现有品质名称“普通·长剑”等，与物品、配方、追踪和成功提示一致；不改目标一次完成语义。

## 修复前证据与复验

seed418 固定真实 `node:22` 石头、`node:41` 铁矿、`enemy:1` 普通敌，记录完整几何和实际 HP/时序。石头顶部 .5943m、矿顶部 .5816m。旧版普通远程只沿身体水平方向，低目标/侧相机、长枪偏心、失焦调用及命名共 **18 PASS / 13 FAIL**；相同位置新实现 **31 PASS / 0 FAIL**。不宣称旧版所有极近敌人必定失败，旧1m普通敌样本确实命中。

矿前的真实石头会先挡住枪口路径：验证矿不受伤、前景石头受伤，不移走石头或强制穿透。早期不符合这一物理关系的断言和失败全部保留。

新增墙内起始爆炸负例曾确认墙后 HP 5000→4980，现已阻断。对非凸 MeshCollider 的 API 探针证明 ClosestPoint 不支持，保留原始警告，未添加宽松猜测 fallback。

## 本轮结果（不同层不混算）

| 层 | 实际结果 | 证据 |
|---|---|---|
| 固定内容配对 | 31 PASS | FinalPaired/before.json，对照 BeforeFinal/before.json |
| 有限几何/输入/生命周期 | 132 PASS | RulesExtended/rules.json |
| 四武器时序/品质/取消/生命周期 | 188 PASS | RegTiming/combat01.json |
| 法杖范围/弓独立箭/同形重复Collider | 34 PASS | RegArea3/area.json |
| 目标选择、真实制造/故障回滚、重启 | 2+195+3 PASS | CraftShared/matrix-*.json |
| 本轮上述规则断言合计 | **585 PASS / 0 FAIL** | FINITE_MATRIX.csv；不是585次独立冒险 |
| 最终非开发验收 Player | Core、Resume 两个进程 PASS | Runtime/Attempts/105021-Observe-629c60、105120-Observe-5085f8 |
| 纯发行非开发构建 | PASS；0错96警告 | ReleaseFinal/Results/build-report-messages.json |
| 带驱动非开发验收构建 | PASS；0错145警告 | Runtime/T/AimFinal/Results/build-report-messages.json |
| 原生 UI/U16、独立人工、完整正常AI出征结算 | NOT_RUN | 本批有限运行时用例不冒充完整冒险/人工 |
| D3D12 UNKNOWN、青色帧、历史 Search/C15 等根因 | UNRESOLVED | 原历史证据保持，不开展无新线索关闭实验 |

规则合计不重复计入早期108项/205项、循环内重复查询或旧批PASS。132项包括100次同状态查询的一个汇总断言。188/34等复用旧测试，显式调整测试相机和同形Collider夹具，原数值/伤害/弹数断言不放宽；详见 FAILURE_HISTORY。

## 实际运行时

复用 PLAYER02 原驱动/编排/独立指针中继，在隔离测试构建加入小型 partial，无 UnityEditor。真实 UI 新建合成档、选择实际弓/杖，实际移动靠近生成资源，虚拟输入经正式输入消费者发射、物理扫掠降低 HP；资源击碎后仍在地面，实际 E 拾取才进入背包及来源账。墙挡为明确标注的临时物理夹具，原资源不改高、不改Collider、不注入奖励；UI暂停用真实按键打开背包并取消前摇。F5 正常保存后第二进程继续，比较 Profile/Run/区域/seed/布局/三随机流/装备ID/来源账/库存/资源HP；没有恢复攻击或投射物。

最终 Core 有140条运行时检查（含有界循环重复检查），Resume6条，不等于146个独立实验。两进程退出码0、无超时、forcedTermination=false，日志与正常退出审计齐全。第一轮驱动等待过短的 exit1 保留；此前 Story2 的通过为中间记录，最终使用 FinalStory 新实例重新执行。

这些是**受控非开发运行时验收**，虚拟设备和排队窗口消息不叫原生键鼠。验收驱动结束时正常 Application.Quit，不等于真实标题栏关闭或UI-01根因关闭。截图是真实运行截图，近距离角色仍可能遮住部分目标，不宣称人工可读性或整体美术已验收。

## 构建、输入与保护

Unity6000.6.5f1，Windows64，BuildOptions.None。最终纯发行/验收构建完整输入、Player/Assembly SHA256、全部消息均归档。纯发行所有托管模块 PE 元数据扫描无 AIM/PLAYER02 运行时验收驱动类型、无 UnityEditor 引用；产品 CombatAim 是正常产品组件，不作测试驱动剔除。验收驱动只存在于隔离副本，未加入仓库 Assets。

索引源码与冻结输入规范化LF内容一致（code-commit-binding.json；Git文本属性可转换CRLF/LF）；六个授权源/元文件 SHA256 与工作源、测试副本、纯发行输入、验收输入逐一一致（authorized-source-inputs.json）。用户 ForestRuins、ProjectSettings、Recovery 五个原始文件 SHA256 均保持；旧交付不改写，v9类型、经济、掉落、经验、防御公式、地图和依赖无变更。警告及 JobTempAlloc 等原始日志保留，不以构建成功宣称引擎异常或性能已通过。

无新增蓄力、追踪、护甲/经验平衡或新地图。交付后暂停，等待固定SHA复审。
