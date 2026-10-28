# COMBAT-01 失败与尝试

所有运行目录只增不覆盖，最终数字见 REPORT 与 Evidence。

1. `Baseline`：初版受控驱动错误使用batch mode且等待自动存档初始化。产品在batch mode明确不自动初始化，等待到驱动240秒deadline，Editor主动exit1。不是产品战斗结论，不是强杀或正常游戏退出证明。保留完整日志、命令及退出回执。
2. 修订驱动复用UI01 GameView、非batch隔离Editor；运行于原始产品源码副本 `B/Project`，不会用修改版回写修复前目录。受控阶段关闭正常AI/流程推进/自动保存，仅用于几何、HP、时钟及对象实验；不冒充正常AI冒险。
3. 旧源码基线已观察到剑、枪输入帧扣血，杖、弓输入帧生成弹体。原命中去重等已成立的PASS仍保留，不把整轮FAIL解读为所有行为错误。

后续尝试与状态以每个独立目录中的原始 JSON/日志为准，尚未运行项不能继承历史PASS。

4. `After2`：新加固定seed夹具提前读取尚不存在的ForestRegionRuntime，测试异常。改为使用既有AddComponent初始化入口；没有修改产品生成器。
5. `After3`：188项规则通过，但夹具只卸载角色后退出，遗留Session退出保存钩子访问已销毁角色，原始NullReference栈保留。因此不能仅凭exit0判定干净。夹具在拆除前显式SuspendEntry，新增独立日志引用异常检查；`After4` 188项通过，没有这项空引用。没有修改产品保存/结算钩子来掩盖夹具错误。
6. `Baseline3`：额外旧版复跑停在Editor启动阶段，600秒超时，未取得新增规则结果；保留原进程/目录，不强杀，也不回写成PASS。已经完成的Baseline2不受影响。
7. `SaveRun`：新增前摇写盘/跨进程专用实验同样停在启动阶段；没有生成断言回执。Resume依赖不成立，保持NOT_RUN。
8. `Story`原验收Player：Setup通过，Main实际采木并击败普通敌人后升级；checkpoint显示level2、三个offers。旧采集循环忽略真实升级选择，30秒无命中失败。有限复用PERF01的真实Digit1选择处理，不改产品或原失败截止时间。`Story2`新的六个Player进程及23项核账通过；两批不同Run，失败未覆盖。
9. `ReleaseSmoke`：纯发行Player标题实际显示，WM_CLOSE请求成功排队，但30秒内未确认宿主退出，测试FAIL；没有强杀。后续观察不到原Player PID不等于取得了实际退出码，不记正常退出PASS，不混同原生标题栏关闭。
10. Windows命令宿主曾返回控制台0xE9启动失败，原输出保留在执行会话；对应编辑命令未完成，随后重新读取文件并用NoProfile入口执行，不假称前一次写入成功。
