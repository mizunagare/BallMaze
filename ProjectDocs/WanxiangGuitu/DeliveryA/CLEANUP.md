# 旧示例清理与共享资源

删除前扫描全部候选 GUID、Assets 场景/预制体/Resources、代码符号、Editor 菜单、构建和测试路径。46 个候选文件（包含目录 meta）中，唯一外部 GUID 引用是 SampleScene 在 EditorBuildSettings 的条目；先移除该条目再删除示例。没有当前游戏依赖的共享资源需要从旧目录迁出，无 Archive 副本。Git 历史保留。

删除明细：

- `Assets/BallMazeDemo/BallMazeDemo.cs`
- `Assets/BallMazeDemo/BallMazeDemo.cs.meta`
- `Assets/BallMazeDemo/BallMazeDemo.unity`
- `Assets/BallMazeDemo/BallMazeDemo.unity.meta`
- `Assets/BallMazeDemo/Editor.meta`
- `Assets/BallMazeDemo/Editor/BallMazeDemoBuilder.cs`
- `Assets/BallMazeDemo/Editor/BallMazeDemoBuilder.cs.meta`
- `Assets/EditableMaze/BallMazeEditable.unity`
- `Assets/EditableMaze/BallMazeEditable.unity.meta`
- `Assets/EditableMaze/Editor.meta`
- `Assets/EditableMaze/Materials.meta`
- `Assets/EditableMaze/MazeExit.cs`
- `Assets/EditableMaze/MazeExit.cs.meta`
- `Assets/EditableMaze/MazeGame.cs`
- `Assets/EditableMaze/MazeGame.cs.meta`
- `Assets/EditableMaze/MazeKey.cs`
- `Assets/EditableMaze/MazeKey.cs.meta`
- `Assets/EditableMaze/MazePlayer.cs`
- `Assets/EditableMaze/MazePlayer.cs.meta`
- `Assets/EditableMaze/Prefabs.meta`
- `Assets/EditableMaze/README.txt`
- `Assets/EditableMaze/README.txt.meta`
- `Assets/EditableMaze/Editor/EditableMazeBuilder.cs`
- `Assets/EditableMaze/Editor/EditableMazeBuilder.cs.meta`
- `Assets/EditableMaze/Materials/Exit.mat`
- `Assets/EditableMaze/Materials/Exit.mat.meta`
- `Assets/EditableMaze/Materials/Floor.mat`
- `Assets/EditableMaze/Materials/Floor.mat.meta`
- `Assets/EditableMaze/Materials/Key.mat`
- `Assets/EditableMaze/Materials/Key.mat.meta`
- `Assets/EditableMaze/Materials/Player.mat`
- `Assets/EditableMaze/Materials/Player.mat.meta`
- `Assets/EditableMaze/Materials/Wall.mat`
- `Assets/EditableMaze/Materials/Wall.mat.meta`
- `Assets/EditableMaze/Prefabs/Exit.prefab`
- `Assets/EditableMaze/Prefabs/Exit.prefab.meta`
- `Assets/EditableMaze/Prefabs/Key.prefab`
- `Assets/EditableMaze/Prefabs/Key.prefab.meta`
- `Assets/EditableMaze/Prefabs/Player.prefab`
- `Assets/EditableMaze/Prefabs/Player.prefab.meta`
- `Assets/EditableMaze/Prefabs/Wall.prefab`
- `Assets/EditableMaze/Prefabs/Wall.prefab.meta`
- `Assets/Scenes/SampleScene.unity`
- `Assets/Scenes/SampleScene.unity.meta`
- `Assets/BallMazeDemo.meta`
- `Assets/EditableMaze.meta`

保留：CombatPrototype 全部现用玩法与两个测试场景 ForestRuins/CombatPlayground；森林/波次入口；FantasyArt 与素材许可证；输入、渲染、相机等共享资源及原 meta/GUID；ProjectDocs 历史夹具与当前游戏回归测试。CombatPrototype 不搬家，业务类不批量改名。ForestRuins 是唯一启用构建场景。

最终资源审计还发现原模板共享配置的11条失效GUID：PC_Renderer 的7条旧 probeVolumeResources（安装的 URP 已将其标记为过时），以及 DefaultVolumeProfile 的4个失效自定义组件。另有5个 m_Script fileID=0 的包测试组件。清理过时资源块与这9个无效组件/根列表引用，保留 SSAO、有效后处理组件、渲染模式与两个资源原 meta/GUID。未删除整份共享配置、未替换渲染管线、未升级包。见资源审计首次失败与复测结果。

已关闭原 Editor/Visual Studio 后，将工程从 D:/unity/BallMaze/BallMaze 移至 D:/unity/WanxiangGuitu；.git/远端配置保留。旧位置只残留空隐藏 .vs 缓存目录，没有游戏资源或业务代码；不在占用时强删缓存。Hub 用户路径缓存需手动添加新目录。

仍名为 SampleSceneProfile 的共享 VolumeProfile（GUID 10fc4df2da32a41aaa32d77bc913491c）由 PC/Mobile 渲染资产使用，故保留，不是已删除 SampleScene 的入口。ProjectSettings.templateDefaultScene 已指向 ForestRuins。云服务的旧 projectName/cloudProjectId、平台包标识/metroPackageName、productGUID 保留原值以免顺带改动外部身份；cloudEnabled 仍为0。Metro 描述已改中文。旧存档定位代码中的 BallMaze 是必要的旧路径标识；历史夹具和报告名称不全局替换。
