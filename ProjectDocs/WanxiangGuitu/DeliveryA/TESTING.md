# 交付 A：本地隔离复跑

使用 PowerShell 7，已安装 Unity 6000.6.5f1（必须有 Windows 构建支持）。关闭要测试的副本 Editor，路径使用全新、工程外、非 LocalLow 的目录，不覆盖旧工作副本。不升级包，不需要 CI。

```powershell
& 'D:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryA/Invoke-DeliveryA.ps1' `
  -SourceProject 'D:/unity/WanxiangGuitu' `
  -WorkProject 'C:/UnityValidation/NewWork' `
  -ArtifactsRoot 'C:/UnityValidation/NewResults' `
  -PlayerProcesses
```

脚本只复制 Assets/Packages/ProjectSettings，不带 Library；安装 B06 保留测试和本批测试，复制合成历史夹具。历史容器读回需要的 `container-v2.json` 是已有 `fixtures/v2.json` 的原字节别名，不修改历史载荷。所有写入显式传入测试目录。运行 19 个方法后产生逐项退出码、异常、耗时、超时、汇总与日志；任何实际失败返回非零。不要仅看最后一个构建退出码。

`Release/WanxiangGuitu.exe` 是没有运行测试驱动的非开发产品构建。可独立启动并指定 `-wanxiang-storage-root "全新隔离绝对路径"`，验证默认存档定位入口。不要在测试时遗漏该参数而使用真实 LocalLow。

`-PlayerProcesses` 另在副本 Assets 中临时加入 WGPlayerFlow，生成独立 `PlayerVariant/Release` 非开发验证构建。三个进程共享同一隔离根目录：zero-save → zero-resume → terminal-resume；检查零遭遇资源/事件、页面、同 Run、撤离、入库/取出/制造/装备存取、再出征、Pending 死亡恢复及重复终局。它是受控规则测试，会定位角色、注入零遭遇与致死伤害，不能冒充正常 AI 试玩；不会将驱动写回原工程或正式构建。

## 正常 AI 原工程自动试玩

Tests/WGNormalAICheck.cs.txt 是另一种验证：正常伤害/速度/生命与 AI，虚拟键盘沿导航路径操作，实际弓箭/伐木/撤离并入库制造后再出征。准备弓主武器、剑副武器，携入石1矿2；固定实际布局种子418，保留请求种子元数据，不把它当随机平衡测试。

要复跑，先关闭原工程 Editor；临时把 `WGNormalAICheck.cs.txt` 与保留 B06 `TestSources/B06OriginalPlay.cs.txt` 复制为原工程 Editor 下同名 `.cs`。在启动该 Editor 的**子进程环境**指定 `UNITY_TEST_ROOT=全新工程外目录`，执行 Unity `-projectPath <原工程> -executeMethod WGNormalAICheck.Run -logFile <隔离目录/Editor.log>`（非 batch，隐藏窗口启动）。240 秒超时由驱动限制。测试始终 `InitializeStorage(<显式隔离根>/isolated-save,false)`，不使用真实玩家数据。结束后移走临时脚本和 meta；保留本文件夹的源码。

正常 AI、关闭 AI 的 CharacterController 通行探针、受控规则/故障注入、人工试玩分别记录。人工操作本轮 NOT_RUN；不可拿前三者当人工验收。

## 结果解读

- WGAssetAudit 检查当前两个场景 Missing Script、所有 Assets 场景/预制体/资源/材质 GUID、品牌/Company/构建入口与示例退出。
- WGRoutesCheck 在20种子对地点、出口交互范围与所有敌人出生点做真实碰撞移动；AI停用且忽略演员碰撞，仅证明通行。
- B06ForestCheck 保留100种子规则检查；其旧直接Build调用适配为产品GeneratePlayable，不放宽断言。
- 现有双武器/冷却/20高品质技能、容器拖放旋转交换、仓库、29高级配方、六材料、旧格式与满仓待领取测试继续执行。
- WGDeliveryACheck 定向故障注入点仅为非序列化测试接口，不是空实现替代产品功能。

首次真实运行曾发现模板失效资源及测试工具问题；历史失败和修复后的复测均记录，不删掉失败再声称从未失败。完整原始 Unity 日志留在本机隔离目录，仓库仅保留断言摘录、结果、原日志 SHA256 和真实截图，避免带入许可/机器信息。
