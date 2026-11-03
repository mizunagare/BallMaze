# 冻结范围内发现的问题与单独修复提案

## F01：第二次训练重开（FAIL，等待授权）

Editor1通过真实Button.onClick调用原训练重开；第一次成功，第二次在CP05Training.Restart的CreateScene抛`Scene with name "CP05 Independent Training Restart" already exists`。源码先创建固定同名新场景，再卸载当前场景；当前场景正好已叫此名字。原堆栈在Editor1/Unity.log.gz，执行时工具快照保留。该轮缺少完整测量回执，普通关闭exit0不构成测量成功。

最小提案：只修改CP05Training.cs，在创建前使用训练专用、可验证唯一的场景身份，重开失败时可靠复位restarting。保持原销毁/材质清理/新角色创建路径，不写生命、库存、存档、RNG，不让第二次调用被永久锁死。需单独授权后验证三次连续重开、暂停/死亡后重开、旧场景和材质销毁。**本批未实施。**

## F02：训练敌人死亡掉落缺少Session（FAIL，等待授权）

Editor2连续真实攻击杀死敌人后，CombatEnemy.DropLootOnce在`Object.FindFirstObjectByType<CombatSession>().Wave`处空引用。CP05训练设计没有正式CombatSession/Run，因此随机装备掉落分支有上下文缺口。原始异常/完整堆栈在Editor2/Unity.log.gz，不删除或改成PASS。

这确认了本次训练环境分支问题，**不能由此推断正式森林都有同样空引用**。本批不修改CombatEnemy、掉落概率、经验、随机流或经济。后续需先明确训练专用的临时战利品上下文，再授权最小文件范围；不能简单跳过掉落、静默填Wave=1、注入奖励或创建会写真实进度的Session。应配对验证训练与正式Run的死亡、掉落归属/唯一性及无真实存档写入。

## 与采样的关系

最终性能夹具每阶段销毁整个旧训练实例/卸载旧场景，再从原训练工厂创建全新实例，**不调用有缺陷的重开按钮，也不声称该按钮通过**。连续弹体负载朝空闲方向，保留真实物理与碰撞；不杀敌、不伪造命中。两项产品FAIL仍开放，纯包仅作为受控试玩候选，不能以采样成功宣布产品问题解决。
