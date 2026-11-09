# UX-PROGRESSION-01 P1 · 复跑说明（TESTING）

本批所有结论只来自**真实 Player 进程**（非 Editor、非模型推算）。下列命令即本次实际执行的命令，
路径按本机实际位置书写；每条命令的原始输出与归档见 `Evidence/Player/<run>/`。

## 0. 前置

| 项 | 值 |
|---|---|
| Unity | `C:\Program Files\Unity\Hub\Editor\6000.6.5f1\Editor\Unity.exe` |
| 纯发行构建入口 | `WanxiangBuild.ValidateBuild`（读 `UNITY_TEST_ROOT`） |
| 构建产物 | `<root>/Release/WanxiangGuitu.exe` + `WanxiangGuitu.exe.summary.txt` |
| 构建身份 | `Release/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll` 的 SHA256（EXE 是固定壳，不随脚本变化） |
| 观察副本 | `I:/WGUP01/Observe`（纯包拷贝，注入 sidecar 驱动；纯包本身零注入） |
| 运行根 | `I:/WGUP01/Runs/<run>`（隔离，不复用） |
| 证据根 | `ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/Evidence/Player/<run>` |

## 1. 纯发行构建（不注入任何验证代码）

```bash
# ValidateBuild 带「必须全新输出」门禁：Release 已存在会直接
#   BuildFailedException: Release privacy gate: fresh output required; existing executable rejected
# 因此先把上一版改名留档（不要删除，失败/旧证据要能对上 SHA），再让构建写全新目录。
cd I:/WGUP01/Build
mv Release "Release-prev-$(date +%H%M%S)"; mkdir -p Release

cd I:/unity/WanxiangGuitu
UNITY_TEST_ROOT='I:/WGUP01/Build' \
  "C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe" \
  -projectPath 'I:/unity/WanxiangGuitu' -executeMethod WanxiangBuild.ValidateBuild \
  -wanxiang-storage-root 'I:/WGUP01/Build' \
  -logFile 'I:/WGUP01/Build/Unity.log' -batchmode
cat I:/WGUP01/Build/Release/WanxiangGuitu.exe.summary.txt
```

验收：`result=Succeeded`、`errors=0`；`Release/WanxiangGuitu_Data/RuntimeInitializeOnLoads.json`
中 `CavernValidationDriver` 出现次数为 **0**（纯包不含驱动）。

构建后**必须**核对 `Assembly-CSharp.dll` 的哈希与时间戳都比最新改动的 `.cs` 新，
否则拿到的是旧产物（本批已发生过一次）。

> Unity 会在构建期自动改写 `ProjectSettings/ProjectSettings.asset`、`ProjectSettings/GraphicsSettings.asset`、
> `Assets/Settings/*.asset`，并生成未跟踪的 `Assets/Resources.meta`。这些都不是本批产品改动，
> 提交前必须 `git checkout -- ProjectSettings Assets/Settings && rm -f Assets/Resources.meta` 还原。

## 2. 观察副本 + sidecar 驱动编译注入（仅副本）

```bash
cp -a I:/WGUP01/Build/Release/. I:/WGUP01/Observe/Release/
python ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/Evidence/Tools/build_driver.py \
  --managed  I:/WGUP01/Observe/Release/WanxiangGuitu_Data/Managed \
  --source   ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/Evidence/Tools/IntDriver.cs.txt \
  --work     I:/WGUP01/Observe/driver \
  --data     I:/WGUP01/Observe/Release/WanxiangGuitu_Data \
  --evidence ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/Evidence/Driver
```

产出 `driver-injection.json`（编译器 SHA、参数、退出码、驱动 DLL SHA、注入前后 Boot 清单 SHA）。
本次结果：`verdict=DRIVER_INJECTED`、`compileExitCode=0`、`driverDllSHA256=49c81de5…`。
编译失败时先看 `Evidence/Driver/driver-compile.log` 里的 `error CS`；
重复定义（`CS0111`）通常意味着上一次补丁是"追加"而不是"替换"。

## 3. 真实 Player 运行

模式串：`p1:<forest|ruins|cavern>:<gather|treasure|challenge>:<success|death|abandon|counter|xproc1|xproc2>`

单条：

