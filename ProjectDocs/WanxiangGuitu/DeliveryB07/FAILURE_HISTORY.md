# B07 尝试记录

这些尝试不是最终 All 的替代品。目录均为工程外隔离副本和合成存档，原始日志保留本机，仓库只发布有清单和哈希的脱敏诊断、测试源码与运行图。后续通过不会抹去先前失败。

| Evidence/Attempts 目录 | 当时结果与定位 | 处理 |
|---|---|---|
| BeforeEntry | 首次入口没有注入新探针，方法不存在 | 修正测试注入；不算产品基线失败 |
| BeforeModelPartial | 开发中途副本接口不全导致编译失败 | 保留，不冒充纯基线 |
| BaselineProbe | 77 个产品 C# 与169fec9归一化一致，探针 exit1：缺少 ForestBossBrain | 真正的实现前红灯；外层脚本 exit0 不改变 Unity 子进程 exit1 |
| Directed1 | 圆形边界浮点比较失败 | 增加1e-5米几何容差，不改变配置范围 |
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

## 后续完整运行与定向回归

- `Attempts/All2`：完整执行，协调器exit1，109 PASS / 5 FAIL / 29 NOT_RUN / 1 UNRESOLVED。失败包含2个预期探针、Boss初始化误警报导致的Bypass失败、Editor截图启动超时与完成标记缺失。两个Boss的正常冒险和12个最终Player进程当轮通过；不能替代后续运行。超时的实际Editor PID133032及host116292保留，不强杀。
- `Attempts/RecoveryBefore`：真实受击回归失败 `HIT_SHORTENED_RECOVERY_OR_COOLDOWN Warden`。`RecoveryAfter`：相同检查对两种Boss通过。修复保留原恢复和就绪时钟，不改伤害或生命。
- `Attempts/RuntimeRestore`：新增恢复断言把无备用武器的null与空串误判为不同，三进程失败；`RuntimeRestore2`仅规范化空ID表示后，Running/Pending/Committed三个进程通过，实际Boss、装备和材料均检查。没有放宽任何非空装备ID。
- `Attempts/All3`：完整执行，协调器exit1，104 PASS / 3 FAIL / 26 NOT_RUN / 1 UNRESOLVED。两探针之外，Land正常AI在三次释放前击败Boss，观察断言失败，其两个恢复阶段及Land Player派生检查按依赖跳过；Lake通过。绕行和受控截图通过。该次产品仍是5ede27b，不含后来的恢复时钟修复。其80个产品脚本、52个注入测试和39个执行驱动均与固定输入匹配。
- 改进证据封存脚本时，Python语法检查曾发现一个多余右括号；在执行封存前修正，随后语法检查和All2封存成功。它是报告工具错误，不归咎游戏，也不计入游戏All探针。

最终结果必须来自新的 `Evidence/FinalAll`，不能合并上述通过项拼成一轮通过。
## 覆盖补齐与固定失败种子

- `Attempts/All4`：113 PASS / 2个预期探针FAIL / 27 NOT_RUN / 1 UNRESOLVED，协调器exit0；15个正常AI进程、12个最终Player进程通过，但还未包含后来补齐的逐攻击中断与种子探针。产品输入dea8f7e、实际正常AI驱动5ff6ffc分别封存，不伪称单一输入。
- `Attempts/AttackConditions`：新夹具120秒脚本deadline，未运行战斗断言。`AttackConditions2`增加后台运行后仍失败，诊断为playing=True、unscaled=119.754、initialized=False。源码确认batchmode默认不初始化存档；新夹具误等IsInitialized。`AttackConditions3`改为显式初始化隔离存档后通过六攻击与冲锋条件。未改产品存档或生命周期。
- `Attempts/All5`：105 PASS / 3 FAIL / 26 NOT_RUN / 1 UNRESOLVED，协调器exit1。除两探针外，Land正常AI在Boss释放三次后遭围攻死亡；其恢复与派生Player按依赖跳过。Lake通过。没有以死亡样本充胜利。
- 改进机器人先应对前摇再接近，并按原翻滚冷却应对普通怪；不改Boss伤害、主角生命或初始5瓶药水。下一完整运行固定重放All5的Land种子1132820888，避免通过换随机地图掩盖失败。
- `Attempts/SeedBefore`缺少安全固定种子入口而exit1；`SeedAfter`通过。新增入口只在Editor、有效隔离参数下设置下一次种子，消费一次并保持Unity全局随机状态；正式Player不编译入口。存档格式与既有在途种子不变。

最终判断仍以新的FinalAll为准。All4的通过不覆盖All5死亡，也不能替代最终固定种子的复验。

All4完整日志另做异常清单：56处以Exception行开头的记录均带UnityEditor.Search索引调用栈，见Attempts/All4/exception-inventory.json。这不等于Editor运行零异常；具体测试断言、正式Player与Editor内部索引问题分别报告，不能将其归因于游戏，也不能凭测试exit0把日志异常隐藏。最终轮同样检查。
