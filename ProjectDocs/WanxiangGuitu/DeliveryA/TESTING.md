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

## 正常 AI 原工程自动试玩（A1 修订）

旧命令只有 UNITY_TEST_ROOT，未约束默认 Start 的首次存档定位；不再作为安全执行命令使用。历史正常AI运行是否访问真实目录 **未核实**，已有日志没有完整首次定位回执，不能据此宣称绝对安全或已损坏。

必须使用 [A1 启动包装器](../DeliveryA1/Invoke-NormalAI.ps1)。它在启动进程前确定隔离根，并传入 `-wanxiang-storage-root`；驱动在打开场景/进入 Play Mode 前再次验证。测试不再在若干帧后重新 InitializeStorage。缺参、相对/驱动器相对路径、LocalLow 或重解析路径会拒绝。所有正常AI存档操作复用默认初始化的同一隔离目录。

```powershell
& 'D:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryA1/Invoke-NormalAI.ps1' `
  -SourceProject 'D:/unity/WanxiangGuitu' `
  -IsolationRoot 'C:/UnityValidation/NormalAI-NewRoot' -Mode Normal
& 'D:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryA1/Invoke-NormalAI.ps1' `
  -SourceProject 'D:/unity/WanxiangGuitu' `
  -IsolationRoot 'C:/UnityValidation/NormalAI-NewRoot' -Mode Resume
```

关闭原工程Editor后执行，正常模式须使用新根。包装器以隐藏非batch Editor运行，子进程环境将UNITY_TEST_ROOT设为相同根；不读取/迁移真实玩家档。`storage-audit.jsonl`记录pre-play、默认定位、首次initialize、保存/读取及before-exit；逐模式进程回执分别保留退出码/超时/替身哨兵哈希检查。根外初始化尝试会在文件访问前拒绝，正常AI使用的替身位于隔离测试父目录Protected/DoNotTouch，绝不是玩家目录。

`RejectMissing`、`RejectRelative`、`RejectLocalLow`是专门负例模式：刻意传入无效配置，预期exit1、明确pre-Play拒绝标记且没有存档访问回执，不能用任意编译失败冒充正确拒绝。包装器自身始终要求合法的日志隔离根。

玩法仍是正常伤害/速度/生命和全启用AI，虚拟键盘实际移动、箭击、伐木、撤离、入库制造再出征，固定实际布局418，准备弓/剑与石1矿2。不将它当四武器全种子平衡测试。临时Editor驱动在退出后移到该隔离根的ExecutedDrivers目录，防止进入产品构建；未知文件存在时停止自动移动。

## 结果解读

- WGAssetAudit 检查当前两个场景 Missing Script、所有 Assets 场景/预制体/资源/材质 GUID、品牌/Company/构建入口与示例退出。
- WGRoutesCheck 在20种子对地点、出口交互范围与所有敌人出生点做真实碰撞移动；AI停用且忽略演员碰撞，仅证明通行。
- B06ForestCheck 保留100种子规则检查；其旧直接Build调用适配为产品GeneratePlayable，不放宽断言。
- 现有双武器/冷却/20高品质技能、容器拖放旋转交换、仓库、29高级配方、六材料、旧格式与满仓待领取测试继续执行。
- WGDeliveryACheck 定向故障注入点仅为非序列化测试接口，不是空实现替代产品功能。

首次真实运行曾发现模板失效资源及测试工具问题；历史失败和修复后的复测均记录，不删掉失败再声称从未失败。完整原始 Unity 日志留在本机隔离目录，仓库仅保留断言摘录、结果、原日志 SHA256 和真实截图，避免带入许可/机器信息。
