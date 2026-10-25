# B08 新手引导与营地体验

状态：本轮实现与证据交付，等待复审。原生UI、人工理解与已知诊断保持开放。

开工本地与远端 main 均为 `638dd9b8159887bd02b6fc0c2e38d817623622cd`。Unity 6000.6.5f1 / URP17.6.0 / Input1.20.0 / uGUI2.6.0 不升级。用户 ForestRuins 场景与 ProjectSettings 保留，测试使用其工作副本并单列哈希，不纳入Git。

## 现状与最小范围

原营地通过Camp.Enter打开永久仓库并暂停；PlayerInventory禁止在营地关闭，关闭按钮跳到出征准备。现有程序化营地已有帐篷、仓库、工作台和营火，但没有可接近的设施交互。PlayerHUD仅对ActiveRun显示，制造目标与准备页长规则并列，准备页两段文字还占用同一个y+236位置。旧波次怪物标签在营地远处仍可投影到屏幕。

保留原仓库/工作台面板和出征、结算入口。增加“营地走动”、四个非碰撞设施标记、短标签与当前设施强调，E继续使用InteractionResolver的展示token与执行校验。关闭面板可在现有18米营地地面内走动；不开新营地地图，不重建美术。H原营地出征准备入口保留。营地中主角攻击和怪物攻击被阻止，战斗实体与奖励规则不改。

常驻一项主目标：教学优先，其次玩家制造目标，再次自由探索/营地准备。生命与核心快捷栏保留；附近才出现E/H情境提示。完整路线、评分、制造缺口和帮助继续按需打开。教学帮助有独立重看入口；准备页详细规则可展开，修复重复行。保存失败在HUD、详情及背包中分别可见，普通消息不能覆盖关键错误。Boss预警层级继续沿用B07-R1。

## 真实教学条件

| 阶段 | 完成依据 |
|---|---|
| 装备、仓库、工作台 | 靠近对应设施、通过现有交互解析实际打开业务页；错序设施可用，但不冒充当前教学完成 |
| 出征 | 原Depart创建并保存新的森林Run，教程绑定runId；失败沿用原营地回滚 |
| 移动 | CharacterController实际水平位移累计3米；RestorePosition不计，低帧率大步长也计入 |
| 采集 | 真实资源击毁产生掉落ID；只有该材料实际拾取、背包与本局来源账增量一致才完成 |
| 拾取与备料 | 另一真实掉落成功归属，随身满足既有白武器配方：木2石1矿2；不自动拾取 |
| 撤离与结算 | 推荐实际可达的免费出口，不要求清场/精英/Boss。原引导成功才产生Extracted；取消不推进；原确认/已保存/回营入口不变 |
| 入仓与取材 | 原结算收益入仓后确认回营；实际仓库取材成功，随身配方材料齐备才推进 |
| 制造 | 原Camp事务真实消耗并生成装备，教学状态同次保存；不是查看配方就完成 |
| 再次出征 | 已提交首局并实际创建不同runId的新森林Run后完成；无额外教程奖励 |

自由行为不被教程锁住；提前撤离、死亡或放弃后可回到准备再尝试，不发补偿、不恢复已用物资。渡口修复为可选进阶，木2石1及原回执不变。教程推荐免费出口，玩家仍可自主选择其他合法撤离。营地走动位置不另存，下次恢复回到原营地落点，教学阶段保留。

营地世界时间继续暂停，只有CharacterController的普通营地移动使用unscaledDeltaTime；不通过恢复全局时间实现走动。技能、攻击、切换、翻滚和药水冷却继续暂停，营地禁用攻击与翻滚；背包/帮助继续阻止移动。第一版恢复TimeScale=1的兼容风险单独补回归和修复，不能沿用第一版All当最终证明。

OnboardingFocus每秒最多一次、每类最多12个候选查询，采用真实NavMesh完整路径并避开路径附近的精英/首领；不是自动移动、精确风险预测或保证绝对安全。无法找到候选时明确提示按M查看，不能伪造距离。营地为既有平坦可行走小场地，距离标为营地近似距离，不冒称NavMesh路径。所有查询不推进玩法随机流。

## 保存兼容与失败

继续使用v9完整封装及既有分页。Profile新增显式hasTutorial与可选TutorialState(version1)，包含enabled、stage、completedMask、learnedMask、seenMask、skipped、reviewAllowed、首局ID、资源掉落ID和已走距离。新Profile才默认启用；旧v1～v9迁移/读取缺少hasTutorial时不启用。Unity内联类会将null对象物化为默认对象，因此不能仅靠null判定旧档；本轮回归暴露并修复该问题。

跳过只保存教程设置，不改Run/库存/随机；重看帮助完全只读。明确点击营地“启用”仅重置教程状态，保留所有业务进度。Camp制造/转移沿用同一事务；补已发布回调异常的磁盘核对，不盲目退款或重复消费。可确认旧修订未发布才回滚；无法确认时冻结并要求读取完整存档，不伪称成功。

