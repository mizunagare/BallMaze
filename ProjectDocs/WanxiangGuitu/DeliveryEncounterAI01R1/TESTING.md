# 独立复跑

固定基线b040b550a5725511a34867de4a2cb27dc56a2b95；Unity6000.6.5f1。仅使用新的工程外 `I:/WGCombat/ER1-*` 根，本次ER1-1030-A不可复用。先核对远端/本地、记录用户5文件SHA和owner；不操作真实玩家档，不关闭用户程序、激活测试桌面或强杀超时进程。

沿用DeliveryUI01/Invoke-Rules.ps1 -PrepareOnly准备拥有副本P/Project。仅副本中的用户Scene/Settings/Recovery保存至DeferredUserInputs，并以基线Git场景/设置替换；主工程原件不动。可从确认空闲的旧测试副本复制Library缓存，不把缓存当PASS。

## 聚焦运行

R1/Invoke-Check是薄适配器，直接委托原DeliveryEncounterAI01/Invoke-Check及UI01 Step/worker。测试类只复制到拥有副本的Editor/B06LocalChecks；预启动显式storage-root，唯一Output，3GB资源门槛，实际退出/超时/日志分别记录。方法默认EncaiR1.Run。

```powershell
$store="$owned/New418Store"
New-Item -ItemType Directory $store
@{seed=418;clearLane=$true}|ConvertTo-Json|Set-Content "$store/r1-config.json" -Encoding utf8
& ./ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01R1/Invoke-Check.ps1 -Project "$owned/P/Project" -Output "$owned/New418Launch" -StorageRoot $store
```

旧版副本用b040b550对应ForestBossBrain；新版副本只复制已审核一行修复的ForestBossBrain。同一最终驱动/clearLane配置分别跑418、419，另补新进程420。每进程两Boss×前摇禁用/真实命中/外部销毁三场景，80断言。不可在失败后覆盖同一目录或更改最终编码存档。

每场景从独立合成Profile/Run创建真实seed森林，Boss来自原生成器；没有直接调用Fire/Begin/Release、设置sequence、RememberReleasedThreat或直接Damage。Warden按自然招式序列运行，先前两招用当前已显示预警触发真实翻滚；Tide自然首招WaterFan。固定合法初始姿态，隔离非目标；实际Boss/弹体/碰撞/Damage运行。普通敌在窗口过期后以明确受控接近位置和原AI进行真实前摇/伤害，不能当作自然完整冒险。

初始419原射线被石柱挡住，原FAIL保留。最终clearLane夹具仅在最多8个现有NavMesh候选中读物理通路，找到无遮挡位置才验证实际命中；找不到即失败，不改障碍/射程/seed。initial-lanes.jsonl记录每候选位置、源、目标、遮挡名与距离，旧/新两个版本必须使用同样配置和候选。auditOnly=true可仅运行初始射线诊断，其seed元数据检查不计生命周期PASS。

外部Destroy是显式生命周期故障夹具，不是战斗胜利；它不改已生成存档。已释放有限窗按原规则过期，检验新许可、普通敌实际Damage和Boss新预警/释放，不能将纯查询通过替代实际攻击恢复。

## 必要回归与构建

Invoke-Verification按有界空闲检查调用相同旧入口：EncaiRepro19、EncaiGuard13、B3StreamRules、B07Economy、B07Rules Run/Resume/PendingResume/CommittedResume。三种子聚焦若失败就停止扩展，独立旧回归仍可继续。原After419失败导致首次流程停止420；最终新夹具结果另记clear-lane-processes，不改旧状态。

Build01Audit.Run -Graphics调用原WanxiangBuild（Options=None）。PureBuild首次完整消息0E96W；PureBuildFinal缓存0E2W，记录Boot/Title旧序列化告警。不要将缓存少报编译警告称为已修复。原Inspect-Build读取PE，排除Encai/BAL01等观测驱动与UnityEditor引用；报告exe/UnityPlayer/核心程序集SHA和全部构建输入。

Audit.py只读核对：一行修复、源与最终构建输入、用户SHA、旧交付无差异、最终相同驱动/配置/射线记录；生成RESULTS.csv和input-binding。Collect.py只拷贝拥有合成证据，排除P/F、Library、用户Deferred与Release二进制。日志/jsonl gzip，保留原SHA与发布SHA；Verify-Publication检查索引原字节/LFS oid及仅一个产品源的授权范围。

原524仅历史保留；本批新聚焦240、既有必要断言19+13，合计272结构化PASS。完整正常冒险、纯发行Player实际操作、原生U16、独立人工和性能本批NOT_RUN；所有历史引擎根因UNRESOLVED。交付后暂停。
