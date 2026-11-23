# UX-05 v10 R1 补验报告

**CONDITIONAL_PASS。** P0、P1、uGUI 和 P3 的约定场景已有运行证据。IMGUI 完整交互在当前窗口环境未能有效送达，仍待前台复验。

R1 在 feature/ux-progression-05-objective-history 上执行。HEAD 为 ae705b944b7d0fe851fbd395229dfc30ec636f5c，父提交为 95caf234256613d4a6e4f89a8ab0dc09c397c6b2。开工时暂存区为空。GitHub 域名在运行环境无法解析，本地 HEAD、父提交及远端跟踪引用已核对。

## 原始 68 条 Run

59 条 PASS 均逐条读取原始结果，按原始 status 或 pass 判定。原索引 1366 个文件逐项复算 SHA-256 和长度，三种构建实际 EXE 与 DLL 也与原记录匹配。完整历史行及原始结果路径见 [原始矩阵](EVIDENCE/R1/original-runs.csv)。

| 原始 Run | 矩阵原状态 | 含义 |
|---|---|---|
| CAPACITY-A01 | SUPPLEMENTAL_STOPPED | 已完成独立的容量复测后关闭加跑 |
| CONTRACT-A01 | FAIL_LAUNCH | 探针启动失败 |
| LOCK-CONTENDER-A04 | EXPECTED_NEGATIVE_BLOCKED | 同根写者被拒绝，探针原始 FAIL |
| MIGRATE-A02 | FAIL | 长路径迁移探针失败 |
| MIGRATION-CUT-A02 | PROCESS_CUT_WITNESSED | 独立宿主观察到故障切点并中断 |
| MIGRATION-CUT-A03 | PROCESS_CUT_WITNESSED | 独立宿主观察到分页切点并中断 |
| PAIR-V9-A01 | OBSERVED_STARTUP_ONLY | 启动观测 |
| UX03-sword-circle-A01 | OBSERVED_STARTUP_ONLY | 启动观测 |
| UX03-sword-triple-A01 | FAIL | 游戏场景初始化超时 |

上表省略了统一的 UX05-20261119 前缀。原始 Run、结果与分类保持其原值。

## R1 验收证据

| 优先级 | 验收项 | 结论和证据 |
|---|---|---|
| P0 | 归档前、外置分页写入前后、候选写入前、替换前后 | PASS。A3、P3、Q3、C3、REPLACE 和 AFTER2 分别观察切点，重启逐项核对原档、归档 SHA、分页、Pending 标识和材料。 |
| P0 | 候选校验失败、替换后回执丢失 | PASS。CHECKSUM 损坏候选校验后未发布目标。RECEIPT2 丢失回执后可直接读回 v10，冷启复用现有迁移，保存状态仍为 Pending。 |
| P0 | Committed 回读受阻、过期世代写入 | PASS。SAVE-READBACK、SAVE-STALE 真实生成 Pending。隔离实验分别持有主档读取拒绝句柄和改变备份世代，核对冻结回执、拒绝重试与恢复后完整收益计划。 |
| P0 | 同根并发、v9 访问 v10 | PASS。两个 v10 PID 运行区间重叠，第二写者被拒。正式 B2 逻辑的旧版副本在默认旧根看不到隔离新版，强制放进旧根后识别未来版本，两次拒绝中候选存档指纹均不变。通用探针的原始 FAIL 保留。 |
| P1 | 128/129、旧终局重放、重复结算、同 Run 冲突和跨 Run 同目标 | PASS。R1 用 129 次真实结算生成的 v10 档复测已裁剪终局，最新回执已经更新，拒绝前后 SHA 一致。另有实际出征中的换卡拒绝、放弃结算和跨两局同 ID 验证。DUAL-OBJECTIVE-A02 在实际业务生成的 Pending 副本中加入第二个不同 ObjectiveId，正确重算校验。产品拒绝两项目标共用同 Run 的候选，原始 FAIL 和前后相同文件指纹保留。 |
| P1 | 双 UTC、同时间排序、改名 | PASS。SAVE-STALE 与 SAVE-READBACK 恢复后整条历史与冻结快照一致。混合夹具保留真实结算的 Run ID 和名称，为三项指定相同完成时间并引入提交时间并列。实际 uGUI 七页顺序与独立复算相同，目录改名后仍显示保存的名称。 |
| P2 | uGUI | PASS。真实控件输入覆盖打开、关闭、上一页及下一页、地区排除、目标类型排除与恢复、空历史和旧版未知。七页为 20、20、20、20、20、20、8 行，查询前后主档相同。 |
| P2 | IMGUI | NOT_RUN（有效交互）。使用队列、OnGUI 测试事件和本进程窗口消息的尝试均未打开产品控件。A05 物理鼠标探针无法确认独立 Player 处于可安全操作的前台，守卫中止。所有原始 FAIL 保留。 |
| P3 | D-23 | PASS。隔离 Mono Player 对各地区和双首领标记做独立受控比较。在同装备和相同随机输入下检查攻击、防御、256 个掉落预览结果、仓库和背包材料及已解锁配方，切换地区记录后结果相等。同步查验真实三地区记录和只读查询。 |
| P3 | UX-03、B1、B2 | PASS。七武器 14 项代表回归完成。B1/B2 用原 v9 正负品质夹具重新迁入，验证金红拒绝分解、仓库存取、收藏和替换预览实装一致。 |

