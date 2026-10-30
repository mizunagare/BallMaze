# 防御与实际伤害基线

开工/限定接受的瞄准基线：f13492df6889fbc628f96c7ab7cbb5075e552014。任务原文TASK.md；本批不复审并关闭原生或历史引擎事项。

## 真实来源

ThirdPersonHero.Defense = HeroEquipment.Defense + HeroProgression.DefenseBonus。存在AdventureLoadout时HeroEquipment完全委托它，不再叠加旧ArmorTier；旧无Loadout路径为5×ArmorTier。Loadout按唯一物品ID，排除overflow/worn，统计装备盘有效物品Defense，再加实际Rig/Bag定义的defenseBonus；主武器不因“主手”重复计算护甲。IronSkin每级+2。GearItem的dataRevision>0使用savedDefense；旧物品使用原legacy计算，迁移仍冻结原值。词缀本身没有额外的动态Defense分支；物品/容器原数据不改。

实际合成装备实例记录见BeforeRules/defense-sources.json：0；白甲8×.4=3.2；绿甲19×.4=7.6；紫甲43×.4+IronSkin2=19.2。该四档容器防御均0，不代表所有容器模板都无加成。其他合法容器仍沿原定义相加，新公式只消费最终总防御。UI属性预览继续显示真实原始防御点，不伪造减伤百分比。

普通12、远程9、精英20由实际遭遇实例产生，六Boss招式逐项为RootSlam23、AntlerCharge27、SeedVolley12、WaterFan11、TidalMark24、ShoreBite21。实际事件六种值全部出现。ForestBossDefinition仍为唯一招式数据，老BossBrain其他攻击路径不调参。

药水50、冷却5秒；翻滚持续.42秒、距离4.2m、起手无敌.24秒、冷却1.5秒，均从源码和真实API核对。伤害观察仍为一次成功Damage事件，既有受伤/撤离中断/反馈调用次序未变。

## 旧问题与候选

旧实际Damage=max(1,raw-D)。D19.2时9-D和12-D为负，因此均被下限压成1；23/27等大招还有3.8/7.8，防御对小伤害的收益出现断崖和触底平台。旧版实际同输入规则用新预期保留13PASS/29FAIL（27条合约变更和NaN/Infinity2条防护负例），不是29个独立历史玩家缺陷。

Model.py产出1224行：旧；A cap40/50/60%；B K5/10/20/30；C K10/20/30 × cap60/75/80%。每种覆盖8防御档和9具名攻击。候选比较、最低伤害比例、100HP与100+50理论受击数均机器可算；后者不声称药水一定能在死亡前喝到，真实5秒冷却/闪避在矩阵中单列。

选择C20/.75的依据与实施前推荐见DESIGN_DECISION.md。小数HP保留float，不在每击先四舍五入；UI整数显示不决定伤害。非有限/非正raw拒绝且不产生回调；无效/负D按0；double中间计算，有限超大值也不溢出。敌方承受玩家武器伤害仍原max(1,raw)，不套玩家护甲。

## 同输入观察

旧/新各3 seed×3独立Run×4防御×6类受控遭遇=216样本；Run内条件重置，不冒充216个独立Run。rep0原地承受30秒，rep1正常移动且攻击90秒，rep2反应闪避且攻击90秒；Mixed rep2有意早闪，原始policy标签仍CorrectDodge，源代码scope已说明，汇总effectivePolicy如实改为WrongDodge，不回写原JSON。seed418混合普通+远程，419普通+精英，420三敌夹击；另含两Boss单体。不是全组合排列。

初始HP、D、攻击、技能、位置和全局随机状态216对逐一相同；Run/Profile/Gear GUID是独立新建身份，不要求跨版本相同。竞技场使用原真实敌人AI和物理，非目标敌人停用、样本前定位/装备/等级/两药初始化，故明确属于受控AI。样本期间无补血/复活/改最终HP；治疗走UseHealthPotion，翻滚走HeroDodge，伤害走Damage。Flow关闭时按原BAL01工具使用显式重置的legacy全局RNG，不能说是Run随机流冒险；正常完整Run另行验证真实Run流。

老/新接触1008/984，高防普通/远程非致死接触45+33=78各自；旧全1，新普通6.1224、远程4.5918。真实六种Boss伤害已覆盖，56条零扣血接触亦保留。旧/新0伤样本108/107，不把无伤等同于AI失效或绝对安全；有击杀先于攻击、闪避、射线/位置等条件。各有22个实际接近90秒窗口；其余真实死亡/清场/30秒窗口如实记录。

零防死亡6→6，白甲2→3，绿甲0→3，紫甲+1级IronSkin档0→1（每档54受控样本）。弱装D0逐击不变，白甲保护较旧固定减法减弱，应保留真实玩家风险。自动化不证明最终平衡。

## 经验只观察

首版经验曲线文件完全不改。受控两版各获得11040 XP、存活样本0来源核对不一致；所取样的击杀集合相同，不推论所有装备TTK相同。正常Gather完整首局实际30 XP，最高等级1、无升级选择；回营/后继Run等级1、XP0。短Gather未达35阈值是本轮观察结果，不擅自调XP。长窗口升级、选择/ranks与逐敌XP事件完整保留，后续如要改曲线另需授权。
