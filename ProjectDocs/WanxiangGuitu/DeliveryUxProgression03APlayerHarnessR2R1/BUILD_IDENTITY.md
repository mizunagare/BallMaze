# BUILD_IDENTITY — PH-R2-R1 构建身份硬绑定

> 本文件回答一个问题：**"这 4 次 Player 运行，跑的到底是哪一份 C# 代码？"**
> 结论：不是靠 EXE Launcher 的 SHA 猜的，而是由 Player 自己对自己实际加载的
> `Assembly-CSharp.dll` 计算 SHA256，并与 Driver 事先声明的期望值逐位比对形成闭合。

---

## 1. 为什么必须重做（PH-R2-FINAL 的 R1 风险）

PH-R2 阶段的身份链存在根本缺陷：

| 项 | PH-R2 做法 | 问题 |
|---|---|---|
| 身份依据 | `Builds/WanxiangGuitu.Acceptance/WanxiangGuitu.exe` 的 SHA256 | EXE 是 **Launcher 桩**，不随 C# 变化 |
| 实测 | Acceptance EXE 与 NoDefine EXE **SHA 完全相同** | `b70442f9…2436` 两者一致 → 无法区分是否编入 Harness |
| 后果 | 19 个 Run 的身份只能间接关联（player.log 的 Managed 路径、version=2、行为指纹、时序） | 审计判定 R1 高风险 |

**R1-01 的修正**：把身份锚点从 EXE 换成 **DLL**，并且必须由 Player 侧独立计算。

---

## 2. 统一构建清单 `Builds/build-manifest.json`

`schemaVersion=1`，由 `player_acceptance_driver.py manifest` 从**实际产物**回读生成（不采信构建脚本自报）。

```json
{
  "schemaVersion": 1,
  "buildId": "phr2r1-318c660afbcaf218d04c469b",
  "unityVersion": "6000.6.5f1",
  "builtAt": "2026-11-11T15:34:59",
  "acceptanceExePath": "…/Builds/WanxiangGuitu.Acceptance/WanxiangGuitu.exe",
  "acceptanceExeSha256": "b70442f90f50cd91f7af7bf2272602645fc5d02c4d3156fb221fc27c328d2436",
  "acceptanceDllPath": "…/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll",
  "acceptanceDllSha256": "b3ce427cdc3970b6412972f4c9de89442dd68f5debf572bcfebf8ad5e54a1e91",
  "noDefineExePath": "…/Builds/WanxiangGuitu.AcceptanceNoDefine/WanxiangGuitu.exe",
  "noDefineExeSha256": "b70442f90f50cd91f7af7bf2272602645fc5d02c4d3156fb221fc27c328d2436",
  "noDefineDllPath": "…/Builds/WanxiangGuitu.AcceptanceNoDefine/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll",
  "noDefineDllSha256": "00373fe72161ba7e7c761983ef5865097584837c594a251f0f60a8f00e08710e",
  "acceptanceMarkerPresent": true,
  "noDefineMarkerPresent": false,
  "scriptingDefineState": {
    "acceptanceBuildDefine": "UX_ACCEPTANCE",
    "shippingDefine": null,
    "projectSettingsDefineLeakCount": 0,
    "cleared": true
  }
}
```

### 2.1 buildId 的构造

```
buildId = "phr2r1-" + sha256( acceptanceDllSha256 | noDefineDllSha256
                             | acceptanceExeSha256 | noDefineExeSha256 )[:24]
```

- 四元组中**两个 DLL** 是主导项：任一 DLL 变化 → buildId 立即变化。
- EXE 参与只是为了让"重建但产物全同"也能得到同一 buildId（幂等）。
- 本次：`phr2r1-318c660afbcaf218d04c469b`。

### 2.2 与 PH-R2 的产物差异（证明本批确实是新代码）

| 产物 | PH-R2 | PH-R2-R1 | 变化原因 |
|---|---|---|---|
| Acceptance DLL | `12ca6ef5…` | `b3ce427c…1e91` | Harness 新增 identity / 逐段 ratio / 严格 T3 |
| NoDefine DLL | `f7830252…` | `00373fe7…710e` | 同上代码基座（未编入 Harness） |
| Acceptance EXE | `b70442f9…2436` | `b70442f9…2436` | **未变**：Launcher 桩，与 C# 无关 |
| NoDefine EXE | `b70442f9…2436` | `b70442f9…2436` | 同上 |

