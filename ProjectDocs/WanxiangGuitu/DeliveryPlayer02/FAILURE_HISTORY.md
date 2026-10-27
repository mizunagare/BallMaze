# PLAYER-02 失败历史

所有运行原件在[Attempts](Evidence/Run-1027-205135/Attempts)，不同尝试目录不可覆盖。五次Player失败exit1，均非强杀、无OS超时；一次启动器拒绝没有Player退出码。最终成功不抹掉以下记录。

|尝试|事实|处理|
|---|---|---|
|210627-Setup-b50ce6|键位面板与底层TitleMenu同名取消按钮，驱动选中底层目标，射线不可达|只修驱动按Canvas层级选择可见按钮；正式UI未改|
|211416-Main-bcd524|隐藏窗口无IMGUI Repaint，准备输入未消费，尚无Run|复用已有非活动桌面SW_SHOWNOACTIVATE显示能力；不激活桌面|
|211630-Main-6bc4e4|驱动的Event.current被消费，但原准备按钮未触发，仍在Preparing|失败保留；移除该模拟方案，不以直接回调代替|
|213027-Main-f9950c|自定义worker参数被PowerShell大小写同名script变量覆盖，预启动路径拒绝|先保存请求参数再校验；此处只有事后Console观察说明，无伪造Player原始日志|
|213111-Main-639770|弓已真实采木/E拾取，但石料生命未减，30秒攻击失败|截图与水平箭高源码、现有低矿切近战教程保留。改为真实装备UI选长枪，不改命中/碰撞/掉落，不声称已修产品弓箭机制|
|213928-Main-896eb8|长枪已采木/石；战斗离开矿点后驱动未重新接近，资源攻击超时|驱动战斗使用实际时长输入，保持90秒上限；战斗后重新导航，资源30秒预算不包含脱离资源的战斗/接近。无属性或AI改动|

技术中断后原游戏正常退出保存：没有把未完成Run改成死亡、放弃、撤离或收入。前两次Main没有创建Run；后两次真实在途状态保留在StorageAfter中。

另有独立工具失败，不并入Player尝试PASS数：

- `ProductIdentity/failed-proof-Acceptance-unaligned.json`：只按偶数字节解码UTF16漏查-p02-mode。保留FAIL，修为两个偏移扫描，并增加真实程序集引用检查；未放宽剔除条件。
- `failed-story4-business-initial.json`、`failed-story5-business-initial.json`：只读核账器误将森林枚举视为1。当前源码`AdventureMode`为TestChallenge=0/EndlessWaves=1/ForestExploration=2；修正测试常量后原快照23项分别通过，原始快照和失败均未改变。
- BUILD-01长路径预检故意启动的拒绝探针为预期非零，不能计为产品构建失败或当作游戏通过。10项预检均有本轮结果。

第一次窗口worker的原始源哈希没有独立冻结；命令、二进制哈希、窗口回执仍在拥有者外部根保留，最终Worker2源/哈希已归档。没有补造历史源码证据。

正式发行91警告不删除；最终临时驱动新增23警告全部归档。[逐条警告核对](Evidence/Run-1027-205135/WARNING_REVIEW.json)。JobTempAlloc等原始导入诊断未静默过滤。历史四项引擎根因仍UNRESOLVED，原生/人工/性能仍NOT_RUN。
