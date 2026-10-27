# S2-R2 本地复跑

仅Python离线审计。不要启动Unity，不读默认玩家目录，不创建玩家档，不改原始证据。新输出必须为不存在的绝对路径。

```powershell
$env:PYTHONUTF8='1'
$py='C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $py -B ProjectDocs/WanxiangGuitu/DeliveryStage2R1/Tests/Test-Summary.py --output D:/WanxiangValidationRuns/S2R2/NEW-Existing35
& $py -B ProjectDocs/WanxiangGuitu/DeliveryStage2R2/Test-R2.py --output D:/WanxiangValidationRuns/S2R2/NEW-Matrix58
& $py -B ProjectDocs/WanxiangGuitu/DeliveryStage2R2/Reaudit-History.py --output D:/WanxiangValidationRuns/S2R2/NEW-History
```

58矩阵复用原35脚本的fixture/write/patch_metric函数（AST提取函数定义，不导入运行整套旧测试），没有第二个调度框架。候选CLI通过实际子进程执行；保存命令、原始stdout/stderr、真实exit、输入、断言、摘要JSON/CSV和源码SHA256。非零/无输出/崩溃不能仅靠期望状态被当通过，结构负例还要求具体文件诊断。

原35fixture唯一变更是在Pending加入`region=metric['region']`，对应真实完整身份；没有改任何断言的期望结果。保留旧源码快照和未经夹具修正的29P/6F结果，不能拿新合法夹具冒称原夹具从未有问题。

修改前复现：将已归档的两个被审脚本存放在同一目录，用：

```powershell
& $py -B ProjectDocs/WanxiangGuitu/DeliveryStage2R2/Test-R2.py --source <被审Module和CLI目录> --output <新的修复前输出>
```

修改前58断言16P/42F是正确新要求对旧版的判定；不是产品42次故障，也不是原包12例已执行。配套ZIP后来取得并核验，原样运行原reproduce.py产生12个输入，再用Reaudit-Supplied.py --inputs <原12输入根> --output <新输出>只读对照。包内源码/hash守卫和旧结果均不改。

## 归一化与资格规则

- 版本1默认economy/Extracted/仅Extracted/Normal＋Resume＋FinalResume。terminal默认Normal，真实终态Death/Abandoned允许按冻结合同通过。顺序无语义的阶段/接受集合规范排序；空数组、重复、错误类型/不支持版本拒绝。
- 计划、冻结stage2-input、指标input都核验CORE和归一化合同；记录的kind/blockId属于稳定条件，description/scope是说明。stage.blockId仍需与实际attempt一致，若case记录blockId也必须相同。
- 原始配置hash按原始字节核验，不能对文件做“等价修复”再计算。合同默认值是审计规则，不是补写原始数据或增加存档版本。
- 登记不是启动；只有NOT_RUN、只有旧launchedUtc登记不能算started。读取现有根sidecar登记，不调用PowerShell执行路径。实际depart和进程/指标痕迹各自列出；只有完整记录的depart身份计出征。
- 可信终态需要与真实depart归属一致。原始声明单列，任何终态身份/结局冲突都不最后覆盖。独立结算记录可供真实旧Snapshot提供原先未记录的outcome，不从指标布尔值猜测。显式null仍拒绝。
- 后继技术失败不抹掉已确认业务终态，但完整合同窗口统计拒绝；statisticsDiagnosticOnly包括行级问题。CSV邻近输出可信、冲突、技术及诊断标记。

## 只读历史重审

`Reaudit-History.py`复用现有Summarize-Matrix CLI，读取本机原有、已结束、拥有者明确的以下根；没有这些本机原件时应记NOT_RUN，不从公开脱敏摘要伪造恢复文件：

- Stage2FinalAll/20261027-010900-ab700d91/Stage2Matrix（19，明确`--legacy-audit`）。
- S2R1/FrozenValidation/20261027-102526-ad379719/Rules 的6主配对组＋2覆盖组（26，schema2原身份）。
- S2R1/BoundaryRecovery2/20261027-101700-1a9ec735/Stage2Protocol（1案例、原实际三进程）。

输出新的JSON/CSV、命令/退出码/错误、原值差异、前后源manifest。46是重审案例数，不是新出征/战斗数量，不合并不同合同的撤离率。工具不改原指标/交易/检查点，原CSV字节SHA单独核验。

本轮无需Unity/构建/31步/26战斗/100规则seed/20物理seed重跑，均记NOT_RUN，原因是没有修改这些依赖或执行路径。原生、独立人工、性能也NOT_RUN；历史根因UNRESOLVED。不要把旧PASS继承为本轮运行或独立审核认可。

## 配套原包12场景复跑

先将已核验ZIP解压到工程外新目录。读取并检查其中的reproduce.py后，从包内s2r1_review目录运行原脚本，不能更改其源码/hash守卫。候选审计读取原脚本刚生成的同一批输入，不覆盖原包或旧结果：

```powershell
# 当前目录为解压后的s2r1_review；两个NEW路径均须不存在。
& $py -B ./reproduce.py --output D:/WanxiangValidationRuns/S2R2/NEW-OriginalPackageReplay
# 回到工程根后运行；--inputs指向上一行的输出根。
& $py -B ProjectDocs/WanxiangGuitu/DeliveryStage2R2/Reaudit-Supplied.py --inputs D:/WanxiangValidationRuns/S2R2/NEW-OriginalPackageReplay --output D:/WanxiangValidationRuns/S2R2/NEW-SuppliedCandidateReplay
```

原reproduce.py退出0代表成功观察旧版行为，包含错误PASS，并非缺陷修复通过。候选12项逐一对照断言及退出码，保存输入前后manifest；结果与58项矩阵分列，不当作新增真实游戏样本。