> EXE 恒定这一事实本身就是 R1 风险的证据：**看 EXE 会把"旧代码"和"新代码"判成同一份**。
> 因此 `run-manifest.json` / `INDEX.json` 中一律以 `dllSha256*` 作为身份主键。

---

## 3. Player 内部身份取证（谁算的 SHA）

`PlayerAcceptanceHarness.ResolveAssemblyIdentity()`：

1. `Assembly.GetExecutingAssembly()` 取当前真正执行的程序集；
2. 取 `.Location`；若为空（部分 Player 环境），回退到
   `Application.dataPath/Managed/Assembly-CSharp.dll`；
3. 打开该**实际文件**流式计算 SHA256；
4. 与命令行 `--expected-dll-sha` 逐位比对 → `identityVerified`；
5. 若路径不可得或比对失败 → `identityVerified=false`，**不降级为"只记录命令行参数"**，
   并在 `Finish()` 中把 `identityOk` 计入 PASS 条件（`pass = … && identityOk`）。

result.json 中记录（顶层，非嵌套）：

| 字段 | 含义 | 本次实测 |
|---|---|---|
| `loadedAssemblyPath` | Player 解析到的真实 DLL 路径 | `I:\unity\WanxiangGuitu\Builds\WanxiangGuitu.Acceptance\WanxiangGuitu_Data\Managed\Assembly-CSharp.dll` |
| `loadedAssemblySha256` | **Player 自己算出的** SHA256 | `b3ce427cdc3970b6412972f4c9de89442dd68f5debf572bcfebf8ad5e54a1e91` |
| `loadedAssemblyName` | 程序集名 | `Assembly-CSharp` |
| `expectedAssemblySha256` | 命令行声明的期望 DLL SHA | 同上（一致） |
| `expectedExeSha256` | 命令行声明的期望 EXE SHA | `b70442f9…2436` |
| `identityVerified` | 上述两者是否一致 | `true` |
| `identityNote` | 失败时的原因文本 | 空（成功） |

---

## 4. Driver 双重校验（启动前 / 退出后）

### 4.1 启动前（§3.3 步骤 1–5）

1. 计算 Acceptance EXE SHA256；
2. 计算 Acceptance DLL SHA256；
3. 读取 `Builds/build-manifest.json`；
4. `verify_manifest()` 逐字段比对实际文件（含 marker、Unity 版本、路径存在性）；
5. 由四元组生成 `buildId`。

随后把 `--build-id / --expected-exe-sha / --expected-dll-sha` 与 `--run-id` 一并传入 Player。

### 4.2 Player 退出后（§3.3 步骤 1–5）

1. 重新计算 EXE SHA256；
2. 重新计算 DLL SHA256；
3. 前后 SHA 必须一致（运行期间产物被替换 → FAIL）；
4. Player 内部 SHA 必须等于 Driver 记录的 DLL SHA；
5. `verify_manifest()` 对**运行后**的产物再校验一次（manifest 与实际一致）。

任一条件不满足 → `finalize("FAIL", …)`，`finalStatus` 记为 FAIL，`identityReasons` 落盘。

### 4.3 每次运行的独立记录 `run-manifest.json`

由 **Driver** 在 Player 退出之后生成（Player 无法在自己 `Application.Quit` 之前伪造退出码）：

```json
{
  "runId": "C-GATE", "processId": 10600,
  "startedAt": "2026-11-11T15:35:46", "finishedAt": "2026-11-11T15:36:01",
  "exitCode": 0, "timedOut": false,
  "buildId": "phr2r1-318c660afbcaf218d04c469b",
  "exeSha256Before": "b70442f9…2436", "exeSha256After": "b70442f9…2436",
  "dllSha256Before": "b3ce427c…1e91", "dllSha256After": "b3ce427c…1e91",
  "loadedAssemblyPath": "…\\WanxiangGuitu_Data\\Managed\\Assembly-CSharp.dll",
  "loadedAssemblySha256": "b3ce427c…1e91",
  "loadedAssemblyName": "Assembly-CSharp",
  "expectedAssemblySha256": "b3ce427c…1e91",
  "identityVerified": true, "identityReasons": [],
  "resultJsonSha256": "d6654f9f79c337760d2e251fb30b2895ecd53b2fffb4a3748682b48ec34a8a17",
  "finalStatus": "PASS"
}
```

