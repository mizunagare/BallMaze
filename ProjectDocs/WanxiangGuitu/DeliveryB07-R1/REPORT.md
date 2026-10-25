# B07-R1 森林战斗可读性

状态：实现与本轮自动化证据交付，待复审；原生UI与人工理解未执行，已知引擎诊断未关闭。

开工本地与远端 main：`91c6664238d47e209c7fff835ccea67eab0d1c52`。用户 `ProjectSettings/ProjectSettings.asset` 和 `Assets/CombatPrototype/ForestRuins.unity` 均有未提交修改，保留且不提交；源工程不打开Play。隔离副本包含其当前场景，构建输入哈希单列，不冒称等于Git场景字节。

## 修复前证据

Before截图来自上轮固定SHA，非本轮重新运行。绿色横块为枝冠Cube（2.6×.25×.35），不是生命条。OrbitCamera将怪物碰撞体当作镜头障碍，近身聚怪会缩短距离并放大模型。普通敌人标签固定210×25且不避让；ForestBossBrain各自OnGUI按固定105/200行显示。冲锋用拉长Cylinder，实际为移动线段胶囊；噬浪画圆，但判定还要求方向dot>.2；散射还额外画小圆。该差异由源码及实际截图共同核实。

修复前隔离探针：B07_R1_MISSING_SHARED_GEOMETRY_RESPONSIVE_HUD_AND_OWNED_WARNING，已保留其实际exit1和原始日志。探针仅证明新显示契约缺失，不冒充完整修复前战斗回归。

## 实现边界

屏幕空间Boss信息按前摇优先、距离、稳定实体ID排序；独立生命及短预警，普通标签避让。单一只读几何驱动原判定与圆、胶囊、扇区、五弹道显示。预警按实体高度投射到地形，透明面与高对比边界不被模型挡住；边界是最大危险包络，环境阻挡仍按原伤害/弹体规则生效。无碰撞、无随机、无时间缩放。湖中水源射线与岸边本体区分；深水实体阻挡不变。

仅缩小枝冠并调整水冠/显灵比例、森林材质及非碰撞地点/岸线标记；不变更地点、地形参数、路线、导航源、掉落、存档字段或生成版本。森林相机忽略怪物对镜头距离的挤压，静态障碍仍阻挡镜头，战斗碰撞不改。

## 显示与验证范围

六攻击名称仍为根脉震击、角卫冲锋、荆种散射、水面潮矢、潮印爆发、岸边噬浪。近战圆与冲锋胶囊、噬浪有向扇区、潮印锁定点，以及五条带来源环的弹道分别显示；HUD以前摇倒计时优先。颜色使用陆地橙色、潮灵青色，不新增天气、陷阱、耐力或其他系统。

原伤害、前摇、恢复和范围有冻结值回归；UI与特效没有Collider，不操作随机流或时间倍率。显示的危险面是原XZ攻击几何的地形投影；在陡峭高度突变处仍可能拉伸，属于首版投影限制，不宣称地形美术完成。弹道会截到现有环境阻挡，实际伤害继续由原碰撞/视线规则决定。

森林改动只涉及既有材质、岸线和地点边缘的非碰撞标记。没有生成新地形、重抽旧布局或新增存档字段；旧revision1～5与徽章、来源账、首次奖励及唯一结算语义不变。透明遮挡为首版简化光照和即时切换，未作专项性能基准或人工舒适度验证。

## 既有开放事项

D3D12 UNKNOWN：UNRESOLVED。原生U16和人工理解：NOT_RUN。Editor领域机器人、受控截图、最终Player后台关闭/恢复分开记录。完成后暂停等待复审，不开发新批次。

## 首轮尝试（保留，不并入最终结果）

Directed1：接口探针与6534点/36矩形规则通过；运行截图因HUD缺失失败。Directed2增加诊断后发现持有的Boss对象已被销毁。检查显示新截图夹具早于非batch存档Start协程完成就出征，随后默认初始化覆盖了夹具场景。第三轮夹具改为等待现有IsInitialized再指定隔离目录，沿用既有B07Combat顺序；不修改产品初始化或存档生命周期。两轮完整原日志保留，其中UnityEditor.Search内部索引异常独立分类。

