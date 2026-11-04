# CP06-A失败及迭代

所有历史CP03/CP04/CP05文件未改写。新证据按独立运行目录保存；[manifest](Evidence/manifest.json)分别记录原始与发布副本SHA，原始根I:/WGCombat/CP06A-1104-A保留。日志仅在发布副本压缩/脱敏。

| 尝试 | 实际结果 | 解释/处理 |
|---|---|---|
| BeforeEditor | 4 PASS/12 FAIL，exit1 | 8项新增技能确实缺失；另4项普攻测试未等待原0.25秒换装门槛，被合法拒绝。修正夹具等待，不改产品门槛 |
| BeforeEditor2 | 8 PASS/8 FAIL，exit1 | 旧四武器普攻/技能均真实通过，8个新技能缺失保留为FAIL |
| BeforePlayer | 8 PASS/8 FAIL，exit1 | 非开发基准包独立复现新增能力缺失 |
| AfterEditor1 | 104 PASS/1 FAIL，exit1 | 三目标世界Z轴阵列不与实际枪口汇聚弹道共线，只命中2个；原轨迹保留 |
| AfterEditor2 | 111 PASS/2 FAIL，exit1 | 辅助测试把敌人AI组件禁用，TargetAssist依原合同拒绝禁用目标；只在辅助夹具重新启用实际AI，不改评分/阈值 |
| AfterEditor3 | 113 PASS | 第一轮基本时序与辅助通过；后续增补动画释放断言 |
| AfterEditor4 | 156 PASS/1 FAIL，exit1 | 新蓄势正确前摇动画导致枪口姿态变化，旧低位相机射线使箭真实撞地，第三目标没有伤害；不是碰撞穿透失败，不改该原样本结论 |
| AfterEditor5 | 157 PASS | 正向预置斜线阵列、躯干高度瞄准，3/4.5/6米不变，真实3接触；没有射后移动敌人或放宽断言 |
| AfterEditorFinal | 157 PASS | 最终技能逻辑增加缺少真实相机时不消耗冷却的预检；完整矩阵重跑 |
| ExtraEditor/Final | 12/14 PASS | 衔接、真实翻滚/AI致死；最终增补缺相机及实际动画绑定 |
| 最终Player各进程 | 157/14/7/10/92/43 PASS | 核心、附加、保存、恢复及旧回归分层，实际exit0 |

设计迭代：蓄势先显示蓄势标记，锁定后才启动攻击动画及前摇；后续段提前准备，避免把新技能命中放在动画已结束之后。没有更改任何旧技能时序，也未伪称该设计改进有旧产品缺陷负例。

工具失败：[tool-failures](Evidence/tool-failures.json)。初次Python默认GBK读取UTF8出错，修正显式编码后才编译；一次基准构建仍在运行时过早启动Player，因release回执缺失被拒绝，未启动或覆盖输出；一次只读rg工作目录错误。

原始Editor日志中的UnityEditor.Search.SearchDatabase异常、JobTempAlloc诊断继续UNRESOLVED，不吞日志、不用exit0证明根因解决。所有人工与原生未执行项保持NOT_RUN。

交付索引生成工具曾NameError（缺e变量），实际exit1；验收/复跑文件已生成，随后独立补写索引并核验链接。见Evidence/documentation-failure.json，不涉及游戏断言或源码修改。
