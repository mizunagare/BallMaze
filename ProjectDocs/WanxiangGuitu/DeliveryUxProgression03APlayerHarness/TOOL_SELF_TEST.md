# TOOL_SELF_TEST — UX-PROGRESSION-03A 真实 Player 验收工具自测

批次：UX-PROGRESSION-03A-PH-R1
构建：Unity 6000.6.5f1，Acceptance EXE SHA256
`b70442f90f50cd91f7af7bf2272602645fc5d02c4d3156fb221fc27c328d2436`
（构建链三步 `set`/`acc`/`nodef` 全部 exit=0，`Builds/acceptance_manifest.json` 记录
markerPresent=true、buildWarnings、builtAt。）

## A. 工具自测结果（player_acceptance_driver.py selftest）

| # | 检查项 | 结果 | 证据 |
|---|--------|------|------|
| 1 | Acceptance 构建产物含 harness 标记 | PASS | Assembly-CSharp.dll（UTF-16 常量）grep 命中 |
| 2 | NoDefine（发行等价）构建产物不含标记 | PASS | 同一 grep 未命中（#if UX_ACCEPTANCE 编出） |
| 3 | EXE SHA 与 manifest 一致 | PASS | b70442f9… |
| 4 | 正向 Run：身份+新鲜度校验下 PASS | PASS | SELFTEST-positive-*/result.json |
| 5 | KeyDown 事件记录 | PASS | result.keyEvents pressed=true |
| 6 | KeyUp 事件记录 | PASS | result.keyEvents pressed=false |
| 7 | 观测到技能 start（真实业务事件） | PASS | WeaponSkillExpansion.Observed stage=start |
| 8 | 观测到技能 complete | PASS | stage=complete |
| 9 | 经公开 API 入口授权 | PASS | entryAuthorized=true（Continue→AskNew+ConfirmNew→DepartRuins） |
| 10 | 旧/陈旧 result.json 被拒绝 | PASS | 预置旧文件+短超时 → driver FAIL，理由含 stale |
| 11 | 错误 buildSha 被拒绝 | PASS | result.buildSha=DEADBEEFWRONG ≠ EXE SHA → FAIL |
| 12 | 超时→FAIL（永不 PASS），进程受控关闭 | PASS | 6s 硬超时，terminate→kill，exit 非 0 |
| 13 | 超时 Run 保留 stdout/stderr/player.log | PASS | Run 目录三文件齐备 |
| 14 | Run 隔离（每 Run 独立根目录） | PASS | Evidence/Runs/ 每次自测独立目录 |
| 15 | 默认 AppData 存档零变化 | PASS | default_save/legacy_save 指纹前后一致（含"缺失保持缺失"） |

结论：**SELF-TEST OK（15/15）**。

## B. 正向 Run 的真实业务证据（sword.triple，期望冷却 7s）

- 实测冷却（两次 start 间隔，unscaled）：**7.107s**（期望 7s，03A 由 8s 调整为 7s）。
- 冷却期内注入探针 F：未产生第二次 start（blockedDuringCooldown=true）。
- 冷却结束后第二次施法成功（skillStarts 两条）。

## C. 3 个小样本（B 阶段）

| Run | 场景 | 实测冷却 | 期望 | 冷却拦截 | 结论 |
|-----|------|---------|------|---------|------|
| SAMPLE01 | sword.triple（旧武器普通技能） | 7.116s | 7s | 是 | PASS |
| SAMPLE03 | spear.charge（旧武器蓄力 0.6s） | 8.107s | 8s | 是 | PASS |
| SAMPLE10 | gs.cleave（新武器 Greatsword slot0） | 9.107s | 9s | 是 | PASS |

原始日志与业务事件位于 `Evidence/Runs/SAMPLE01|03|10/`（result.json/harness.log/
player.log/stdout/stderr/entry-audit.jsonl）。

## D. 自测过程中发现并修复的工具缺陷（留档）

1. `KeyboardState` 需 `UnityEngine.InputSystem.LowLevel` 命名空间（CS0246）。
2. MiniJson 模式变量 `d` 作用域冲突（CS0136）与非泛型 `IEnumerable` 解析（CS0305）。
3. 标记 grep 误查 EXE 启动器——常量字符串在 Assembly-CSharp.dll（UTF-16）；改为
   dll+exe 双查。
4. `EditorApplication.Exit` 不展开 try/finally —— UX_ACCEPTANCE 重置必须显式在
   Exit 前执行，否则宏泄漏进 ProjectSettings 污染 NoDefine 构建。
5. `-batchmode` 下 `CombatSaveSystem.Start` 直接 yield break → 存档永不初始化 → Run 挂死；
   改为真实窗口 Player 运行。
6. `Time.timeScale=0`（Title/营地）冻结 `Time.time` —— harness 内部计时全部改为
   `Time.unscaledTime`，且不再越权改 timeScale。
7. 新档案 AtCamp → BlockCombat —— 必须经 `DepartRuins()` 真实出征才能施法。
8. `Focus(true)` 每帧调用会让 `Barrier()` 每帧执行 → UIBlocked 永真 → 输入被阻断；
   改为每次施法仅调用一次。
9. Windows 覆盖写文件保留 ctime —— driver 新鲜度改用 mtime；自测 Run 目录用
   每次唯一 id，历史不被覆盖。
