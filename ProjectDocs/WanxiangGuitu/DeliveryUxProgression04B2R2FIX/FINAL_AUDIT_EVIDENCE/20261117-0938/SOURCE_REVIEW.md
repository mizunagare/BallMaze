# UX04B2R2FIX 最终独立源码审计

## 双层结论：R2FIX限定源码审计 PASS；整包B2提交/发布候选 CONDITIONAL

本结论来自实际源码、真实 FIX 前 snapshot、HEAD 源、差异和编译PDB，不是复述交付 PASS。双基线严格区分：HEAD用于核实原始攻击顺序及整段B2累计改动；FIX前真实snapshot用于逐字节冻结Active/ComputeDefense及限定本次修复改动。**未发现此 FIX 新引入的明确装备事务缺陷；四当前源→既有FINAL-A02 DLL身份已由独立PDB补证闭合。** 不扩大为全部运行边界或所有 HEAD 防御浮点位等价。

HEAD 95caf234256613d4a6e4f89a8ab0dc09c397c6b2，branch feature/ux-progression-04-b2，已只读确认。遵守不 Build、不 Player、不编辑产品/历史、不作 Git 修改；仅用 lead 澄清允许的只读 git show/diff/rev-parse/ls-files。该审计员仅新增本报告和[同名机器证据](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/SOURCE_REVIEW.json>)。

## 1. 实物比较与 SHA

FIX 前使用用户指定真实 workspace 快照，根路径为 I:/unity/WanxiangGuitu-UX04B2R2FIX-snapshot-20261116-1536/workspace；不是旧summary。已读取三份封存 HEAD 源：[loadout](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/SOURCE_HEAD/AdventureLoadout.cs>)、[uGUI](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/SOURCE_HEAD/CatInventoryPresenter.cs>)、[IMGUI](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/SOURCE_HEAD/ContainerInventoryView.cs>)，并检查完整 HEAD 差异。[B2AttackModel](<Assets/CombatPrototype/B2AttackModel.cs>) 为未跟踪文件，HEAD无该文件，不能虚构其HEAD版本。HEAD对象LF与工作副本CRLF区别也不能当成逐字节相同。

| 实际当前源 | 当前 SHA256 | FIX前 SHA256 |
|---|---|---|
| [B2AttackModel](<Assets/CombatPrototype/B2AttackModel.cs>) | 6e45644e73ca6d5a8a4eaf560714d44bda5a69df2fcbdb4e05bf1b5e6a899e1d | 90077277db077e02f6a5edee365be7a73073754d5851d1fe0d92834f7ed106db |
| [AdventureLoadout](<Assets/CombatPrototype/AdventureLoadout.cs>) | c6791285164e388f0b686b2558e89bead2bd985a216fb4ff21f21e8e9b074d48 | c2113764da97f25c765dde3c291f3850723c1af2edddfb30c40f0a678a434505 |
| [CatInventoryPresenter](<Assets/CombatPrototype/CatInventoryPresenter.cs>) | c493e7b164c08a0be6477f9068da66c61cc5ce7286a9db7b714218870372b0fc | b93011c1cc08fdea36399b78431ab9cf83c6119512de1ad97207a6928716f3f5 |
| [ContainerInventoryView](<Assets/CombatPrototype/ContainerInventoryView.cs>) | 93710dbd66bba1dd5cdd0ac5f57fbcf63eacb75a4dc57c38bd86f2ac50ef7466 | 96558816eac633d907187118a0589f698754a6abf0814b7d52db865ebf7fe34d |

四组均精确匹配既有 [SourceDiff identity](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/EVIDENCE/SOURCE_DIFF/identity.json>)。另逐hunk核对旧/新内容，再将四份既有patch完整重放到实际snapshot，均重建当前全部行，没有漏掉patch外漂移；不仅检查端点SHA。

## 2. 求和顺序与逐字节冻结

