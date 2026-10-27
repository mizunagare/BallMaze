# INPUT-01 动作与提示映射

输入身份为稳定的 `PlayerAction` 名称；`PlayerBinding.action/primary/secondary` 是独立首选项，不是装备ID、Run或v9存档字段。定义、有效快照及显示统一来自 `PlayerBindings` / `PlayerInput`，没有页面私有绑定表。

|动作ID|默认主键|允许场景|正式消费者|显示|
|---|---|---|---|---|
|Forward/Back/Left/Right|W/S/A/D|探索、营地走动|ThirdPersonHero.Update，按住向量并限幅|帮助、教程、旧CombatHud|
|Sprint|LeftShift|探索、营地走动|ThirdPersonHero.Update，按住|帮助、旧HUD|
|Dodge|Space|探索、营地走动的原门禁|ThirdPersonHero→HeroDodge.TryDodge|HUD键帽、帮助、旧HUD|
|Attack|鼠标左键|探索|ThirdPersonHero.Update→原Attack/Strike，仍要求镜头捕获|HUD、帮助、采集教程|
|Skill|F|探索|AdventureCombat.Update→UseSkill|技能键帽、帮助、旧HUD|
|SwitchWeapon|V|探索|AdventureCombat.Update→SwitchWeapon|副武器键帽、帮助、教程|
|Potion|Q|探索、营地、管理|PlayerInventory.Update→UseHealthPotion，沿原可用性|药水键帽、帮助、旧背包/战斗HUD|
|Interact|E|探索、营地|InteractionResolver.LateUpdate→ExecuteDisplayed(false)|同一offer提示、掉落通知、教程、旧展示分支|
|Exit|H|探索、营地及管理页的原营地准备入口|InteractionResolver→ExecuteDisplayed(true)；AdventureFlow/CampRuntime原准备入口|出口/合并键位/取消引导、帮助、旧分支|
|Inventory|Tab|探索、营地、管理|PlayerInventory.Update→SetOpen|背包入口/返回/教程|
|Items|B|探索、营地、管理|PlayerInventory.Update→OpenPage(Items)或关闭；与Tab保留不同原语义|补给键帽、帮助|
|Character|C|探索、营地、管理|PlayerInventory.Update→角色页或关闭|帮助、旧角色按钮|
|Abandon|R|探索/营地，保留确认|CombatSession→CombatSaveSystem.RequestNewGame→原放弃/营地准备|旧HUD、设置行|
|Route|M|探索、营地、管理|PlayerHudPresenter.SetDetails(路线)，沿原面板可用性|可点击路线按钮、帮助|
|Help|F1|探索、营地、管理|PlayerHudPresenter.SetDetails(帮助)|可点击帮助按钮、帮助|
|Rotate|R|管理|CatInventoryPresenter或旧ContainerInventoryView→RotateSelection|背包拖放、旋转提示|

Tab/B/C是三个原语义入口，不合并成不同作用的同一动作；同帧同时按它们按Tab→B→C优先级只执行一个页面操作。每个动作可设置一个主键和一个可选别名；同动作多个键同时按下仍只产生一个布尔触发。R的放弃与旋转上下文互斥，因此默认可复用；同场景的不同动作冲突拒绝，不交换、不清空另一行。

## 保留输入

- Esc：UI返回、取消捕获或释放鼠标，不允许绑定。
- 鼠标右键：镜头捕获及背包拖放取消，不能占作其他动作。
- F2 HUD缩放、F3现有诊断、F5存档、F9受原Editor权限控制的快速读取；不改其开发/正式边界。
- 1/2/3：原升级选择；N：原波次测试，未加入正式重绑动作。
- 视角鼠标位移、滚轮/UI滚动、uGUI导航/提交保持原InputSystemUIInputModule，不列成可重绑的游戏离散动作。
- 只支持单键/离散鼠标按钮；方向只允许键盘，不支持和弦、滚轮轴、宏或手柄。本功能不能绕过Snipaste或操作系统拦截，鼠标帮助/路线入口保留。

## 输入边界与成本

`PlayerInput` 在早期Update采样，所有消费者读同一快照；物理控件映射仅在绑定/设备变化时更新。按住与按下分开，不每帧读盘或重建InputAction/Canvas。焦点丢失、设备变化、场景切换、上下文变化及设置应用/关闭均清空当帧触发，并要求已有按住键释放后重新按下。管理、技能选择、确认、死亡及营地原业务门禁继续有效。

捕获先等待启动点击/按键释放，Esc取消；捕获输入与关闭帧不穿透游戏和保留快捷键。绑定行在捕获及释放前停用，避免选中的鼠标按钮又点击改键入口。关闭恢复进入前的时间、光标和嵌套帮助状态，营地0时钟仍为0，不无条件解暂停。

## 首选项与失败规则

沿用 `GamePreferences.CurrentPath` 和旧preferences.json路径，version仍1，新增可选bindingVersion=1/inputBindings。缺字段使用当前默认，原音量/灵敏度/HUD/窗口值保留。未知JSON说明字段按JsonUtility原能力忽略；未知动作、重复、冲突、无效控制或不支持键位版本使键位显式回退默认并显示警告，读取不自动写回。损坏整文件显示读取警告，原件保留。

编辑副本仅在应用时校验、持久化、发布；取消/恢复默认草稿不写盘。应用使用tmp+原子替换及旧文件.bak，核对编辑期间文件指纹，故障不改变有效绑定，界面允许重试/取消。主动应用才覆盖原件并留下备份，绝不把默认回退当作自动修复原文件。新游戏保留该独立偏好，不触碰Profile/Run/装备/来源账或随机流。
