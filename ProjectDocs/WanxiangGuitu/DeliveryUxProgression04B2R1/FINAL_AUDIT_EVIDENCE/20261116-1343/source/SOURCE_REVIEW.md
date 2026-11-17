# UX04B2R1-FINAL 独立源码审查

## 边界与方法
- 本审查仅新增本附件目录中的报告；未改产品、原交付、历史证据，未构建/运行Player/暂存/修复。
- 独立读取当前源码，read每次不超过100行，grep/glob定位；未采用前轮PASS作为证明。
- git rev-parse HEAD实得95caf234256613d4a6e4f89a8ab0dc09c397c6b2，符合要求。工作区原有5个tracked源码修改及3个untracked B2源码；不是干净HEAD交付。git diff --cached --numstat为空。
- 结论均为SOURCE_PASS，不等同于独立Player实测、截图布局验收或磁盘故障注入；C05不在本委派范围。

## C01 收藏生命周期：SOURCE_PASS
- [B2Collection.cs:27–58](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/B2Collection.cs#L27-L58>)：单进程Ordinal HashSet，以item.id为唯一键，非按容器、类型或同属性共享；同属性物品不会被误收藏。普通进程重启静态集合自然重新创建；未发现保存序列化接入。
- [B2Collection.cs:95–103](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/B2Collection.cs#L95-L103>)：仅检查favorite∩before是否包含于after；别的容器/待领取装备不在before，不会误阻止整理。不是全局favorite必须全部在after的错误逻辑。
- [AdventureLoadout.cs:84–95](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/AdventureLoadout.cs#L84-L95>)：背包预览Clone，before/after仅InBag；失败保留原布局，成功只提交x/y。[CampRuntime.cs:63–67](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/CampRuntime.cs#L63-L67>)：仓库仅以stored做before/after，重排同一组引用，不清收藏。
- [CampRuntime.cs:99–114](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/CampRuntime.cs#L99-L114>)：Deposit/Withdraw克隆保留id，不调用收藏删除/清理；满仓/无空间在提交前拒绝。[CampRuntime.cs:75–97](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/CampRuntime.cs#L75-L97>)：提交有旧物品/仓库快照和回滚/已发布识别，收藏集合独立且无清理。
- [AdventureLoadout.cs:228–253](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/AdventureLoadout.cs#L228-L253>)：Owns/穿戴/装备盘/携带/入场保护、品质、收藏、素材容量全在移除前拒绝；成功才Remove及NotifyGearDestroyed，然后PruneStale。
- 关键待领取ID：[AdventureLoadout.cs:245–252](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/AdventureLoadout.cs#L245-L252>)把loadout、warehouse及pending中equipment且item非空的item.id并集传入PruneStale；使用装备ID而非pendingId。活着的待领取装备不被成功拆解另一件时误清理。
- 全Assets *.cs搜索仅发现成功Salvage处调用NotifyGearDestroyed/PruneStale，没有额外产品Clear/Remove调用。集合公开API允许外部错误传参不等于当前实际路径缺陷；本审查限实际产品调用链。

## C02 两UI真实共享排序及身份/状态只读：SOURCE_PASS
- [B2InventoryQuery.cs:160–204](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/B2InventoryQuery.cs#L160-L204>)：状态只读判断；Matches先筛选，再向新List加入原引用，排序只构造新列表，不改id/x/y/rotation/worn/overflow/board/main/reserve/favorite。
- None没有sort分支，保留输入次序；攻击/品质/类型等均以Ordinal item.id作为确定性二级键。此处“稳定”指同输入ID的确定次序，不是同主键保留原插入顺序；跨新建随机GUID会话不能假设同主键物品顺序完全相同。
- [B2InventoryQuery.cs:131–136](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/B2InventoryQuery.cs#L131-L136>)：真实循环None→AttackDesc→QualityDesc→TypeAsc→None。[B2InventoryQuery.cs:212–227](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/B2InventoryQuery.cs#L212-L227>)：ApplySortOnly保留所有行，仅复用排序；DisplayOrder共享完整filter+sort。
- IMGUI [ContainerInventoryView.cs:65–101](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/ContainerInventoryView.cs#L65-L101>)：DisplayOrder结果逐行真实绘制排序目录，不仅写观测标签；[ContainerInventoryView.cs:146–157](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/ContainerInventoryView.cs#L146-L157>)实际grid也消费Apply/ApplySortOnly。
- uGUI [CatInventoryPresenter.cs:39–60](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/CatInventoryPresenter.cs#L39-L60>)：同DisplayOrder结果按n*18逐行建立目录；grid同Apply/ApplySortOnly。物理格子x/y不随展示排序移动是有意只读，不是整理背包。
- 仓库存取：[CampInventoryView.cs:29–38](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/CampInventoryView.cs#L29-L38>)、[CatInventoryPresenter.cs:78–82](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/CatInventoryPresenter.cs#L78-L82>)均消费共享sort-only后数组绘制实际行。Board及转移列表不套收藏/类别过滤以免隐藏功能物品；不是误把warehouse当loadout改写。
- [B2InventoryQuery.cs:249–273](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/B2InventoryQuery.cs#L249-L273>)重复提示仅计数；不合并或替换身份。[B2InventoryQuery.cs:303–319](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/B2InventoryQuery.cs#L303-L319>)Publish只写UI观测字符串/计数，不写业务状态；不应泛称整个运行时“零写入”。

## C03 唯一B2Controls及热键：SOURCE_PASS
- 全Assets搜索B2Controls：唯一实际调用[ContainerInventoryView.cs:73](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/ContainerInventoryView.cs#L73>)，唯一定义[ContainerInventoryView.cs:107–117](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/ContainerInventoryView.cs#L107-L117>)；另一命中是解释删除重复调用的注释，不是第二次执行。
- [基线:65–67](<I:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/_baseline_snapshot/ContainerInventoryView.cs#L65-L67>)确有顶部和y+338两次，当前仅保留y+338；标题y不再叠该控件条。
- 当前[ContainerInventoryView.cs:123–127](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/ContainerInventoryView.cs#L123-L127>)保留PlayerAction.Rotate与右键取消；uGUI [CatInventoryPresenter.cs:16](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/CatInventoryPresenter.cs#L16>)同样保留。基线对应IMGUI98–99/uGUI16完全同处理语义。
- [PlayerBindings.cs:19–22](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/PlayerBindings.cs#L19-L22>)定义管理界面R旋转，世界R放弃场景隔离；未新增热键。独立SHA256比外部完整snapshot，PlayerInput.cs/PlayerBindings.cs/PlayerInventory.cs均逐字节相同。
- 源码几何只证明重复条删除，不替代所有分辨率/缩放的视觉无重叠验收。

## C04 新增3meta唯一、原GUID未改：SOURCE_PASS
- [B2AttackModel.cs.meta:2](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/B2AttackModel.cs.meta#L2>) f2e7d10e4f9a42788f9c15e6e4dd7e1e；[B2Collection.cs.meta:2](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/B2Collection.cs.meta#L2>) c189b5d478364a7a81ca99738a8e0fa1；[B2InventoryQuery.cs.meta:2](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/B2InventoryQuery.cs.meta#L2>) bd256a15e7e944038fdb3180e0f08a8f。
- 在Unity项目导入作用域Assets/Packages/ProjectSettings全部*.meta独立grep三GUID，各恰1条，均为本身；不把ProjectDocs历史snapshot副本当Unity导入GUID冲突。
- 对[I盘完整snapshot](<I:/unity/WanxiangGuitu-UX04B2R1-snapshot-20261116-1108/workspace>)原有Assets/Packages/ProjectSettings共763个meta逐文件SHA256比较：missing=0，changed=0。因此原有GUID及meta全字节未改，含已在11:08快照存在的这3个meta。不是声称3meta在11:08之后新建。
- 较早八源文件_baseline_snapshot不含meta，不能单独用它证明GUID；本项实际依据外部完整snapshot及当前GUID搜索。

## C06 PreviewReplacement九项只读源码写入路径：SOURCE_PASS（仅只读范围）
- [AdventureLoadout.cs:30–32](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/AdventureLoadout.cs#L30-L32>)仅转发；[B2AttackModel.cs:152–178](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/B2AttackModel.cs#L152-L178>)先读真实状态，复制real每件及candidate，主/备ID变为局部变量；[B2AttackModel.cs:180–211](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/B2AttackModel.cs#L180-L211>)所有字段赋值、RemoveAll/Add均只作用copy/c，不回写gear或hero。
- [AdventureItems.cs:9–44](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/AdventureItems.cs#L9-L44>)GearItem字段为值类型/string，唯一可变数组affixes在Clone另行复制，避免浅复制共享可写数组。攻击/防御getter只读。
- [B2AttackModel.cs:99–147](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/B2AttackModel.cs#L99-L147>)Compute/Snapshot纯遍历求值；[AdventureLoadout.cs:40–44](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/AdventureLoadout.cs#L40-L44>)ContainerFor只取第一个worn定义；[ContainerDefinition.cs:6–20](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/ContainerDefinition.cs#L6-L20>)定义未被预览写入。
- 九项路径逐项：GearItem→copy/c字段；Inventory→无材料/药水Add/Remove调用；EquipmentGrid→只改copy坐标/board；Main→局部mainId；Reserve→局部reserveId；Worn→copy/c.worn；Overflow→copy/c.overflow；AttackPower→快照局部浮点计算，无hero写入；Container→仅读共享定义，无属性赋值。均未发现真实业务写入。
- [AdventureCatalog.cs:13–28](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/AdventureCatalog.cs#L13-L28>)首次取定义会填缓存/Resources.Load，这是九项业务只读之外的惰性缓存写入，不能扩张成全Unity内存完全不变。预览路径无Random、存档写、Refresh或真实装备调用。

## 未关闭风险（不自主修复）
1. **R-PREVIEW-CONTAINER / 明确数值不一致**：[B2AttackModel.cs:200–211](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/B2AttackModel.cs#L200-L211>)仅把candidate克隆设为worn并追加，没有撤销旧同类型worn。[AdventureLoadout.cs:40–44](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/AdventureLoadout.cs#L40-L44>)FirstOrDefault仍选择旧容器，故ContainerBag/Worn对未穿戴新背包的bonus预览通常仍是旧值。[Resources/ContainerData/bag_relic.asset:15–28](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/Resources/ContainerData/bag_relic.asset#L15-L28>)真实attackBonus=6；从标准包换遗物包可显示Δ0而真实更换应+6。实际更换[AdventureLoadout.cs:160–173](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/AdventureLoadout.cs#L160-L173>)会取消旧worn并重排，二者不等价。影响预览数值/可行性，不构成九项状态写入，因此不反向判C06只读失败。
2. **R-PREVIEW-FEASIBILITY**：Preview Main/Reserve会把任意候选武器复制为InBag，Board也未Fit/Find检查；ContainerRig/Bag只检查Container不校验具体角色类型。feasible=true不能作为实际装备/容量成功保证；真实[AdventureLoadout.cs:107–141](<I:/unity/WanxiangGuitu/Assets/CombatPrototype/AdventureLoadout.cs#L107-L141>)另有Owns/InBag/布局校验。未完成全替换方案数值与可行性矩阵。
3. **R-RUNTIME-BOUNDARY**：仅源码独立审查，不新增/运行Player；不能据此独立确认重启行为、事务故障下磁盘结果、所有显示分辨率及热键实际交互。需由既有证据独立复核者结合，不可将本SOURCE_PASS扩大为运行时全PASS。

## 工具异常记录
- 一次grep转义导致正则括号错误，改用字符类后成功；一次PowerShell foreach直连管道解析失败，改为先存数组后成功，未产生写入。
- 曾猜测容器资源位于Assets/Resources/ContainerData而不存在；使用glob定位实际CombatPrototype/Resources后读取。均为定位/只读命令失败，未绕过权限或修改产品。
