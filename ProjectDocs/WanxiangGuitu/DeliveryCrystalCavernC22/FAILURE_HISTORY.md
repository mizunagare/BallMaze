# 失败与重试历史

完整日志保留于隔离根，Git 中记录断言、进程回执、可读文件的 SHA256 及关键截图。较早运行保留原判定。

| 原始记录 | 结果及处理 |
| --- | --- |
| player-driver-compile-BaselineMaterials.log | 两个驱动局部变量遮蔽外部同名变量，编译失败。改名后保留原日志。 |
| BaselineMining1 | 第一帧输入请求被拒绝。复跑等待出征后的输入屏障结束，并独立核对矿脉实际耗尽和物资。 |
| player-driver-compile-ObservedFinal.log | PowerShell 把单个预处理参数展开为字符。显式使用字符串数组后复跑。 |
| player-driver-compile-ObservedC22.log / EditorChamberResume1 | 测试驱动变量 `start` 重名。保留 Compiler 诊断和私有桌面 Safe Mode 证据，在可用的隔离工程用更正后的驱动继续。 |
| PlayerChamberResume3 | 过宽的场景材质检查误将角色遮挡淡化临时材质纳入固定场景资源。复跑检查本批固定素材材质和实机截图。 |
| PlayerElite3 / PlayerElite4 / PlayerElite5 / EditorElite4 | 真实普攻 API 的初始请求被拒绝，未据此判定产品攻击失败。重试仅在真实前摇窗口内发送合法请求，仍要求实际生命下降、释放和受击。 |
| PlayerLive3 / PlayerLive5 / EditorLive4 | 前者缺少三种新武器的出征前合成夹具；后两者在第一次普攻请求失败。保留各自已执行的断言及回执。复跑仍逐项要求活体真实掉血。 |
| PlayerElite6 | 实际打倒精英后升级选择暂停了缩放时间，驱动的缩放计时未结束。改为有限的实时等待，保留首次伤害轨迹和超时。 |
| 首次纯包启动命令 | 对照合成存档位于旧隔离根，脚本在启动前拒绝。使用新隔离根中的等用途合成存档复跑。 |
| PureBuild2 | BuildReport 成功且 0 错误，105 条警告。退出日志仍有 JobTempAlloc 警告，成因 UNRESOLVED。 |
| C1 / R7 / C2.1 | 旧失败、严格像素差异、未匹配阶段指纹与原始验收继续保留。 |

[证据索引](Evidence/INDEX.md)
