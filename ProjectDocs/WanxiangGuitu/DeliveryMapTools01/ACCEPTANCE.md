# 分层验收

|层|结果|证据/限制|
|---|---|---|
|官方免费版身份与模块范围|PASS|官方资料核对；不代表导入|
|Dungeon Architect Unity功能研究|PASS|DUNGEON_ARCHITECT_STUDY.md；非运行结果|
|独立Unity/URP初始化|PASS|Acquire2/Unity.log.gz|
|原工程与用户输入保护|PASS|2413项未变，protected-after-acquisition.json|
|MapMagic官方包获取|BLOCKED|Acquire4/acquisition.json；用户已领取，SDK未完成下载|
|MapMagic地形、种子、碰撞、导航、Scene、Player及性能|NOT_RUN|未导入，不能用自制地图替代|
|Dungeon Architect运行验证|NOT_RUN|没有安装包；本轮仅研究，不采购|
|人工美术与编辑效率|NOT_RUN|没有真实操作计时与独立试玩|

完整24条自动汇总见[acceptance.json](Evidence/acceptance.json)。PASS仅对应具名层级。总体BLOCKED；不计算虚假的插件通过率。

此前产品历史FAIL、法杖/引擎UNRESOLVED和原生/人工NOT_RUN均不属于本轮可关闭事项。
