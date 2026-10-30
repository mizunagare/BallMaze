# UX-TECH-01 复跑与层级

使用 Windows PowerShell 7、Unity 6000.6.5f1，工程外唯一测试根 `I:/WGCombat/UT01-1030-A`。`owner.json` 和 `user-before.json` 绑定本轮输入；禁止复用其中存档作为真实玩家进度。

## 已用入口

- `Audit-Consumers.py <repo>`：只读生成消费者清单。
- `Invoke-Editor.ps1 -Project <owned clone> -Output <new directory>`：新定向18断言，复用旧 Step/非激活测试桌面。
- 同一入口 `-Method Input01Rules.Run`、`Input01Play.Run`、`Input01Play.Resume`：原 INPUT-01 用例原文，Play/Resume 添加 `-Graphics -NonBatch`；同一合成 `-StorageRoot` 才能跨进程恢复。
- `Invoke-Runtime.ps1 -Build <acceptance Release> -Output <new directory>`：独立非开发 Player、虚拟 InputSystem 事件、明确合成根；不是原生输入。当前驱动从 Boot/Title 显式调用实际 NewGame 业务入口，后续由产品 Update 消费输入。
- `Invoke-NormalAI.ps1 -Project <clone> -RunRoot <synthetic state> -Output <new directory> [-Mode Resume|FinalResume]`：复用现有正常AI驱动。正常AI与受控输入用例分开。
- `Inspect-Build.ps1 -BuildRoot <pure Release> -Output <json>`：只读 PE；补入 UXTech 驱动类型检查。
- `Collect.py <owned root> <repo>`：发布日志、回执和输入，不发布缓存、构建二进制或用户覆盖层。

## 隔离验收与纯发行构建

只在隔离副本把 `Tests/UXTechCases.cs.txt`、`UXTechPlayer.cs.txt` 放入 `Assets/UXTechAcceptanceOnly/`。Editor adapter 与旧夹具均在 Editor 目录；共享 Cases 不得同时出现两份。调用原 `DeliveryEncounterAI01/Invoke-Check.ps1 -Method Build01Audit.Run`，其内部使用原正式构建方法、Options=None，并保存全输入和原警告。

纯发行构建前将整份 AcceptanceOnly 移出 Assets，将共享 Cases 放回 Editor 目录。产品仓库不增加任何 runtime 验收类。验收驱动 opt-in 不等于发行产品入口改变。

每次使用新 Output；不得覆盖 Before、失败构建或失败运行。命令/UTC/实际退出码/超时/日志位于每项 results.json、launch-spec、exit.json。驱动有界自退出不等于自然标题栏关闭；异常和超时必须保留。不得强杀超时进程。

## 解释边界

焦点回调、设备替换均为受控模拟；原生OS焦点、物理热插拔、原生U16、人工理解与手感 NOT_RUN。后台进程退出与退出码不证明历史 UNKNOWN/C15 根因消失。单次受控暂停检查也不等于所有菜单/敌人/投射物组合已穷尽。