**PASS：** [B2AttackModel:112-118](<Assets/CombatPrototype/B2AttackModel.cs#L112-L118>) 真实执行 Active.Sum(i=>i.Attack)，再加Rig，再加Bag，保持左结合；没有先合并两个容器加成。[HEAD攻击式:22](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/SOURCE_HEAD/AdventureLoadout.cs#L22>) 相同顺序。[AdventureLoadout:23-31](<Assets/CombatPrototype/AdventureLoadout.cs#L23-L31>) live getter / Snapshot共享该计算。[B2AttackModel:133-160](<Assets/CombatPrototype/B2AttackModel.cs#L133-L160>) AP仍为base+loadout+progression，普攻仍沿既有SpearPower。

**PASS，仅相对FIX前真实snapshot：** 完整方法抽取从public声明行缩进起，至配对闭括号止，保留内部原字节换行。双方精确相等：

| 方法 | 双方方法字节SHA256 |
|---|---|
| [B2AttackModel:96-108](<Assets/CombatPrototype/B2AttackModel.cs#L96-L108>) Active | 7d363939fd6035b24524bdfeb00d2f90c9ef835b5c01b017e72fa4b3c1395e77 |
| [B2AttackModel:121-127](<Assets/CombatPrototype/B2AttackModel.cs#L121-L127>) ComputeDefense | cd97adefc981d577e267fc3a463714154a1d1c164045850ab4930234d61c5cb8 |
| [B2AttackModel:80-89](<Assets/CombatPrototype/B2AttackModel.cs#L80-L89>) FindMain | 552e5ebc05c92c5db5e6ccc11b36ece535fd5903094f7c11c74f55fd215b36ca |
| [B2AttackModel:133-160](<Assets/CombatPrototype/B2AttackModel.cs#L133-L160>) Snapshot | e0138eac188255463eca1de61818b5d9f102229dd951456c762a9f59b1916d10 |

相对HEAD还包括早先B2/R1 filter、sort、favourite、容量提示修改；不能冒称全部为本FIX。相对FIX前，计算改动只有ComputeAttack从Single foreach改回LINQ Sum；Active/ComputeDefense/Snapshot不变。

读取并实比十依赖源全部与snapshot字节相等：[AdventureItems](<Assets/CombatPrototype/AdventureItems.cs>)、[ContainerDefinition](<Assets/CombatPrototype/ContainerDefinition.cs>)、[ItemDefinition](<Assets/CombatPrototype/ItemDefinition.cs>)、[AdventureCatalog](<Assets/CombatPrototype/AdventureCatalog.cs>)、[AdventureCombat](<Assets/CombatPrototype/AdventureCombat.cs>)、[HeroEquipment](<Assets/CombatPrototype/HeroEquipment.cs>)、[ThirdPersonHero](<Assets/CombatPrototype/ThirdPersonHero.cs>)、[HeroProgression](<Assets/CombatPrototype/HeroProgression.cs>)、[CampRuntime](<Assets/CombatPrototype/CampRuntime.cs>)、[CampWorkbenchRuntime](<Assets/CombatPrototype/CampWorkbenchRuntime.cs>)；受保护战斗/定义源相对HEAD的diff为空。[AdventureItems:30-52](<Assets/CombatPrototype/AdventureItems.cs#L30-L52>) 保存属性/强度、[HeroProgression:38-42](<Assets/CombatPrototype/HeroProgression.cs#L38-L42>) Strength×5、[AdventureCombat:82-94](<Assets/CombatPrototype/AdventureCombat.cs#L82-L94>) SpearPower=1.25、[ThirdPersonHero:22-26](<Assets/CombatPrototype/ThirdPersonHero.cs#L22-L26>) AP及[HeroEquipment:15-16](<Assets/CombatPrototype/HeroEquipment.cs#L15-L16>)桥接没有搭车修改。六真实ContainerData asset、accessory/arms/标准胸挂/标准背包四ItemData asset逐个读取，与snapshot字节相同，相对HEAD diff为空；bag_relic的+6属于容器bonus，不是worn物体Attack。

**不能扩张的既存数值边界，已通知lead：** [HEAD防御式:23](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/SOURCE_HEAD/AdventureLoadout.cs#L23>) 用LINQ Sum；[B2AttackModel:124-126](<Assets/CombatPrototype/B2AttackModel.cs#L124-L126>) 仍Single foreach。FIX前后不变，不代表与HEAD全浮点位等价。纯Math.fround示例（非Unity运行）：Single输入1.600000023841858、2.4000000953674316、1.600000023841858，逐步Single为5.599999904632568，double累加再转Single为5.600000381469727。此为旧B2精度范围风险，不是本FIX搭车改Defense，未擅修。

## 3. Add / Replace / Clone / 空间与原子提交

- **PASS，显式身份：** [AdventureLoadout:34-41](<Assets/CombatPrototype/AdventureLoadout.cs#L34-L41>) 分Add/Replace；[AdventureLoadout:54-65](<Assets/CombatPrototype/AdventureLoadout.cs#L54-L65>) 拒绝null/空/重复ID；候选须真实InBag，原包位置Fit且旋转合法，Replace须另一实际old ID。不是按类型猜第一件。
- **PASS，Add不移旧：** [AdventureLoadout:66-95](<Assets/CombatPrototype/AdventureLoadout.cs#L66-L95>) 已占Main/Reserve拒绝Add，worn容器拒绝伪Add；[AdventureLoadout:107-125](<Assets/CombatPrototype/AdventureLoadout.cs#L107-L125>) Board Add碰撞就拒绝，不进入old移动。
- **PASS，精确target/role/rotation：** 武器槽坐标/旋转固定候选当前包位置，old须实际槽；容器role种类匹配、target=(-1,-1)、rotation=0，old须唯一实际worn。Board不失败后改找更好target。
- **PASS，clone-only：** [AdventureLoadout:56-95](<Assets/CombatPrototype/AdventureLoadout.cs#L56-L95>)、[AdventureLoadout:287-306](<Assets/CombatPrototype/AdventureLoadout.cs#L287-L306>) 只投影clone；[AdventureItems:44](<Assets/CombatPrototype/AdventureItems.cs#L44>) 单独复制affixes，其他为值/不可变string；Definitions仅读。[B2AttackModel:68-72](<Assets/CombatPrototype/B2AttackModel.cs#L68-L72>) 投影存储和返回继续防御clone。
- **PASS，真实空间与双向swap：** [AdventureLoadout:189-207](<Assets/CombatPrototype/AdventureLoadout.cs#L189-L207>) 旋转Cells和Container.Allows含blockedCells；[AdventureLoadout:233-257](<Assets/CombatPrototype/AdventureLoadout.cs#L233-L257>) 两方向均Fit，覆盖只能一件；[AdventureLoadout:107-114](<Assets/CombatPrototype/AdventureLoadout.cs#L107-L114>) 碰撞ID必须指定old，双向失败直接false，无Find fallback。
- **PASS，旧件回包：** 碰撞swap使old维持原旋转回候选原包位置；空target替换先在clone摘old，放候选后为old找真实包空间，找不到整个失败，见[AdventureLoadout:116-125](<Assets/CombatPrototype/AdventureLoadout.cs#L116-L125>)。不能借overflow把失败伪装成功。
- **PASS，Apply重验/旧路径：** [AdventureLoadout:130-156](<Assets/CombatPrototype/AdventureLoadout.cs#L130-L156>) 不信feasible/缓存投影，重新ProjectEquipment。Main/Reserve调用原[AdventureLoadout:273-274](<Assets/CombatPrototype/AdventureLoadout.cs#L273-L274>)；Container沿原[AdventureLoadout:308-315](<Assets/CombatPrototype/AdventureLoadout.cs#L308-L315>)→[CampWorkbenchRuntime:56](<Assets/CombatPrototype/CampWorkbenchRuntime.cs#L56>)→[CampRuntime:68-97](<Assets/CombatPrototype/CampRuntime.cs#L68-L97>)营地保存事务。Board Add/swap实调Place；空target Replace检查全通过后同步复制布局字段、Refresh，验证失败不写真实布局。原子含义限定正常Unity主线程同步路径，不是异常/任意重入/进程崩溃证明，亦不重写原营地发布结果不确定处理。

## 4. UI接线确实可由正常界面操作

**PASS，静态接线层：** [CatInventoryPresenter:30-31](<Assets/CombatPrototype/CatInventoryPresenter.cs#L30-L31>) 有实际入口；[CatInventoryPresenter:87-112](<Assets/CombatPrototype/CatInventoryPresenter.cs#L87-L112>) 提供真实候选/old ID、模式、role、target、rotation、Evaluate/Commit；经[CatInventoryPresenter:21-22](<Assets/CombatPrototype/CatInventoryPresenter.cs#L21-L22>)原generation/data/page guard、[CatUI:7-11](<Assets/CombatPrototype/CatUI.cs#L7-L11>)真实raycastable Image + Unity Button + onClick，到[ContainerInventoryView:22-31](<Assets/CombatPrototype/ContainerInventoryView.cs#L22-L31>)共享session，再到模型/Apply。不是只留给测试脚本的裸函数。

IMGUI [ContainerInventoryView:75-79](<Assets/CombatPrototype/ContainerInventoryView.cs#L75-L79>)、[ContainerInventoryView:116-142](<Assets/CombatPrototype/ContainerInventoryView.cs#L116-L142>)也是真实CombatUI.Button并接同一请求。参数改变Invalidate，提交前须Evaluate，但允许“失败预览后提交验证拒绝”，不是仅依赖feasible。grep所有生产PreviewAdd/Replace/Apply调用方后，实际调用在共享session；详情legacy PreviewReplacement改为Add查询，失败会引导打开工作面锁old，不静默猜旧件。

**此项不把Button接线当成历史driver确实走物理输入的证据**；历史输入事件/driver行为由主审计另查，本审计不新开Player。

## 5. 原编译回执限制与新PDB补证

原 [FINAL-A02回执:2-12](<Evidence/Runs04B2R2FIX/FINAL-A02/_product/receipt/b2-product-build.json#L2-L12>) 的b2SourceSHA256只有B2AttackModel/B2Collection/B2InventoryQuery三个源，不是本次四修改源。B2AttackModel与当前SHA相同，另外三个修改源原回执没有该字段。RSP确含四源： [loadout:510](<Evidence/Runs04B2R2FIX/FINAL-A02/_product/b2-product.rsp#L510>)、[uGUI:535](<Evidence/Runs04B2R2FIX/FINAL-A02/_product/b2-product.rsp#L535>)、[IMGUI:563](<Evidence/Runs04B2R2FIX/FINAL-A02/_product/b2-product.rsp#L563>)、[model:647](<Evidence/Runs04B2R2FIX/FINAL-A02/_product/b2-product.rsp#L647>)，但仅路径不证当时字节。[BUILD_IDENTITY:11-15](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/EVIDENCE/BUILD_IDENTITY.json#L11-L15>) 的166 current census是事后盘点，不是编译时SHA记录，153才是RSP编译源计数。

**PASS，新证据独立补齐，不改写旧记录：** 已读取审查[原PDB解析器](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/read_pdb_checksums.py>)、[生成源补证解析器](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/audit_pdb_generated_source.py>)、[最终PDB证据](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/PDB_SOURCE_AUDIT.json>)。又以本审计自己的Node代码重新hash全部153实际项目源及1份提取生成源，并独立解析PE debug directory的RSDS GUID+stamp，对照PortablePDB #Pdb ID，全部匹配。四授权源均在153 Document内，compiler checksum与表中当前SHA完全一致。DLL SHA256=ab3d5ba4f4a234598056915ab7b1dca4ad4be57f68298fc24d1b718d267a2df1；PDB SHA256=eaab070ccae46f03db8e1e4932795669f0332b13cb3bdf7a743c41460a2f6816。

154 Document=153实际项目源（SHA256）+1 Unity生成源（内嵌原文SHA1 b56f82ba804a5a4ee9e6d6ef1792e213dcf22b49）；不可把第154个无磁盘路径误报产品源码漂移。[首轮诊断](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/COMPILER_PDB_SOURCE_CHECKSUMS.json>) 保留原FAIL不涂改，最终补证解释该差异。补证是读取既有编译器文档checksum，不是166盘点倒填编译时间；仅证明这些源与此现存DLL/PDB绑定，不推断场景/资源已重烘。

## 6. 未覆盖边界与接受范围

1. 不运行Build/Player；静态审查不新增证明Reserve、ContainerRig、全部合法旋转/稀疏形状、preview→commit间外部状态变化、保存失败、IMGUI真实输入等运行边界。
2. None/Overflow明确不支持Add/Replace，可在UI显示拒绝；legacy详情默认/当前件预览失败，不等同真实装备失败。hero=null查询采用25基础值，不是实际战斗角色身份证据。
3. 不全局修复损坏数据：缺失/未知Definition、零/非法尺寸、非有限属性、其他既存物体重叠。Active正常非空唯一ID下保留HEAD first-order/reference-main规则；null/空ID病态数据不保证全等。
4. R2FIX限定源码审计PASS仅指“攻击求和顺序与显式预览/提交语义静态审查未发现新事务缺陷，四源与既有DLL编译身份匹配”。整包B2提交/发布仅CONDITIONAL候选；此报告不解除旧R1证据归档条件，不授予暂存或提交授权。若扩成“所有HEAD Defense浮点位全等”或“166源有原编译回执SHA”，应拒绝扩张。此源审计整体CONDITIONAL不覆盖主审计其他轨道。

完整检查项与机器边界见[JSON](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/SOURCE_REVIEW.json>)。
