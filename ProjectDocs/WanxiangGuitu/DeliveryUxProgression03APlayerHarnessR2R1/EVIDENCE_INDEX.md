# EVIDENCE_INDEX — PH-R2-R1 证据索引

> 本文件回答：**"证据在哪、怎么核、核什么？"**
> 全量 124 个文件的 SHA256 索引见 `Evidence/PH-R2-R1/INDEX.json → evidenceFiles`
> （`INDEX.json` 自身不在清单内，避免自引用）。

---

## 1. 目录结构

```
Evidence/PH-R2-R1/
├── INDEX.json               # 批次总索引：build / phases A-E / runs / protection / 124 文件 SHA
├── RECOMPUTE.json           # 40 项独立复算（不启动 Player）
├── build/
│   ├── build-manifest.json      # 四产物 SHA + marker + define 状态 + buildId
│   ├── acceptance-build.json    # Acceptance: EXE/DLL SHA + marker + buildId
│   └── nodefine-build.json      # NoDefine: EXE/DLL SHA + marker + defineLeakCount
├── runs/
│   ├── C-GATE/                  # sword.triple（C-gate）
│   ├── TWIN-COUNTER/            # twin.counter（消费一次）
│   └── STAFF-FIELD/             # staff.field（逐段 0.65+0.40×3）
├── selftest/
│   ├── SELFTEST.json            # 23 项自检结果
│   ├── console.log              # 自检控制台原文
│   ├── SELFTEST-positive-153637/
│   ├── SELFTEST-stale-153637/         # 负向：陈旧 result 被拒
│   ├── SELFTEST-wrongsha-153637/      # 负向：buildSha 不符被拒
│   ├── SELFTEST-timeout-153637/       # 负向：超时不判 PASS
│   └── SELFTEST-wrongdllsha-153637/   # 负向：DLL SHA 不符被拒（真实 Player）
└── protection/
    ├── pre_change_snapshot.json   # 改动前 311 份历史证据快照（14:56:19）
    ├── history_recheck.json       # 改动后复核：311/311 一致
    ├── B_protected_recheck.json   # 219 行 / 190 唯一路径保护文件复核
    ├── PROTECTED_SHA256.tsv       # 同上的 TSV（便于 diff/审计工具）
    ├── GIT_HEAD.txt
    ├── GIT_STATUS_porcelain_v2.txt
    ├── GIT_DIFF_STAT.txt
    └── GIT_DIFF_NAME_STATUS.txt
```

每个 Run 目录固定包含：

| 文件 | 作用 |
|---|---|
| `result.json` | Harness 自述（含 `loadedAssemblyPath/Sha256`、`identityVerified`、伤害取证） |
| `run-manifest.json` | **Driver 在 Player 退出后生成**的退出与身份记录 |
| `damage-events.jsonl` | 原始伤害事件（逐段 HP 前后 / applied / hitTime） |
| `target-events.jsonl` | 原始目标事件（第二路独立证据） |
| `recompute.json` | 从上述工件复算的 11/18/11 项断言 |
| `player.log` / `harness.log` | Unity Player 日志 / Harness 日志 |
| `stdout.txt` / `stderr.txt` | 进程输出（超时用例也有） |
| `entry-audit.jsonl` / `storage-audit.jsonl` | 入口授权审计 / 存储根审计 |
| `WanxiangGuitu/ForestRuins/save.json(.bak)` | **该 Run 自己的隔离存档根**（非 AppData） |

---

## 2. 关键文件指纹（SHA256 前 16 位）

| 文件 | 大小 | SHA256（前 16） | 说明 |
|---|---|---|---|
| `build/build-manifest.json` | 1256 | `8db274cd77b5ddf8` | 身份主键 |
| `RECOMPUTE.json` | 12006 | `b0cdeb7daae4ba31` | 40 项复算 |
| `selftest/SELFTEST.json` | 3808 | `fbcb08761cbd8690` | 23/23 |
| `runs/C-GATE/result.json` | 8426 | `d6654f9f79c33776` | C-gate 自述 |
| `runs/C-GATE/run-manifest.json` | 1119 | `13a7c050c7d8cb1a` | 退出+身份 |
| `runs/TWIN-COUNTER/result.json` | 8707 | `c3023625c85b95c6` | 反击自述 |
| `runs/TWIN-COUNTER/run-manifest.json` | 1124 | `036a0686a07067fc` | 退出+身份 |
| `runs/STAFF-FIELD/result.json` | 9036 | `cb6f07d9bead858a` | 逐段自述 |
| `runs/STAFF-FIELD/run-manifest.json` | 1124 | `a2fbd31fad09bfe7` | 退出+身份 |
| `protection/PROTECTED_SHA256.tsv` | 53237 | `595888dd98b66414` | 190 路径 |
| `protection/history_recheck.json` | 92646 | `1b11a73e6502125d` | 311/311 |

