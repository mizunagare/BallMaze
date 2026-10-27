# S2-R2 失败与兼容历史

原始路径统一位于`D:/WanxiangValidationRuns/S2R2/20261027-115821-offline/`。每次输出目录独立，原件不覆盖。

1. 配套ZIP路径未提供：检查任务书指定名称和常见输入位置，未找到；异步询问路径。标BLOCKED_SOURCE_UNAVAILABLE，未假称下载/读取/运行原包。修改前源码按实际b4a08e98复制，Git payload与任务书给出的blob/SHA一致；任务书明确负例独立重建。
2. 新离线测试入口第一次有第78行字符串引号SyntaxError，exit1，未执行任何案例。错误版脚本和错误回执在外部根保留；只修测试语法，不当作被审汇总器失败。
3. `Existing35Before`：35P。`TaskMatrixBefore`：51断言13P/38F；随后补预期结局集合内漂移检查，`TaskMatrix52Before`13P/39F。最终57有限矩阵按同一修改前模块再跑：16P/41F。旧源码快照保持不变，新增用例不是新增战斗或扩大平衡样本。
4. `TaskMatrixAfter1`51P；`Existing35UnchangedAfter1`29P/6F：旧合法控制夹具的Pending缺region，无法证明完整终态身份，影响R01完整/分组、R07正常子例、R09完整子例及R10两终态。仅在原fixture的Pending写入已经存在的`metric.region`，保留35项原断言和期望，没有放松候选工具。旧夹具原件、35P旧版结果和29P/6F新拒绝结果保留。
5. `TaskMatrix52After`52P、`Existing35After2`35P。这里尚未形成最终冻结输入，不继承为新冻结执行。
6. `HistoricalAfter1`：26受控案例通过；旧19和完整三阶段案例被候选误拒，原因是Stage2Experiment.Snapshot从来没有outcome字段，合法结局实际在独立结算记录。核对实际源码和文件后，允许“字段确实未记录＋实际同Run结算枚举”确认结局，仍检查Pending全部身份；显式null/无效值/身份或结局冲突不能被后文件覆盖。不填旧字段，不读取存档猜测。添加对应正/负兼容用例。
7. 新增kind条件绑定与description元数据正例，形成最终固定57矩阵；`TaskMatrix57After`57P、`Existing35After3`35P、`HistoricalAfter2`10组46例P。所有原值不变。
8. 工具/测试冻结4ccffe99后新运行`Frozen57`57P、`Frozen35`35P、`FrozenHistory`10组46例P。组合PowerShell末尾查询不存在ZIP使壳层exit1，但三个实际测试命令明确exit0，分别保存；没有把该查询错误当测试失败或掩盖。没有重跑Unity/战斗/构建来凑PASS。

负子进程按预期exit1/2的断言PASS与游戏PASS不是同一计数。旧S2-R1的失败记录、31步、26场及历史引擎诊断不变。本批只修离线工具，根因未定位仍UNRESOLVED，原生/人工/性能NOT_RUN。

9. 最后增加一条RV-02兼容边界：现代attempt/stage不可经legacy参数降级。修改前58矩阵16P/42F；增加guard后58P、原35P、10组历史P。最终工具冻结233db6a2027c462ee8cf2dc8c08b78b6412bed4e，FinalFrozen58/FinalFrozen35/FinalFrozenHistory各自新运行通过；此前4cc/57矩阵及源快照仍保留，不改旧结果。