## 正常AI截图促成的第二次最小修复

首轮完整All虽无非预期自动断言失败，但Normal-Land真实聚怪截图中，Boss位于相机与主角之间，身体仍遮挡主角。该次以独立视觉检查FAIL记录，未关闭任务。增加CameraActorFade：用控制器及实际模型包围盒识别主角脚/胸/头视线上的遮挡者，仅替换其身体、枝冠或启用原始外形的材质；复用原贴图/颜色，自有透明shader不影响碰撞、血量、攻击、导航或随机。预警仍保持清晰可见。转开镜头恢复原材质，停用/返营清理克隆；帮助页提供一行短规则。

独立受控同位置开/关照片证明主角从Boss后方变得可见；不是人工试玩。第一版材质块构造时机错误、第二版遗漏独立枝冠及之后的回归均保留。最终运行改为D:/WanxiangValidationRuns/B07R1ReleaseAll/20261025-145529-a973b767，冻结输入dc55ece3c3d880090f562e120ebbc472a9f3eae4。

<!-- FINAL_VALIDATION -->
## 最终实际验证

完整 All 运行目录：`D:\WanxiangValidationRuns\B07R1ReleaseAll\20261025-145529-a973b767`。

冻结输入：`dc55ece3c3d880090f562e120ebbc472a9f3eae4`；产品脚本 84 个、注入测试 59 个、执行正常AI驱动 45 个分别核对。

状态行：`{"PASS": 120, "FAIL": 2, "NOT_RUN": 27, "UNRESOLVED": 2}`；非预期FAIL：0。

非开发 Windows64 构建（BuildOptions.None）：

```text
result=Succeeded
errors=0
warnings=77
bytes=114105726
duration=00:01:05.7058292
product=万象归途
company=DefaultCompany
```

正常 AI 证据是隔离Editor中的正常NPC+领域机器人。没有冻结NPC、覆盖生命或直接写胜利字段。正式Player另有启动/退出/恢复证据，不把两类互相冒充。

| 策略 | 首领真实释放数（最大记录） | 结算保留材料（皮/晶/核心/木/石/矿） | 保留装备 |
|---|---:|---|---|
| Land | 4 | 8/5/2/8/0/0 | 2件保留装备（品质详见summary） |
| Lake | 4 | 11/6/2/8/0/0 | 3件保留装备（品质详见summary） |

合成初始物资、制造与实际选用武器见 TESTING。采木后实际制作白弓，主战仍用原选中的白弓；不把这条验证称作装备搭配平衡完成。生命超过100可来自实际升级选择，不是覆盖生命。

12次Player进程的实际退出码、超时、强杀标记和审计见 `review-summary.json` 与各cell的process/analysis/storage-audit；仅在该轮全部实际执行时才称12次。

最终交付SHA由本报告所在Git提交及交付消息给出；完整运行输入之后仅提交报告/证据工具，不改变产品或测试执行源码。


## B07-R1 专项结果

| 编号 | 检查 | 状态 |
|---|---|---|
| V01 | 新显示契约、旧独立OnGUI停用 | PASS |
| V02 | 6534点几何等价、六攻击原数值、36布局矩形、随机只读 | PASS |
| V03 | 38张实际相机受控截图、双Boss/缩放/坡地、像素检查与生命周期 | PASS |
| V04 | 相机遮挡契约 | PASS |
| V05 | 身体/枝冠淡化与恢复、材质清理、HP/控制器/随机不变 | PASS |
| D02 | Editor短暂青色帧内部原因 | UNRESOLVED |

受控显示验证停用NPC，仅验证渲染/相机/几何与规则，不是正常AI战斗。正常AI与最终Player结果仍使用前表的独立进程行。

稳定帧截图通过不证明短暂青色帧根因已定位，也不代表最终Player原生UI或人工体验通过。
所有首次失败、诊断入口错误、元数据路径错误及修复结果见 [失败历史](FAILURE_HISTORY.md)。

