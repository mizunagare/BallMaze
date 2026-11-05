# CP06-C1 远古遗迹原型交付

状态：实现与本地技术验证完成，待固定SHA独立复审；不是完整人工体验或正式发行批准。不合并main，不开始C2。

## 输入与分阶段门槛

产品基准07e47664101b1e4476b675e2b2163ae2ca9f512f；工具参考27a1e8159439b5c3d6fa7badcf932f3df7ba2c3c。开工远端main72db192a527bd256e2ba18cd7ab334d8334051da。独立分支feature/cp06-ancient-ruins直接从产品基准创建，未合并研究/旧C1分支。

兼容映射提交8affd0e0a85bb95f373ed4d98bbefef061b64efc；前三地区实现及双层26+26 PASS提交3ce9346825b279560b6015672b9cb961ff8990fd后，才启用后两区。最终产品输入冻结cd820b6363b1df689d9ad639684a5e1f1c04d747，后续仅验证夹具、文档及证据。最终交付SHA以本文件所属固定提交和交付回复/远端ls-remote回执为准，不能把产品冻结SHA冒充文档最终提交。

工程H:/unity/WanxiangGuitu-Ruins；唯一新测试根I:/WGCombat/C1-1105-A；独立游戏验证工程I:/WGCombat/CP06C1-1104-A/Validation/Project；独立MapMagic作者工程I:/WGCombat/MAPTOOLS02-A/Project。复用已关闭缓存，不复制使用中的Library。未关闭用户程序或强杀，低于3GB不启动Unity，Editor构建实际门槛更严格为5GB。

## 实际实现

五个有真实物理/导航关系的逻辑区域：入口、石柱广场、机关走廊、地下祭坛、守护者大厅。程序使用已保存TerrainData和自有模块搭建同一个权威区域实例，不是五个独立流式Scene。MapMagic免费核心仅编辑器高度生成，四块80m/257地形、固定作者seed424242；孔洞、镜头净空和模块为自有适配器。正式Player没有MapMagic/UnityEditor程序集依赖，也没有把自制散布说成免费Objects/Splines。

自有倒角石材、十棱石柱、拱门、台阶、祭坛、门、宝箱、符石、局部顶盖与已有猫族石像；四个既有猫族角色的石材衍生Prefab。原型材质/刚性分件，不是最终精修美术或新原创完整骨骼动画。台阶使用连续坡面碰撞，地下空间保留采光缺口，不冒充完整封闭地下城。

真实机关、双向门、碑文/密室、三个唯一宝箱、普通守卫/侦察者/精英和独立两阶段回响石像。新Boss具有横扫、真实三连弹体、震波及前摇/恢复，复用真实生命/物理/伤害/死亡。两处免费出口复用旧撤离与结算，不要求清场。运行时几何净空及漏收集事件碰撞均由实际行走失败定位后修正，未修改CP05相机或CombatAim。

新供给为矿石、晶体、兽皮、核心与三类新武器，参数为候选；不宣称经济不变或平衡完成。旧森林掉落与三旧随机流不变。全部奖励先落地，依靠原拾取/来源账/结算；地面紫装不当成已入仓。Run/区域/内容/实体SHA派生身份，不占用旧随机流。保存发布故障用完整状态确认、回滚或读取屏障，不凭revision/Run ID单项判成功。

关键源码：ForestRegionRuntime.Ruins、RuinsLayout、RuinsAssets、RuinsExploration、RuinsBossBrain；共享修改限于新地域出征/布局校验/保存边界/新地图掉落分派/路线收益/HUD和区域表现。CombatAim、AdventureCombat、TargetAssist、OrbitCamera、CameraActorFade、现有技能和新武器核心保持原始Windows字节及Git内容一致；ProjectSettings、Packages、用户Scene、CI无差异。详见[设计](ANCIENT_RUINS_DESIGN.md)、[布局](WORLD_LAYOUT.md)、[奖励](REWARD_RULES.md)、[存档](SAVE_COMPATIBILITY.md)。

## 本轮验证与保护

