# B08 失败历史

历史独立保留，不拼入最终All统计，也不以PASS覆盖FAIL。原始本地完整目录在attempts.json；发布日志仅经过既有许可/凭据脱敏与UTF-8标准化，分别保留原始和发布哈希。

| 尝试 | PASS / FAIL / NOT_RUN | 真实问题和后续处理 |
|---|---|---|
| [Before](Evidence/History/Before/results.json) | 1 / 1 / 0 | 基线源码没有新教程契约，反射探针exit1；只是契约缺失，不冒充修复前完整冒险 |
| [Directed1](Evidence/History/Directed1/results.json) | 2 / 3 / 1 | JsonUtility内联类将旧档null教程物化为默认对象，旧v9关闭引导断言失败；后继两个恢复也实际失败。增加显式hasTutorial；后继依赖改为失败即跳过 |
| [Directed2](Evidence/History/Directed2/results.json) | 2 / 1 / 3 | 已发布设置回调异常后，磁盘无活动Run的占位对象与内存null比较失败；改按hasActiveRun判定，并核对修订/Profile/教程 |
| [Directed3](Evidence/History/Directed3/results.json) | 5 / 1 / 2 | 真实低帧率大步长移动被过滤，主角已经走远但教程累计未足3米，机器人自身320秒期限exit1；改累计实际CharacterController位移，不通过RestorePosition推进 |
| [Directed4](Evidence/History/Directed4/results.json) | 3 / 2 / 3 | 首个规则进程GC/CoreCLR初始化失败，未证明具体根因。当时存在并行导入，之后串行运行恢复，不能据此断言必然因果。另一个真实失败为1280×720/150%营地仅3个设施标签可见；改为有上限的横向/纵向候选避让 |
| [Directed5](Evidence/History/Directed5/results.json) | 9 / 1 / 2 | 8个教程受控检查通过，正常AI用弓瞄低矮石矿时采集停滞、期限exit1；机器人改为真实V换剑及正常普攻接近，不修改资源生命或授予材料 |
| [Incremental6](Evidence/History/Incremental6/results.json) | 9 / 1 / 1 | 复用已结束副本，8规则与40截图通过。首次交接被已有OwnedMove跨运行目录安全检查拒绝，tool-safety-failure.json保留；改为所有源/目标均在同一已核对拥有的副本内的独立包装。正常首进程通过，但恢复比较因未排序出口数组失败；按稳定ID所有字段一致。改用既有region.Capture规范快照，不改产品恢复逻辑 |
| [Normal7](Evidence/History/Normal7/results.json) | 3 / 0 / 0 | 新合成存档、复用已结束副本，三个正常AI进程通过；不是全新导入，不替代最终All |

这些失败均保留真实exit1、进程回执与日志；没有强杀后标成正常退出。后继NOT_RUN不写成PASS。

## 完整All后的营地时钟补测

第一轮完整[All1](Evidence/All1/results.json)实际结束：137 PASS / 2预期探针FAIL / 31 NOT_RUN / 2 UNRESOLVED，0非预期FAIL，协调器exit0。输入4d48e6e0f0aad67e501f059f9bc5c5053d8eda4b；87产品源码、63注入测试、54正常AI执行C#驱动已封存。它没有覆盖后补的营地时钟断言，不作为修复后的最终验收。

源码复核发现Camp.Explore恢复TimeScale=1会推进旧有暂停冷却。先冻结旧产品隔离副本、写入新的共同回归，再仅对营地普通移动改用unscaledDeltaTime，世界TimeScale仍为0；森林普通移动不改。没有重写冷却、存档或战斗时钟。

| 尝试 | 结果 | 证据与解释 |
|---|---|---|
| [ClockEntryFailure](Evidence/ClockEntryFailure/results.json) | 1 PASS / 1 FAIL | 新夹具错误地等待batch自动初始化；原系统在batch明确不自动初始化，测试自身120秒期限exit1。未进入冷却断言，不能作为产品失败或修复证明 |
| [ClockBefore](Evidence/ClockBefore/results.json) | 1 PASS / 1 FAIL | 修正显式隔离初始化后，同一回归在旧4d48产品真实失败。约一秒Editor时间内游戏时间推进0.8341214，技能6→5.165879、攻击2→1.165879、切换1→0.165879、翻滚3→2.165879、药水4→3.165879；exit1，无外部超时或强杀 |
| [ClockAfter](Evidence/ClockAfter/results.json) | 2 PASS | 相同回归、固定后的产品：实际水平移动1.735米、显示E目标真实执行，游戏时间增量0，五类冷却前后一致，exit0 |

ClockBeforeRetry1仅在专属隔离目录将两个产品文件替换为4d48的Git字节，原工程没有回退；其余产品用完整源码核对。ClockEntryFailure、ClockBefore、ClockAfter分别保留，不覆盖。前后冷却回归共同测试源为c7ae847b3f9121236cb5521d4c8fb4a9bc896c05；最早夹具入口错误来自dcded5b，另行记录。

新增回归与修复之后再启动全新B08ReleaseAll，最终数据只取该新根，不将上面的定向PASS拼进最终All。

## 发布检查

全范围git空白检查因原始证据的CRLF/原有尾随空白返回非零；完整约26.7MB输出留在工程外B08Publication，哈希与退出码见[记录](Evidence/Checks/whitespace.json)。没有为了通过空白检查改动日志、源码快照或用户文件；新增作者代码/说明排除原始证据并以cr-at-eol单独检查，exit0。这不是游戏回归失败。

第一轮[暂存字节检查](Evidence/Checks/staged-bytes.json)实际FAIL：刚生成的whitespace.json尚未暂存；没有任何内容哈希不匹配，受保护用户文件也没有进入暂存。按正确顺序纳入新回执后再次检查，最终结果另存，首个FAIL保留，不改写。

Directed5的Project后来被合法复用，当前目录字节不能作为该次原输入证据。Incremental6/PreviousSources是在首次复用前保存的产品与注入源码；NormalInputSources为各次正常流程启动时副本，另存驱动执行源码与哈希。最终All使用另一个全新工程目录，按输入提交独立封存。

部分森林入口受控截图有青色立柱/底座遮住角色，与既有撤离标记的位置和形状相符。本轮未修改这些几何，不将这一画面直接归因为引擎异常；低于大面积纯青帧阈值也不能代表画面完全无遮挡。既有Editor大面积青色帧根因仍单独UNRESOLVED，原生UI及人工理解NOT_RUN；不对生命周期作试探修改。

[所有历史状态与说明](Evidence/History/attempts.json) · [最终结果](ACCEPTANCE.md)
