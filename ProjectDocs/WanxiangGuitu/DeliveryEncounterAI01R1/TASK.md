# ENCOUNTER-AI-01-R1：已释放Boss弹体威胁的生命周期

用户明确授权，固定基线b040b550a5725511a34867de4a2cb27dc56a2b95；开工重新核对远端main与本地，保护所有用户改动。

独立源码复审指出ForestBossBrain.OnDisable无条件ClearReleasedThreat，可能在只禁用Boss AI、CombatEnemy和GameObject仍活动时，提前清除仍在飞行的EnemyProjectile对应威胁。

先实际复现：Boss发射、仅禁用ForestBossBrain、弹体继续运行、其他敌人是否仍识别其威胁窗。确认后仅修复必要生命周期：取消尚未释放意图，保留已释放且有效的弹体预测威胁；不改Boss参数/招式/序列、护甲、武器、经济、掉落、随机流、地图或v9。

独立回归覆盖前摇禁用恢复不补发、已释放禁用/恢复、实际命中、弹体销毁、有限窗口过期、其他敌人和Boss正常攻击恢复。原ENCOUNTER-AI-01的524PASS及全部原失败/证据只作为历史保留，不覆盖或继承为R1结果。

使用隔离工程与合成档，不访问真实玩家档、覆盖用户Scene/ProjectSettings/未提交改动、抢桌面、关闭用户程序或强杀进程。不升级依赖、不新增CI。交付报告、验收、复跑说明和原始证据；提交推送，重新核对远端完整SHA，暂停等待独立复审。