判定顺序（`run_one`）：超时 → 退出码非 0 → INCOMPLETE → 身份 → marker → harness pass。
**超时即便 result.json 写着 pass=true 也一律 FAIL**（自检项 "timeout produces FAIL (never PASS)" 已实测）。

---

## 5. 身份闭合矩阵（4 次运行）

| Run | EXE 前 | EXE 后 | DLL 前 | DLL 后 | Player 自算 | 期望 DLL | identityVerified | buildId |
|---|---|---|---|---|---|---|---|---|
| C-GATE | b70442f9 | b70442f9 | b3ce427c | b3ce427c | b3ce427c | b3ce427c | true | phr2r1-318c66… |
| TWIN-COUNTER | b70442f9 | b70442f9 | b3ce427c | b3ce427c | b3ce427c | b3ce427c | true | phr2r1-318c66… |
| STAFF-FIELD | b70442f9 | b70442f9 | b3ce427c | b3ce427c | b3ce427c | b3ce427c | true | phr2r1-318c66… |
| SELFTEST-positive | b70442f9 | b70442f9 | b3ce427c | b3ce427c | b3ce427c | b3ce427c | true | phr2r1-318c66… |

（SHA 均截断显示，前 8 位；完整值见各 `run-manifest.json`。）

### 5.1 负向证明：Player 确实在"自己算"

`Evidence/PH-R2-R1/selftest/SELFTEST-wrongdllsha-153637/run-manifest.json`（自检 ID-1，真实 Player 运行）：

| 字段 | 值 |
|---|---|
| 传入 `--expected-dll-sha` | `0000000000000000000000000000000000000000000000000000000000000000`（全零） |
| Player 自算 `loadedAssemblySha256` | `b3ce427cdc3970b6412972f4c9de89442dd68f5debf572bcfebf8ad5e54a1e91` |
| `expectedAssemblySha256` | `0000…0000` |
| `identityVerified` | **false** |
| `identityReasons` | `["Player identityVerified is not true", "Player expectedAssemblySha256 mismatch"]` |
| `exitCode` / `finalStatus` | `1` / **FAIL** |

如果 Player 只是把命令行原样回写，`loadedAssemblySha256` 会是全零并且 `identityVerified=true`。
实测得到的是**真实 DLL 的哈希 + 校验失败**，这就是"Player 自己算"的直接证据。

---

## 6. NoDefine（出货等价）隔离

| 检查 | 方法 | 结果 |
|---|---|---|
| NoDefine DLL SHA 与 manifest 一致 | `verify_manifest` | 一致 `00373fe7…710e` |
| NoDefine DLL 不含 Harness marker | 双编码扫描（UTF-16LE / UTF-8）`UX_ACCEPTANCE_HARNESS_v1` | 0 次出现 |
| Acceptance DLL 含 marker | 同上 | 2 次出现（UTF-16LE） |
| `UX_ACCEPTANCE` 未泄漏到 ProjectSettings | `ProjectSettings.asset` 计数 | 0；`scriptingDefineSymbols: {}` |
| 不因 EXE Launcher 相同而误判 | 身份主键取 DLL，不取 EXE | §2.2、§5 |

> marker 在 Mono 构建中以 **UTF-16LE** 存放在 #US 字符串堆。只按 ASCII/UTF-8 grep 会得到
> "0 次"的假阴性——本批工具统一使用双编码扫描（`marker_in_dll`）。

---

## 7. 复核方法（审阅者可独立重跑）

