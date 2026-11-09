# CP06-C24-B2 原始证据索引

基线 `a013c15aae15e17af6a7596a022f01f56a745c34`；分支 `fix/cp06-crystal-warden-b2`。
所有文件以 SHA256 固化；**全量清单**见 `After/hash-manifest.json`（最后生成，含本文件哈希，
不含其自身）。保护哈希见 `After/protection.json`。

## 1. 先写合同，后跑测试

| 文件 | SHA256 | 说明 |
|---|---|---|
| `../DESIGN_DECISIONS.md` | `bbbb27e8c418d8150725083e0dd6342d695668767d77be9db8716b6c7e79ecb8` | 语义变更声明、冻结参数、容差、切线、判定分层、版本化设计 |
| `Tools/RingContract/contract.json` | `a04a1540f21bed90dd892f34261f9ad2e75f94a53d1763f26ac59ca420ffc8f5` | 机器可读冻结副本；14 组几何期望 + 5 组运行期望 |

两者在任何产品改动与任何测试运行之前写入；运行前仅按 `origin.y=0.08` 校正了竖直切线用例的
`centerY`（2.2→2.28 / 2.201→2.281），半径/半高/容差/闭集切线规则未变，详见设计文档 2.5 节。

## 2. 修复前（`Before/`，任何产品改动之前生成）

| 文件 | 说明 |
|---|---|
| `Before/reproduce_before.py` | 一次性只读复现脚本；拒绝覆盖已有输出，避免把修复后源码哈希写成修复前证据 |
| `Before/inputs.json` | 25 个输入（B1/C24B 历史证据 + 基线产品源码）的 SHA256 / 字节数 |
| `Before/route-fields-before.json` | F1：逐字段对照 + 通用分支公式重算（4/4 不一致） |
| `Before/ring-matrix-before.json` | F2：四组真实胶囊径向范围、旧根点判定、按 TSV 读取的真实 HP 与伤害调用栈（2 组冲突） |
| `Before/c05-timeline-before.json` | C05：历史 v2.0 `INCOMPLETE`、工具 SHA、两条限制原文 |
| `Before/before-repro.json` | 汇总裁决 `PRE_FIX_REPRODUCED`；明确列出「不是」新 Unity/Player 运行 |

`Before/inputs.json` SHA256：`3bee4d8de6b8c93eabef29c5edae6e2441fa9267f6ec60793b1cd01ae4e6f300`

## 3. 工具（`Tools/RingContract/`）

| 文件 | 说明 |
|---|---|
| `contract.json` | 冻结合同（见 §1） |
| `ring_contract.py` | float32 逐行镜像 `CrystalCavernRingContact.Touches()` 的确定性几何模型 |
| `reward_projection.py` | 逐字段前后重算 + 以 `git show a013c15a...` 做源码归一化等价证明 |
| `c05_correlate.py` | 冻结原始逐帧 TSV 的只读关联，不改写历史 `INCOMPLETE` |
| `C24B2RingContractEditor.cs.txt` | 注入隔离 Unity 工程的 Editor 契约脚本；调用**真实产品函数**，不加载游戏场景 |

所有工具默认拒绝覆盖已有输出；复跑请用 `C24B2_EVIDENCE_OUT=<新目录>`，见 `../TESTING.md`。

## 4. 修复后（`After/`）

| 文件 | 说明 |
|---|---|
| `After/route-fields-after.json` | 逐字段前后、派生评分重算、UI 文案、六份旧地图门禁静态证明 |
| `After/reward-factory-equivalence.json` | 14 组 uint 哈希 + 源码归一化 ⇒ `FACTORY_PAYLOAD_EQUIVALENT` |
| `After/ring-matrix-after.json` | 14/14 冻结合同几何模型 + B1 四组真实世界样本 + 运行态 `NOT_RUN` 登记 |
| `After/c05-correlation.json` | C05 有序链、关联键、唯一性论证、控制流模型、P2 下一招证据边界 |
| `After/phase-timeline.json` | 有序阶段时间线（Begin → 跨半血 → Release → Damage → Recovery → Transition） |
| `After/protection.json` | 用户场景 / `ProjectSettings` / 旧证据 / 依赖 / 存档保护哈希 |
| `After/build-identity.json` | Unity 版本、编译诊断、改动源码哈希、证据层级 |
| `After/remote-verification.json` | 本批提交完整 SHA、推送与 `git ls-remote` 复核、`main` 未移动 |
| `After/hash-manifest.json` | 交付目录全量 SHA256（最后生成） |

## 5. 真实 Unity Editor 运行（`Runs/Editor-RingContract-A1/`）

| 文件 | SHA256 / 说明 |
|---|---|
| `Editor.command.json` | 完整命令行、`-projectPath` 隔离工程、`-executeMethod`、输出/日志路径、起始 UTC |
| `Unity.log` | `b669d4c488999b700d4d77ed5d83e07c6ee5d00ce310d84ed7b6c27fab95bf11` — 完整原生日志；`error CS` 0，含 `C24B2_RING_CONTRACT EDITOR_CONTRACT_PASS geometry=14/14 bodies=6/6 rewards=14/14` |
| `ring-contract.json` | `1681f5a219bb9fb2a17c27aed4d54d5f96e8fcc16b7e7c66b9fe2f5752c6969f` — `EDITOR_CONTRACT_PASS`；14 几何用例、6 受击体用例、14 奖励哈希用例逐项 expected/actual/pass |
| `Editor.exit.json` | 原生退出码 0、起止 UTC、无强制终止 |
| `Editor.stdout` / `Editor.stderr` | 原生标准输出/错误（stderr 为空） |

**层级**：真实 Unity Editor batchmode 运行，调用真实产品函数并完成整项目脚本编译；
不是观测 Player、不是纯发行包、不是原生输入、不是独立人工。

## 6. 未运行项（不得推断通过）

`NOT_RUN`：非开发观测 Player（sidecar 驱动）、纯发行包、原生键鼠、独立人工、最终平衡、性能；
墙后遮挡 / 翻滚免疫 / 同次窗口多帧 / 七武器站位的**运行态**验证；连续查询前后状态快照；
六份旧布局新 Editor 评分对照。原因与补跑方式见 `../TESTING.md` 与 `../ACCEPTANCE.md`。

## 7. 历史证据（只读引用，未改动）

- `DeliveryCrystalCavernC24B1/Evidence/Runs/b1-name-cavern-A1/arena-route.json`、`route-ui.txt`
- `DeliveryCrystalCavernC24B1/Evidence/Runs/b1-ring-{inner,outer,band,safe}-A1/ring-release.json`、`ring-damage.tsv`
- `DeliveryCrystalCavernC24B1/ROUTE_AUDIT.md`、`RING_AUDIT.md`、`ACCEPTANCE.md`
- `DeliveryCrystalCavernC24B/Evidence/Runs/WindupNewAudit1/audit.json`、`PlayerWindupA2/`、`PlayerWindupB2/`
- `DeliveryCrystalCavernC24B/Evidence/PlayerPhase1/phase-releases.tsv`、`Tools/Driver.cs.txt`
- `Assets/CombatPrototype/Resources/RouteScoring.json`（权重，未改）

这些文件的 SHA256 已分别记录在 `Before/inputs.json`、`After/route-fields-after.json`、
`After/c05-correlation.json` 与 `After/protection.json` 中。
