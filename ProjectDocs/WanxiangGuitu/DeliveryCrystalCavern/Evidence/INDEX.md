# C2.1 原始证据及复跑

隔离根 I:/WGCombat/C2-1106-A。最终纯发行包在 PureBuild2/Release。产品冻结范围及发行身份以逐文件清单和 Assembly-CSharp 哈希为准。原始日志、运行副本和合成档正文留在本机隔离根。发布清单记录原始与发布 SHA256。PNG 原图按原字节保留。[证据清单](manifest.json) · [最终发行清单](Audit/release-manifest.json)

| 验证 | Editor | 非开发测试 Player |
| --- | --- | --- |
| 入口、矿脉、巡守、危险区、保存 | [运行](EditorFinal-start/) | [运行](PlayerFinal-start/) |
| 新进程恢复、免费撤离、回营、新 Run | [运行](EditorFinal-restore/) | [运行](PlayerFinal-restore/) |
| 七武器实际释放和法杖实体撞墙 | [运行](EditorFinal-weapons/) | [运行](PlayerFinal-weapons/) |
| 实际危险区死亡及卸载 | [运行](EditorFinal-death/) | [运行](PlayerFinal-death/) |
| 旧森林在途档 | [历史夹具](EditorHistoricalForest/) | [历史夹具](PlayerFinal-old-forest-resume/) |
| 旧 C1 在途档 | [历史夹具](EditorFinal-old-ruins-resume/) | [历史夹具](PlayerFinal-old-ruins-resume/) |
| 森林出征接口 | [运行](Editor-forest/) | [运行](PlayerFinal-forest/) |
| C1 出征接口 | [运行](Editor-ruins/) | [运行](PlayerFinal-ruins/) |
| 晶石脉实采及稳定 ID 保存 | [运行](EditorCrystal/) | [运行](PlayerCrystal/) |

- [入口](PlayerFinal-start/01-entry.png) · [矿脉](PlayerFinal-start/02-mining.png) · [通道](PlayerFinal-start/03-channel.png) · [预警](PlayerFinal-start/04-warning.png) · [生效](PlayerFinal-start/05-active.png)
- [逐进程断言计数](Audit/results.json) · [连续采集轨迹](PlayerTrace/continuous.tsv) · [连续进程回执](PlayerTrace/process.json) · [完整运行日志](PlayerTrace/Player.log.gz)
- [发行摘要](Audit/build-summary.txt) · [实际构建进程](PureBuild2/editor-actual-exit.json) · [Bee 输入](Audit/build.bee.json) · [正式发行回执](Audit/build.release.json) · [完整构建日志](PureBuild2/Unity.log.gz) · [警告记录](Audit/warnings.txt)
- [纯包标题](PureBootFinal/title-player.png) · [纯包退出回执](PureBootFinal/pure-runtime.json) · [发行及保护核验](Audit/release-audit.json)
- [素材导入与剔除](Audit/packaged-cavern-materials.json) · [URP Lit 构建记录](Audit/lit-build.txt) · [构建输入差异](Audit/build-input-differences.json)
- [失败历史](../FAILURE_HISTORY.md) · [验收](../ACCEPTANCE.md)

## 复跑

在新隔离工程复制产品输入，使用 Unity 6000.6.5f1 和既有固定 Release Profile。Invoke-Editor.ps1 的 Method 传 CrystalCavernAuthoring.Bake 可复跑固定资源烘焙。纯构建使用 WanxiangBuild.ValidateBuild，检查独立 Editor 进程、BuildReport、Bee 和发行回执。纯包中不得放 Driver.cs.txt 的产物。Prepare-Player.ps1 在纯包副本外部编译验证驱动并只修改两份加载注册。Invoke-Player.ps1 运行 start、restore、death、weapons、forest、ruins、old-forest-resume、old-ruins-resume、trace 或 crystal。restore 的 Seed 为已成功的 start 输出，工具逐项哈希复制合成档。Editor 使用单独的 EditorProject，把 Driver.cs.txt 仅复制为该工程的 CavernValidationDriver.cs，运行 CavernValidationEditor.Begin 并使用 NonBatch 与 ValidationCopy。测试期间使用私有桌面和隔离存档。

运行入口、捕获时序、退出状态和原始警告保存在各运行目录。截图与连续轨迹为受控 Player，人工试玩、原生输入及性能测量保持独立。[验证工具](../Tools/)
