# B3 随机流隔离交付（2026-10-24）

仓库 mizunagare/BallMaze，main。开始本地与远端均为 `0230ae0c8c0b57cb6dceb0f9aef566ad8e78c6cc`，提交前重新读取远端仍一致。用户确认该边界补丁通过限定源码与证据复审，不代表独立运行 Unity；B2 原审阅基线 `1be7ad6819aec8f642eae59f3b8d447686ca63b1` 保留。最终SHA以本报告所在提交及推送后的完整远端核对为准。

B3 本轮可自动执行范围通过，待复审。只增量隔离随机源；ShouldDropChestGear 与其边界测试不改，不重写 B2/B1/A1/UI-01。ProjectSettings.asset 用户修改保留未暂存；不升级引擎/依赖、不启用CI、不访问真实玩家存档、不抢桌面、不关闭用户程序、不强杀测试进程。未进入B4或B07。

## 实现与实际入口

从原营地出征即可。新Run按已有seed初始化Rewards、Placement、Events三个可保存状态，森林布局继续用原局部System.Random(seed)，表现继续用既有独立System.Random和显式粒子种子。宝箱、敌人、采集量、装备品质/类型/词缀、制造词缀和技能候选改读Rewards；波次布点和事件位置分别读Placement/Events。原概率、材料范围、算法、ID和结算规则不变。同步抽样后finally恢复外部Unity全局状态，绘制/噪声不再扰动新Run奖励。

复用原RunState及同一v9封装，新增hasRandomStreams默认false及randomStreams(version1)。旧在途无启用标志继续原全局流，下一次新出征才启用；不补抽旧宝箱，不更改布局、种子、装备或既有事件。JsonUtility会物化空嵌套类，因此使用明确标志，启用后缺失/损坏/未知状态拒绝保存或恢复，不重开。恢复中临时建对象所消耗的状态不推进保存的随机流。

详见[全项目随机调用审查与兼容规则](RANDOM_AUDIT.md)。地图revision3、generation5、contentRevision B06-B2及历史ID维持原值；独立随机算法版本为1。营地/无Run沿用旧随机语义，不影响新Run种子。装备新建ID仍Guid，仅要求已有ID保存恢复一致，不承诺跨独立实验ID一致。

## 实际运行与结果

最终全新根：`C:/Users/guan/Documents/unitytest/WanxiangB3Verified/20261024-120353-057d1bd3`。既有GameplayOnly编排完整执行，不继承旧PASS。21个选定业务方法、合成夹具、正式构建、正常AI/Resume和92帧受控矩阵；协调器exit0。**37 PASS / 2预期探针FAIL / 17 NOT_RUN / 1 UNRESOLVED，非预期FAIL=0**。预期探针保留exit7及诊断超时，不强杀；其余测试无超时，最终所有自有测试进程已退出。

