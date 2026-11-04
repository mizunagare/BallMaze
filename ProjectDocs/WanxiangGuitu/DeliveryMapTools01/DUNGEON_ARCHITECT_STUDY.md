# Dungeon Architect Unity：功能与兼容性研究

研究时间2026-11-04。没有安装包、没有购买、没有导入。下列是官方资料核对，不是本机插件测试。

## 工作流匹配

遗迹房间、转角通道和Boss厅适合先评估Snap Grid Flow：房间作为Prefab模块，尺寸是统一Chunk Size的整数倍；支持旋转时X/Z尺寸必须匹配，门的高度基准必须统一。先制作入口、转角、普通房、终点大厅四类模块，再验证连接、碰撞及实际角色通行。模块大小和门宽应由本项目角色、相机及Boss净空反推，不能把文档示例尺寸当作游戏规范。[官方模块文档](https://docs.dungeonarchitect.dev/unity/snap-grid-flow/sgf-modules/)

Grid/Grid Flow更适合主题标记驱动的平面布局；Snap系列更适合已制作模块。自然森林高度场不是本次首选用途。图上的门锁与生成路径只描述结构，实际钥匙、奖励、存档、交互和唯一身份仍须由产品业务层管理。

## 引擎边界

厂商声明Unity版1.23.0支持Unity6，在6.3 LTS及6.5测试，示例使用URP。不能将这一声明等同于6000.6.5f1、URP17.6.0、Windows64非开发Player在本机已通过。[厂商FAQ](https://dungeonarchitect.dev/faq/)

Unity产品有Grid、Grid Flow、Snap、Snap Grid Flow、City。Unreal的GPU voxel、Cell Flow及多人Build System等不能自动纳入Unity能力。具体已发布/路线图状态须逐项核对Unity文档与变更日志，避免采用首页跨引擎宣传作验收。[Unity产品](https://dungeonarchitect.dev/unity/)、[Unity变更日志](https://dungeonarchitect.dev/changelog/unity/)

## 导航接入

官方运行时导航教程明确针对主题文件类构建器，要求启用Runtime Navigation并标记参与导航的静态Prefab；NPC等动态对象不应产生烘焙孔洞。这不能证明任意Snap模块自动兼容现有NavMesh。取得合法包后应分别验证烘焙保存、运行时生成、门开关、模块连接与实际Agent穿行。[官方导航文档](https://docs.dungeonarchitect.dev/unity/advanced-dungeons/runtime-navigation/)

## 最小适配方案（未实施）

1. 优先编辑器生成并固化几何，导出只读模块清单：生成器版本、seed、模板GUID和哈希、模块坐标/旋转、连接端口及语义标记。
2. 游戏维护独立Run/区域实例ID、敌人ID、宝箱回执和奖励派生；不让插件随机源接管Rewards、Placement、Events。
3. 玩家存档保存生成版本与已确定布局；插件升级不能使旧在途Run重新求解。
4. 可视门、Collider、NavMesh及产品交互门状态须共同恢复；生成成功后再启用敌人和交互。
5. 初期不做运行时无限拼接或流式副本。先验证静态导出能否从发行构建移除编辑器生成依赖。

以上均是接入提案；没有修改ForestLayout、地图、存档或任何产品Assets。

## 仍需实测

精确引擎编译、URP材质、确定性重复、失败布局回退、Scene持久化、模块/NavMesh连接、非开发构建、卸载引用、GC/CPU/GPU和包移除后的依赖：全部NOT_RUN。没有编辑操作计时、真人美术评价或性能预算，不能给出效率/画质/性能PASS。

结论：DA是室内模块化遗迹的首选研究候选；本批不采购，先完成MapMagic免费地形实测，再根据真实缺口决定是否申请DA验证条件。
