# CP06-A：四武器技能扩展

开始基准 `397d53fe87ce5b6c490c86c63d59015de26a46af`；独立分支 `feature/cp06-skill-expansion`。最终完整SHA为本文件所在提交，在交付消息与远端核验。不合并main，未修改CP05历史分支。

已实际接入8个新技能，每武器两个，原技能保留在槽0，新增槽1/2通过真实uGUI按钮选择，沿用可重绑定的Skill输入释放。不是占位按钮或纯设计提案。

- 长剑：三拍连斩、回旋剑阵。
- 长枪：蓄势穿刺、扫锋拒敌。
- 法杖：余烬符阵、回响连珠。
- 弓：追点连射、蓄势贯矢。

[设计](SKILL_DESIGN.md) · [完整配置/机制矩阵](WEAPON_SKILL_MATRIX.md) · [实现及共享系统风险](IMPLEMENTATION.md) · [验收](ACCEPTANCE.md) · [失败历史](FAILURE_HISTORY.md) · [证据](Evidence/INDEX.md)

## 真实实现

在AdventureCombat做10处精确接入，原Release、MeleeGeometry、Melee、Fire、Sight、TrackMelee及旧AdventureProjectile正文不变；新增WeaponSkillExpansion、SkillPhysicalEffects、WeaponSkillPanel。独立ID/配置集中定义，实际前摇、分段释放、蓄势、取消和恢复由新状态机控制；默认原技能及原数值继续运行。

远程逐段用现有CombatAim和TargetAssist从真实武器枪口求解，弹体物理碰撞后才能经WeaponHit伤害。新贯矢初始重叠/有序SphereCast、实体去重、实心墙终止；符阵只从真实弹体Impact产生，固定位置三次真实范围/遮挡查询。近战调用现有物理几何，保留有限面向，没有新增攻击位移或Damage注入。现有动画剪辑、音效通道、轨迹及碰撞反馈复用；没有引入新素材。

新技能共享现有v9技能冷却；取消不退款，已释放物在暂停时冻结、恢复继续，切武器不清除已发弹体。选择是临时配置，读取后回到旧槽0，剩余冷却仍阻止旧槽绕过；不新增存档字段、不重放未释放动作。

## 实际结果（本轮重新运行）

| 层次 | 核心技能 | 衔接/输入/死亡 | 前摇保存 | 新进程恢复 | CP05训练 | 正式森林 | 合计 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Editor | 157 PASS | 14 PASS | 7 PASS | 10 PASS | 92 PASS | 43 PASS | 323 PASS/0 FAIL |
| 非开发测试Player | 157 PASS | 14 PASS | 7 PASS | 10 PASS | 92 PASS | 43 PASS | 323 PASS/0 FAIL |

共646条功能断言PASS，历史失败另列，未被覆盖。另20项语义/配对汇总与上述断言有重叠，不重复相加。[analysis.json](Evidence/analysis.json)检验回执非空、唯一名称、无错误，以及旧8条普攻/技能的实际伤害、发射数和冷却配对一致。

每层正式森林另有480组旧品质/词缀/随机流规则数据（32种子×5进度×3分支，不是480场战斗），以及同一真实合成Run继续后的实际剑击死亡、来源身份、掉落语义、XP/等级、背包和三流配对一致。CP05连续重开、失败重试、掉落唯一性和卸载重进也重新通过，不继承旧PASS。

8技能均记录真实释放、物理碰撞、实际健康变化及截图。八种墙阻挡、额外Collider去重、取消不发伤害/不退冷却、虚拟Held蓄势、3个真实目标贯穿、暂停/切武器后的真实命中、符阵暂停恢复、旧辅助面向/自由镜头等独立覆盖。新技能支持普攻衔接，未增加无冷却互取消或大型连招系统。

首次贯矢阵列的两类FAIL保留：世界Z轴阵列与汇聚弹道不共线；低位相机导致箭真实撞地，第三目标未受伤。最终正向阵列在释放前固定3/4.5/6米及斜线位置，以躯干高度瞄准；没有射后移动敌人、关碰撞、改伤害或降低三目标断言。原错误阵列不被改写为成功。

## 版本、构建及保护

基准测试包0错误/100条BuildReport警告；最终测试包0错误/107警告；纯发行包0错误/98警告。完整原日志和摘要保留。纯包Development=false，固定PRIVACY-A Profile SHA和实际Bee五项服务false；[assembly-audit](Evidence/assembly-audit.json)确认18类产品IL与验收包一致，且无CP6/CPC/旧测试驱动、UnityEditor或测试原生桥引用。

纯发行包本机 `I:/WGCombat/CP06A-1104-A/PureBuild/Release`，真实启动训练及普通关闭exit0，**只烟测**，不是纯包人工战斗通过。EXE SHA256 `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`；Assembly-CSharp SHA256 `c7c56f1ae45306f54e69c25b2bc3c9eee1c8ba2f81bb5eacbf63f5f9729939a8`；[全文件哈希](Evidence/release-files.json)。

[保护](Evidence/protection-final.json)：2349项既有文件核验，仅允许的AdventureCombat发生10处接入；其余产品、用户场景/ProjectSettings/未提交文件不变。另新增3脚本及meta。CP04 CombatAim、CP05 TargetAssist/OrbitCamera/CameraActorFade、掉落/经济/随机流及v9源码冻结。119个产品脚本与最终实际构建输入逐字节匹配；[输入及构建写回](Evidence/isolated-build-writes.json)单列，不用EXE壳哈希代替程序集身份。

Editor核心运行后仅将技能面板下移20px避开已有辅助提示；该旧布局脚本快照保留于AfterEditorFinal，最终布局已在ExtraEditorFinal、保存/恢复、旧回归及全部Player运行使用。未把旧Editor截图冒充最终Player画面。

## 未关闭事项

原生物理键鼠、独立人工观感/音质/手感、最终平衡、完整自主AI冒险及新Profiler性能测量均NOT_RUN。虚拟InputSystem、API、受控截图不替代这些项目。新技能样本为功能/边界验证，不足以宣称四武器全面平衡或所有新技能词缀组合完成。

Editor.Search内部异常及退出JobTempAlloc日志继续UNRESOLVED；历史D3D12 UNKNOWN、青色帧、旧关闭样本根因等不因本批通过而关闭。Bee服务关闭不等于所有OS/CrashHandler外发路径绝对关闭。完成推送后停止等待固定SHA独立复审。

Git既有属性对源码CRLF/LF进行规范化，[119项索引绑定](Evidence/git-source-binding.json)同时记录实际编译原字节SHA和Git索引SHA；仅投影既有换行策略后逐字节一致，不忽略任何代码。