```bash
cd /i/unity/WanxiangGuitu

# 1) 产物指纹
sha256sum Builds/WanxiangGuitu.Acceptance/WanxiangGuitu.exe \
          Builds/WanxiangGuitu.Acceptance/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll \
          Builds/WanxiangGuitu.AcceptanceNoDefine/WanxiangGuitu.exe \
          Builds/WanxiangGuitu.AcceptanceNoDefine/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll

# 2) manifest 与实际是否一致（只读，不启动 Player）
python player_acceptance_driver.py recompute

# 3) 逐 Run 身份
cat Evidence/PH-R2-R1/runs/*/run-manifest.json
```

不接受"EXE SHA 相同 ⇒ 同一份代码"的论证；只接受 `dllSha256*` 与 `loadedAssemblySha256` 的三方一致。

---

## 8. PH-R2-R1-FIX 的构建身份（追加，不覆盖上文 PH-R2-R1 记录）

FIX 批次改动了 Harness（稳定期单时钟 + v3 + 运行时时钟探针），因此 **DLL 必然变化**，
上文 §2 的 `phr2r1-318c660afbcaf218d04c469b` / `b3ce427c…1e91` 只对 PH-R2-R1 成立，不可混用。

### 8.1 本轮构建（第三轮，最终用于 A–F）

| 产物 | SHA256 |
|---|---|
| Acceptance **DLL** | `db258d6e7f02b0b8…`（完整值见 `Builds/build-manifest.json`） |
| NoDefine **DLL** | `f8b44e1e7471e354…` |
| Acceptance EXE（Launcher） | `b70442f90f50cd91…2436`（恒定，不随 C# 变化） |
| NoDefine EXE（Launcher） | `b70442f90f50cd91…2436`（与 Acceptance **相同**） |
| buildId | `phr2r1-e32e240735e921f7c4aad220` |

Harness `VERSION` 由 2 → **3**；`MARKER` 仍为 `UX_ACCEPTANCE_HARNESS_v1`（出货排除用的 grep 标识不变）。

### 8.2 构建输入保护（FIX-04 新增，原 F-2 缺陷修复）

原 190 文件保护清单**不含** `Assets/Settings/PC_RPAsset.asset` 与
`Assets/Settings/UniversalRenderPipelineGlobalSettings.asset`，且没有构建前逐文件快照。

本轮改为：每次构建前写 `build-preflight-manifest.json`（size / mtime / SHA256 / worktree git OID /
HEAD git OID / `userEditPresent`），构建后写 `build-postflight-manifest.json` 并逐文件判定。

| 轮次 | 时间 | 结果 |
|---|---|---|
| 第 1 轮 | 16:42 | `GATE=CHANGED_BY_TOOLCHAIN`，4/4 变化（Unity 编辑器一次性 schema 升级：URP prefilter 模式重算 + `scriptingDefineSymbols` 由 `{}` 规范化为 `Standalone:`）；构建前 4 个文件 **均与 HEAD 一致**，不存在被覆盖的用户修改。差异留档 `build/build-input-diff.round1.patch` |
| 第 2 轮 | 16:45 | `GATE=PASS`，4/4 **逐位相同** → 证明该变化是一次性归一化，不是每次构建都改写 |
| 第 3 轮 | 16:49 | `GATE=PASS`，4/4 **逐位相同** → 最终产物由"零构建输入漂移"的构建产生 |

**没有执行任何 `git checkout` / `restore` 来伪造零变化**：第 1 轮的归一化结果原样留在工作区，
因此 `git status` 现在把这 4 个文件显示为 modified —— 这是有意保留、可审计的状态。

保护清单同时从 219 行（含 29 个重复路径）收敛为 **192 个唯一文件**（190 + 2 新增），
见 `Evidence/PH-R2-R1-FIX/protection/PROTECTED_SHA256.tsv`。

### 8.3 本轮身份闭合

3 次真实 Player 运行（TIMEBASE / C-GATE / STAFF-FIELD）与 30 项自检中的 2 次负向运行，
其 `loadedAssemblySha256` 均由 Player 用 `Assembly.GetExecutingAssembly().Location` 自算，
并与 `dllSha256Before` / `expectedAssemblySha256` / `dllSha256After` 四方一致；
逐 Run 证据见 `Evidence/PH-R2-R1-FIX/runs/*/run-manifest.json`。
