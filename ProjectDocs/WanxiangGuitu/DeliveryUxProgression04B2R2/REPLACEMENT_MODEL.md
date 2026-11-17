# R2 新增/替换模型状态

**状态：NOT_STARTED_STOP_GATE。** R03先执行真实位比较发现1 ULP，按停止条件不继续R01实施。当前产品仍为原B2/R1代码；不存在本轮已完成的PreviewAdd/PreviewReplace API。

已授权但尚未实施的契约：PreviewAdd只增加指定候选，不自动移旧；PreviewReplace显式传candidateGearId、replacedGearId、targetPosition、replacementRole，不按type寻找或删除旧件。同类饰品/护臂允许并存，不引入唯一类型槽。

后续恢复时，应在克隆装备状态中复用现有Find/Fit/CanPlace及碰撞、旋转、交换规则：旧件退出、新件入目标、旧件安全回包、双方Fit及无非法重叠，失败给明确原因。攻击贡献一律由现有权威B2AttackModel计算，不另建第二套公式。

本轮未实现或验证上述行为，不声明R-01关闭；饰品/护臂/主备武器/容器/Strength/Worn/Overflow替换矩阵均保持待验收。[停止原因](<FLOAT_RUNTIME.md>)。
