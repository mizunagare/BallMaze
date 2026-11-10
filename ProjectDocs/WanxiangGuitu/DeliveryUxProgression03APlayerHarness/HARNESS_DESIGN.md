# HARNESS_DESIGN — UX-PROGRESSION-03A 真实 Player 验收工具链

批次：UX-PROGRESSION-03A-PH-R1（真实 Player 验收工具链修复）
分支：`verify/ux-progression-03a-player-harness`（基于 `feature/ux-progression-03a` @ `679815fc0a47a8aa19b54e1d5c1ae88d7a9fd50b`）
产品源码改动：**零**（全部工具位于 `Assets/CombatPrototype/Acceptance/`、`Assets/CombatPrototype/Editor/AcceptanceBuild.cs`、仓库根的 driver/build runner）

## 1. 架构总览

```
AcceptanceBuildRunner.sh                 一次构建链编排（3 个独立 Unity 进程）
  ├─ AcceptanceBuild.SetAcceptanceDefine     持久化 UX_ACCEPTANCE 脚本宏
  ├─ AcceptanceBuild.BuildAcceptance         构建 Acceptance EXE（harness 编入）
  │    └─ 构建产物中 grep 标记 UX_ACCEPTANCE_HARNESS_v1 → 写 Builds/acceptance_manifest.json
  │       （在 Assembly-CSharp.dll 中 grep，常量字符串为 UTF-16；EXE 启动器里没有）
  │       退出前显式 ResetDefine（EditorApplication.Exit 不展开 finally）
  └─ AcceptanceBuild.BuildNoDefine           无宏构建（harness 编出）→ 证明发行排除

player_acceptance_driver.py              每 Run 独立进程驱动 + 校验 + 证据留存
PlayerAcceptanceHarness.cs (#if UX_ACCEPTANCE)  运行在真实 Player 内的验收状态机
```

构建场景集：`Boot.unity → Title.unity → ForestRuins.unity`（三场景）。
Harness 经真实公开入口 API 授权，因此 Title 必须在包内；ForestRuins 是真实战斗场景。

## 2. Harness 状态机（全部走公开业务入口）

```
entry      GameEntry.GameSceneAuthorized？否则 Instance.Continue()，失败 AskNew()+ConfirmNew()
waitScene  等 GameEntry.Loading=false 且 CombatSession.Saves.IsInitialized（Boot 完成存档）
locate     session/hero/AdventureCombat/AdventureLoadout/WeaponSkillExpansion/NewWeaponCombat
setup      营地内配置装束：AdventureItems.New + GearItem.affixes（公开字段）+
           AdventureLoadout.AddOrStore/SelectMain + expanded.Select(slot)（新武器自动委托
           NewWeaponCombat.Select）；订阅 Observed/MeleeObserved
depart     AdventureFlow.Find(hero).DepartRuins() —— 新档案 AtCamp=true → BlockCombat=true，
           不出征则技能永远被禁；Departure 是唯一合法进入战斗的路径
rearm      确认 ActiveRun 非空、timeScale=1、重新 Select(slot)、PlayerInput.Focus(true)
warmup     1.5s 落地等待
cast1      注入真实 F KeyDown（InputSystem.QueueStateEvent，虚拟键盘），蓄力场景按住
           charge 秒后 KeyUp；观察 Observed start/complete
cooldown   期注入探针 KeyDown，验证 0.7s 内无第二次 start（冷却拦截）
cooldownAllow  skillStarts[0]+expectedCooldown+0.1s 后再次注入，验证第二次 start，
           实测冷却 = 两次 start 间隔（unscaledTime）
done       写 result.json；PASS 退出码 0 / FAIL 退出码 1
```

关键工程事实（本批实测发现，均已内建处理）：
- `CombatSaveSystem.Start` 在 `Application.isBatchMode` 下直接 yield break —— **不能以
  -batchmode 启动**，否则存档永不初始化、Run 挂死。
- 新档案 AtCamp → `AdventureCombat.Ready` 为 false → 技能被 BlockCombat 禁用；
  必须真实 Departure。
- Title/camp 期间 `Time.timeScale=0`，harness 内部计时全部使用 `Time.unscaledTime`，
  且不再擅自改 timeScale（营地 0 是合法状态，Depart 自己恢复 1）。
