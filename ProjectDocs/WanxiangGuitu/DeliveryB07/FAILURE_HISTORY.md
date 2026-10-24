# B07 尝试记录

这些尝试不是最终 All 的替代品。目录均为工程外隔离副本和合成存档，原始日志保留本机，仓库只发布有清单和哈希的脱敏诊断、测试源码与运行图。后续通过不会抹去先前失败。

| Evidence/Attempts 目录 | 当时结果与定位 | 处理 |
|---|---|---|
| BeforeEntry | 首次入口没有注入新探针，方法不存在 | 修正测试注入；不算产品基线失败 |
| BeforeModelPartial | 开发中途副本接口不全导致编译失败 | 保留，不冒充纯基线 |
| BaselineProbe | 77 个产品 C# 与169fec9归一化一致，探针 exit1：缺少 ForestBossBrain | 真正的实现前红灯；外层脚本 exit0 不改变 Unity 子进程 exit1 |
| Directed1 | 圆形边界浮点比较失败 | 增加1e-5米几何容差，不扩大实际攻击范围 |
| Directed2 | 原始seed8导航被正确拒绝；旧布局测试误要求直接使用它。受控战斗停在缩放时间门槛 | 旧布局从已接受快照重建；初始化使用非缩放时间与明确就绪条件 |
| Directed3 | 测试调用不可访问的内部 CaptureLegacy | 改用公开的只读已保存检查点，不扩大业务 API |
| Directed4 | 生成/原子保存通过；恢复比较受枚举顺序和未处理升级抽取影响；背包填充留空格 | 按稳定ID比较，先实际选完升级再保存；用1×1饰品建立真正满包 |
| CombatDiagnostic1/2 | 背包暂停；手动冲锋步长与旧攻击状态未重置 | 隔离测试键盘、关闭测试面板；修复冲锋使用传入dt和ResetBrain |
| CombatDiagnostic3 | 六攻击命中/闪避/越界、中断死亡通过 | 属于增量受控诊断，不是原生输入；OWNER_CORRECTION说明运行副本修改 |
| Composite1 | 八项受控检查通过，后续 normal handoff 被现有跨根安全检查拒绝 | 记录协调器失败，未把正常AI写成运行通过 |
| Normal1 | 两 Boss 确实被击败，但测试在下一帧死亡管线写回执前断言失败 | 驱动等待实际回执，不修改结果或直接发奖 |
| FixturePatch1 | 旧revision夹具混入新增Boss描述符 | 仅旧布局夹具移除新增字段/描述符；校验器未放宽，三个历史检查复验通过 |
| All1 | 67 PASS、5 FAIL、2 NOT_RUN；其中2个预期探针、2个旧夹具失败、1个报告发布共享冲突 | 完整保留部分运行；不是最终完成的All |
| CombatDiagnostic4 | 四武器普攻/主动技能命中通过，随后中断夹具因前面攻击已触发硬直冷却而失败 | 每个中断夹具重置敌人；另加重复硬直冷却断言 |
| CombatDiagnostic5 | Editor启动未到测试方法，300秒超时 | FAIL；未强杀，独立保存进程状态与无可用窗口关闭记录；不称正常退出 |
| ReportLock1 | 复现旧发布锁失败；首次原子写原型只捕获IOException，重命名抛出UnauthorizedAccessException | 保留工具失败；限定报告文件、两类异常、最多6次有限重试 |
| ReportLock2 | 原失败复现；新发布经历4次重试后完整JSON通过 | 2 PASS及1本地预期负例，未并入最终All的两个标准探针 |
| GuardBefore / GuardBefore2 | 错选旧副本，新增测试依赖HudTop导致编译失败；首次还选了三个历史方法 | 保留协调器选择错误，不称为感知问题的复现 |
| GuardBefore3 | 精确复现：BOSS_INITIAL_HEALTH_BASELINE_FALSE_ALERT，原模板感知基准500，实际Boss生命320 | 新增断言先失败，再同步初始化感知基准 |
| GuardAfter | 同一新断言及40seed、原子回执流程通过 | 最小产品修复，不修改追击/返巢边界或绕行断言 |

最终 All 和上一轮完整 All 的独立结果、退出码与环境超时另见 REPORT、ACCEPTANCE 和 Evidence/INDEX。Editor Search 索引内部异常、Editor启动阻塞、最终 Player D3D12 UNKNOWN 分开归类，不相互推导根因。
