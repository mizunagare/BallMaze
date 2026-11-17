# 空间容量与无副作用验证

## 几何判定，不只比较占格数

[Fit:189–197](<../../../Assets/CombatPrototype/AdventureLoadout.cs#L189>) 对每个旋转后的真实 cell 校验容器 Allows、占用与重叠；[CanPlaceState](<../../../Assets/CombatPrototype/AdventureLoadout.cs#L233>) 校验归属、容器/携带武器限制、边界及交换双方能否落位。[ProjectBoard](<../../../Assets/CombatPrototype/AdventureLoadout.cs#L98>) 要求只碰撞指定旧件，失败不兜底搬走其他装备；[PreviewContainer](<../../../Assets/CombatPrototype/AdventureLoadout.cs#L287>) Clone 重排并验证旧容器安全回包，空间不足即整体拒绝。

最终六Run来自正常 factory/Add/Place setup，不改尺寸、数值或资产。拒绝案例原件：[D 满盘/多件碰撞](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-board-insufficient/result.json>)（AP 240→240，reason=目标碰撞非指定旧件或多件装备），[F 双向尺寸不兼容](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-illegal-swap/result.json>)（AP 54.6500015→54.6500015）。合法交换 [E 原件](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-legal-swap/result.json>) AP 57.5→69.5、swapped=true、旧件回包，完整结果与投影字段一致。

## 独立几何复核

最终 [oracle](<EVIDENCE/REPLACEMENT_ORACLE.md#L38-L42>) 独立从资产形状与原始状态复核：D 盘满48格，目标 (0,2)/(1,2) 在界内但碰到非指定其他ID；F 双向交换时旧件回到候选原位置后占格含 (12,0)，超出包边界；E 合法交换回包格 (11,0) 合法。故失败不是只信 UI reason，也不是把盘外目标冒称满盘失败。

## 取证口径

[最终观测驱动](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-illegal-swap/ReplacementDriver.compiled.cs>) 的 Nine/Capture/Change 保存九类 canonical **完整 JSON 字符串**与 UTF16FNV：GearItem、Inventory、EquipmentGrid、Main、Reserve、Worn、Overflow、AttackPower、Container。random 保存 Unity 状态、ActiveRun、训练流；save 对目录每个文件保存相对路径、字节数、base64、SHA256。不是仅比较 FNV，也不删时间戳、revision 等 save 字段。

- 全六Run UI Evaluate：九类、random、save 全不变。
- D/F 真实拒绝 Commit：同样全部不变；成功 Commit 则对照完整 projected item fields、ID集合、主备槽、AP/普攻位及旧件回包，不能要求成功装备操作完全不变。
- 每次通过 InputSystem 鼠标状态→EventSystem Raycast→正常按钮，不使用 onClick.Invoke。setup API 和附加 API 检查单独标注，不计作真实 UI 操作。

## 自然保存边界不是关闭保存器

A05 F 的九类与 random 相同，但 5 秒自然 autosave 写盘，原结果仍 FAIL。A06-PROBE 仅调整验证器：**等待正常 LastSavedAt 自然推进**，确认无保存失败、到达原 nextSave 且无 focus/pause 跨界；随后在同 timer 周期内前后取样，跨窗就失败。

最终 F [measurement-gates 原件](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-illegal-swap/original-root/measurement-gates.jsonl>) 可见 interval=5、LastSavedAt 由 4.07351732→9.073833，再由 9.073833→14.0754652；自然写盘的完整前后保存数据如实记录。产品保存器未关、interval/clock 未改、save 字段未过滤；等待不等于“伪关自动存档”。[状态前后原件](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-illegal-swap/state-changes.jsonl>) 与 [逐项检查](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-illegal-swap/checks.jsonl>) 共同界定测量窗，失败数据没有豁免。独立 [oracle逐项原件](<EVIDENCE/REPLACEMENT_ORACLE.json>) 还核对12个自然gate共163项检查、gate-after与操作before的保存字节衔接，以及操作两侧LastSavedAt均属于同一自然边界。

附加 Reserve0、Worn 本体 Attack0/排除 Active 但容器槽总贡献6、Strength3/bonus15、Overflow0、BoardAdd保留旧盘装备，仅属 API 证据；不是额外真实 UI 场景。
