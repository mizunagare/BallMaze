# 显式 Add / Replace 模型

## 请求与只读投影

[入口:33–95](<../../../Assets/CombatPrototype/AdventureLoadout.cs#L33>)：Add 传 candidate ID、target、role、rotation，不指定也不猜旧件；Replace 另传真实 replaced ID。拒绝重复/空ID、非合法包内候选、同一新旧ID、错误角色、非法旋转和非法当前包位置。失败返回 reason，不把“同类型第一件”当替换目标。

[ProjectEquipment](<../../../Assets/CombatPrototype/AdventureLoadout.cs#L50>) 在 Clone 列表上推演；[Evaluate](<../../../Assets/CombatPrototype/B2AttackModel.cs#L175>) 从同一权威链取得 before/after/AP/普攻/贡献/容量；失败 after 保持 before。[ProjectedItems](<../../../Assets/CombatPrototype/B2AttackModel.cs#L67>) 设置和返回均防御性 Clone，调用方不能借结果改真实装备。贡献来自真实 Active 或容器槽加成，不是候选自身攻击减旧件自身攻击。

## 空间、身份与提交

- Board Add 不驱逐旧件。Board Replace 只准覆盖指定旧件；覆盖非指定或多件立即拒绝。
- 碰撞交换用 [CanPlaceState / PlaceState:233–264](<../../../Assets/CombatPrototype/AdventureLoadout.cs#L233>) 双向 Fit，旧件必须能回到候选原处；失败不以 Find 偷换位置。空目标替换才在投影里安排旧件安全回包；无处回收则整个失败。
- Main/Reserve 坐标固定为候选当前包坐标，不移动/旋转；旧ID须对应真实槽。Container 使用 (-1,-1)、rotation=0，且须明确指定真实 worn ID。
- [ApplyEquipment:130–156](<../../../Assets/CombatPrototype/AdventureLoadout.cs#L130>) 不信缓存 feasible，不信可变投影，提交时重新 ProjectEquipment。Main/Reserve 走原 SelectMain/SelectReserve，容器走原 EquipContainer（保留营地保存事务）；Board 共用 PlaceState 或提交已重新验证的完整投影。ID、数值、词缀、来源保留。

## 两套工作面与覆盖界线

[ReplacementSession:10–33](<../../../Assets/CombatPrototype/ContainerInventoryView.cs#L10>) 统一候选/旧件锁ID、模式、role、target、rotation、Evaluate/Commit；参数变化须重新预览。[IMGUI 工作面](<../../../Assets/CombatPrototype/ContainerInventoryView.cs#L117>) 与 [uGUI 工作面](<../../../Assets/CombatPrototype/CatInventoryPresenter.cs#L86>) 都呈现真实ID、前后 AP/普攻、精确贡献、容量、swapped、旧件回包及 reason，关闭后回原界面。

模型和 UI 独立 review 已通过（主线程确认）；最终 [独立 oracle](<EVIDENCE/REPLACEMENT_ORACLE.md>) 对成功Commit的实际/预测 Single位、完整字段投影和ID/状态保全复核通过。本轮六端到端 Run **仅为 uGUI**；IMGUI 的证据是源码共享，不是另一套六端到端实测。真实执行矩阵见 [验收](<ACCEPTANCE.md>)；正常 GameEntry/New/Add/Place setup 与实测操作边界见 [最终观测驱动](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-illegal-swap/ReplacementDriver.compiled.cs>)。
