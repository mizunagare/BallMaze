# COMBAT02：测量后的剑/枪差异化

仓库mizunagare/BallMaze，main。开工本地/远端均为`71877635f3b5891abeccaff4032045156ce8af85`；审计归档提交`d3b06571cfffe3d2727c73101b3e990db565a53c`；产品冻结提交`ef2ba04f90790607742d4b5b4f11bfbf93293026`。最终证据提交由本文件的Git固定版本及交付消息完整SHA标识；不能把冻结源码SHA冒充最终报告SHA。

UX02仅在源码/交付方受控证据范围有条件接受，没有审核方独立重跑；不继承旧PASS。开工哈希、复审全文与审计见本目录Reviews和AUDIT_AND_MEASUREMENT。

## 实际改动

先运行Before和BeforeBoundary，再冻结DESIGN，最后改7个产品C#，没有改场景/设置/依赖/地图/随机流/经济/掉落/结算/v9结构。

- AdventureCombat：枪普攻3.8→3.1米（仍加原ReachBonus），横向半宽.85→.4；根方向阈值仍.88。普攻间隔乘1.30、威力乘1.25；白装从33/.5s变为41.25/.65s。剑/弓/杖数值和所有技能品质分支保持原样。
- FantasyActorVisual：复用已有可重复动作时钟；枪普攻动作采用同一实际周期（仍受原.55s动作上限），不伪造可靠动画事件。未释放取消不伤害、不退款；已释放弹体独立、暂停、死亡/卸载规则不变。
- CombatFeedback/Effect：枪释放用窄直刺，不再与剑共用弧光。AdventurePulse近战反馈使用扇形/横向条带交集，不再画扩张整圆；使用实际判定参数，Collider外缘接触的根距离差异单列。命中特效仍只来自真实扣血；不添加碰撞或使用随机。
- HUD、猫族角色页与旧回退角色页使用真实普攻间隔/威力，不把基础技能威力当作新枪普攻；技能文本/数值不改。

旧存档剩余冷却按原秒数恢复，不退还、不按新比例重算；后续新攻击使用当前规则。装备冻结数值、品质、长枪追加段、弓独立箭和法杖AoE全部复用，v9无迁移字段。

## 实测与限制

完整表见[WEAPON_DATA](WEAPON_DATA.md)。10cm边界：普通/精英/波次Boss剑2.1/2.2/2.4m，枪Before4.1/4.2/4.4m，After3.4/3.5/3.7m；枪/剑约1.54～1.62。剑近身横向覆盖更宽，枪远距正面可命中但侧向更窄。684+81条前后逐键数据、8+8时序、前后各24短战和20条独立比对均有原件；243格普攻采样枪39→23命中，剑63不变，不能当玩家命中率。

每武器/体型短战n=2，枪普通/精英/波次Boss均值约.711→.880、2.227→2.194、5.283→5.495s；受到伤害0/20/24未变。当前只有有限节奏取舍证据，不宣称平衡完成或更少受伤。掉落随机初态未作为短战配对条件，数量仅事实记录，不用于奖励等价结论。固定地图418与正常森林AI实际seed分开记录。

新增15条实际品质/多目标伤害、16条±10°静态坡面、旧188条战斗规则通过。原样旧规则先187P/1F（枪伤害预期33→41.25），保留exit1；仅替换这一预期后188P。输入/观测/双Boss原回归进程通过。

正常森林AI三进程全部exit0：实际采集木材4、修复渡口一次、撤离、统一结算、存取制造、再次森林出征、同Run新进程恢复。实际请求/接受seed650558838、revision5、fallbackFalse。证据属于Editor正常AI，不是最终Player或人工。

**新增开放项：**首次附加B07Rules在40请求seed（39个不同接受seed）导航通过后，读取原出征再Single查找Boss失败；三次依赖恢复随后缺少expected文件失败。原清单的依赖门控已补，旧4个exit1原封保留。另一个全新隔离Run仅增加只读Dump后，Run/Resume/Pending/Committed四进程及保存故障重试、重复提交、确认/再次出征通过。但身份/初始seed不同，不能用这次PASS关闭首次失败，根因继续UNRESOLVED；没有改产品恢复代码。

## 构建与证据

Unity6000.6.5f1、Windows64、BuildOptions.None：Succeeded，0错误94警告，346.718秒，构建进程exit0且未超时。所有消息在build-report-messages.json，未过滤警告。EXE SHA256 `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`；Assembly-CSharp `e0c1ed904d4d43f9b618ed3494c535cf3263f72abb9ef585d280198e7be0b9e5`。DLL元数据不含本批Editor驱动名；发行Player战斗操作NOT_RUN，构建不等于运行通过。

源仓库与副本所有C#逐文件哈希一致；构建后部分副本URP/Graphics/UnityConnect设置重序列化差异照录，不假称所有输入字节一致。用户ForestRuins、ProjectSettings及Recovery共5项SHA前后相同，未暂存。没有访问真实档、关闭用户程序、抢桌面、升级依赖或启用CI；没有强杀超时进程。

受控前后图使用同机位1280×720、布局418与同配置；raw与URP RenderRequest分别归档。它们只是有限固定场地反馈对照，受伤高亮会遮挡模型局部，不算人工可读性通过。没有用图像替代实际命中记录。

[验收表](ACCEPTANCE.md)与[分层结果](Evidence/FINAL_SUMMARY.json)：17 PASS /1历史预期FAIL /4 NOT_RUN /7 UNRESOLVED。未执行原生U16、独立人工、最终发行战斗操作、完整性能。旧C15、D3D12 UNKNOWN、青色帧、Search、JobTempAlloc和旧Editor启动阻塞不关闭。新增恢复首因也不关闭。保留全部失败，不把编排器exit0或第二轮PASS当整体验收。

[复跑](TESTING.md)、[失败历史](FAILURE_HISTORY.md)、[证据索引](Evidence/INDEX.md)。本批停止，等待固定SHA独立复审，不开始新地图/武器/后续批次。

整体汇总为 **FAIL**，Verify-RunStatus实际exit1：4个非预期首次恢复链失败、1个精确识别的历史预期失败。后续新Run通过不抵销首因；17P/1历史F/4N/7U仅为分层验收条目数，不能作为总体通过率。见[汇总原件](Evidence/aggregate-status.json)。工具最终版本以本报告所在提交为准。
