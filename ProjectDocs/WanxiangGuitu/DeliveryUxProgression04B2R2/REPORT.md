# UX-04-B2-R2 停止报告

## 决策：BIT_DIFFERENCE_STOP — 等待额外授权

**R-03已取得真实Unity Mono结果：原路径与当前B2路径相差1 ULP。按第六/十节停止条件，已立即停止，不修复浮点实现，不继续R-01代码修复及六场景验收。R-01本轮未完成，不报告修复成功。**

基线95caf234256613d4a6e4f89a8ab0dc09c397c6b2，分支feature/ux-progression-04-b2均未变。现有B2/R1修改全部保留。产品Assembly-CSharp.dll原样复制且仍为6f876c60…，本轮只编译独立观察sidecar。

| 项目 | Unity Player实际记录 |
|---|---|
| runId | UX04B2R2-FLOAT-001 |
| PID / exitCode | 17352 / 21（有意的位差停止码，不是超时/崩溃） |
| buildId | ux04b2r2-float-6f876c60-b70442f9-20eb10c0 |
| Unity / Mono | 6000.6.5f1 / 6.13.0 (Visual Studio built mono) |
| 平台 / 架构 | WindowsPlayer，非Editor，64位 |
| 原Enumerable.Sum装备贡献返回值 / bits | 17.450000762939453 / 0x418B999A（1099667866） |
| 现B2AttackModel装备贡献返回值 / bits | 17.44999885559082 / 0x418B9999（1099667865） |
| ULP | 1；未使用容差 |

[完整运行原件](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R2/SESSION-20261116-R2-01/UX04B2R2-FLOAT-001/result.json>)、[manifest](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R2/SESSION-20261116-R2-01/UX04B2R2-FLOAT-001/run-manifest.json>)、[逐步累加](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R2/SESSION-20261116-R2-01/UX04B2R2-FLOAT-001/state-changes.jsonl>)。数值由同一个真实Unity Mono进程直接调用真实LINQ Sum与加载的B2AttackModel.ComputeAttack产生；Python仅启动、归档、哈希和核对整型bit距离，不计算这些浮点结果。

## 保护与停止范围

先保存完整工作区至I:/unity/WanxiangGuitu-UX04B2R2-snapshot-20261116-1459：42279文件，3.828 GiB，robocopy=1，Mismatch/Failed=0；外部Git metadata另存。R2前保护域12763文件的hash/大小作为输入，最终逐个对快照及当前文件复核，见[保护清单](<PROTECTION_SHA256.tsv>)、[实物核验](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R2/SESSION-20261116-R2-01/protection-result.json>)。961项候选白名单及其原件未更新；新R2文件只记录，未擅自纳入白名单。

未修改任何Assets产品源/Schema/品质/系数/尺寸/概率/随机算法/成本/Boss/P1/P1C/ProjectSettings/Packages/场景/Prefab。没有直接写最终AttackPower。测试三件GearItem是隔离验证夹具，不写玩家库存；夹具序列化前后相同，Unity Random.state前后相同。此Run不冒充PreviewAdd/PreviewReplace九项只读验收，更不冒充六场景正常用户操作验收。

## 交付与待审批

- [FLOAT_RUNTIME](<FLOAT_RUNTIME.md>)：同进程、逐步原值/位值、运行时与身份。
- [单独修复方案](<FLOAT_FIX_PROPOSAL.md>)：仅文档提案，未执行、未生成产品补丁。
- [替换模型状态](<REPLACEMENT_MODEL.md>)、[容量验收状态](<CAPACITY_VALIDATION.md>)：均明确停在实施前。
- [验收状态](<ACCEPTANCE.md>)、[Run矩阵](<PLAYER_RUN_MATRIX.csv>)、[证据索引](<EVIDENCE/INDEX.json>)、[风险登记](<RISK_REGISTER.md>)。

**本轮只有1个新增定向Run。原B2/R1、失败历史及961项冻结清单原样保留。不暂存、不提交、不推送、不合并、不启动UX-05。已暂停，等待负责人对浮点方案及后续恢复工作另行审批。**
