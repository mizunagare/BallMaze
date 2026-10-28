# COMBAT-01 验收

本表区分当前产品规则证据、运行层次和仍开放事项。不是独立复审结论。原始失败始终保留。

| 编号 | 项目 | 结果 | 证据／边界 |
|---|---|---|---|
| C01 | 修复前四武器时序、命中和取消基线 | PASS | Baseline2：92 PASS / 33 FAIL；FAIL是针对新合同的负例，不是33种独立缺陷 |
| C02 | 四武器普攻：命中、未中、距离外、遮挡、多Collider | PASS | After4受控Play Mode，HP真实变化，逐帧时间 |
| C03 | 四武器技能及白至红品质弹数 | PASS | After4，保留长枪追加段和弓独立箭 |
| C04 | 单次释放及每目标／每伤害段去重 | PASS | After4，多Collider与紫枪3.2倍原合计伤害 |
| C05 | startup、释放与取消 | PASS | After4，输入帧不扣血或生弹；翻滚、UI、暂停、死亡、切换取消未释放攻击 |
| C06 | 冷却接受时开始、重复拒绝、取消不退款 | PASS | After4；未增加后摇锁或普攻/技能互斥 |
| C07 | 已释放弹体切换保留、暂停恢复、死亡／重置／卸载清理 | PASS | After4；暂停3.2秒不消耗弹体寿命 |
| C08 | 起手与实际伤害反馈 | PASS | After4受控截图与HealthObservation；不是人工动作观感验收 |
| C09 | 重复弹体与自有材质有限负载回收 | PASS | 3轮×12弹体自然到期，材质数回归；不是零GC或全局无泄漏证明 |
| C10 | 既有输入、健康观测和B07战斗回归 | PASS | Regression1：3个Editor过程exit0 |
| C11 | 正常AI采集、渡口、结算、制造与新进程继续 | PASS | Regression1：Normal/Resume/FinalResume，正常敌人AI，Editor驱动 |
| C12 | 临时非开发验收Player实际业务与恢复 | PASS | Story2六进程exit0，23项独立业务核账；虚拟设备／uGUI／独立窗口消息，不是原生输入 |
| C13 | 非开发发行构建及测试驱动剔除 | PASS | R2：0错误93警告；T3：0错误116警告；两者BuildOptions.None；PE与143程序集检查 |
| C14 | 无测试驱动发行Player标题实际显示 | PASS | ReleaseSmoke/title-player.png、entry-audit、exe哈希 |
| C15 | 本次发行Player后台关闭的限时退出确认 | FAIL | 30秒内未确认宿主退出；请求已发送不等于正常退出，未强杀。后续PID消失也不补造退出码 |
| C16 | 新增“前摇中写盘再新进程恢复”专用用例 | NOT_RUN | SaveRun隔离Editor停在启动阶段；已有受控RestoreCooldown和Story2跨进程恢复不能冒充该专用用例 |
| C17 | 原生U16 | NOT_RUN | 当前没有获准的独立交互环境 |
| C18 | 独立人工战斗手感／可理解性 | NOT_RUN | 截图、Editor与验收Player不替代人工 |
| C19 | 完整性能预算与有效GC字节测量 | NOT_RUN | 沿用PERF02能力边界；未宣称零分配或性能达标 |
| C20 | D3D12 UNKNOWN根因 | UNRESOLVED | 无新因果证据，不重复关闭实验 |
| C21 | Editor青色帧根因 | UNRESOLVED | 未用稳定截图关闭历史问题 |
| C22 | Editor.Search内部异常 | UNRESOLVED | 本轮原始日志保留其完整栈，未归咎于战斗代码 |
| C23 | JobTempAlloc根因 | UNRESOLVED | 原始日志保留；不与有界Material计数混为一谈 |
| C24 | 附加Editor启动阻塞 | UNRESOLVED | Baseline3／SaveRun，无战斗用例结果；保留进程与目录，不强杀，不猜测根因 |

条目汇总：**14 PASS / 1 FAIL / 4 NOT_RUN / 5 UNRESOLVED**。与188项受控断言、进程次数属于不同统计单位，不能相加制造通过率。整批不是全绿，也未宣称独立复审通过。