> `run-manifest.json` 中的 `resultJsonSha256` 与上表 `result.json` 的实测 SHA 相互闭合：
> 例如 C-GATE 的 `resultJsonSha256 = d6654f9f…` 即 `runs/C-GATE/result.json` 的实际哈希。

---

## 3. 四条证据链（缺一不可）

### 3.1 身份链

```
build-manifest.json (acceptanceDllSha256)
   └─== dllSha256Before (run-manifest)
        └─== loadedAssemblySha256 (Player 自算, result.json / run-manifest)
             └─== expectedAssemblySha256 (命令行)
                  └─ buildId = phr2r1-318c660afbcaf218d04c469b
```

### 3.2 数值链

```
damage-events.jsonl (原始) ──┐
target-events.jsonl (原始) ──┼─→ recompute.json (逐段断言) ─→ RECOMPUTE.json (汇总)
result.json.damageForensics ─┘
```

### 3.3 退出链

```
process exit code ─→ run-manifest.exitCode / timedOut ─→ finalStatus
（超时/非 0/身份不符 → FAIL，与 result.pass 无关）
```

### 3.4 保护链

```
pre_change_snapshot.json (改动前) ─→ history_recheck.json (311/311)
B_protected_files.json (审计基线 219 行) ─→ B_protected_recheck.json (190/190 MATCH)
```

---

## 4. 复核命令

```bash
cd /i/unity/WanxiangGuitu

# ① 一键复核（纯读，不启动 Player、不重建）
python player_acceptance_driver.py recompute
#   期望：C-GATE 11/11, TWIN-COUNTER 18/18, STAFF-FIELD 11/11, allOk=True

# ② 逐 Run 身份
python - <<'PY'
import json,glob
for p in glob.glob('Evidence/PH-R2-R1/runs/*/run-manifest.json'):
    d=json.load(open(p,encoding='utf-8'))
    ok = d['dllSha256Before']==d['dllSha256After']==d['loadedAssemblySha256']==d['expectedAssemblySha256']
    print(d['runId'], d['finalStatus'], 'exit=%s'%d['exitCode'], 'timedOut=%s'%d['timedOut'], 'identityChain=%s'%ok)
PY

# ③ 保护面
grep -c "MATCH$" Evidence/PH-R2-R1/protection/PROTECTED_SHA256.tsv      # 期望 190
python -c "import json;d=json.load(open('Evidence/PH-R2-R1/protection/history_recheck.json'));print(d['summary'])"

# ④ 全量文件指纹
python -c "import json;d=json.load(open('Evidence/PH-R2-R1/INDEX.json'));print(len(d['evidenceFiles']),'files')"
```

---

## 5. 与历史证据的边界

| 目录 | 归属 | 本批操作 |
|---|---|---|
| `Evidence/INDEX.json`、`Evidence/PLAYER_RUN_MATRIX.csv`、`Evidence/Runs/R01..R19` | PH-R1（冻结） | **只读**，311/311 SHA 一致 |
| `Evidence/PH-R2/**` | PH-R2（冻结） | **只读**，同上 |
| `Evidence/PH-R2-R1/**` | 本批新增 | 全部新建，未覆盖任何历史文件 |
| `ProjectDocs/.../DeliveryUxProgression03APlayerHarnessR2R1/` | 本批交付 | 新建 6 份文档 |

> PH-R1 的 466 个证据文件处于 sparse-checkout（`skip-worktree`）状态，物理未检出，
> 因此本批的复核口径为"索引 OID 与快照 SHA 一致"，而非"文件在磁盘上可读"。
> 该限制沿用 PH-R2-FINAL 的 R5 风险登记，本批未改变仓库工作模式。

---

## 6. PH-R2-R1-FIX 证据树（追加，不覆盖上文 PH-R2-R1 记录）

### 6.1 目录结构

