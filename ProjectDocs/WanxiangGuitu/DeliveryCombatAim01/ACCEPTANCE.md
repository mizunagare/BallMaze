# COMBAT-AIM-01 有限验收

本表 PASS 指所列自动化范围，不能扩大为原生操作、人工手感、整体难度或独立复审通过。开工804b4abb；详细输入/版本/命令和哈希见 Evidence。

| ID | 状态 | 本轮对应证据 / 边界 |
|---|---|---|
| A01 固定输入与实际内容 | PASS | BeforeFinal→FinalPaired；seed418、node22/node41/enemy1，同初始位置和相机；完整Collider/Renderer元数据 |
| A02 低石头/矿实际弓杖 | PASS | 配对HP/时序；FinalStory 实际Bow-Stone、Staff-Ore发射/接触/HP和一次采集；前景遮挡不强制穿透 |
| A03 普通/高敌与距离 | PASS | RulesExtended：2m/4m Collider、.7/7/18m实际弓杖；真实enemy1配对；共享camera/muzzle/yaw/frame |
| A04 极近/重叠/偏移 | PASS | 真实1m敌 + 受控初始重叠/枪口段/非法固体起点；零重复/越墙伤害 |
| A05 相机可见枪口被挡 | PASS | RulesExtended墙挡；最终验收Player临时低掩体，资源Collider保持原样，实际接触与HP不变 |
| A06 空目标/极端方向 | PASS（有限） | sky/背向有效相机、有界输出、零/NaN拒绝；实际资源与地面扫掠。不是任意物理图全排列 |
| A07 品质/多弹 | PASS | 四武器时序188 + 区域34 + Bow/Staff全五品质共享解/原角度，独立箭语义不改 |
| A08 输入/生命周期 | PASS | 原取消/冷却/换武器/死亡/场景卸载回归；实际验收Player背包打开取消前摇、关闭无补发 |
| A09 长枪/剑/多Collider | PASS | 原尺寸内交集，真实偏心石头及受控偏心/第二Collider/边界；188项保留剑普通/技能及品质 |
| A10 名称/追踪/制造 | PASS | 20种物品/目标名称一致；CraftShared真实制造、回调失败核对、扣费/目标清除、跨进程3项 |
| A11 非Editor运行时 | PASS | 最终两个非开发验收Player新运行，真实输入消费者/采集与恢复；不是原生鼠标键盘 |
| A12 构建/保护 | PASS | 纯发行0错96警告、验收0错145警告；源码/副本/构建哈希相同；发行无驱动；五用户文件相同 |

## 保持开放

- 原生U16 / 真实标题栏关闭验收：NOT_RUN。
- 独立人工可理解性、手感、整体难度：NOT_RUN。
- 本批完整正常AI出征→结算→制造全环：NOT_RUN；不把本次局部采集运行冒充全环。
- D3D12 UNKNOWN、Editor青色帧、Search/C15/JobTempAlloc等未定位历史项：UNRESOLVED。
- 护甲平衡、经验再次调参、弓蓄力、新法杖机制、自动追踪：本批未实施，不改变既有授权边界。

585规则断言PASS/0FAIL；最终2个运行时阶段PASS；最终2类构建PASS。历史/中间FAIL全部在 FAILURE_HISTORY 与原始证据中保留，不与最终条目混算。
