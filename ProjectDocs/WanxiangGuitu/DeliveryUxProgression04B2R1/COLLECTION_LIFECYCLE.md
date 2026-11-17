# 收藏生命周期与跨容器保护

- 收藏为进程内 `HashSet<string>`，键是 `GearItem.id`。不属于背包或仓库、不写入装备或存档字段；进程重启清空。
- `BatchPreservesFavourites(beforeIds, afterIds)`仅要求本操作 before 集合内的收藏 ID 在 after 中仍存在。
- `SortBag`只提交背包内操作对象给收藏守卫；`SortWarehouse`只提交仓库对象；其它容器中的收藏不会造成误拒绝。
- Deposit/Withdraw沿用既有事务，移动/Clone保留同一ID，不读写收藏集合；整理不取消收藏。
- Salvage继续沿用既有受保护、品质、矿石堆栈门禁；额外收藏门禁阻止分解。所有失败分支不移除收藏，成功消费后执行ID清理。返还数量保持 `quality+1`。
- 成功分解后的陈旧项清理以随身、仓库及现有待领取装备ID联合为存活集合，防止把仓满待领装备当作销毁。

真实Player顺序：收藏 → 入库 → 仓库有收藏时整理背包 → 取回且仍收藏 → 背包有收藏时整理仓库 → 取消收藏 → 正常整理 → 再收藏 → UI和产品门禁拒绝分解 → 取消收藏 → 两步确认分解成功 → ID不再收藏 → 保存同角色 → 新PID加载同档，装备保留、收藏清空。

每一步记录before/action/after；真实鼠标动作、初始化API、直接门禁API测试分别标注，不能混称全程鼠标。详见 [验收矩阵](<PLAYER_RUN_MATRIX.csv>)、[证据索引](<EVIDENCE/INDEX.json>)。