当前35个真实案例915 PASS/0 FAIL：规则33、受控Editor441、隔离非开发Player441。三区先行Gate另26+26。七武器各自真实装备/身份、普通战斗、走廊/大厅通行；法杖/弓有真实弹体墙体接触。精英、新Boss两阶段、真实死亡、故障重试、Run/地形/装备/奖励/来源账跨进程、三次读取、撤离取消和重复结算/再次出征均分层归档。脚本英雄控制，目标NPC保持真实AI；其他NPC隔离冻结，不称完整多人群遭遇或人工操作。旧B3流四组、B07经济两组受控夹具另列，后者含原有直接Damage/填包，绝不充当C1战斗证明。

历史结构化probe/rules65 FAIL全部保留，另有初始缺口、编译、反射、工具和超时失败。原始命令/输入/退出/重试保留，[失败历史](FAILURE_HISTORY.md)逐项说明；进程0不替代语义断言。最终[验收表](ACCEPTANCE.md)：37 PASS / 0 FAIL / 6 NOT_RUN / 4 UNRESOLVED。

六次非开发构建分别为三区测试包、四次完整测试包和纯发行包。纯包0错误104警告，四完整测试包0错误108警告，三区包0错误110警告。全部原日志及[警告索引](Evidence/warning-index-final.csv)保留。纯包移出全部C1驱动，四套测试包与纯包审计所列38项关键产品类型IL逐项一致，未检出原测试类型、Editor/MapMagic引用或测试原生桥。固定Privacy Profile SHA235d3703e301574ed8ba8326829d8019410700f9c14e4ddf37ac361e1d975876；六次实际Bee五项服务全部false。

纯包实际标题启动（有效合成营地可继续、未自动入游戏/创建HUD）和后台关闭后的实际exit0通过，合成存档字节不变。后台WM_CLOSE不是菜单退出的原生输入证明。exe是通用Unity启动器，同SHA不能唯一标识游戏，必须同时核对程序集与全部数据文件清单。完整包在I:/WGCombat/C1-1105-A/PureBuild1/Release，不将测试包当发行包，不将此原型标成已批准对外发布。

2413项用户/旧产品文件、199项供应商源码无变化；最终1368项产品输入哈希归档。测试工程有四处与仓库模板不同的序列化设置（URP资源/全局设置/Graphics/产品显示名等），来源阶段未在本轮干净配对定位，完整输入等同性UNRESOLVED；不是回写用户工程。UnityConnectSettings与模板一致、Bee五项关闭已实测。实际差异和SHA在[配置差异](Evidence/isolated-settings-differences.json)，不恢复字段掩盖差异。

## 未完成及限制

本机i5-12400F/RTX3060、1280×720实际Profiler Main Thread/DrawCalls有原始80帧有效样本；不是性能预算通过。GC正分配返回0未校准，GPU/显存未有效校准，长时间多敌性能预算NOT_RUN。原生分配漂移、JobTempAlloc、MapMagic版本标签维护原因继续UNRESOLVED；用户工程和供应商源码不改。

原生键鼠、U16、独立人工理解/美术/手感/最终平衡、本轮完整v1–v8迁移矩阵NOT_RUN。历史UI-01 UNKNOWN、Editor青色帧/黑帧、旧C15、Editor.Search及外部数据发送路径不因新截图/退出/Bee结果关闭。七武器全技能/所有Boss命中边界/所有相机位置未穷举。中间stage3仅逻辑兼容，不冒称本批迭代前后美术资产逐值一致。

证据入口：[Evidence/INDEX.md](Evidence/INDEX.md)。源码/资源和报告推送独立分支后暂停等待审核，不自动合并或进入水晶洞窟。

补充辅助专项：AssistEditor1/AssistPlayer1各20 PASS，实际剑前摇跟踪约24°（未逐帧强制转向），法杖释放reason=ASSIST_MUZZLE_TO_TARGET并发生真实碰撞/生命27→0；实体石柱为首遮挡体时目标被排除。查询保留三流和Random.State；不将仅选择目标当命中。