最终All运行输入之后只修改报告及证据工具。产品、规则与正常AI代码均按冻结输入核对，构建输入与用户场景/设置差异明确列出。

## 运行截图与边界复核

本轮代理逐图查看了六种攻击的正常AI照片、1280/1920/3440的代表性受控照片，以及同位置淡化开关对照，见[截图复核记录](Evidence/FinalAll/visual-review.json)。它不是独立人工试玩，也不把停用NPC的受控夹具称为正常AI。38张攻击/坡地图加2张遮挡对照，共40张专项PNG，原字节与哈希均保留。

修复前：[实际聚怪](Evidence/Before/boss-telegraph-boss-warden-AntlerCharge.png)。修复后：[本轮正常聚怪](Evidence/FinalAll/Screens/Normal-Land/boss-telegraph-boss-warden-AntlerCharge.png)。两者是固定种子流程的不同运行，不宣称逐帧完全同姿势。精确同位置渲染开关对照另见[关闭](Evidence/FinalAll/ReadabilityScreens/b07r1-occlusion-controlled-off.png)与[开启](Evidence/FinalAll/ReadabilityScreens/b07r1-occlusion-controlled-on.png)。

实际入口仍是ForestRuins：从营地新出征森林，前往精英哨站东侧或湖泊北岸。新HUD/相机淡化随森林场景运行自动接管，不需重新摆放对象。已有在途仍加载原布局和实体，未遇到首领的旧在途不补怪。未更新的Editor应等待脚本编译完成后再Play。

## 构建、输入与日志审计

协调器真实退出码0见[回执](Evidence/FinalAll/coordinator-exit.json)。12个正式Player实际exit0、无超时、无强杀；closeMethod均为Owned-window WM_CLOSE。每个cell的process、timeline、storage-audit与before/after断言独立保留，不能证明物理标题栏或原生U16通过。步骤起止以results.json的UTC区间为准；辅助.exit.json的exitObservedUtc可由最终清理再次观察而晚于真正退出，不当作精确退出瞬间。

84个产品脚本、59个注入测试和45个实际正常AI C#驱动匹配dc55ece3c3d880090f562e120ebbc472a9f3eae4。Provenance还记录驱动目录的其他文件，因此其executedDrivers数组105项不等于105个C#驱动。源工程与隔离构建输入有6项既有配置差异：两个URP设置、EditorBuildSettings、GraphicsSettings、ProjectSettings和UnityConnectSettings，两边完整哈希单列。用户ForestRuins场景按原字节进入副本，原Scene与ProjectSettings均保持开工哈希，且不提交用户改动；不能宣称所有构建输入等于干净Git检出。

正式程序集SHA256：`23e05c9f21a858db7f1f19222912e312b9e4792e6b873843b4eeb406ab63201b`，显示组件存在而Editor种子与测试入口不存在，见[静态检查](Evidence/FinalAll/release-hud-check.json)。它仅是元数据检查；启动/恢复另有真实进程证据。构建总大小114105726字节，BuildReport为0错误77警告；[完整warning行索引](Evidence/FinalAll/build-warning-lines.json)含重复编译/汇总行，154个标记行不等于154条BuildReport警告。

本轮规则/构建/正常AI日志共59处Exception起始行，均含UnityEditor.Search内部索引调用栈，见[清单](Evidence/FinalAll/exception-inventory.json)及完整日志。未定位其内部根因，不归因于产品，不声称Editor零异常，不隐藏原始错误。D3D12 UNKNOWN与短暂青色帧各自保持UNRESOLVED；稳定帧检查通过不代表根因消失。

最终All状态行120 PASS / 2预期探针FAIL / 27 NOT_RUN / 2 UNRESOLVED，0非预期FAIL。这是本轮新运行结果，不继承All1或B07。UI01历史65/2/20/1保持不变；原生U16、正式Player原生Boss战、独立人工可理解性仍NOT_RUN。范围内实现与自动化证据待固定提交复审，不宣布发布验收或美术平衡完成。本轮交付后暂停，不开始新批次。
