# 本机复跑

Unity6000.6.5f1，开工main f13492df6889fbc628f96c7ab7cbb5075e552014。用**新的**I:/WGCombat/BAL02-*根和合成档；本轮根BAL02-1030-A不可覆写。禁止读取真实存档、关闭用户程序、激活桌面、强杀超时进程。

## 输入与候选

复用DeliveryUI01/Invoke-Rules.ps1 -PrepareOnly创建根/P/Project旧版与F/Project新版，owner.json及用户原始SHA先记录。只在副本中把用户场景/设置/Recovery另存Deferred，并用Git开工blob替换副本；不动用户原件。旧/新除CombatHealth和新增ArmorMitigation/.meta外产品输入一致。

`python -X utf8 -B Model.py`重生成两CSV和formula-summary。模型不是Unity结果；K为防御点数，min1、float小数/双精度中间与无效输入语义见DESIGN_DECISION。

## 规则与受控AI

Invoke-Check.ps1直接复用旧编排Step，强制工程外根、进程/资源门槛3GB、唯一Output、启动前-wanxiang-storage-root、退出/超时/日志/exception检查；不强杀。无矩阵时移出BAL02Matrix以免无观测类编译依赖。方法：BAL02Rules.Run、BAL02Math.Run、BAL02Recovery.Save（旧）、Load（新）、Aim01Before.Run、Aim01Rules.Run、UX04CombatTiming.Run、Combat03Area.Run、B07Economy.Run。

```powershell
& ./ProjectDocs/WanxiangGuitu/DeliveryBalanceAI02/Invoke-Check.ps1 -Project "$owned/F/Project" -Output "$owned/Rules" -Method BAL02Rules.Run -NoGraphics
```

矩阵前 `Instrument.py <repo> <project> <新观测目录>`只在拥有副本给CombatEnemy/EnemyProjectile/ForestBossBrain包裹原单次Damage/GainExperience，拷贝BAL01Trace。封存原始/观测源SHA。两版同一BAL02Matrix.Run模板，Mode各自独立StorageRoot/Output，种子418/419/420，3次独立Run，4防档×6组、30/90秒。非目标停用、条件前定位/装备/等级/两药重置，条件期间实际AI/移动/闪避/治疗，不复活凑窗口。全局legacy RNG显式按条件重置；不是Run-owned正常冒险。示例：

```powershell
& ./ProjectDocs/WanxiangGuitu/DeliveryBalanceAI02/Invoke-Check.ps1 -Project "$owned/F/Project" -Output "$owned/AfterMatrix" -Method BAL02Matrix.Run -NoGraphics
python -X utf8 -B ./ProjectDocs/WanxiangGuitu/DeliveryBalanceAI02/Summarize.py $owned
```

`hp.csv`无头列：活动time,frame,HP,Defense,potionCooldown,level,XP。逐击events中的projectile来源通过attack身份与实际spawn/telegraph join，不能猜最近敌人；汇总HIT_EVENTS无未解析来源。PAIRED_INPUTS检查初始HP/D/power/ranks/位置/RNG，不比较独立生成UUID。截尾TTK=-1，不换成0。

## 旧v9与正常AI

旧BAL02Recovery.Save生成真实高防v9 Store，原字节复制到新LegacyLoad/Store，经正常InitializeStorage(loadExisting=true)读取。9条恢复/低HP真实Damage/免费撤离中断/成功Pending/Committed断言。不得编辑编码后的最终存档。

正常AI用本批安全薄包装Invoke-NormalAI.ps1（仍是原Step，不新建编排）：Project、RunRoot、Output、Mode Normal/Resume/FinalResume。明确非batch，私有测试桌面不激活；batch的默认Save.Start跳过是已证实工具边界。包装只在拥有副本去重/保存三个旧驱动；相机目标用真实Collider，后退用S键。全部敌人AI保持，材料/制造/结算走原业务。BAL02NormalObserve只读记录XP/级别/HP/ranks。三个不同Output、同一RunRoot，断言和正常退出均独立。

## 两类非开发Player

还原三AI产品源码，BAL01Trace移到Editor，确认产品源码字节与工作源一致后复用Build01Audit.Run输出纯发行。Inspect-Build检查PE所有模块无BAL02/PLAYER02等驱动和UnityEditor；完整消息、输入、exe/assembly SHA保留。

本批Runtime/*.cs.txt只复制进拥有验收副本Assets/BAL02AcceptanceOnly，复用PLAYER02原驱动的partial分派。旧LegacySave/Store原字节复制为Runtime/ArmorStore/WanxiangGuitu/ForestRuins，配置先Rules后Resume；Runtime/owner.json kind=`PLAYER-02 isolated runtime acceptance`。复用原DeliveryPlayer02/Invoke-P02Case.ps1 -Mode Observe及既有worker，配置使其执行ArmorCase而非旧Observe标题检查。两个进程均真实菜单继续/F5/退出恢复；Damage标量用例每次初始化HP，不叫战斗胜利。禁止把Runtime模板接入纯发行或用户Assets。

## 发布与核查

Collect.py只收本批根的合成日志/输入/回执，排除P/F工程、Deferred用户、Release二进制和Worker。日志及大hp.csv gzip，凭据字段脱敏，manifest分别记原始/发布SHA。冻结源/两构建input对齐；用户5文件SHA不变；旧交付、AIM、AI、XP、v9、Packages等不改。LFS核查、定向stage/push、ls-remote完整SHA后暂停。原生/人工/完整性能未执行写NOT_RUN，历史根因UNRESOLVED。
