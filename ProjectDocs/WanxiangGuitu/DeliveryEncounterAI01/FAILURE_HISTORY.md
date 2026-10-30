# 失败、技术尝试与未关闭项

原任务材料和所有历史交付不覆盖。以下路径均相对本批Evidence（拥有根EAI01-1030-A）。

| 尝试 | 实际结果 | 处理与边界 |
|---|---|---|
| BeforeRepro | 编译exit1 | 固定Unity已禁止GetInstanceID；测试改用对象引用去重。不是游戏AI失败，原log保留 |
| BeforeRepro2 | 6PASS/9FAIL，exit1 | 实际薄掩体越过枪口、对侧射手/Boss叠加、禁用隐藏攻击和独立暂停时钟负例 |
| AfterRepro | 13PASS/2FAIL，exit1 | 已堵穿透，但高薄障碍使旧Steer阻止侧移，停滞。未降低断言，补受物理/导航约束的侧移 |
| AfterRepro2 | 15PASS，exit0 | 原15项同条件复测，不代表后续新增负例已关闭 |
| LateBeforeRepro | 7PASS/10FAIL，exit1 | 新增已发弹体+晚进入近战约.04秒叠加；保留原组合其余旧失败 |
| LateAfterRepro | 18PASS/1FAIL，exit1 | 首修仍遗漏已释放威胁窗，约.08秒；不是用新PASS掩盖 |
| FinalRepro | 19PASS，exit0 | 保留已释放预约后约.24秒，另验证前摇后遮挡取消与不退冷却 |
| BeforeMatrix初轮 | 1个包装PASS、其余8个包装FAIL | 中途新增Guard工具含pois误名/旧版不存在的新API，部分编译失败；后一个真实Unity exit0仍受PowerShell旧LASTEXITCODE=1污染，保留完整命令/原始退出。工具改为方法依赖隔离、修正字段、显式exit0；不归咎产品 |
| BeforeMatrixRetry | 8个新进程PASS | 有界只补失败过程；原真实运行和工具失败均不覆写。此阶段216条件只是旧任务口径的阶段证据 |
| AfterMatrix | 9进程/216条件PASS | 首修中间矩阵，不是最终产品/扩展场景的验收 |
| FinalBeforeMatrix / FinalMatrix | 各9进程/360条件 | 远端任务修订后扩充双近战、多近战混合、两Boss单独场景；全部独立新运行，输入配对/真实死亡/删失完整保留 |

直连GitHub一次DNS解析失败，改用本机已有代理读取，不改变网络/系统设置。实施期间远端仅新增任务/计划两提交，正常快进；第一次/第二次快进因本批计划文件工作区行尾未匹配而被Git拒绝，保存本批文档副本并恢复其原始字节/工作区CRLF后正常快进。没有reset、强推、stash用户文件或回写用户Scene/Settings。

最终矩阵前后均59个玩家死亡、109个窗口删失、192个清场；治疗224→217，不能据此宣称整体难度相同或已经平衡。28个零释放条件均是敌人在玩家移动攻击中被清场，不删样本，也不将它们当成命中率0的正常估计。没有释放时hitRate=-1表示不可估计。

预期的保存故障、背包满等旧规则探针保留在对应原始日志，测试捕获并验证失败语义才是该规则用例通过；不把预期故障日志删除。所有新非预期失败必须在报告中单列。

UI01的D3D12 UNKNOWN、旧C15、Editor青色帧、Search及其他已记录引擎根因不关闭。原生U16、独立人工/最终手感和完整性能仍NOT_RUN。没有新因果证据，不重复无效关闭实验或改产品生命周期来试错。

初轮Invoke-Regression在UX04CombatTiming实际exit0/188断言通过后，目录占用保护检测到同项目Unity残留而停止，进程包装exit1；没有强杀。原脚本另存Failed-Invoke-Regression.ps1.txt；初轮未记录残留PID，不能推断其具体原因。目录随后空闲，只续跑剩余10项，原7项不重复挑样。工具增加30秒有界只读空闲检查并记录PID/命令；仍占用则停止。业务结果与编排中断分开。


交付差异检查仍提示BossBrain、CombatEnemy、ForestBossBrain各新增一个EOF空行；仅格式警告，不把git diff --check写成PASS。为保持已验证/构建输入字节，本轮没有在构建后再改产品源。
