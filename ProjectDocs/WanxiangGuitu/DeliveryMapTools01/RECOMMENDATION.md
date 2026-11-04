# 建议与下一步门槛

**本轮先采用MapMagic 2免费基础版作自然地形验证；遗迹/地下通道/Boss大厅的首选工具候选为Dungeon Architect。** 后者是基于官方功能与需求的设计匹配判断，不是实测胜出或采购建议。

MapMagic的免费、地形节点图与可读C#源码适合先核实有限森林地形、Collider、Seed和URP/Windows构建。免费Objects能力不可凭空补齐。地下房间、转角和大厅仍需要独立模块化几何；不要强迫高度场承担多层室内拓扑。

Dungeon Architect的Snap/Grid Flow更贴近房间与连接约束、可选分支及Boss空间。官方Unity文档提供按配置seed再Build的运行时方式；静态标记/碰撞/导航仍需产品适配，不把选择目标或图求解当作实际通行证明。[Unity运行时文档](https://docs.dungeonarchitect.dev/unity/advanced-dungeons/runtime-dungeons/)、[Snap Grid Flow](https://docs.dungeonarchitect.dev/unity/snap-grid-flow/sgf-introduction/)

Gaia本轮不采购、不导入；自然环境整套生态能力可能有价值，但现阶段不应为遗迹房间引入更大的整体环境依赖。没有实际样例/编辑计时/Profiler，三者美术、效率、性能都不打主观分数。

## 当前状态

MapMagic免费核心已在独立工程完成小规模真实地形、碰撞、Seed重复、NavMesh、Scene及非开发Player验证。它是**当前不购买条件下的首选工具**，建议先作为编辑器地形底板生成器，导出固定TerrainData，再由自有模块和业务系统管理室内、交互、敌人及奖励。

不建议目前将免费MapMagic当成完整森林/遗迹生成器：Objects/Splines另售，当前树木是自有夹具摆放，转角通道和Boss房是自制模块，且转角通道尚无顶盖。真正地下空间语法、门锁约束与模块生成仍应保留为DA后续验证门槛。DA没有包，不能宣布实测优于其他工具。

接入必须显式配置URP地形材质，避免默认Shader在Player中缺失。有限种子与轻载场景不是稳定性/性能完成证明；构建JobTempAlloc开放项和GC/GPU缺口见PERFORMANCE.md。不得因本次烟测通过自动把插件加入产品。

只有MapMagic免费版真实验证后，才决定是否值得继续构建室内模块或评估合法DA包；不自动采购、不改正式项目、不合并main。