R1 全部新增 Run、退出码、二进制身份及原始路径见 [执行矩阵](PLAYER_RUN_MATRIX.csv)。构建身份见 [身份表](BUILD_IDENTITY.tsv)，逐字段与文件复算见 [独立复核](EVIDENCE/R1/independent-review.json)。

## 失败与复测记录

| 初次现象 | 诊断与新证据 |
|---|---|
| A02 Acceptance 编译失败 | 测试内的 Event DTO 遮蔽 UnityEngine.Event，修正类型限定后 A03 编译并执行。 |
| 初次迁移批次部分宿主结果不完整 | 宿主复核错误地按枚举值 1 判 Pending。按实际 Pending 值 0 修复，保留原目录，在 A3/P3/C3 重跑。 |
| CANDIDATE2 在目标切点之前终止 | 中转目录加分页名称触及 Windows Mono 路径边界。原档保留，C3 使用短隔离根命中预定切点并通过恢复。 |
| UI A01 无法读主档 | 独立夹具生成器输出了小写校验值，产品格式需要大写。保留首跑，夹具修正后 uGUI-A02 和混合 uGUI-A03 通过。 |
| B1B2-A01 缺金红背包夹具 | 复用了已由历史验收改变装备位置的 v10 快照。从原 v9 夹具重新导入后 B1B2-A02 通过。 |
| UX-03 两个长枪用例超时 | 同期窗口运行在 warmup 或 cooldown 阶段停滞。分时启动并沿用相同数值断言，两个 R1-A02 稳定通过。 |

## 保护和范围

仅测试工具和 UX-05 自身的 Acceptance 探针接点变更。v9/v10 Schema、收益公式和迁移业务流沿用冻结方案。所有故障和数据投影发生在独立试验根。真实用户存档未访问。原始证据保留。项目保护与当前检查见 [保护核对](EVIDENCE/R1/protection.txt)。

## 最终构建 [B] 与启动 [P]

Acceptance-A06、NoDefine-A03、Release-A03 退出码均为 0。早期 NoDefine 和 Release 的产物排除了探针类型，但 ConditionalAttribute 仍嵌有 UX_ACCEPTANCE 字符串。将探针定义与调用统一放入编译守卫后重新构建。最终 NoDefine 和 Release 两个产物均检测不到该字符串、探针及观察接点，均从空隔离目录启动至标题且未生成主档。Release 发布回执与实际 EXE SHA 一致。完整值见 [最终构建身份](EVIDENCE/R1/final-build-identity.json)。

## 剩余边界 [H]

IMGUI 尚需实际点击覆盖打开、关闭、两类筛选、七页、空历史和未知历史。R1 拒绝将未送达的输入算作功能通过。极长路径下 Mono 仍可能拒绝归档，隔离测试已观察到安全拒绝并用较短路径复测恢复。故障注入针对进程级切点和读取异常。现场断电耐受性未验证。

## Run 汇总

新增 79 条 Run，原 68 行逐字段保持一致。当前矩阵共 147 行，证据索引覆盖 4142 个文件。本轮原始 FAIL 保留。预期拒绝、故障切点和缺少宿主回执的尝试单列。

| R1 分类 | 数量 |
|---|---:|
| EXPECTED_NEGATIVE_BLOCKED | 1 |
| FAIL | 15 |
| FAIL_TIMEOUT | 4 |
| INCOMPLETE_EVIDENCE | 5 |
| PASS | 43 |
| PROCESS_CUT_WITNESSED | 11 |