- B3固定/不同种子、30合法布局/奖励差异、通道隔离、异常状态恢复、损坏状态拒绝PASS。
- 实际装备/材料序列在500次全局随机噪声及独立地图生成后相同；只读缺口/路线/目标/来源查询前后完整Run与全局状态相同，后续奖励也相同，PASS。
- 实际遗迹开箱、重复拒绝、未领取不入账、已开箱/装备ID/地面材料保存恢复、旧v9空字段和写盘故障恢复、新进程同Run/区域/seed/布局/来源账/下一奖励序列PASS。
- B2遗迹roll=1、其他地点概率边界、五地点收益、敌人重复掉落、制造目标PASS；B1收费原子性/回执/恢复、10种子通行、A1隔离与迁移、装备/容器/双武器/制造、分页及保存故障PASS。
- 正常AI（Editor脚本驱动，不冻结敌人、不覆盖伤害/速度/生命、不在出征后传送）实际击杀、木材4拾取、石料拾取、木2石1修复、未清场撤离、结算入仓、取木2制造、再次出征和新进程PASS。修复后木2，取2制造后仓库木0；最终仓库材料数组 `0,0,0,0,5,0`，详见原日志。B3_CHECKPOINT与新进程完整随机状态断言PASS。正常AI两进程实际exit0、timedOut=false、隔离哨兵未变。
- 正常AI后继出征为波次模式；重复森林由受控B2/B3规则验证，不称为B4多路线完整冒险。规则中禁用NPC，正常AI不禁用，两者明确分开。
- 非开发Windows构建PASS：Unity6000.6.5f1 / URP17.6.0 / Input1.20.0 / uGUI2.6.0；0错误、63警告，114033989字节，41.5432922秒。较前轮增加的2条为新helper复用FindObjectsByType旧签名产生的弃用警告，不声称全是旧警告。程序集SHA256 `b3dbaf8fbe42a1c9d4d889a8e392bf100d2f0054876bc3b661adcbd6c98d9387`。完整构建文件哈希已发布，exe是Unity启动壳，不用其不变哈希冒充程序集相同。
- 92帧实际受控截图及布局检查PASS，哈希清单已发布；正常AI实际PNG单独发布。不是原生输入或人工可理解性验收。

73个业务C#与最终运行副本归一化LF逐文件匹配，见source-provenance。保留测试副本与原始日志；发布版为白名单脱敏转换，manifest列前后SHA。没有上传save、分页载荷、构建、Library、Temp、转储或凭据。

## 失败历史（未覆盖）

| 运行 | PASS / FAIL / NOT_RUN / UNRESOLVED | 实际非预期失败 |
|---|---|---|
| Before，协调器exit1 | 33 / 4 / 18 / 1 | B3全局噪声改变奖励；B1通行seed10 physical missing path |
| Attempt1，exit1 | 34 / 4 / 18 / 1 | 测试直接比较未排序Layout与保存排序后的出口数组；旧森林随机空对象校验失败 |
| Attempt2，exit1 | 34 / 4 / 18 / 1 | 合成旧字段保存失败；旧森林随机空对象校验失败 |
| Final，exit0 | 37 / 2 / 17 / 1 | 无；两个故意探针仍保留FAIL |

Before产品代码是开始提交，仅新增能暴露耦合的测试。Attempt1已通过噪声/查询隔离，但原测试布局比较方法不正确；改为比较实际Capture快照，不放宽业务状态断言。Attempt2补实际旧字段测试，暴露JsonUtility空对象兼容问题；以hasRandomStreams修复，最终旧森林夹具和合成旧语义均通过。对应源码/测试快照与失败日志已保存。

Before的B1通行失败发生在未改产品代码时，后续三轮同测试通过；具体根因未定位（UNRESOLVED），未为使其变绿修改导航代码或放宽断言。不能宣称该历史失败已因B3修复。部分Editor日志含UnityEditor.Search.SearchDatabase启动索引异常，保留完整栈，不归为产品或Player关闭根因，不吞日志。

## 开放项与下一步

UI-01 UNKNOWN继续UNRESOLVED，原生U16与人工理解继续NOT_RUN；历史65/2/20/1保留，本轮没有重复关闭实验、ProcDump或Player原生关闭。未选完整历史矩阵17项NOT_RUN，不继承旧PASS。正式Player原生输入及标题栏退出本轮NOT_RUN，编译/构建不等于运行验收。

旧在途刻意保留全局随机耦合；营地随机未全面迁移。新Run同一Rewards流仍对实际操作顺序敏感，本批不实现每个实体独立子流。随机状态采用当前Unity序列化格式，升级引擎必须另做版本兼容验证。B4及B07未开工，等待本批固定提交复审及明确授权；推送不等于复审通过。

入口与复跑见[TESTING](TESTING.md)，验收见[ACCEPTANCE](ACCEPTANCE.md)，实际证据见[INDEX](Evidence/INDEX.md)。