关键源码：Onboarding.cs、OnboardingFocus.cs、CampFacilities.cs、PlayerHudPresenter.cs；小范围接入AdventureFlow、LootPickup、AdventureResource、CampRuntime/Workbench、InteractionResolver、Inventory及实际移动方法。没有新增奖励经济、结算器、存档目录或随机源。

## 开放事项

原生U16、最终Player原生键鼠教学与独立人工可理解性 NOT_RUN。D3D12 UNKNOWN及既有Editor青色帧诊断 UNRESOLVED。不重复无新线索的关闭实验，不修改退出生命周期。Editor领域机器人、受控规则/截图和最终Player启动恢复分别报告。

首版营地仅支持普通走动，世界时间与动画继续暂停，不是完整自由营地美术或动画重构。OnboardingFocus沿用既有FindObjectsByType(..., FindObjectsSortMode.None)扫描模式，新增节点/掉落扫描带来4条CS0618弃用警告；构建总计81警告，不能全部归为旧警告。没有升级依赖或为清零警告批量改旧API，全部原文与行号归档。

最终数据与失败历史见下节及验收表。交付后暂停复审，不自动开B09或后续地图。
<!-- FINAL_VALIDATION -->
## 最终实际验证

运行目录：`D:\WanxiangValidationRuns\B08ReleaseAll\20261025-190134-7b35aac0`。冻结输入：`c7ae847b3f9121236cb5521d4c8fb4a9bc896c05`。

源码核对：产品87份、注入测试64份、正常AI执行驱动54份。

All状态行：`{"PASS": 138, "FAIL": 2, "NOT_RUN": 31, "UNRESOLVED": 2}`；非预期FAIL 0。

```text
result=Succeeded
errors=0
warnings=81
bytes=114126452
duration=00:00:37.8365524
product=万象归途
company=DefaultCompany
```

正常AI进程：18；最终Player进程：14，各自真实退出码/超时/审计独立列出，不相互替代。

实际首次教学路线、材料收益、首局/后继Run与教程阶段见review-summary.json。测试无自动授予教程物品；白武器使用既有木2石1矿2配方。

产品与执行测试冻结后只增加报告及证据后处理工具。最终完整交付SHA由本报告所在提交和交付消息给出。

森林入口的部分受控截图有青色立柱/底座遮挡角色，与ForestRegionRuntime既有入口撤离标记的位置和形状相符；本轮未修改这些几何。不能把它直接当作引擎异常，也不能用布局断言或40%阈值宣称所有画面无遮挡。既有大面积青色帧内部根因仍单独UNRESOLVED。

[验收](ACCEPTANCE.md) · [失败历史](FAILURE_HISTORY.md) · [复跑](TESTING.md) · [证据索引](Evidence/INDEX.md)

## 最终证据复核

新手正常流程实际带回木4、石4、矿3；回营取木2、石1、矿2制作白长剑，后继仓库余额为木2、石3、矿1。没有教程物资补发。Profile、首局和后继Run为真实不同ID，第三进程继续同一后继森林；最终Player教程完成/账目身份在第二次退出保存修订39→40后仍一致。

87个产品脚本、64个注入测试、54个实际正常AI C#驱动与c7ae输入匹配。Provenance另记录驱动目录的其他文件，因此126项不是126个C#驱动。815项Assets/Packages/ProjectSettings输入中有6项原有隔离构建配置差异：两个URP设置、EditorBuildSettings、GraphicsSettings、ProjectSettings和UnityConnectSettings。用户ForestRuins和ProjectSettings开工字节均保持不变，不提交这两项。

正式程序集SHA256：`0c4177977e9ed4b9800dffffea2588124948b370e83ee4257ee46dfa1d62ab37`。81条BuildReport警告与162个日志warning标记行不同；新扫描代码4条弃用警告已单列。规则/构建/正常AI日志70处Exception起始行均含UnityEditor.Search内部调用栈，根因未定位，不归因产品，也不声称Editor零异常；完整日志不删除。

14个最终Player进程均实际exit0、无超时、无强杀，方法均为Owned-window WM_CLOSE。退出/恢复审计另存，不能证明真实标题栏关闭干净或原生U16通过。协调器真实子进程exit0见回执；观察时间不当作精确退出瞬间。

[五张代表图复核](Evidence/FinalAll/visual-review.json)包含1280×720/150%、1920×1080教程、3440×1440仓库、保存失败及正常结算。它是代理读图，不是独立人工试玩。帮助正文在滚动区内，首屏下段被裁切；原生滚动理解未验证。旧IMGUI背包仍沿用CombatUI缩放，不将新HUD百分比称作所有旧面板重做。

新Profile自动教学；已有进度的老档可在营地“帮助/教程”中明确启用，单纯重看不重置任何物资或Run。营地关闭面板走动，靠近标记E交互；完成真实拾取后推荐免费出口，再回营取材制造并再次森林出征。交付后暂停等候固定提交复审。
