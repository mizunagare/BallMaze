# R2 容量与交换验收状态

**全部NOT_RUN_STOP_GATE，不能记PASS。** R03真实位差出现后，未执行新增/替换模型修复与下列任何正常用户操作Run：

| 场景 | 状态 |
|---|---|
| A 同类型饰品替换 | NOT_RUN_STOP_GATE |
| B 同类型护臂替换 | NOT_RUN_STOP_GATE |
| C 主武器替换 | NOT_RUN_STOP_GATE |
| D 装备盘空间不足 | NOT_RUN_STOP_GATE |
| E 合法交换 | NOT_RUN_STOP_GATE |
| F 非法交换 | NOT_RUN_STOP_GATE |

本次float夹具中的board坐标只是固定输入状态，**不是CanPlace/Fit/交换机制实测**。不把其无重叠布局当容量验收，更不以feasible=true代替真实可行性。失败只读与完整Inventory/Main/Reserve/Worn/Overflow/Container/存档/随机指纹尚未对新Preview API执行，因为该API没有在本轮实现。