```
Evidence/PH-R2-R1-FIX/
├── INDEX.json                       批次总索引（含 build / buildInputGate / protection / history / coverage）
├── SELFTEST_COVERAGE_MATRIX.json    23 条要求 × 真实证据的映射（机器可读）
├── timebase-probe.json              A 阶段探针原件副本（与 runs/TIMEBASE/ 内一致）
├── build/
│   ├── build-preflight-manifest.round1.json    第 1 次构建前（= FIX 起点，4 文件均与 HEAD 一致）
│   ├── build-postflight-manifest.round1.json   第 1 次构建后（4/4 变化，一次性归一化）
│   ├── build-input-diff.round1.patch           上述变化的完整 diff（169 行）
│   ├── build-preflight-manifest.json           第 3 次构建前（最终产物所用）
│   └── build-postflight-manifest.json          第 3 次构建后（GATE=PASS，4/4 未变）
├── protection/
│   ├── protection_manifest.json      192 个唯一保护文件（含 219→190 去重记录）
│   ├── PROTECTED_SHA256.tsv          逐文件：起点 SHA / 当前 SHA / HEAD OID / worktree OID / userEdit
│   ├── PROTECTED_RECHECK.json        188 未变 + 4 变化（全部为构建输入）
│   ├── HISTORY_RECHECK.json          1340 份历史证据逐位比对（0 变化）
│   └── pre_change_snapshot.json      FIX 起点全量快照（tracked + 历史证据）
├── recompute/
│   ├── twin-timeline.json            双刃反击统一时钟时间线（偏移 4.358567s）
│   ├── build_coverage_matrix.py      覆盖矩阵生成器（只读 SELFTEST.json）
│   ├── recheck_protection.py         192 文件复核器
│   ├── recheck_history.py            1340 历史证据复核器
│   └── enrich_index.py               INDEX 字段补全
├── runs/
│   ├── TIMEBASE/                     A 阶段：10 例时钟探针（真实 Player）
│   ├── C-GATE/                       B 阶段：sword.triple 三段真实伤害
│   └── STAFF-FIELD/                  C 阶段：staff.field 四段逐段伤害
├── failed/
│   └── TIMEBASE-probe-data-error/    第一版探针用例数据错误（完整原件 + FAILURE_NOTE.json）
└── selftest/
    ├── SELFTEST.json                 31 项自检（18 原始 + 5 身份 + 8 时间基准）
    ├── console.log                   自检过程输出
    └── SELFTEST-*/                   每次自检运行的独立隔离目录（含 run-manifest.json）
```

### 6.2 每个 Run 目录的固定内容

`result.json`（Harness 全量结果，含 `timebase` 区块）、`run-manifest.json`（Driver 在 Player 退出后写，
含 exitCode / timedOut / 四 SHA / loadedAssemblySha256 / identityVerified / resultJsonSha256 / finalStatus）、
`damage-events.jsonl`（逐命中，含 `hitActiveTime` + `hitUnscaledTime`）、
`target-events.jsonl`（逐次生命观测，含 `activeTime` + `unscaledTime` 与两者差值）、
`player.log` / `harness.log` / `stdout.txt` / `stderr.txt`。

### 6.3 新增的四条证据链（与 §3 并列，替换关系）

| 链 | 问题 | 本批新增依据 |
|---|---|---|
| 时钟链 | 每个时间数字属于哪个时钟？ | `result.json#timebase`（settleClock / productClock / 两者数值 / 偏移）+ JSONL 中的成对字段 |
| 构建输入链 | 构建有没有偷改工程设置？ | `build-preflight/postflight` 双清单 + 三轮 gate 记录 + 第 1 轮 diff |
| 覆盖链 | 自检到底断言了什么？ | `SELFTEST_COVERAGE_MATRIX`（四分法，未覆盖 0） |
| 失败链 | 失败有没有被洗掉？ | `failed/TIMEBASE-probe-data-error/` 原件保留 |

### 6.4 边界（与历史证据）

| 目录 | 归属 | 本批操作 |
|---|---|---|
| `Evidence/PH-R2-R1/**`（125 文件） | PH-R2-R1（冻结） | **只读**，逐位一致 |
| `Evidence/PH-R2/**`（15）、`Evidence/PH-R2-FINAL-AUDIT/**`（47） | 冻结 | **只读** |
| `Evidence/Runs/**`（1151）、`Evidence/INDEX.json`、`Evidence/PLAYER_RUN_MATRIX.csv` | PH-R1/PH-R2（冻结） | **只读** |
| `Evidence/PH-R2-R1-FIX/**` | 本批新增 | 全部新建，未覆盖任何历史文件 |

> 与 §5 相同的 sparse-checkout 限制仍成立，但本批复核改用 `git hash-object`（worktree 侧）与
> `git rev-parse HEAD:<path>`（索引侧）双口径，因此 1340 份历史证据的"未改动"结论不依赖文件是否物理检出。
> 另：`Evidence/**/*.log` 仍被 `*.log` 规则忽略，入库需 `git add -f`（沿用原 F-4 提示）。