- `PlayerInput.Focus(true)` 内部调用 `Barrier()`，只能每次施法调用一次；每帧调用会把
  UIBlocked 永久置真、阻断全部输入。
- 宿主机存在物理键盘时 `Keyboard.current` 不一定指向注入目标；EnsureKeyboard 移除全部
  键盘后加装虚拟键盘，保证 PlayerInput 轮询的就是被注入设备。

## 3. 合规边界（任务 24 行约束）

- 只用公开 API：Continue/AskNew/ConfirmNew、AdventureItems.New、AddOrStore/SelectMain、
  expanded.Select、DepartRuins、PlayerInput.Focus/Barrier、GearItem.affixes 公开字段。
- 不写任何产品私有字段；不调用内部 Release/Hit/ApplyDamage；不直接杀敌；
  不伪造词缀效果（词缀通过公开 affixes 字段配置，由产品真实生效）。
- 输入为真实 InputSystem KeyDown/KeyUp，走 PlayerInput → AdventureCombat.UseSkill 原路径。

## 4. 用户数据隔离与 AppData 保护

- 每个 Run 独立目录 `Evidence/Runs/<run_id>/`，同时作为 `-wanxiang-storage-root`（游戏存档根）
  与 `--data-root`（harness 结果根）。
- 默认 AppData 存档目录（`AppData/LocalLow/DefaultCompany/万象归途/ForestRuins` 与
  `AppData/LocalLow/BallMaze/ForestRuins`）在整批测试前后做递归指纹（路径+大小+SHA256），
  必须零变化；缺失状态亦须保持缺失。每次自测/样本/矩阵均实时校验并记录。

## 5. Driver 每 Run 校验清单

1. 独立 Player 进程；记录 PID、完整命令行、起止时间、时长。
2. 硬超时 180s；超时先 terminate 再 kill，日志全部保留。
3. 退出码非 0 → FAIL（永不 PASS）。
4. result.json 修改时间必须晚于本 Run 启动（旧结果拒绝）。
5. result.runId / processId / buildSha 与启动记录逐一比对，不一致 → FAIL。
6. stdout/stderr/player.log/result.json/harness.log 全部留存于 Run 目录。
7. 不跨 Run 拼接断言；缺失/超时/身份不符一律 NOT_RUN/FAIL。
8. 自测（A）覆盖：标记存在/排除、KeyDown/KeyUp、身份一致、超时/异常退出/缺结果/
   旧结果拒绝、AppData 不变、Run 隔离。

## 6. 矩阵映射（25 行 → 真实动作）

- 旧武器（slot 1/2 = WeaponSkillExpansion）：sword.triple/spear.charge/staff.field/bow.burst=1，
  sword.circle/spear.sweep/staff.echo/bow.pierce=2。
- 新武器（slot 0/1 = NewWeaponCombat）：twin.volley/gs.cleave/sc.reap=0，gs.wave/twin.counter/sc.pull=1。
- 词缀 id：2=回响（area×1.25），5=聚能（冷却 +1s）。
- 描述一致性断言：`--desc-contains` / `--desc-excludes` 校验 `combat.SkillDescription`
  （面板渲染来源）中「含回响 +25%」的有无（#18/#19，R-1 边界）。
- T3 冻结（#13/#14）：真实施放双刃反击/灵魂牵引，按事件验收（start/complete 观测；
  #14 附加 0 伤害断言 `--expect-zero-damage`）。
- 纯 UI 面板行（#20-#24）与回归行（#25）保持 NOT_RUN，理由见 PLAYER_RUN_MATRIX.csv；
  其运行时来源已被对应真实运行覆盖（如 #18/#19 覆盖回响标注，#10-#12 覆盖数值）。

## 7. 已知局限

- 伤害断言为证据记录（damages/observations），不作为 PASS 门槛：英雄出生点位与敌人
  距离不可控，强行要求命中会引入假失败。冷却/生命周期断言是本批数值改动的核心验收点。
- UI 面板文本（AffixInfo/SkillTradeoffs）在无头环境不可可靠读取，对应行保持 NOT_RUN。
