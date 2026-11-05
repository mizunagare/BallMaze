# 机关与探索事件

营地准备选择远古遗迹 → DepartRuins → 原有Depart保存新Run → 保存地形与模块加载 → 广场机关 → 双向可开关石门 → 地下碑文开启密室 → 可选精英/守护者 → 原有免费撤离与结算。

使用既有SavedWorldEvent的entityId/used。c1:lever一次激活；c1:door需机关、角色在门口拒绝关闭；c1:archive一次碑文事件并打开密室；c1:plaza-chest、c1:hidden、c1:hall-chest各有独立身份。交互需真实范围和视线，门仅认可自己的门板作为合法接触，不绕过其他墙体。

交互保存失败时比较完整规范化存档与预期、旧快照：确认新修订已发布则同步live revision；确认旧快照未变化则回滚门/used/落地奖励及检查点；不确定则保留读取屏障。不是直接写库存，也不是只按Run ID推断成功。

阶段3先通过Editor/非开发Player后才启用阶段5。保存ruinsStage=3的旧原型Run不会加载时插入后两区。旧森林1–5布局不进入遗迹分支。
