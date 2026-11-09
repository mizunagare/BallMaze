# CP06-INTEGRATION-02 · 复现与测试说明

## 1. 环境

| 项 | 值 |
|---|---|
| Unity | `6000.6.5f1` |
| 候选 | `integration/cp06-playable-candidate` @ `2964ad7413d2644f23c12a8c82e1d439e2884a01` |
| 构建命令 | Unity 批处理 `WanxiangBuild.ValidateBuild`，环境变量 `UNITY_TEST_ROOT` 指向**项目工作树外**目录 |
| 纯构建产物 | `I:/WGInt02Release/Release/WanxiangGuitu.exe`（SHA256 `001aeebf…`） |
| 观察副本 | `I:/WGInt02Obs/Release`（驱动仅注入此副本） |
| 运行根 | `I:/WGInt02Runs/<run>`（每 run 独立，含隔离存储根） |
| 证据归档 | `I:/WGInt02Evidence/<run>` → 已复制到本交付 `Evidence/Player/<run>` |

## 2. 构建纯发行（INT02-01）

```bash
# 关键：输出根必须在项目工作树之外（Bee 路径规范化要求），并先清理损坏的 Bee 缓存
UNITY_TEST_ROOT="I:/WGInt02Release" <Unity批处理执行 WanxiangBuild.ValidateBuild>
# 产物: <root>/Release/WanxiangGuitu.exe + .release.json（身份三元组 SHA256）
```

隐私门禁（ReleaseDiagnosticsGuard）在 `OnPostprocessBuild` 强制：Bee 输入唯一匹配、
Unity 版本、Profile 身份、遥测全禁。任一失败即构建失败。

## 3. 编译并注入验证驱动（仅观察副本）

```bash
cd ProjectDocs/WanxiangGuitu/DeliveryCp06Integration02/Evidence/Tools
# 每次重编译前先从纯构建重置观察副本清单（保持纯包不变式）：
cp I:/WGInt02Release/Release/WanxiangGuitu_Data/{RuntimeInitializeOnLoads,ScriptingAssemblies}.json \
   I:/WGInt02Obs/Release/WanxiangGuitu_Data/
rm I:/WGInt02Obs/Release/WanxiangGuitu_Data/Managed/CavernValidationDriver.dll

python3 build_driver.py \
  --managed "I:/WGInt02Obs/Release/WanxiangGuitu_Data/Managed" \
  --source "IntDriver.cs.txt" \
  --work "I:/WGInt02Obs/work" \
  --data "I:/WGInt02Obs/Release/WanxiangGuitu_Data" \
  --evidence "I:/WGInt02Obs/evidence"
# 成功输出 verdict=DRIVER_INJECTED + driverDllSHA256
```

## 4. 运行各模式

```bash
python3 run_player.py \
  --exe "I:/WGInt02Obs/Release/WanxiangGuitu.exe" \
  --managed "I:/WGInt02Obs/Release/WanxiangGuitu_Data/Managed" \
  --run-root "I:/WGInt02Runs/<run>" \
  --evidence "I:/WGInt02Evidence/<run>" \
  --mode <mode> --timeout 600
```

模式清单与判定：

| mode | 用途 | 通过 run |
|---|---|---|
| `forest-loop` / `ruins-loop` / `cavern-loop` | INT02-02 三地区完整循环 | forest-loop-7 / ruins-loop-3 / cavern-loop-1 |
| `cavern-boss` | Boss 真实交战+合法撤离 | cavern-boss-1 |
| `cross-region-chain` | INT02-03 跨区切换 | cross-region-chain-1 |
| `xproc-1` → `xproc-2` | INT02-03 跨进程在途恢复 | xproc-1/xproc-2 |
| `weapon-smoke` | INT02-04 七武器 | weapon-smoke-2 |
| `skill-smoke` | INT02-04 八技能+弓蓄力+法杖符阵 | skill-smoke-3 |
| `reward-loop` | INT02-05 奖励制造循环 | reward-loop-2 |
| `fail-paths` | INT02-06 失败路径 | fail-paths-2 |

判定物：`complete.txt`（PASS/FAIL）+ `failure.txt`（异常栈）+ `assertions.tsv`
（逐断言 PASS/FAIL/SKIP）+ `int-events.jsonl`（带身份三元组的产品事件）。

## 5. 跨进程恢复（xproc）专用流程

```bash
# 1) 进程1：出征→战斗→中途 SaveProgress→退出（run-root A）
python3 run_player.py ... --mode xproc-1 --run-root I:/WGInt02Runs/xproc-1 ...
# 2) 预置进程2 run-root B：原样复制存档树 + xproc-expect.txt，生成前后 SHA256 清单
#    （storage-copy-manifest-before/after.txt，diff 必须为空）
# 3) 进程2：真实 Continue() 入口恢复
python3 run_player.py ... --mode xproc-2 --run-root I:/WGInt02Runs/xproc-2 \
    --allow-existing-root ...
```

`--allow-existing-root` 是 run_player 唯一放宽项（仅用于预置存档的跨进程场景），
证据目录覆盖拒绝始终生效，保证跨 Run 不拼接。

## 6. 驱动与产品交互契约（本次验证发现的要点）

1. **同帧 Focus+Strike 冲突**：`PlayerInput.Focus()` 内部 `Barrier()` 置
   `barrier=Time.frameCount`，使当帧 `UIBlocked=true` → `Ready=false`。驱动不得同帧调用。
2. **出征遗留 stale 状态**：出征后需一次 `RestorePosition`（内部 `Respawn→ResetCombat`
   清 `Expanded.Busy` 等）后 `Strike()` 才能开始；此后每轮 `PinHero` 保持相邻 1.1m。
3. **双技能槽共享冷却**：`PrepareExpanded` 置统一 `skillAt`，槽 2 施放需等待槽 1 的
   `Definition.cooldown`（产品真实行为）。
4. **死亡结算需 Acknowledge**：`CommitSettlement` 后 `HasResult` 未清，必须
   `AcknowledgeSettlement()` 回营才能再次 `Depart`（产品真实行为）。
5. **遗迹无矿脉**：`BuildRuins` 隐藏全部场景内 `AdventureResource` 且不重建（产品事实）。
6. **弹体 AttackId 过滤**：跨地区弹体 AttackId 不同，计数需用原始 spawn 事件。

## 7. 不可用项

- Editor Play / 模型推断 / 虚拟输入：**不作为**本批验证手段（与历史口径一致）。
- 人工试玩 / 观感 / 最终打击感：`NOT_RUN`。