```bash
python ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/Evidence/Tools/run_player.py \
  --exe      I:/WGUP01/Observe/Release/WanxiangGuitu.exe \
  --managed  I:/WGUP01/Observe/Release/WanxiangGuitu_Data/Managed \
  --run-root I:/WGUP01/Runs/p1-forest-gather-success \
  --evidence ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/Evidence/Player/p1-forest-gather-success \
  --mode "p1:forest:gather:success" --timeout 600
```

本批实际使用的批量入口（13 条）：

```bash
bash ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/Evidence/Tools/run_batch2.sh
```

| run | mode | 语义 |
|---|---|---|
| `p1-forest-gather-success` | `p1:forest:gather:success` | 采集 12 → 撤离 → 达成 |
| `p1-forest-treasure-death` | `p1:forest:treasure:death` | 开 3 箱 → 死亡 → 条件满足但未撤离 |
| `p1-forest-counter` | `p1:forest:gather:counter` | 带 30 木材不采集=0 → 采 18 → 消费 5 不回退 |
| `p1-ruins-gather-success` | `p1:ruins:gather:success` | 机关链 + 宝箱/敌人材料 → 撤离 |
| `p1-ruins-challenge-abandon` | `p1:ruins:challenge:abandon` | 守护者目标 → 放弃 |
| `p1-cavern-gather-success` | `p1:cavern:gather:success` | 3 矿脉 + 矿晶 → 撤离 |
| `p1-cavern-treasure-abandon` | `p1:cavern:treasure:abandon` | 双箱目标 → 放弃 |
| `p1-xproc-{forest,ruins,cavern}-1` | `…:xproc1` | 第一段：选目标 → 采集 → 消费 → 存盘 |
| `p1-xproc-{forest,ruins,cavern}-2` | `…:xproc2` | 第二段：同一 run-root `--allow-existing-root` 继续存档，读回快照 |

> **必须在沙箱外运行**：沙箱会吞掉 run-root 下的子目录，导致归档只剩部分文件。
> `xproc2` 需要 `--allow-existing-root`（产品语义就是"继续存档"），`run_player.py` 默认拒绝复用目录。

## 4. 每条 Run 归档的原始文件（15 个）

`run-summary.json`、`Player.command.json`、`Player.log`、`Player.stdout`、`Player.stderr`、
`process.json`、`Player.exit.json`、`assertions.tsv`、`int-events.jsonl`、`int-frames.tsv`、
`entry-audit.jsonl`、`storage-audit.jsonl`、`complete.txt`、`cavern-test.txt`、`exe-sha256.txt`。

`run_player.py` 在证据目录已存在时直接拒绝运行，因此档案不可拼接、不可覆盖；
`verdict` 仅在 `exitCode==0 && 未超时` 时为 `PLAYER_RUN_COMPLETED`，其余如实记为
`PLAYER_RUN_FAILED`，**不把 FAIL 改写为 PASS**。

## 5. 汇总与保护比对

```bash
python ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/Evidence/Tools/summarize_runs.py
bash   ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/Evidence/Tools/protection_hashes.sh
```

- `summarize_runs.py` → `PLAYER_RUN_MATRIX.csv`（只读归档产物，缺文件记 `MISSING_SUMMARY`，不推断）
- `protection_hashes.sh` → `Evidence/PROTECTION_HASHES.tsv`，末行必须是 `RESULT: ALL_IDENTICAL`（本次 22/22 `YES`）

## 6. 判定口径

- `assertions.tsv` 每行 `id<TAB>PASS|FAIL|SKIP<TAB>detail`；任一 FAIL 则 `complete.txt=FAIL` 且进程退出码 2。
- SKIP 只用于**产品在当前地区/布局确实不提供该对象**的情形——本批 9 次 SKIP 全部是
  `p1-ruins-no-vein-notice` 在森林/洞窟的显式跳过；SKIP 不计入 PASS，报告逐条列出。
- 目标达成判定：`conditionsMet && settledSuccess`，`settledSuccess = AdventureRules.Success(outcome)`
  （`Extracted` / `TestChallengeComplete`）。死亡与放弃一律不达成。
- 进度口径：`gross = max(EarnedRemaining, 运行时单调计数)`，排除带入（`CarriedIn`）；
  消费不回退；跨进程重进"发生过消费的局"时 `exact=false` 并取持久下界。
