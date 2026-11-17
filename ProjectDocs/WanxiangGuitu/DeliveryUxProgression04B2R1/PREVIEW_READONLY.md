# PreviewReplacement 九项只读验证

按每次调用分别保存调用前后 canonical 明文与指纹：GearItem、Inventory、EquipmentGrid、Main、Reserve、Worn、Overflow、AttackPower、Container。必须逐项一致，不用单个汇总布尔值代替原始记录。

预览计算使用装备副本和局部主备 ID；不改动装备字段、容器定义、收藏或存档。预览完成后通过真实 EventSystem 输入将被预览武器设为主武器，确认实际装备操作仍有效。

最终A03：8种角色×9项＝72/72前后相同，144个前/后指纹由独立UTF16 FNV1a64重算，另有真实选中与设为主武器成功，Player 10/10检查通过。canonical包含装备全部现有字段、原始ID列表顺序、物品位置/状态、材料药水、主备、穿戴、overflow、真实攻击链以及完整容器定义。指纹只覆盖明确定义的这九类业务状态，不泛称所有Unity运行时对象内存完全不变。

输入/原始快照/独立复算结果见 [证据索引](<EVIDENCE/INDEX.json>)。有效角色与类型不匹配早退必须在原始记录中区分；本轮 C-06 的关闭依据是九项只读与实际可用性，不扩展为所有替换方案数值及容量可行性的完整验证。
